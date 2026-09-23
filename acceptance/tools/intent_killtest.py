"""Kill-test harness: hand-written Intent -> plan() -> classify.

Separates the two failure sources the transcript kept conflating:
  * a hand-written Intent that PLANS  -> the planner is capable; interpretation was the fault
  * a hand-written Intent that FAILS  -> a real planner/declaration gap, named exactly
"""
from __future__ import annotations
import sys, json
from pathlib import Path

from mac_console.ask_engine import load_bundle
from mac_runtime.resolver import LookupResolver
from mac_runtime.resolver.register_match import RegisterResolver
from mac_runtime.resolver.enumeration import EnumerationResolver
from mac_runtime.planner import plan
from mac_runtime.models import Plan, Refusal, Clarification, Intent

ROOT = Path("/Users/e6db365/dev/mac-ontology-contoso")
SCHEMA = "contoso_served"


def build():
    loaded = load_bundle("example", "contoso", ROOT)
    index = loaded.index.with_default_schema(SCHEMA)
    # the meaning plane: 8 system concepts merged in, same as the live loader
    try:
        from mac_runtime.meaning_plane import generate_system_concepts, generate_system_edges
        from mac_runtime.ontology.graph import Graph
        sys_concepts = generate_system_concepts(SCHEMA, index)  # dict[str, Concept]
        for name, c in sys_concepts.items():
            index.concepts.setdefault(name, c)
            index.groundings.setdefault(name, c.grounding)
        for e in generate_system_edges(SCHEMA):
            try: index.edges.add(e)
            except Exception: pass
    except Exception as exc:  # meaning plane optional for the kill-test
        print(f"  (meaning plane not merged: {exc})", file=sys.stderr)
    # Mirror the live loader: self-entries are recomputed for the MERGED index, so the
    # meaning-plane concepts resolve as slice/filter terms and not only as subjects.
    from dataclasses import replace as _dc_replace
    from mac_runtime.resolver.registers import self_entries_for
    _selves = self_entries_for(index)
    registers = _dc_replace(loaded.registers, entries=_selves, self_entries=len(_selves))
    resolver = RegisterResolver(
        registers,
        inner=EnumerationResolver(index, inner=LookupResolver(index, registers.entries)),
    )
    return index, resolver


def _fill(payload: dict) -> dict:
    """Default the `utterance` bookkeeping field so hand-written intents stay readable.

    `utterance` is what the LLM echoes back as the phrase it matched; for a hand-written
    intent there is no phrase, so it mirrors the term. It does not affect planning.
    """
    p = dict(payload)
    for key in ("slices", "filters"):
        if key in p:
            p[key] = [
                {**r, "utterance": str(r.get("utterance") or r.get("term") or "")}
                for r in p[key]
            ]
    return p


def classify(outcome):
    if isinstance(outcome, Plan):
        return "PLAN", (outcome.sql_preview or "").replace("\n", " ")
    if isinstance(outcome, Refusal):
        return "REFUSAL", f"{getattr(outcome,'reason_code','')}: {getattr(outcome,'missing','')}"
    if isinstance(outcome, Clarification):
        return "CLARIFY", str(getattr(outcome, "question", ""))
    return "OTHER", repr(outcome)[:200]


def run(intents: dict[str, dict]):
    index, resolver = build()
    results = {}
    for qid, payload in intents.items():
        payload = _fill(payload)
        try:
            intent = Intent(confidence=1.0, **payload)
        except Exception as exc:
            results[qid] = ("INTENT_INVALID", f"{type(exc).__name__}: {exc}"[:300])
            continue
        try:
            results[qid] = classify(plan(intent, index, resolver))
        except Exception as exc:
            results[qid] = ("PLANNER_CRASH", f"{type(exc).__name__}: {exc}"[:300])
    return results


if __name__ == "__main__":
    intents = json.load(open(sys.argv[1]))
    res = run(intents)
    from collections import Counter
    print(Counter(k for k, _ in res.values()))
    for qid, (kind, detail) in sorted(res.items()):
        print(f"\n[{qid}] {kind}\n  {detail[:400]}")
