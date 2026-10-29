---
type: Rule
title: Store.trading
state: ruled
---

# Store.trading

> PROJECTED from `ontology/rules/Store.trading.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A store is active while it has no closing date. A store with a closing date is closed, and a closed store is either shut — closed for good — or restructured — closed and replaced. A question about stores covers active stores unless it names another state.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Store
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — store, active, open, closed, trading, shut, restructured, close date
- **Formerly** — `store.resolution.active_is_the_absent_close_date`

## How and where it is implemented

```
  declared at   ontology/concepts/store.yaml#readings.trading
                ontology/relations/dim_store.yaml#columns.status_annotation.rules
  realized by   mac.canon.population_select  (kind resolution)   default: active
                closed: close_date is not null None
                active: everything `closed` is not
                shut: status_annotation = 'Closed'
                restructured: status_annotation = 'Restructured'
  executed by   planner/populations.py — WHICH ROWS a concept has. Named populations as structured predicates (planner/predicates.py), one marked `default`, and the rule's own 
  tested by     RC05  'How many stores do we have?'  board: pass (stale)
  tested by     RC08  'How many stores are closed?'  board: pass (stale)
  tested by     STORE-01  'How many stores are still open?'  board: pass (stale)
  tested by     STORE-12  'List all closed stores'  board: pass (stale)
```

## What was said

> *"stores that are closed, restructured have close date and are not active anymore; other stores without status do not have close date are ONLY stores currently active and this is the scope of our interest in most questions."* — operator, 2026-09-30 (`knowledge/store.md`)

> *"we should define that closed stores have only close date is not null, then the active stores will be the negation of it ... this should be able to avoid the problem by design."* — operator, 2026-10-01 (`knowledge/store.md`)

> *"this is data impurity ... we can fix in transformation ... but the business side is correct"* — operator, 2026-10-01 (`data/transforms/dim_store.sql`)


## Examples

| Question | Reading |
|---|---|
| how many stores are open | stores with no closing date |
