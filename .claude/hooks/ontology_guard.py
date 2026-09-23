#!/usr/bin/env python3
"""ontology_guard.py — the PreToolUse hook that enforces the DATA / ONTOLOGY pipeline split.

THIS FILE IS THE ONE AUTHORED COPY. Every other copy in the estate is a projection written by
`ontology/tools/install_lock.py` and never by hand; `ontology/tools/check_lock_in_step.py` reds when
any copy's sha256 differs from this one's. Measured 2026-09-18 before that gate existed: ELEVEN
copies in THREE distinct bodies, seven of them a generation stale, and nothing noticed for as long
as that took — because the estate's only drift check verified PRESENCE plus the TARGET's own
self-test, never the BODY against its source.

WHAT CHANGED, AND WHY THE BLANKET LOCK HAD TO GO
------------------------------------------------
The old rule was a path blanket: any path under a bundle's `ontology/` was denied unless the
operator had touched an unlock marker. It protected a live ontology and it BROKE A FIRST INGESTION.
Measured 2026-09-18 10:09: a concept-authoring agent's first Write to a fresh bundle's
`ontology/concepts/…` was refused; the agent read this guard, searched for an unlock marker, found
none, and wrote its concepts INTO A TEMP DIRECTORY. The lock did not protect meaning — it silently
diverted the pipeline's output somewhere the ontology would never see it, and the refusal's own
message is why: it advertised a workaround ("the operator approves the exact diff, then unlocks"),
so an agent that could not find a marker reasonably went looking for somewhere else to write.

The operator's actual reason for wanting a gate was never "the files are incomplete". It was that A
HUMAN HAD NOT YET APPROVED THE DATASET CONFIGURATION. So the blanket is replaced by a DECLARED
SPLIT: a bundle names two pipelines in its manifest, the DATA pipeline's declared exit is a named
human's sign-off over the issues its own register holds, and this guard stops asking "is this path
under ontology/?" and starts asking "HAS THIS BUNDLE'S DATA PIPELINE REACHED ITS DECLARED EXIT?".

    ontology/** in a bundle declaring two pipelines, data plane APPROVED  -> allow
    ontology/** in a bundle declaring two pipelines, not approved         -> DENY, naming the act
    ontology/** in a bundle declaring ONE pipeline (legacy)               -> DENY unless unlocked
    the sign-off, the marker, and the lock's own two halves               -> DENY, ALWAYS

CREATE IS GRANTED BY THE GATE; MUTATE IS STILL GRANTED BY THE OPERATOR. "Incomplete ontology" was
the wrong reason for the lock. "Meaning already under a ruling must not change without one" is the
right one, and it survives intact: a bundle that has finished authoring flips to a locked phase and
behaves exactly as before. What does NOT survive is a file-count cliff — a rule keyed on "zero
concepts exist" would allow concept number one and deny concept number two, which is the same defect
wearing a smaller blanket.

THE UNCONDITIONALLY PROTECTED FAMILIES, and every one was measured WRITABLE on 2026-09-18
------------------------------------------------------------------------------------------
No unlock marker lifts these, ever, because an unlock the agent can also satisfy is not a gate:
  • `governance/data_plane_approval.yaml` and `governance/sme-questions.yaml` — an agent may never
    write a human's signature. This is the gate's token.
  • `.claude/hooks/**` and `.claude/settings*.json` — THE LOCK'S OWN TWO HALVES. `decide({Edit,
    .claude/hooks/ontology_guard.py}) -> 0` and `decide({Edit, .claude/settings.json}) -> 0` were
    both measured true, so an agent could disarm the lock by rewriting the guard that governs it, or
    by editing the settings block that names the hook. One Write, no shell, no marker.
  • `.ontology-unlocked` itself — measured writable, and it contains no `/ontology/` substring, so
    it needs an explicit branch rather than falling out of the suffix rule.

FAILURE SEMANTICS — deliberate, and the reason this file must never be installed without its
settings block or vice versa:
  • unparseable payload, or a tool we do not govern  -> exit 0 (fail OPEN; never brick unrelated work)
  • a positively identified protected path with no permission -> exit 2 (fail CLOSED; deny)
  • AN INPUT WE CANNOT READ -> exit 2. UNKNOWN MEANS DENY, the estate's own compile-gate rule. A
    gate that could not run must never read as an open door.
  • THIS SCRIPT MISSING -> the interpreter itself exits 2, which the host reads as DENY for EVERY
    edit in the repo, not just ontology ones. A half-installed lock bricks the repo rather than
    silently vanishing. Install both halves atomically.

NO PyYAML, AND THAT IS LOAD-BEARING. Because this file fails closed on protected paths, an import
error would deny every edit in nine repositories. So the sign-off is restricted to FLAT `key: value`
scalars and read with the standard library alone, a malformed file counts as NO approval (deny — the
safe direction) and prints its offending line number, and `sdk/gate/check_seam_agreement.py` proves
this parser and `yaml.safe_load` agree over every sign-off in the estate. The manifest is probed for
its `pipelines:` declaration by the same flat scanner — it looks for the KEY, never for a value, so
it needs no nesting.

WHAT THIS GUARD DOES NOT CLAIM. Bash is a write surface, and the matcher below DETECTS the obvious
shell writes — `>`, `>>`, `touch`, `tee`, `cp`, `mv`, `sed -i`, a path literal in `python -c`. A
constructed path, a base64'd one, a heredoc written to a script and then executed, or `cd` plus a
relative path all walk past it. That is DETECTION, never impossibility. The installed
`permissions.deny` block raises the cost again without closing the class. Real authorization is
out-of-band. The honest claim, in the estate's own words, is DETECTED-AND-BLOCKED, AUTHORIZED
OUT-OF-BAND.

    python3 ontology_guard.py --self-test          prove it reds on mutants and greens on a clean fixture
    python3 ontology_guard.py --explain <path>      the verdict for one path, read-only, no stdin
"""
import json
import os
import re
import sys
import tempfile
import time

# The contract this body implements, printed in every deny message so a DRIFTED copy is visible to
# the agent reading the refusal and not only to a gate nobody ran.
GUARD_CONTRACT = "mac.ontology-guard/3"

# THE GOVERNED WRITE SURFACE, and it is DECLARED rather than assumed. Everything else fails OPEN,
# which is the correct default for not bricking unrelated work and the wrong one for this gate: an
# MCP server, a patch applier or a subagent with its own tool surface is ungoverned by construction.
# `ontology/install/governed_tools_floor.txt` carries this same set and check_lock_in_step.py reds
# when the two disagree, so the day the surface grows is a FAIL and not a silent hole.
GOVERNED_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "Bash"}
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}

UNLOCK_MARKER = ".ontology-unlocked"
APPROVAL_REL = os.path.join("governance", "data_plane_approval.yaml")
REGISTER_REL = os.path.join("data", "quality", "data_quality_register.yaml")

_AGENT_DECISION = re.compile(r"/\.claude/agents/[^/]*(interpreter|evaluator|diagnostician)[^/]*\.md$")

# A governed meaning file is DATA a human authored: yaml, json, markdown, a lock or a register.
# SOURCE CODE IS NOT MEANING, even when it lives in a package called `ontology`. Measured
# 2026-09-17: this guard blocked a build from editing `packages/mac-runtime/src/mac_runtime/
# ontology/parser.py` — the runtime's own PARSER, whose defect was that it dropped the very
# declarations the ontology makes. A guard that protects a locked ontology by making the code that
# READS it unfixable protects nothing and costs a day.
_MEANING_SUFFIXES = (".yaml", ".yml", ".json", ".md", ".lock", ".csv", ".ttl", ".cypher", ".mmd", ".sql")
_SOURCE_TREES = ("/src/", "/site-packages/", "/node_modules/", "/dist/", "/build/", "/.venv/")

# THE METHOD TRACK IS NOT A BUNDLE, and its `ontology/` directory is not a meaning plane.
#
# The kit that SHIPS this guard keeps its whole method under `ontology/` — BLUEPRINT.md, METHOD.md,
# the skills, the seats, the plane docs, the installable assets and this file's own source. The bare
# "/ontology/" test classified ALL of it as locked meaning, so writing
# `ontology/install/templates/settings.lock.json` — the file that ARMS THE LOCK — was denied by the
# very lock it installs. Measured 2026-09-18, twice: on that template and on the plane docs.
#
# Same class of defect as the 2026-09-17 one recorded above: a guard that makes its own mechanism
# unfixable protects nothing and costs a day. The fix is the same shape, and it is SELF-IDENTIFYING
# rather than a list of directory names that would have to grow every time the method did — an
# `ontology/` directory that CONTAINS THIS GUARD'S OWN SOURCE is the track that ships the lock, not
# a bundle governed by it. A bundle cannot acquire the exemption without shipping a guard, and the
# nine bundle repositories in this estate hold no such file.
_GUARD_SRC_REL = ("install", "hooks", "ontology_guard.py")


def _is_method_track(path):
    """True when `path` lives under an `ontology/` directory that ships this guard's own source."""
    p = path.replace(os.sep, "/")
    i = p.find("/ontology/")
    if i == -1:
        return False
    onto = p[:i + len("/ontology")]
    return os.path.isfile(os.path.join(onto.replace("/", os.sep), *_GUARD_SRC_REL))

# ---------------------------------------------------------------- shell write targets
#
# DETECTION, NOT CLOSURE — see the module docstring. And the target must be BOUND TO THE VERB, not
# merely present on the same line.
#
# MEASURED 2026-09-18, on the first live use of this matcher: a read-only verification command
#     rc=$(echo '{...}' | python3 "$g" >/dev/null 2>&1; echo $?)
# was DENIED, because a naive matcher saw a redirect (`>/dev/null`) and, separately, a protected
# path (`$g`, the guard being EXECUTED) somewhere in the same command. Neither was a write to the
# other. A guard that blocks reading and running the very files it protects is the 2026-09-17
# "source code is not meaning" defect again in a new costume, and it costs real work immediately.
#
# So the rule is: a protected path is a write target only when it is the DESTINATION of a redirect,
# or an operand of a verb that writes its operand. A protected path that is merely read, executed,
# grepped, diffed or hashed is none of this guard's business.
_REDIRECT = re.compile(r"(?:^|[^0-9<>&])>>?\s*(?:\"([^\"]+)\"|'([^']+)'|([^\s'\"|;&<>]+))")
# Verbs whose LAST operand is the destination (source first, destination second).
_DEST_LAST = ("cp", "mv", "rsync", "install", "ln")
# Verbs that write EVERY path operand they are given.
_DEST_ALL = ("touch", "tee", "truncate", "mkdir", "unlink", "rm", "shred")
# In-place editors: the flag is what makes them write.
_INPLACE = re.compile(r"\b(sed|perl|ruby|gsed)\b[^|;&]*\s-i")
_SEGMENT = re.compile(r"[;&|]{1,2}|\n")


def bash_write_targets(command):
    """Every path this command plausibly WRITES. Conservative by design; see above."""
    targets = []
    for segment in _SEGMENT.split(command or ""):
        seg = segment.strip()
        if not seg:
            continue
        for m in _REDIRECT.finditer(seg):
            t = m.group(1) or m.group(2) or m.group(3)
            if t and not t.startswith("/dev/"):
                targets.append(t)
        tokens = [t for t in re.findall(r"\"[^\"]*\"|'[^']*'|[^\s]+", seg)]
        tokens = [t.strip("\"'") for t in tokens]
        if not tokens:
            continue
        verb = os.path.basename(tokens[0])
        operands = [t for t in tokens[1:] if not t.startswith("-")]
        if verb in _DEST_ALL or _INPLACE.search(seg):
            targets += operands
        elif verb in _DEST_LAST and len(operands) >= 2:
            targets.append(operands[-1])
    return [t for t in targets if t and not t.startswith("/dev/")]

# The digest surface, INLINED — it must match tools/check_data_plane_approved.py's `_SURFACE`
# byte-for-byte in meaning. Two derivations that can disagree is the only arrangement in which
# either can be checked, and check_seam_agreement.py is what stands over the pair.
_SURFACE = (
    ("data/datasets", (".yaml",)),
    ("data/transforms", (".yaml", ".sql")),
    ("data/sources", (".yaml",)),
    ("data/profiles", (".yaml",)),
    ("data/lookups", (".csv",)),
)
_SURFACE_SINGLETONS = ("data/quality/data_quality_register.yaml", "mac.project.yaml")


# ---------------------------------------------------------------- protection

def _unconditional(path: str) -> str:
    """The families no marker and no pipeline state ever lifts. Returns a reason, or ''."""
    p = path.replace(os.sep, "/")
    if p.endswith("/" + APPROVAL_REL.replace(os.sep, "/")) or p.endswith("/governance/sme-questions.yaml"):
        return ("the data-plane sign-off — an agent may never write a human's signature; it is this "
                "gate's own token")
    if "/.claude/hooks/" in p:
        return "the lock's own guard body — an agent may not rewrite the guard that governs it"
    if re.search(r"/\.claude/settings(\.local)?\.json$", p):
        return "the lock's own settings block — an agent may not disarm the hook that governs it"
    if p.endswith("/" + UNLOCK_MARKER):
        return "the operator's unlock marker — only a human places or removes it"
    return ""


def is_protected(path: str) -> bool:
    """True if `path` names a governed meaning file or one of the unconditional families."""
    if _unconditional(path):
        return True
    if "/ontology/" in path:
        if any(marker in path for marker in _SOURCE_TREES) or _is_method_track(path):
            return False
        return path.endswith(_MEANING_SUFFIXES)
    if "/.claude/" in path and path.endswith("PROCESS.md"):
        return True
    return bool(_AGENT_DECISION.search(path))


def repo_root(path: str) -> str:
    """The BUNDLE root — the directory holding the ontology/ or .claude/ folder `path` lives under.

    Per BUNDLE and not per REPO, which matters: one repository in this estate holds two bundles side
    by side, so the sign-off, the marker and the digest are all per-bundle facts and a ruling on one
    can never open the other.
    """
    p = path.replace(os.sep, "/")
    for anchor in ("/ontology/", "/.claude/", "/governance/"):
        i = p.find(anchor)
        if i != -1:
            return path[:i]
    return os.path.dirname(path)


# ---------------------------------------------------------------- the flat reader
#
# ~20 lines of standard library, deliberately. See the docstring on why PyYAML is refused here.

class _FlatError(ValueError):
    def __init__(self, lineno, text):
        self.lineno, self.text = lineno, text
        ValueError.__init__(self, "line %d: %s" % (lineno, text))


def parse_flat(text):
    """Flat `key: value` scalars only. Anything else raises, naming its line."""
    out = {}
    for i, raw in enumerate(text.split("\n"), 1):
        line = "" if raw.lstrip().startswith("#") else raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line[:1] in (" ", "\t", "-"):
            raise _FlatError(i, "nested or list content — the sign-off must be flat scalars")
        if ":" not in line:
            raise _FlatError(i, "not a `key: value` pair")
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if not k:
            raise _FlatError(i, "empty key")
        if v[:1] in ("[", "{", "|", ">", "&", "*"):
            raise _FlatError(i, "unsupported value form %r — flat scalars only" % v[:1])
        if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
            v = v[1:-1]
        out[k] = v
    return out


def _declares_two_pipelines(root):
    """Does the manifest declare `reproduction.pipelines`? (None = the manifest is unreadable.)

    A KEY probe and never a value read, so no nesting is parsed. Keyed on the DECLARED SPLIT and
    never on a phase field: a bundle holding a live locked ontology says `phase: BUILD` in its own
    phase file, and a guard that keyed the open path on that word would silently unlock it.
    """
    mp = os.path.join(root, "mac.project.yaml")
    if not os.path.isfile(mp):
        return None
    try:
        with open(mp, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return None
    in_repro = False
    for raw in text.split("\n"):
        if raw.lstrip().startswith("#") or not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()
        if indent == 0:
            in_repro = stripped.startswith("reproduction:")
            continue
        if in_repro and indent == 2 and stripped.startswith("pipelines:"):
            return True
    return False


# ---------------------------------------------------------------- the digest

def _normalise(path):
    """Content with the churn taken out. Byte-identical in meaning to the framework gate's."""
    with open(path, "rb") as fh:
        raw = fh.read().replace(b"\r\n", b"\n")
    if os.path.splitext(path)[1].lower() in (".yaml", ".yml"):
        keep = [ln.rstrip() for ln in raw.split(b"\n")
                if ln.strip() and not ln.lstrip().startswith(b"#")]
        return b"\n".join(keep) + b"\n"
    return b"\n".join(ln.rstrip() for ln in raw.split(b"\n"))


def data_plane_digest(root):
    import hashlib
    files = []
    for rel, suffixes in _SURFACE:
        d = os.path.join(root, rel.replace("/", os.sep))
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                p = os.path.join(d, name)
                if os.path.isfile(p) and os.path.splitext(name)[1].lower() in suffixes:
                    files.append((rel + "/" + name, p))
    for rel in _SURFACE_SINGLETONS:
        p = os.path.join(root, rel.replace("/", os.sep))
        if os.path.isfile(p):
            files.append((rel, p))
    roll = hashlib.sha256()
    for rel, p in sorted(files):
        roll.update(rel.encode())
        roll.update(hashlib.sha256(_normalise(p)).digest())
    return "sha256:" + roll.hexdigest(), len(files)


# ---------------------------------------------------------------- the verdict, cached
#
# A PreToolUse hook is in the critical path of every edit in nine repositories, and this one reads a
# manifest, a sign-off and a multi-file digest. The verdict is therefore cached on the (mtime, size)
# of its inputs — the idiom the console's own document cache already uses — so a burst of writes in
# one authoring run costs one computation. The cache lives in the process, which is the right
# lifetime: the hook is a fresh process per tool call in normal operation, so the cache only ever
# helps a caller that batches, and a changed input invalidates it by construction.

_CACHE = {}


def _stamp(root):
    keys = []
    for rel, suffixes in _SURFACE:
        d = os.path.join(root, rel.replace("/", os.sep))
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                p = os.path.join(d, name)
                if os.path.isfile(p) and os.path.splitext(name)[1].lower() in suffixes:
                    try:
                        s = os.stat(p)
                        keys.append((rel + "/" + name, s.st_mtime_ns, s.st_size))
                    except OSError:
                        keys.append((rel + "/" + name, 0, -1))
    for rel in _SURFACE_SINGLETONS + (APPROVAL_REL.replace(os.sep, "/"),):
        p = os.path.join(root, rel.replace("/", os.sep))
        try:
            s = os.stat(p)
            keys.append((rel, s.st_mtime_ns, s.st_size))
        except OSError:
            keys.append((rel, 0, -1))
    return tuple(keys)


def gate_state(root):
    """(code, sentence) — the ontology plane's permission for this bundle, right now.

    `code` is a `mac.data_plane_gate` term. This is the guard's own derivation of the verdict
    `tools/check_data_plane_approved.py#approval_state` computes with PyYAML; the framework gate's
    `--agree` asserts the two reach the same answer ON THE LIVE BUNDLE, not on a fixture pair.
    """
    key = (root, _stamp(root))
    hit = _CACHE.get(key)
    if hit is not None:
        return hit
    verdict = _gate_state_uncached(root)
    if len(_CACHE) > 64:
        _CACHE.clear()
    _CACHE[key] = verdict
    return verdict


def _gate_state_uncached(root):
    declared = _declares_two_pipelines(root)
    if declared is None:
        return ("gate_unreachable",
                "this bundle has no readable mac.project.yaml, so nothing declares how it is built "
                "and the gate cannot judge it. Unknown means deny.")
    if not declared:
        return ("not_declared",
                "this bundle declares ONE pipeline, so the two-pipeline gate does not apply to it "
                "and its ontology plane is governed by the operator's unlock marker alone.")

    ap_path = os.path.join(root, APPROVAL_REL)
    if not os.path.isfile(ap_path):
        ids, total = _register_ids(root)
        named = (" (" + ", ".join(ids) + ")") if ids and len(ids) <= 8 else ""
        return ("approval_missing",
                "THE ONTOLOGY PIPELINE HAS NOT BEEN STARTED. This bundle declares two pipelines and "
                "its DATA pipeline has not reached its declared exit: %d of %d registered data "
                "issues are uncovered%s — nobody has ruled on them — and no data-plane sign-off "
                "exists at %s." % (len(ids), total, named, APPROVAL_REL.replace(os.sep, "/")))
    try:
        with open(ap_path, "r", encoding="utf-8", errors="replace") as fh:
            ap = parse_flat(fh.read())
    except _FlatError as exc:
        return ("approval_unreadable",
                "the data-plane sign-off cannot be read (%s). The bundle is treated as NOT approved "
                "until the operator fixes it — no agent may edit that file, so only a human can."
                % exc)
    except OSError as exc:
        return ("gate_unreachable", "the data-plane sign-off cannot be opened (%s)." % exc)

    if (ap.get("status") != "applied" or ap.get("verdict") != "confirmed"
            or ap.get("outcome") != "ratified"):
        return ("approval_unratified",
                "a data-plane sign-off exists and it does not ratify (status=%r, verdict=%r, "
                "outcome=%r). A draft is not an approval."
                % (ap.get("status"), ap.get("verdict"), ap.get("outcome")))
    if ap.get("submitted_via") != "human" or ap.get("identity_basis") not in (
            "verified", "local-declared"):
        return ("approval_agent_stamped",
                "the sign-off's write stamp does not name a human act (submitted_via=%r, "
                "identity_basis=%r). An agent may write a description; only a human may write a "
                "disposition." % (ap.get("submitted_via"), ap.get("identity_basis")))
    if not (ap.get("by") or "").strip():
        return ("approval_unratified",
                "the sign-off names nobody. A disposition claiming a human acted must name the "
                "human — never \"the team\", never a tool.")

    ids, total = _register_ids(root)
    if total == 0:
        return ("register_unrun",
                "the data-quality register holds no issues, so there is nothing the sign-off could "
                "have covered. A step that did not run is not a clean bill of health.")
    covers = [c for c in re.split(r"[,\s]+", ap.get("covers", "") or "") if c]
    uncovered = [i for i in ids if i not in covers]
    if uncovered:
        return ("issue_uncovered",
                "the data plane is NOT approved: %d of %d registered issues are not named in the "
                "sign-off (%s). The threshold is per-issue human acknowledgement, so the count "
                "cannot move unless a person names the specific thing."
                % (len(uncovered), total, ", ".join(uncovered)))

    signed = (ap.get("digest") or "").strip()
    now, nfiles = data_plane_digest(root)
    if not signed:
        return ("approval_unratified",
                "the sign-off carries no digest, so it does not say WHICH data plane was approved.")
    if signed != now:
        return ("plane_moved",
                "THE DATA PLANE MOVED AFTER IT WAS APPROVED. The sign-off of %s by %s covers a "
                "plane whose digest no longer matches (%s signed, %s now, over %d data-plane "
                "files). The ontology already authored is untouched and still answerable; renewing "
                "the sign-off reopens the pipeline."
                % (ap.get("at", "<undated>"), ap.get("by", "<unnamed>"), signed[:19], now[:19],
                   nfiles))
    return ("approved",
            "the data plane was APPROVED by %s on %s over %d file(s); %d of %d registered issues "
            "are covered." % (ap.get("by"), ap.get("at"), nfiles, len(covers), total))


def _register_ids(root):
    """(ids, total) from the register, by a flat scan for `- id:` lines. No YAML parser.

    The guard needs the IDS, not the structure — so it reads the one line shape the register's own
    schema fixes. A register it cannot read yields ([], 0), which lands on `register_unrun` and
    denies: the safe direction.
    """
    p = os.path.join(root, REGISTER_REL)
    if not os.path.isfile(p):
        return [], 0
    ids = []
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                m = re.match(r"\s*-\s+id:\s*['\"]?([A-Za-z0-9_.\-]+)", raw)
                if m:
                    ids.append(m.group(1))
    except OSError:
        return [], 0
    return ids, len(ids)


# ---------------------------------------------------------------- decide

def _deny(path, root, code, sentence):
    """The refusal, and CORE.md §2 governs its shape: print the ACCEPTED SHAPE, not only the
    objection. It names the pipeline, the missing act, the route and its denominator — and it
    FORBIDS DIVERSION, because the measured 10:09 failure was not the refusal. It was that the
    agent, finding no way in, wrote the meaning somewhere else."""
    approval = APPROVAL_REL.replace(os.sep, "/")
    lines = [
        "BLOCKED by ontology_guard [%s] — %s" % (GUARD_CONTRACT, code),
        "  file:     %s" % path,
        "  bundle:   %s" % root,
        "  why:      %s" % sentence,
    ]
    if code == "not_declared":
        lines += [
            "  pipeline: legacy — this bundle declares ONE pipeline, so its ontology plane is",
            "            governed by the operator's unlock marker alone, exactly as before.",
            "  the accepted shape: the operator reviews the exact diff and unlocks explicitly.",
            "            That is a human act and an agent must not perform it.",
        ]
    elif code in ("approval_missing", "issue_uncovered", "register_unrun"):
        lines += [
            "  pipeline: DATA — this bundle is still in its data pipeline.",
            "  the accepted shape — and it is the OPERATOR'S act, not yours:",
            "      1. rule on each registered issue in %s" % REGISTER_REL.replace(os.sep, "/"),
            "         (a graded DQ- id needs a disposition with `ruled_by` and `reason`;",
            "          an NS- non-promotion needs only to be named in the sign-off)",
            "      2. python3 <framework>/tools/check_data_plane_approved.py %s --print-approval" % root,
            "      3. save that block to %s and commit it" % approval,
            "  then the ontology pipeline starts, manually:",
            "      python -m sdk.cli.harvest --content-root %s --mode ontology" % root,
            "  NOTE: severity is NOT read by this gate. A non-defect graded `high` blocks nothing.",
        ]
    elif code == "plane_moved":
        lines += [
            "  pipeline: DATA — the plane moved, so the bundle is back in its data pipeline.",
            "  the accepted shape: review what changed, then re-sign %s" % approval,
            "            with the new digest. Nothing already authored has been deleted.",
        ]
    elif code in ("approval_unreadable", "approval_unratified", "approval_agent_stamped",
                  "gate_unreachable"):
        lines += [
            "  the accepted shape: only the operator can clear this — %s is" % approval,
            "            unwritable by every tool you have, deliberately.",
        ]
    lines += [
        "",
        "  DO NOT WRITE THIS CONTENT ANYWHERE ELSE. Not to a temp directory, not beside the",
        "  bundle, not under a different plane. Meaning authored outside the declared ontology",
        "  plane is invisible to every gate in this framework, and check_no_shadow_ontology.py",
        "  now FAILS on it. If the gate is closed, the answer is to have it opened — by the",
        "  human whose act opens it — and to hand the work back until then.",
        "",
    ]
    return 2, "\n".join(lines) + "\n"


def decide(payload):
    """(exit_code, message). Pure apart from reading the bundle's own declarations — the unit
    under test, and the one function the whole mechanism turns on."""
    tool = payload.get("tool_name")
    if tool not in GOVERNED_TOOLS:
        return 0, ""

    if tool == "Bash":
        # DETECTION, never closure. See the module docstring and bash_write_targets.
        command = ((payload.get("tool_input") or {}).get("command") or "")
        for target in bash_write_targets(command):
            if not is_protected(target):
                continue
            root = repo_root(target)
            reason = _unconditional(target)
            if reason:
                return _deny(target, root, "unconditional",
                             "%s. A shell write is still a write, and this path is protected "
                             "unconditionally — no marker lifts it." % reason)
            code, sentence = gate_state(root)
            if code == "approved":
                return 0, ""
            if os.path.exists(os.path.join(root, UNLOCK_MARKER)):
                return 0, ""
            return _deny(target, root, code, "%s A shell write is still a write." % sentence)
        return 0, ""

    path = ((payload.get("tool_input") or {}).get("file_path") or "").strip()
    if not path or not is_protected(path):
        return 0, ""
    root = repo_root(path)

    reason = _unconditional(path)
    if reason:
        # NO MARKER LIFTS THESE. Every one was measured writable on 2026-09-18.
        return _deny(path, root, "unconditional", reason +
                     ". The unlock marker does NOT lift this path, because an unlock the agent can "
                     "also satisfy is not a gate.")

    code, sentence = gate_state(root)
    if code == "approved":
        # (A), fixed at its cause: a first ingestion authors its ontology because a HUMAN ACTED.
        return 0, ""

    # THE OPERATOR'S MARKER STILL LIFTS — in every case, and that is deliberate.
    #
    # It is a HUMAN ACT and it stays one: `.ontology-unlocked` is now in the unconditionally
    # protected set, so no agent may place it by Edit/Write/MultiEdit/NotebookEdit, and an obvious
    # `touch` from a shell is refused too. Keeping it as the universal escape costs the gate
    # nothing an agent can spend, and NOT keeping it would cost the operator something real:
    #
    #   • a repository whose ontology plane carries no manifest at all resolves to
    #     `gate_unreachable`, and there are such repositories in this estate. Denying the marker
    #     there would take away the only way a human could authorise an edit — the new mechanism
    #     would have removed an affordance rather than added one, which is the failure this whole
    #     change is repairing, in the opposite direction.
    #   • an operator whose own sign-off is malformed would otherwise be locked out of a bundle
    #     with no way back in but hand-fixing a file the host refuses to let anything write.
    #
    # So the asymmetry is exact: the marker is a HUMAN's override of a MACHINE's refusal, and it is
    # always allowed. What is never allowed is an agent reaching either the marker or the sign-off.
    if os.path.exists(os.path.join(root, UNLOCK_MARKER)):
        return 0, ""
    return _deny(path, root, code, sentence)


# ---------------------------------------------------------------- self-test

def _self_test():
    failures = []
    total = [0]

    def check(name, got, want):
        total[0] += 1
        if got != want:
            failures.append("%s: got exit %r, want %r" % (name, got, want))

    def says(name, msg, needle):
        total[0] += 1
        if needle.lower() not in (msg or "").lower():
            failures.append("%s: refusal does not mention %r" % (name, needle))

    def silent(name, msg, needle):
        total[0] += 1
        if needle.lower() in (msg or "").lower():
            failures.append("%s: refusal MUST NOT mention %r" % (name, needle))

    def edit(p):
        return {"tool_name": "Edit", "tool_input": {"file_path": p}}

    def write(p):
        return {"tool_name": "Write", "tool_input": {"file_path": p}}

    def sh(c):
        return {"tool_name": "Bash", "tool_input": {"command": c}}

    def seed(base, name, two_pipelines=True, concepts=0):
        b = os.path.join(base, name)
        for d in ("data/datasets", "data/quality", "ontology/concepts", "governance", "decisions"):
            os.makedirs(os.path.join(b, *d.split("/")), exist_ok=True)
        repro = ("reproduction:\n  pipelines:\n    data:\n      exit:\n"
                 "        approval: governance/data_plane_approval.yaml\n"
                 "    ontology:\n      requires:\n        pipeline: data\n"
                 "  stages:\n  - id: measure\n    authoring: tool\n    pipeline: data\n"
                 if two_pipelines else
                 "reproduction:\n  stages:\n  - id: measure\n    authoring: tool\n")
        _put(os.path.join(b, "mac.project.yaml"),
             "spec_version: mac.container/1\ndescriptors: data/datasets\n" + repro)
        _put(os.path.join(b, "data", "datasets", "v_example_one.yaml"), "dataset: v_example_one\n")
        _put(os.path.join(b, "data", "quality", "data_quality_register.yaml"),
             "issues:\n  - id: NS-ALPHA-01\n    severity: high\n    status: open\n"
             "  - id: DQ-ALPHA-01\n    severity: low\n    status: accepted\n")
        for i in range(concepts):
            _put(os.path.join(b, "ontology", "concepts", "t%d.yaml" % i), "concept: t\n")
        return b

    def sign(b, **over):
        digest, _ = data_plane_digest(b)
        f = [("id", "s.data-plane.approved"), ("status", "applied"), ("verdict", "confirmed"),
             ("outcome", "ratified"), ("covers", "NS-ALPHA-01, DQ-ALPHA-01"),
             ("digest", digest), ("at", "2026-09-18"), ("by", "A. Operator"),
             ("role", "operator"), ("identity_basis", "local-declared"),
             ("submitted_via", "human")]
        d = dict(f)
        d.update(over)
        _put(os.path.join(b, APPROVAL_REL), "".join("%s: %s\n" % kv for kv in d.items()))

    with tempfile.TemporaryDirectory() as tmp:
        # ============ (A) THE DEFECT THAT STARTED THIS: a first ingestion authors its ontology.
        b = seed(tmp, "beta")
        sign(b)
        first = os.path.join(b, "ontology", "concepts", "order", "order_line.yaml")
        check("approved/first-concept-allowed", decide(write(first))[0], 0)
        os.makedirs(os.path.dirname(first), exist_ok=True)
        _put(first, "concept: order_line\n")
        # …and concept number two. A zero-concepts precondition would have denied this one.
        check("approved/second-concept-allowed",
              decide(write(os.path.join(b, "ontology", "concepts", "order", "order.yaml")))[0], 0)
        check("approved/whole-plane-open", decide(edit(os.path.join(b, "ontology", "edges.yaml")))[0], 0)
        check("approved/rules-open", decide(edit(os.path.join(b, "ontology", "rules", "r.yaml")))[0], 0)

        # ============ (B) UNAPPROVED: deny, and the refusal names the act rather than the path.
        a = seed(tmp, "alpha")
        code, msg = decide(write(os.path.join(a, "ontology", "concepts", "x.yaml")))
        check("unapproved/denied", code, 2)
        says("unapproved/names-the-code", msg, "approval_missing")
        says("unapproved/names-the-pipeline", msg, "DATA")
        says("unapproved/names-the-ids", msg, "NS-ALPHA-01")
        says("unapproved/carries-the-denominator", msg, "2 of 2")
        says("unapproved/names-the-signoff-path", msg, "governance/data_plane_approval.yaml")
        says("unapproved/names-the-ontology-command", msg, "--mode ontology")
        says("unapproved/forbids-diversion", msg, "DO NOT WRITE THIS CONTENT ANYWHERE ELSE")
        says("unapproved/discloses-severity-is-unread", msg, "severity is NOT read")
        silent("unapproved/offers-no-workaround", msg, "touch ")
        says("unapproved/names-its-contract", msg, GUARD_CONTRACT)

        # ============ (C) THE UNCONDITIONAL FAMILIES. Every one measured WRITABLE 2026-09-18.
        for label, rel in (
            ("sign-off", APPROVAL_REL),
            ("question ledger", os.path.join("governance", "sme-questions.yaml")),
            ("unlock marker", UNLOCK_MARKER),
            ("guard body", os.path.join(".claude", "hooks", "ontology_guard.py")),
            ("settings block", os.path.join(".claude", "settings.json")),
            ("local settings", os.path.join(".claude", "settings.local.json")),
        ):
            p = os.path.join(b, rel)
            for tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                check("unconditional/%s/%s" % (label, tool),
                      decide({"tool_name": tool, "tool_input": {"file_path": p}})[0], 2)
        # …and the marker does not lift them. This is the line that makes the token a token.
        _put(os.path.join(b, UNLOCK_MARKER), "")
        for label, rel in (("sign-off", APPROVAL_REL),
                           ("guard body", os.path.join(".claude", "hooks", "ontology_guard.py")),
                           ("settings block", os.path.join(".claude", "settings.json")),
                           ("unlock marker", UNLOCK_MARKER)):
            check("unconditional-with-marker/%s" % label,
                  decide(write(os.path.join(b, rel)))[0], 2)
        os.remove(os.path.join(b, UNLOCK_MARKER))

        # ============ (D) THE LEGACY BUNDLE — today's meaning, byte for byte. This is the branch
        # that keeps every live locked ontology in this estate exactly as it is.
        g = seed(tmp, "gamma", two_pipelines=False, concepts=22)
        code, msg = decide(edit(os.path.join(g, "ontology", "concepts", "t0.yaml")))
        check("legacy/denied", code, 2)
        says("legacy/says-the-gate-does-not-apply", msg, "ONE pipeline")
        _put(os.path.join(g, UNLOCK_MARKER), "")
        check("legacy/marker-still-lifts", decide(edit(os.path.join(g, "ontology", "concepts", "t0.yaml")))[0], 0)
        os.remove(os.path.join(g, UNLOCK_MARKER))
        # THE REGRESSION THAT WOULD SILENTLY UNLOCK A LIVE ONTOLOGY. A legacy bundle with a
        # perfectly valid sign-off must STILL deny: the open path is keyed on the DECLARED SPLIT,
        # never on the presence of an approval and never on a phase word.
        sign(g)
        check("legacy/a-valid-signoff-alone-does-NOT-unlock",
              decide(edit(os.path.join(g, "ontology", "concepts", "t0.yaml")))[0], 2)
        # …not even with a phase file saying BUILD, which every live bundle here carries.
        _put(os.path.join(g, "ontology", "PHASE.yaml"), "phase: BUILD\nlock: ontology/rules.lock\n")
        check("legacy/phase-BUILD-does-NOT-unlock",
              decide(edit(os.path.join(g, "ontology", "concepts", "t0.yaml")))[0], 2)
        check("legacy/its-PHASE.yaml-is-protected",
              decide(edit(os.path.join(g, "ontology", "PHASE.yaml")))[0], 2)

        # ============ (E) UNKNOWN MEANS DENY.
        s = seed(tmp, "stale")
        sign(s, digest="sha256:" + "0" * 64)
        code, msg = decide(write(os.path.join(s, "ontology", "concepts", "x.yaml")))
        check("stale/denied", code, 2)
        says("stale/names-the-code", msg, "plane_moved")
        says("stale/dates-the-signoff", msg, "2026-09-18")
        says("stale/says-nothing-was-deleted", msg, "untouched")

        u = seed(tmp, "unreadable")
        sign(u)
        with open(os.path.join(u, APPROVAL_REL), "a", encoding="utf-8") as fh:
            fh.write("nested:\n  deep: 1\n")
        code, msg = decide(write(os.path.join(u, "ontology", "concepts", "x.yaml")))
        check("malformed/denied", code, 2)
        says("malformed/names-the-code", msg, "approval_unreadable")
        says("malformed/prints-the-line-number", msg, "line ")

        n = seed(tmp, "nomanifest")
        sign(n)
        os.remove(os.path.join(n, "mac.project.yaml"))
        code, msg = decide(write(os.path.join(n, "ontology", "concepts", "x.yaml")))
        check("no-manifest/denied", code, 2)
        says("no-manifest/names-the-code", msg, "gate_unreachable")
        # …AND THE OPERATOR IS NOT LOCKED OUT. A repository whose ontology plane carries no manifest
        # resolves to gate_unreachable, and there are such repositories in this estate. If the
        # marker did not lift it, this change would have TAKEN AWAY the only way a human could
        # authorise an edit there — the same defect as the blanket lock, facing the other way.
        _put(os.path.join(n, UNLOCK_MARKER), "")
        check("no-manifest/the-operators-marker-still-lifts",
              decide(write(os.path.join(n, "ontology", "concepts", "x.yaml")))[0], 0)
        os.remove(os.path.join(n, UNLOCK_MARKER))

        r = seed(tmp, "noregister")
        sign(r)
        os.remove(os.path.join(r, "data", "quality", "data_quality_register.yaml"))
        check("no-register/denied", decide(write(os.path.join(r, "ontology", "concepts", "x.yaml")))[0], 2)

        ag = seed(tmp, "agentstamped")
        sign(ag, submitted_via="agent")
        code, msg = decide(write(os.path.join(ag, "ontology", "concepts", "x.yaml")))
        check("agent-stamped/denied", code, 2)
        says("agent-stamped/names-the-code", msg, "approval_agent_stamped")

        un = seed(tmp, "uncovered")
        sign(un, covers="NS-ALPHA-01")
        code, msg = decide(write(os.path.join(un, "ontology", "concepts", "x.yaml")))
        check("uncovered/denied", code, 2)
        says("uncovered/names-the-uncovered-id", msg, "DQ-ALPHA-01")
        says("uncovered/carries-the-denominator", msg, "1 of 2")
        # The operator can override a MACHINE refusal in a two-pipeline bundle too — the marker is
        # a human act and an agent can reach neither it nor the sign-off.
        _put(os.path.join(un, UNLOCK_MARKER), "")
        check("uncovered/the-operators-marker-still-lifts",
              decide(write(os.path.join(un, "ontology", "concepts", "x.yaml")))[0], 0)
        os.remove(os.path.join(un, UNLOCK_MARKER))

        # ============ (F) SEVERITY IS INERT. Move the grade in either direction; nothing moves.
        for sev in ("low", "medium", "high"):
            sv = seed(tmp, "sev_" + sev)
            _put(os.path.join(sv, "data", "quality", "data_quality_register.yaml"),
                 "issues:\n  - id: NS-ALPHA-01\n    severity: %s\n    status: open\n"
                 "  - id: DQ-ALPHA-01\n    severity: %s\n    status: accepted\n" % (sev, sev))
            sign(sv)
            check("severity-%s-does-not-move-the-verdict" % sev,
                  decide(write(os.path.join(sv, "ontology", "concepts", "x.yaml")))[0], 0)

        # ============ (G) BASH IS A WRITE SURFACE. Detection, and the docstring says so.
        for cmd in ("cat > %s" % os.path.join(a, "ontology", "concepts", "x.yaml"),
                    "touch %s" % os.path.join(a, UNLOCK_MARKER),
                    "printf x >> %s" % os.path.join(a, APPROVAL_REL),
                    "tee %s < /dev/null" % os.path.join(a, ".claude", "hooks", "ontology_guard.py"),
                    "sed -i '' s/a/b/ %s" % os.path.join(a, ".claude", "settings.json"),
                    "cp /dev/null %s" % os.path.join(a, UNLOCK_MARKER),
                    "mv /tmp/x %s" % os.path.join(a, APPROVAL_REL)):
            check("bash-write/%s" % cmd.split()[0], decide(sh(cmd))[0], 2)
        # …and the marker is denied from a shell even in a LEGACY bundle, where the marker is the
        # operator's affordance: placing it is a human act, so an agent may not run the touch.
        check("bash-write/marker-in-legacy-bundle",
              decide(sh("touch %s" % os.path.join(g, UNLOCK_MARKER)))[0], 2)
        # FAIL OPEN on every ordinary command, or the hook bricks the session.
        for cmd in ("ls -la", "git status", "git commit -m x", "python3 -m pytest",
                    "cat %s" % os.path.join(a, "mac.project.yaml"),
                    "grep -rn foo .", "echo hello", "rm -rf /tmp/scratch"):
            check("bash-open/%s" % cmd.split()[0], decide(sh(cmd))[0], 0)

        # THE FALSE-POSITIVE CLASS, MEASURED IN LIVE USE the first time this matcher shipped. A
        # read-only verification command was DENIED because a naive matcher saw a redirect
        # (`>/dev/null`) and, separately, a protected path somewhere on the same line — the guard
        # being EXECUTED, not written. A guard that blocks reading and running the files it protects
        # costs real work immediately, and it is the 2026-09-17 defect in a new costume. The target
        # must be BOUND TO THE VERB; a protected path that is merely read, executed, hashed, diffed
        # or piped is none of this guard's business.
        gp = os.path.join(a, ".claude", "hooks", "ontology_guard.py")
        sp = os.path.join(a, ".claude", "settings.json")
        ap = os.path.join(a, APPROVAL_REL)
        cp_ = os.path.join(a, "ontology", "concepts", "x.yaml")
        for label, cmd in (
            ("execute-with-redirect-to-devnull", 'echo "{}" | python3 "%s" >/dev/null 2>&1' % gp),
            ("execute-self-test", "python3 %s --self-test" % gp),
            ("read-with-cat", "cat %s" % ap),
            ("hash-it", "shasum -a 256 %s | cut -c1-16" % gp),
            ("grep-it", "grep -n phase %s" % cp_),
            ("diff-it", "diff %s %s" % (gp, sp)),
            ("find-and-hash", "find . -name '*.yaml' | sort | xargs shasum -a 256 > /tmp/out"),
            ("git-read", "git log --oneline -- %s" % ap),
            ("redirect-elsewhere", "cat %s > /tmp/copy.yaml" % ap),
            ("stdout-capture", "rc=$(python3 %s --explain %s >/dev/null; echo $?)" % (gp, cp_)),
        ):
            check("bash-false-positive/%s" % label, decide(sh(cmd))[0], 0)
        # …and the writes in the SAME shapes must still be caught, so the fix did not just widen
        # the hole it closed.
        for label, cmd in (
            ("redirect-into-protected", "cat /tmp/x > %s" % ap),
            ("append-into-protected", "echo x >> %s" % gp),
            ("quoted-redirect-target", 'echo x > "%s"' % sp),
            ("second-segment-writes", "ls -la && cat /tmp/x > %s" % ap),
            ("piped-segment-writes", "cat /tmp/x | tee %s" % gp),
            ("inplace-edit", "sed -i '' s/a/b/ %s" % sp),
            ("copy-onto-protected", "cp /tmp/x %s" % ap),
        ):
            check("bash-still-caught/%s" % label, decide(sh(cmd))[0], 2)
        # An approved bundle's shell write to its ontology plane is allowed, like any other write.
        check("bash-write/approved-bundle-ontology",
              decide(sh("cat > %s" % os.path.join(b, "ontology", "concepts", "y.yaml")))[0], 0)

        # ============ (H) SOURCE CODE IS STILL NOT MEANING. The 2026-09-17 fix must survive.
        src = os.path.join(tmp, "repo3", "packages", "rt", "src", "rt", "ontology", "parser.py")
        os.makedirs(os.path.dirname(src))
        _put(src, "# a runtime parser is not meaning\n")
        check("source-code/ontology-package", decide(edit(src))[0], 0)
        check("source-code/fixture-yaml", decide(edit(os.path.join(os.path.dirname(src), "f.yaml")))[0], 0)
        check("py-in-bundle-ontology",
              decide(edit(os.path.join(b, "ontology", "concepts", "build.py")))[0], 0)
        # THE METHOD TRACK IS NOT A BUNDLE. The kit's own settings template arms this lock, and the
        # bare "/ontology/" test denied it — the mechanism made itself unfixable. The exemption is
        # SELF-IDENTIFYING: an ontology/ directory shipping this guard's own source is the track
        # that ships the lock. Both halves are seeded — the method track is exempt, and a bundle's
        # real ontology plane is NOT, even for identically-named files.
        kit_onto = os.path.join(tmp, "kit", "ontology")
        _put(os.path.join(kit_onto, "install", "hooks", "ontology_guard.py"), "# the source\n")
        for tooling in ("install/templates/settings.lock.json", "planes/data.md",
                        "planes/ontology.md", "knowledge/knowledge-base.json", "BLUEPRINT.md",
                        "METHOD.md", "tools/estate.json", "tests/fixture.yaml",
                        "skills/concept-authoring/SKILL.md"):
            check("method-track/%s" % tooling,
                  decide(edit(os.path.join(kit_onto, *tooling.split("/"))))[0], 0)
        # A BUNDLE CANNOT ACQUIRE THE EXEMPTION without shipping a guard: the same relative paths
        # inside a real bundle's ontology plane stay protected.
        for same in ("planes/data.md", "BLUEPRINT.md", "concepts/install.yaml",
                     "install/templates/settings.lock.json"):
            check("method-track/does-not-exempt-a-bundle/%s" % same,
                  decide(edit(os.path.join(g, "ontology", *same.split("/"))))[0], 2)
        for suffix in (".yaml", ".yml", ".json", ".md", ".lock", ".csv"):
            check("legacy-suffix%s-still-protected" % suffix,
                  decide(edit(os.path.join(g, "ontology", "concepts", "Thing" + suffix)))[0], 2)

        # ============ (I) THE ORIGINAL FAIL-OPEN CONTRACT, unchanged.
        check("ordinary-file", decide(edit(os.path.join(b, "data", "datasets", "d.yaml")))[0], 0)
        check("register-is-agent-writable",
              decide(edit(os.path.join(b, REGISTER_REL)))[0], 0)
        check("ungoverned-tool", decide({"tool_name": "Read", "tool_input": {"file_path": first}})[0], 0)
        check("empty-path", decide({"tool_name": "Edit", "tool_input": {}})[0], 0)
        check("empty-bash", decide(sh(""))[0], 0)
        proc = os.path.join(tmp, "repo2", ".claude", "PROCESS.md")
        os.makedirs(os.path.dirname(proc))
        check("process-md-protected", decide(edit(proc))[0], 2)
        adef = os.path.join(tmp, "repo2", ".claude", "agents", "x-interpreter.md")
        check("agent-def-protected", decide(write(adef))[0], 2)

        # ============ (J) THE CACHE MUST NOT SERVE A STALE VERDICT.
        c = seed(tmp, "cached")
        target = os.path.join(c, "ontology", "concepts", "x.yaml")
        check("cache/denied-before-signing", decide(write(target))[0], 2)
        sign(c)
        check("cache/allowed-after-signing", decide(write(target))[0], 0)
        _put(os.path.join(c, "data", "datasets", "v_example_two.yaml"), "dataset: v_example_two\n")
        check("cache/denied-again-once-the-plane-moves", decide(write(target))[0], 2)

    if failures:
        for f in failures:
            sys.stderr.write("  %s\n" % f)
        print("FAIL: ontology_guard self-test [%s] — %d of %d assertions failed"
              % (GUARD_CONTRACT, len(failures), total[0]))
        return 1
    print("PASS: ontology_guard self-test [%s] — %d/%d assertions: a first ingestion authors its "
          "ontology under a human sign-off; an unapproved one is refused by name; the sign-off, the "
          "marker and the lock's own two halves deny unconditionally; a legacy bundle is unchanged "
          "and a valid sign-off alone does NOT unlock it; severity is on no code path; shell writes "
          "are detected; source code in a package named ontology is NOT meaning"
          % (GUARD_CONTRACT, total[0], total[0]))
    return 0


def _put(path, text):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


# ---------------------------------------------------------------- main

def _explain(path):
    """Read-only: the verdict for one path, so an operator or a gate can ask without writing."""
    root = repo_root(path)
    print("path:      %s" % path)
    print("bundle:    %s" % root)
    print("contract:  %s" % GUARD_CONTRACT)
    print("protected: %s" % ("yes" if is_protected(path) else "no"))
    reason = _unconditional(path)
    if reason:
        print("family:    UNCONDITIONAL — %s" % reason)
    code, sentence = gate_state(root)
    print("gate:      %s" % code)
    print("           %s" % sentence)
    print("marker:    %s" % ("present" if os.path.exists(os.path.join(root, UNLOCK_MARKER))
                             else "absent"))
    rc, msg = decide({"tool_name": "Write", "tool_input": {"file_path": path}})
    print("verdict:   %s (exit %d)" % ("ALLOW" if rc == 0 else "DENY", rc))
    return rc


def main():
    if "--self-test" in sys.argv:
        return _self_test()
    if "--explain" in sys.argv:
        i = sys.argv.index("--explain")
        if i + 1 >= len(sys.argv):
            sys.stderr.write("usage: ontology_guard.py --explain <path>\n")
            return 2
        return _explain(sys.argv[i + 1])
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # unparseable → not our business
    code, msg = decide(payload)
    if msg:
        sys.stderr.write(msg)
    return code


if __name__ == "__main__":
    sys.exit(main())
