---
type: Reference
title: Usage guardrails — how to answer CONTOSO safely
tags: [reference, guardrail]
---

# Usage guardrails (read first)

This page is projected from the ontology — every routing decision, default, and prohibition below
is authored on a concept, not invented here. **Only interpretation is probabilistic; generate SQL
from the question + this ontology ALONE, never from a live probe.** A fact the ontology does not
state is a GAP to flag, not a value to guess.

## Routing — which serving relation answers what

| concept | class | relation | answer with |
|---|---|---|---|

## How to answer — per-concept playbooks (verbatim `no_probe_guarantee`)

## Filter traps & known issues

Recorded data-quality findings that change how you must query. Full detail in `references/known_issues/`.

- [NS-CUSTOMER-01](known_issues/NS-CUSTOMER-01.md) — _low_ · 12 of the 24 customer columns measured, deliberately not served · **not yet reconciled**
- [NS-ORDERS-01](known_issues/NS-ORDERS-01.md) — _low_ · `sales` measured, deliberately not served — it is the served order line delivered a second time · **resolved**
- [NS-ORDERS-02](known_issues/NS-ORDERS-02.md) — _low_ · the order header measured, deliberately not served as a relation of its own · **not yet reconciled**
- [NS-SERVING-01](known_issues/NS-SERVING-01.md) — _medium_ · 15 leftover views in the warehouse, measured, neither treated as sources nor served · **not yet reconciled**
