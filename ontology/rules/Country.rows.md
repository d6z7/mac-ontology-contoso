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

## Implemented at

- `ontology/concepts/country.yaml#readings.rows`
- `ontology/relations/dim_country.yaml#columns.country_code.rules`

## Examples

| Question | Reading |
|---|---|
| how many countries do we sell in | real countries only; the placeholder is not counted |
