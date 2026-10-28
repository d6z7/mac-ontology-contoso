#!/usr/bin/env python3
"""Extract one TRACE per capture: every hop from the question to the answer, plus what each hop LOST.

WHY IT EXISTS. The captures already record five stages -- load, interpret, plan, execute, evaluate --
each with its own `detail`. Nothing read them together, so a question that came out wrong was
diagnosed by hand, one YAML at a time. Measured 2026-10-01: RC08 was diagnosed from the 13:49 capture
while a background run rewrote it at 15:05 with a DIFFERENT intent and a different failure mode, and
the diagnosis was of a file that no longer existed. Every trace here carries its `captured_at` for
exactly that reason.

THE LOSS RULES ARE NOT HERE. They live in `mac-console/trace_losses.py`, the one home, which the live
Debug view reaches through POST /trace/{domain}/{dataset}/losses and this extractor imports directly.
Two copies of a diagnostic drift, and the one you are not reading is the one that is right.

Usage:  python3 tools_trace_extract.py [bundle_root] > traces.json
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

import yaml

#: The console package, for the shared loss rules. A path rather than a dependency: this bundle is a
#: worked example and must stay installable without the platform on sys.path -- the import below is
#: the only thing that needs it, and it fails loudly rather than silently skipping the diagnosis.
#:
#: FOUND, NEVER TYPED. This line held one operator's home directory, which was two defects at once:
#: an identity leak in a bundle whose declared leak floor is zero (`check_mac_public` reported it
#: twice, as a home path and as a user id), and a tool that could not run on any other machine. The
#: order is the estate's: `$MAC_CONSOLE_SRC` wins, because an operator who sets it knows where their
#: checkout is; otherwise the repositories sit beside each other, so the location is DERIVED from
#: this file's own position and names no home.
_ENV_CONSOLE = "MAC_CONSOLE_SRC"
#: contoso5 -> example -> the sources repository; the platform checkout is its neighbour.
_SIBLING_CONSOLE = (pathlib.Path(__file__).resolve().parents[2].parent
                    / "mac-platform" / "packages" / "mac-console" / "src" / "mac_console")


def _console_src() -> pathlib.Path:
    """The directory holding the shared loss rules, or an error that NAMES what to set."""
    for cand in (os.environ.get(_ENV_CONSOLE), _SIBLING_CONSOLE):
        if cand and (pathlib.Path(cand) / "trace_losses.py").is_file():
            return pathlib.Path(cand).resolve()
    raise ImportError(
        f"the console's loss rules are neither beside this bundle nor configured: set "
        f"${_ENV_CONSOLE} to the directory holding trace_losses.py"
    )


_CONSOLE = _console_src()
if str(_CONSOLE) not in sys.path:
    sys.path.insert(0, str(_CONSOLE))

import trace_losses  # noqa: E402


def _stage(doc: dict, name: str) -> dict | None:
    """The LAST stage with this name -- interpret can run twice and the second is what shipped."""
    found = None
    for stage in doc.get("stages") or []:
        if (stage or {}).get("stage") == name:
            found = stage
    return found


def trace(path: pathlib.Path, types: dict[str, str]) -> dict:
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    interpret = (_stage(doc, "interpret") or {}).get("detail") or {}
    load = (_stage(doc, "load") or {}).get("detail") or {}
    plan_detail = (_stage(doc, "plan") or {}).get("detail") or {}
    execute = (_stage(doc, "execute") or {}).get("detail") or {}
    evaluate = (_stage(doc, "evaluate") or {}).get("detail") or {}
    plan = plan_detail.get("plan") or {}
    n_interpret = sum(1 for s in doc.get("stages") or [] if (s or {}).get("stage") == "interpret")

    return {
        "id": doc.get("id") or path.stem,
        "captured_at": doc.get("captured_at"),
        "route": doc.get("route"),
        "question": interpret.get("question_sent"),
        "answer": doc.get("answer"),
        "result": doc.get("result") or {},
        "engine": (doc.get("engine") or {}).get("resolved_model"),
        "ontology_fingerprint": doc.get("ontology_fingerprint"),
        "interpret_passes": n_interpret,
        "stage_status": {
            (s or {}).get("stage"): (s or {}).get("status") for s in doc.get("stages") or []
        },
        "hops": [
            {"name": "load", "detail": {
                "pack": (load.get("pack") or {}).get("name"),
                "concepts": load.get("concepts"), "measures": load.get("measures"),
                "dimensions": load.get("dimensions"), "rules": load.get("rules"),
                "edges": load.get("edges"), "register_files": load.get("register_files"),
                "register_entries": load.get("register_entries"),
                "adapter": load.get("adapter_kind"), "skipped": load.get("skipped"),
            }},
            {"name": "interpret", "detail": {
                "question_sent": interpret.get("question_sent"),
                "confidence": interpret.get("confidence"),
                "threshold": interpret.get("threshold"),
                "passes": n_interpret, "error": interpret.get("error"),
                "intent": interpret.get("intent"),
            }},
            {"name": "resolve", "detail": {"resolutions": plan_detail.get("resolutions") or []}},
            {"name": "plan", "detail": {
                "sql": plan.get("sql_preview"), "params": plan.get("params"),
                "concepts_used": plan.get("concepts_used"), "rules_used": plan.get("rules_used"),
                "edges_used": plan.get("edges_used"), "caveats": plan.get("caveats_known"),
                "laws": plan.get("laws_applied"), "pins": plan_detail.get("pins_applied"),
            }},
            {"name": "execute", "detail": {
                "status": execute.get("status"), "facts": execute.get("facts"),
                "bytes_scanned": execute.get("bytes_scanned"), "error": execute.get("error"),
                "sql": doc.get("sql"), "sql_valid": doc.get("sql_valid"),
                "sql_errors": doc.get("sql_errors"),
            }},
            {"name": "evaluate", "detail": {
                "evaluation": evaluate.get("evaluation"), "disclosures": doc.get("disclosures"),
            }},
        ],
        "losses": trace_losses.losses(
            stages=doc.get("stages"),
            route=doc.get("route"),
            result=doc.get("result") if isinstance(doc.get("result"), dict) else None,
            types=types,
        ),
    }


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    types = trace_losses.column_types(root)
    answers = sorted((root / "acceptance" / "answers").glob("*.yaml"))
    traces = [trace(p, types) for p in answers]
    json.dump({"bundle": root.name, "column_types": len(types), "traces": traces},
              sys.stdout, indent=None, default=str)
    print(f"{len(traces)} traces, {sum(len(t['losses']) for t in traces)} losses, "
          f"{len(types)} declared column types read", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
