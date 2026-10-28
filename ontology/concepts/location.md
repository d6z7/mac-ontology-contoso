---
type: Entity
title: Location
description: THE PLACE a store stands on — a country and a state, and nothing that belongs to the shop itself.
tags:
- CONTOSO5
- entity
- confidence:I
rule_pages:
- rules/location.exclusion.the_online_row_is_not_a_place.md
---

THE PLACE a store stands on — a country and a state, and nothing that belongs to the shop itself. Floor area, opening and closing dates are properties of PREMISES and live on Store; what a place owns is where it is.
ONE PLACE MAY HOLD A SUCCESSION OF PREMISES over time, which is the fact this concept exists to keep separate from Store: `dim_store.store_key` declares `finer_than: location_code`, so premises roll UP into a place and a place never divides down into one. Summing a per-premises measure over a place that has been re-let counts it once per tenancy.
A PLACE IS NOT A CITY IN THIS BUNDLE. Its finest geography is `state`, which in France means regions and overseas territories; `main.store` carries no city or town column. City exists only on the customer, as where a customer lives, and is declared personally identifying.
No counts here, by the ruling of 2026-10-24 — they belong in data/profiles/dim_location.yaml where they can be re-measured. The account is knowledge/location.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.3.0-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-29

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

**1 binding rule(s)** — each one's clauses are on its own page; these are not optional and not defaults an answer may silently ignore.

- [location.exclusion.the_online_row_is_not_a_place](rules/location.exclusion.the_online_row_is_not_a_place.md) — `exclusion` · binds `location_code` · confidence P

## Grounded in

- `dim_location` — key `location_code` — semantics: [`ontology/relations/dim_location.yaml`](../relations/dim_location.md)

## Grain

- One row is one Location, identified by `location_code`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `location_code` | integer | key | — | — | — | — | — | — |
| `country_code` | string | dimension | — | — | — | — | — | [Country](country.md) |
| `country_name` | string | dimension | — | — | label_of `country_code` (long) | — | — | — |
| `state` | string | dimension | — | — | finer_than `country_code` | — | — | — |
| `units_ever_here` | integer | measure | — | precomputed · units | — | — | — | — |

_Declared per column, over 5 columns: type 5 of 5 · role 5 of 5 · identity 0 of 5 · measure 1 of 5 · rulings 2 of 5 · register 0 of 5 · description 0 of 5 · joins → 1 of 5. An em dash is a column for which nothing is declared._

## Axes

Measure type: `precomputed`.

| axis | axis kind | fold |
|---|---|---|
| `country_code` | categorical | none |
| `country_name` | categorical | none |
| `state` | categorical | none |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*1 join(s) out · 1 in — click a concept to open it.*

**Joins to** — this concept references:

- [Country](country.md) — joined on `country_code`

**Referenced by** — these point at this concept:

- [Store](store.md) — on `location_code`

## Source of record

- Full MAC concept: `location.yaml` — open the **YAML** tab for the complete typed definition.
