---
type: Entity
title: Store
description: THE PREMISES Contoso sells from — a shop that stood on one place for one trading period, with its own name, floor area, opening date and closing date.
tags:
- CONTOSO5
- entity
- confidence:I
rule_pages:
- rules/store.resolution.the_channel_is_the_location_sentinel.md
- rules/store.resolution.active_is_the_absent_close_date.md
---

THE PREMISES Contoso sells from — a shop that stood on one place for one trading period, with its own name, floor area, opening date and closing date. It is what every sale is recorded against.
A PLACE MAY HOLD A SUCCESSION OF PREMISES, so a store is NOT its place: see the Location concept for the place, and `dim_store.store_key#rulings.finer_than` for the declaration that one rolls up into the other. The account is knowledge/store.md.
THIS DEFINITION CARRIES NO COUNTS, by the operator's ruling of 2026-10-24: "you are disclosing values that variy through the time as constnts?!?!?! this is no go ... you can decribe things without constants too". It used to say how many stores there were and how many were trading, which was a measurement of one day frozen into a sentence — and it disagreed with this concept's own `counts:` key, which is how one word came to name two grains. Counts belong where they can be re-measured: data/profiles/dim_store.yaml.

## Details

- **Version** — 1.1
- **Schema version** — 0.3.1-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-30

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

**2 binding rule(s)** — each one's clauses are on its own page; these are not optional and not defaults an answer may silently ignore.

- [store.resolution.the_channel_is_the_location_sentinel](rules/store.resolution.the_channel_is_the_location_sentinel.md) — `resolution` · binds `store_code` · confidence P
- [store.resolution.active_is_the_absent_close_date](rules/store.resolution.active_is_the_absent_close_date.md) — `resolution` · binds `close_date`, `status_annotation` · confidence C

## Grounded in

- `dim_store` — key `store_key` — semantics: [`ontology/relations/dim_store.yaml`](../relations/dim_store.md)

## Grain

- One row is one Store, identified by `store_key`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `store_key` | integer | key | — | — | finer_than `store_code` | — | — | — |
| `store_code` | integer | key | -> Location | — | — | — | — | [Location](location.md) |
| `store_name` | string | dimension | — | — | label_of `store_code` (common) | — | — | — |
| `country_code` | string | dimension | — | — | — | — | — | [Country](country.md) |
| `state` | string | dimension | — | — | — | — | — | — |
| `open_date` | date | dimension | — | — | — | — | — | — |
| `close_date` | date | dimension | — | — | — | — | — | — |
| `status_annotation` | string | dimension | — | — | — | — | — | — |
| `square_metres` | integer | measure | — | stock · m2 | — | — | — | — |

_Declared per column, over 9 columns: type 9 of 9 · role 9 of 9 · identity 1 of 9 · measure 1 of 9 · rulings 2 of 9 · register 0 of 9 · description 0 of 9 · joins → 2 of 9. An em dash is a column for which nothing is declared._

## Axes

Measure type: `stock`.

| axis | axis kind | fold |
|---|---|---|
| `close_date` | time | none |
| `country_code` | categorical | additive |
| `open_date` | time | none |
| `state` | categorical | additive |
| `status_annotation` | categorical | additive |
| `store_name` | categorical | additive |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*2 join(s) out · 1 in — click a concept to open it.*

**Joins to** — this concept references:

- [Country](country.md) — joined on `country_code`
- [Location](location.md) — joined on `store_code`

**Referenced by** — these point at this concept:

- [Order](order.md) — on `store_key`

## Source of record

- Full MAC concept: `store.yaml` — open the **YAML** tab for the complete typed definition.
- Source table: [store](../../data/sources/store.md)
