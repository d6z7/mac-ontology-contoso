---
type: Rule
title: Store.premises_not_place
state: ruled
---

# Store.premises_not_place

> PROJECTED from `ontology/rules/Store.premises_not_place.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A store is the premises Contoso sells from: a shop standing on one place for one trading period, with its own name, floor area, opening date and closing date. It is part of a location, not the location itself — one place may hold a succession of premises over time, each of them a store. So one store is counted by its premises, and a count or sum over stores is a different question from the same figure over places; an answer that could be read at either level says which level it used.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Location, Store
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — store, premises, shop, location, place, site, count stores, tenancy
- **Supersedes** — `Store.counted_by_site`

## How and where it is implemented

```
  declared at   ontology/relations/dim_location.yaml#columns.units_ever_here.rules
  tested by     RC05  'How many stores do we have?'  board: pass (stale)
```

## What was said

> *"a Store is a PLACE on one location you can shop at ... store is part of location"* — operator, 2026-10-24 (`ontology/concepts/store.yaml`)
