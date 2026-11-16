---
type: Entity
title: Store
description: THE PREMISES Contoso sells from — a shop that stood on one place for one trading period, with its own name, floor area, opening date and closing date.
tags:
- CONTOSO5
- entity
- confidence:I
resource: table://dim_store
---

THE PREMISES Contoso sells from — a shop that stood on one place for one trading period, with its own name, floor area, opening date and closing date. It is what every sale is recorded against.
A PLACE MAY HOLD A SUCCESSION OF PREMISES, so a store is NOT its place: see the Location concept for the place, and `dim_store.store_key#rulings.finer_than` for the declaration that one rolls up into the other. The account is knowledge/store.md.
THIS DEFINITION CARRIES NO COUNTS, by the operator's ruling of 2026-10-24: "you are disclosing values that variy through the time as constnts?!?!?! this is no go ... you can decribe things without constants too". It used to say how many stores there were and how many were trading, which was a measurement of one day frozen into a sentence — and it disagreed with this concept's own `counts:` key, which is how one word came to name two grains. Counts belong where they can be re-measured: data/profiles/dim_store.yaml.

## Details

- **Version** — 1.1
- **Schema version** — 0.4.0-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-30

## How to answer

_No content available — the bundle declares nothing for this section._

## Grounded in

- `dim_store` — key `store_key` — semantics: [`data/datasets/dim_store.yaml`](../../data/datasets/dim_store.md)

## Grain

- One row is one Store, identified by `store_key`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `store_key` | integer | key | — | — | finer_than `store_code` | — | THE PREMISES — one row per shop per trading period, and the grain every sale is recorded against: `v_contoso5_sales_line.store_key` points here, never at the site. A shop has its own name, floor area, opening date and closing date, because those are properties of premises and not of a place. `999999` is the online outlet. A PLACE MAY HOLD A SUCCESSION OF PREMISES, which is why this is finer than `location_code` and why the two must never be used interchangeably: summing floor area over premises counts a re-let site once per tenancy, and counting premises answers a different question from counting sites. The `finer_than` ruling below is what says so to a reader. | — |
| `store_code` | integer | key | -> Location | — | — | — | THE SITE code: several store rows can share it over time. The value -1 is the ONLINE PLACEHOLDER and not a place. The transform turns it into `is_online`, which is what rule Store.channel reads (`physical` is false, `online` is true). | [Location](location.md) |
| `store_name` | string | dimension | — | — | label_of `store_code` (common) | — | the store's name as a reader would see it. 'Online store' is the single non-physical outlet. A reading that finds the online channel by MATCHING THIS NAME is right by luck; the channel is `is_online` (rule Store.channel). | — |
| `country_code` | string | dimension | — | — | — | — | the country the store trades in. The online store carries '--', the sentinel dim_country names 'Online' and country.exclusion.sentinel_is_not_a_country excludes — so this column cannot attribute an internet sale to a real country. | [Country](country.md) |
| `state` | string | dimension | — | — | — | — | the state, province or region the store sits in, within its country. | — |
| `open_date` | date | dimension | — | — | — | — | the day the store opened for trade. | — |
| `close_date` | date | dimension | — | — | — | — | the day the store closed, or null if it is still trading. THE TRADING-STATE COLUMN: `active` is this being null (store.resolution.active_is_the_absent_close_date). | — |
| `status_annotation` | string | dimension | — | — | — | — | why a store stopped trading, where the source said: blank for a trading store, 'Closed' or 'Restructured' for an ended one, null on the online placeholder. Prose from the source, not a closed vocabulary of this bundle's own (rule Store.trading). | — |
| `square_metres` | integer | measure | — | stock · m2 | — | — | the store's floor area in square metres. | — |
| `is_online` | boolean | housekeeping | — | — | — | — | true on the online outlet (its site code is -1), false on every physical shop, never empty. Rule Store.channel reads `physical` as false and `online` as true. | — |
| `is_shut` | boolean | housekeeping | — | — | — | — | true where the store closed for good (`status_annotation` is Closed), false otherwise, never empty. Rule Store.trading reads its `shut` option from it. | — |
| `is_restructured` | boolean | housekeeping | — | — | — | — | true where the store closed and was replaced (`status_annotation` is Restructured), false otherwise, never empty. Rule Store.trading reads its `restructured` option from it. | — |

_Declared per column, over 12 columns: type 12 of 12 · role 12 of 12 · identity 1 of 12 · measure 1 of 12 · rulings 2 of 12 · register 0 of 12 · description 12 of 12 · joins → 2 of 12. An em dash is a column for which nothing is declared._

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
