---
type: Rule
title: Location.site
state: ruled
---

# Location.site

> PROJECTED from `ontology/rules/Location.site.yaml` by tools/mac_rules.py — do not edit; change the yaml.

Site and location name the same notion: the place a store stands on, described by its country and its state or region. A store's place has no city in this business's data — its finest geography is the state or region — and a city is only where a customer lives, so a question about the cities stores are in has no answer here and must say so rather than offer site codes.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Location
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — site, location, place, city, state, region, geography

## How and where it is implemented

```
  declared at   ontology/relations/dim_location.yaml#columns.location_code.rules
  tested by     (nothing names a question)
```

## What was said

> *"dont call it site code ... just site, location, city"* — operator, 2026-10-24 (`ontology/relations/dim_location.yaml`)
