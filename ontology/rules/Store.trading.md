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
- **Formal** — **Symbolic** — declared at `ontology/concepts/store.yaml#readings.trading`
- **Keywords** — store, active, open, closed, trading, shut, restructured, close date
- **Formerly** — `store.resolution.active_is_the_absent_close_date`

## What was said

> *"stores that are closed, restructured have close date and are not active anymore; other stores without status do not have close date are ONLY stores currently active and this is the scope of our interest in most questions."* — operator, 2026-09-30 (`knowledge/store.md`)

> *"we should define that closed stores have only close date is not null, then the active stores will be the negation of it ... this should be able to avoid the problem by design."* — operator, 2026-10-01 (`knowledge/store.md`)

> *"this is data impurity ... we can fix in transformation ... but the business side is correct"* — operator, 2026-10-01 (`data/transforms/dim_store.sql`)


## Examples

| Question | Reading |
|---|---|
| how many stores are open | stores with no closing date |
