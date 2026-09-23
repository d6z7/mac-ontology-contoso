"""trace_question.py — one question through every planner stage, showing what each stage READ.

WHY THIS EXISTS. A wrong answer looks the same whether the model misread the question or the
planner could not do it, and for a long time nothing here could tell those apart — so the same
question got fixed repeatedly in the wrong layer. Handing the planner an intent YOU wrote answers
it: if the SQL is right, the planner was never the problem.

It prints what each stage read, not just the result, because the interesting part is usually WHY
the anchor moved or WHY a name did not resolve — neither of which is visible in the SQL.

  usage:  <platform>/.venv/bin/python acceptance/tools/trace_question.py cases.json
  input:  {"<id>": {"question": "...", "intent": {"measure": "...", "operation": "...", ...}}}

No database is touched: planning reads declarations only. The SQL is printed, never executed.
Companion to intent_killtest.py, which replays a whole corpus instead of narrating one question.
"""
from __future__ import annotations
import sys, json
from intent_killtest import build, _fill
from mac_runtime.models import Intent, Plan, Refusal, Clarification, OperationKind
from mac_runtime.planner.plan import _resolve_measure, _resolve_slice, _resolve_filter
from mac_runtime.planner.joins import select_anchor
from mac_runtime.planner import plan as run_plan


def trace(question: str, payload: dict, idx, res) -> None:
    print("=" * 96)
    print(f"QUESTION:  {question}")
    print("=" * 96)

    intent = Intent(confidence=1.0, **_fill(payload))
    print(f"\n[1] INTENT            subject={intent.subject!r}  operation={intent.operation}")
    for f in intent.filters:
        print(f"      filter          {f.term} {f.op.value} {f.value!r}")
    for s in intent.slices:
        print(f"      slice           {s.term}" + (f" column={s.column}" if s.column else ""))
    if intent.period:
        print(f"      period          [{intent.period.start} .. {intent.period.end})")
    if intent.ordering:
        print(f"      ordering        by={intent.ordering.by} {intent.ordering.direction}  limit={intent.limit}")

    out = _resolve_measure(intent.subject, idx, operation=intent.operation)
    if isinstance(out, Refusal):
        print(f"\n[2] SUBJECT           REFUSED {out.reason_code.value}: {out.missing}")
        return
    concept, rule = out
    print(f"\n[2] SUBJECT           {concept.name}  class={concept.klass.value}")
    print(f"      declares        canonical_key={concept.identity.canonical_key!r}  "
          f"rule={concept.derived_by_rule!r}")
    print(f"      grounded on     {concept.grounding.table}")

    anchor = select_anchor(concept, rule, idx, intent=intent)
    why = ("the rule names it in `over`" if rule else
           "an event concept carries the counted key" if anchor.name != concept.name else
           "the subject's own relation")
    print(f"\n[3] ANCHOR            {anchor.name} -> FROM {anchor.grounding.table}")
    print(f"      chosen because  {why}")

    print("\n[4] TERMS")
    for s in intent.slices:
        r = _resolve_slice(s, resolver=res, index=idx)
        print(f"      slice {s.term:14} -> {getattr(getattr(r,'concept',None),'name','REFUSED')}")
    for f in intent.filters:
        r = _resolve_filter(f, resolver=res, index=idx, anchor=anchor)
        if isinstance(r, (Refusal, Clarification)):
            print(f"      filter {f.term:13} -> REFUSED {getattr(r,'reason_code','')} "
                  f"{getattr(r,'missing','')}")
        else:
            print(f"      filter {f.term:13} -> {r.concept.name}  value {f.value!r} -> "
                  f"codes {list(r.values)}  (via {'register' if r.registers else 'identity'})")

    outcome = run_plan(intent, idx, res)
    if isinstance(outcome, Refusal):
        print(f"\n[5] PLAN              REFUSED {outcome.reason_code.value}: {outcome.missing}")
        print(f"      reason          {outcome.human_reason[:200]}")
        return
    print(f"\n[5] JOINS/EDGES       {outcome.edges_used or '(none — single relation)'}")
    print(f"    RULES             {outcome.rules_used or '(none)'}")
    print(f"    CONCEPTS          {outcome.concepts_used}")
    print("\n[6] SQL")
    for line in outcome.sql_preview.strip().split("\n"):
        print("      " + line)
    if outcome.params:
        print(f"\n    PARAMS            {outcome.params}")
    if outcome.caveats_known:
        print(f"\n    CAVEATS           {len(outcome.caveats_known)} disclosed")
    print()


if __name__ == "__main__":
    idx, res = build()
    cases = json.load(open(sys.argv[1]))
    for qid, c in cases.items():
        trace(c["question"], c["intent"], idx, res)
