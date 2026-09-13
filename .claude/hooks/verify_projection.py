#!/usr/bin/env python3
"""verify_projection.py — is this workspace still VANILLA?

Projected into every workspace the kit sets up, and deliberately **standalone**: it reads
`.claude/.kit-manifest.json` and re-hashes what is on disk. It does not need the kit, the network,
or any dependency, so a repository can prove its own method has not drifted in CI, on a fresh
clone, or on a machine that has never seen the kit.

WHY THIS EXISTS. Every time this estate copied a method artifact into a second home, it drifted:
skills hand-mirrored into two trees and diverged; two divergent resolvers; two copies of the
ontology guard with different checksums; a vendored ontology fixture that went stale. The one
counter-example is the ontology guard, byte-identical across nine repositories — because it is
INSTALLED by a tool that can prove what it wrote, not copied by hand.

So "vanilla" is not a place. It is a mechanism: projected, never authored in place, and verifiable.
This is the verifier.

    python3 .claude/hooks/verify_projection.py            # PASS/FAIL, exit 0/1
    python3 .claude/hooks/verify_projection.py --json
    python3 .claude/hooks/verify_projection.py --self-test

A FAIL is not necessarily bad news — it means someone edited a projected file, which is exactly the
signal you want. The fix is to move the edit into the kit and re-install, so every workspace gets
it, rather than leaving one repository quietly different from the other eight.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

MANIFEST_REL = Path(".claude") / ".kit-manifest.json"


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verify(repo: Path) -> tuple[int, dict]:
    mf = repo / MANIFEST_REL
    if not mf.is_file():
        return 2, {"status": "no-manifest", "detail": str(MANIFEST_REL)}
    try:
        m = json.loads(mf.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return 2, {"status": "unreadable-manifest", "detail": str(exc)}

    files = m.get("files")
    if isinstance(files, list):
        # A manifest from before hashes were recorded cannot answer the question. Saying so beats
        # reporting a green that means "did not compare".
        return 2, {"status": "manifest-has-no-hashes", "track": m.get("track"),
                   "detail": "re-run install_workspace.py to record hashes"}
    files = files or {}

    missing, edited = [], []
    for rel, want in sorted(files.items()):
        f = repo / rel
        if not f.is_file():
            missing.append(rel)
        elif _sha256(f) != want:
            edited.append(rel)

    out = {"status": "vanilla" if not (missing or edited) else "drifted",
           "track": m.get("track"), "kit_commit": m.get("kit_commit", "unknown"),
           "checked": len(files), "missing": missing, "edited": edited}
    return (0 if out["status"] == "vanilla" else 1), out


def _self_test() -> int:
    f: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        d = repo / ".claude" / "agents"
        d.mkdir(parents=True)
        (d / "a.md").write_text("alpha", encoding="utf-8")
        (d / "b.md").write_text("beta", encoding="utf-8")
        mf = repo / MANIFEST_REL
        good = {".claude/agents/a.md": _sha256(d / "a.md"), ".claude/agents/b.md": _sha256(d / "b.md")}
        mf.write_text(json.dumps({"track": "t", "kit_commit": "abc", "files": good}), encoding="utf-8")

        if verify(repo)[0] != 0:
            f.append("an untouched projection must verify vanilla")

        (d / "a.md").write_text("TAMPERED", encoding="utf-8")
        rc, out = verify(repo)
        if rc != 1 or out["edited"] != [".claude/agents/a.md"]:
            f.append("an edited file must be reported as drifted, by name")
        (d / "a.md").write_text("alpha", encoding="utf-8")

        (d / "b.md").unlink()
        rc, out = verify(repo)
        if rc != 1 or out["missing"] != [".claude/agents/b.md"]:
            f.append("a deleted file must be reported as missing, by name")
        (d / "b.md").write_text("beta", encoding="utf-8")

        # A manifest with no hashes cannot answer, and must NOT answer green.
        mf.write_text(json.dumps({"track": "t", "files": [".claude/agents/a.md"]}), encoding="utf-8")
        if verify(repo)[0] != 2:
            f.append("a hashless manifest must be COULD NOT RUN, never a pass")

        mf.unlink()
        if verify(repo)[0] != 2:
            f.append("a missing manifest must be COULD NOT RUN, never a pass")

        if verify(repo)[0] == 0:
            f.append("nothing above may end in a green")

    if f:
        for x in f:
            sys.stderr.write(f"  {x}\n")
        print(f"FAIL: verify_projection self-test — {len(f)} of 6 assertions failed")
        return 1
    print("PASS: verify_projection self-test — 6/6 (vanilla, edited, deleted, hashless, absent, no false green)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Prove this workspace's projected method is unmodified.")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return _self_test()

    rc, out = verify(a.repo.resolve())
    if a.json:
        print(json.dumps(out, indent=2, sort_keys=True))
        return rc
    if rc == 2:
        print(f"COULD NOT RUN: verify_projection — {out['status']} (not a verdict)")
        return 2
    for r in out["missing"]:
        sys.stderr.write(f"  MISSING: {r}\n")
    for r in out["edited"]:
        sys.stderr.write(f"  EDITED:  {r}\n")
    if rc:
        sys.stderr.write("  fix: move the edit into the kit and re-install, so every workspace gets it\n")
        print(f"FAIL: verify_projection — {len(out['missing'])} missing, {len(out['edited'])} edited "
              f"of {out['checked']} projected (track={out['track']}, kit={out['kit_commit'][:8]})")
    else:
        print(f"PASS: verify_projection — {out['checked']} projected files unmodified "
              f"(track={out['track']}, kit={out['kit_commit'][:8]})")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
