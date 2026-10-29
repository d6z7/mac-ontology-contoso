---
type: Rule
title: Country.rows
state: proposed
---

# Country.rows

> PROJECTED from `ontology/rules/Country.rows.yaml` by tools/mac_rules.py — do not edit; change the yaml.

The placeholder country code `--` is not a country. It marks rows that carry no real country, such as the online store. Questions about countries count and list real countries only, unless they name the placeholder.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Country
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — country, countries, placeholder, sentinel, no country, unknown country, online
- **Formerly** — `country.exclusion.sentinel_is_not_a_country`

## How and where it is implemented

```
  declared at   ontology/concepts/country.yaml#readings.rows
                ontology/relations/dim_country.yaml#columns.country_code.rules
  realized by   mac.canon.population_select  (kind resolution)   default: real
                real: country_code != '--'
                sentinel: country_code = '--'
  executed by   planner/populations.py — WHICH ROWS a concept has. Named populations as structured predicates (planner/predicates.py), one marked `default`, and the rule's own 
  tested by     RC02  'List all countries where we have customers.'  board: pass (stale)
```

## Examples

| Question | Reading |
|---|---|
| how many countries do we sell in | real countries only; the placeholder is not counted |
