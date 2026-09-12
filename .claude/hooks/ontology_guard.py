#!/usr/bin/env python3
"""ontology_guard.py — PreToolUse hook that makes it mechanically impossible for an assistant to
edit a locked ontology without the operator's explicit unlock.

Wired on Edit|Write|MultiEdit|NotebookEdit. Reads the tool payload on stdin; if the target file is
a governed MEANING file it DENIES the call (exit 2) unless the operator has placed an unlock marker
in that repo. Default state = LOCKED.

Protected (source-agnostic — the kit never names a source):
  • any  …/ontology/**              concepts, rules, edges, shapes, vocabulary, PHASE, rules.lock
  • any  …/PROCESS.md under .claude/
  • any  …/.claude/agents/*{interpreter,evaluator,diagnostician}*.md

Operator unlock, per repo, explicit and temporary:
    touch <repo-root>/.ontology-unlocked     # permit edits
    rm    <repo-root>/.ontology-unlocked     # re-lock when done

FAILURE SEMANTICS — deliberate, and the reason this file must never be installed without its
settings block or vice versa:
  • unparseable payload, or a tool we do not govern  → exit 0 (fail OPEN; never brick unrelated work)
  • positively identified protected path, no marker  → exit 2 (fail CLOSED; deny)
  • THIS SCRIPT MISSING → the interpreter itself exits 2, which the host reads as DENY for EVERY
    edit in the repo, not just ontology ones. A half-installed lock bricks the repo rather than
    silently vanishing. Install both halves atomically; `--self-test` and the installer both check.

Run `python3 ontology_guard.py --self-test` to prove the guard reds on mutants and greens on a
clean fixture. Exits 0 on pass, 1 on failure, and prints one PASS:/FAIL: line.
"""
import json
import os
import re
import sys
import tempfile

GOVERNED_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
UNLOCK_MARKER = ".ontology-unlocked"

_AGENT_DECISION = re.compile(r"/\.claude/agents/[^/]*(interpreter|evaluator|diagnostician)[^/]*\.md$")


def is_protected(path: str) -> bool:
    """True if `path` names a governed meaning file."""
    if "/ontology/" in path:
        return True
    if "/.claude/" in path and path.endswith("PROCESS.md"):
        return True
    return bool(_AGENT_DECISION.search(path))


def repo_root(path: str) -> str:
    """The directory holding the ontology/ or .claude/ folder that `path` lives under."""
    for anchor in ("/ontology/", "/.claude/"):
        i = path.find(anchor)
        if i != -1:
            return path[:i]
    return os.path.dirname(path)


def decide(payload: dict) -> tuple:
    """(exit_code, message). Pure — the unit under test."""
    if payload.get("tool_name") not in GOVERNED_TOOLS:
        return 0, ""
    path = ((payload.get("tool_input") or {}).get("file_path") or "").strip()
    if not path or not is_protected(path):
        return 0, ""
    root = repo_root(path)
    if os.path.exists(os.path.join(root, UNLOCK_MARKER)):
        return 0, ""
    marker = os.path.join(root, UNLOCK_MARKER)
    return 2, (
        "BLOCKED by ontology_guard: this is a LOCKED meaning file — the assistant must NOT edit "
        "the ontology.\n"
        f"  file: {path}\n"
        "  The operator approves the exact diff, then unlocks explicitly:\n"
        f"      touch {marker}\n"
        "  and re-locks afterwards (rm the marker). No edit happens without that unlock.\n"
    )


# ---------------------------------------------------------------- self-test

def _self_test() -> int:
    failures = []

    def check(name, got, want):
        if got != want:
            failures.append(f"{name}: got exit {got}, want {want}")

    with tempfile.TemporaryDirectory() as tmp:
        onto = os.path.join(tmp, "repo", "ontology", "concepts")
        os.makedirs(onto)
        target = os.path.join(onto, "Thing.yaml")
        open(target, "w").close()
        edit = {"tool_name": "Edit", "tool_input": {"file_path": target}}

        # MUTANT 1 — a protected file with no unlock marker must be denied.
        check("protected/locked", decide(edit)[0], 2)

        # CLEAN — the operator's explicit unlock must permit the edit.
        marker = os.path.join(tmp, "repo", UNLOCK_MARKER)
        open(marker, "w").close()
        check("protected/unlocked", decide(edit)[0], 0)

        # MUTANT 2 — removing the marker must re-lock (no cached permission).
        os.remove(marker)
        check("protected/re-locked", decide(edit)[0], 2)

        # MUTANT 3 — a decision agent-def is protected too.
        agents = os.path.join(tmp, "repo2", ".claude", "agents")
        os.makedirs(agents)
        adef = os.path.join(agents, "x-interpreter.md")
        check("agent-def/locked", decide({"tool_name": "Write", "tool_input": {"file_path": adef}})[0], 2)

        # MUTANT 4 — PROCESS.md under .claude/ is protected.
        proc = os.path.join(tmp, "repo2", ".claude", "PROCESS.md")
        check("process/locked", decide({"tool_name": "Edit", "tool_input": {"file_path": proc}})[0], 2)

        # FAIL-OPEN 1 — an ordinary file must never be blocked.
        data = os.path.join(tmp, "repo", "data", "datasets", "d.yaml")
        check("ordinary-file", decide({"tool_name": "Edit", "tool_input": {"file_path": data}})[0], 0)

        # FAIL-OPEN 2 — a tool we do not govern is none of our business.
        check("ungoverned-tool", decide({"tool_name": "Bash", "tool_input": {"command": "ls"}})[0], 0)

        # FAIL-OPEN 3 — a payload with no path must not brick the session.
        check("empty-path", decide({"tool_name": "Edit", "tool_input": {}})[0], 0)

    if failures:
        for f in failures:
            sys.stderr.write(f"  {f}\n")
        print(f"FAIL: ontology_guard self-test — {len(failures)} of 8 assertions failed")
        return 1
    print("PASS: ontology_guard self-test — 8/8 (4 mutants deny, 3 fail-open cases allow, 1 unlock allows)")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
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
