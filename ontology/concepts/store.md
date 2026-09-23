---
type: Reference
title: Store
description: 'A retail outlet, served as ONE ROW PER VERSION of that outlet: 74 versions of 67 stores, each with its own validity window, geography, floor area and status.'
tags:
- CONTOSO
- reference
- confidence:I
resource: table://dim_contoso_store
rule_pages:
- rules/store.versions.entity_count_is_the_code.md
- rules/store.sentinel.online_is_served.md
---

A retail outlet, served as ONE ROW PER VERSION of that outlet: 74 versions of 67 stores, each with its own validity window, geography, floor area and status. The order line carries the version it was placed against.
IT IS NOT ONE ROW PER STORE. Six store codes carry more than one version and one carries three; the windows do not overlap (measured 0 overlapping pairs). So a count of rows here is a count of versions, and a question about "how many stores" means 67, not 74.
IT IS NOT A LIST OF PHYSICAL PLACES EITHER. The sentinel version — StoreKey 999999, StoreCode -1, GeoAreaKey -1, CountryCode '--', CountryName and State both 'Online' — is a SALES CHANNEL sitting in a store dimension. It IS served, because 93 550 of 223 974 lines (41.8 %) point at it: dropping it is the single largest silent error available in this bundle.
AND ITS GEOGRAPHY STOPS AT COUNTRY. There is no continent column here (measured 0), so a store-side continent roll-up is not servable; that level exists only on the customer side.

## Details

- **Identity** — fk_name
- **Version** — 1.0
- **Schema version** — 0.1.14
- **Status** — draft
- **Owner** — operator
- **Governance owner** — operator
- **Last reviewed** — 2026-09-18

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
All 74 versions are in data/lookups/dim_contoso_store.lookup.csv, cut from the served plane, each with its description as a search key, its store code, country, state and status — so a store word resolves offline to a StoreKey. The version collapse is the declared snapshot_rule with a canon behind it, the status value set is the StoreStatus concept, and the geography resolves through data/lookups/contoso_country.lookup.csv and data/lookups/contoso_geo_area.lookup.csv. Nothing here needs a probe.
```

## Grounded in

- `dim_contoso_store` — key `StoreKey`

## Grain
one row = one VERSION of one store — StoreKey; the business entity is StoreCode

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `StoreKey` | integer | key | `dim_contoso_store` (key) | StoreKey — the version surrogate, the identity, and the column the fact joins on. | [Store Status](store_status.md) _(business)_ |
| `StoreCode` | integer | key | `dim_contoso_store` | the store's natural code; NOT unique (67 codes over 74 rows). (StoreCode, OpenDate) is measured unique (74/74) — the natural temporal key of the SCD-2 (P2 G6). | — |
| `GeoAreaKey` | integer | key | `dim_contoso_store` | no geography relation exists in this delivery to join it to (P1 O9); it behaves as a state/region key (1:1 with State, measured P2). | [Region](geo_area.md) _(business)_ |
| `CountryCode` | varchar | dimension | `dim_contoso_store` | 9 measured values, one of which is the sentinel '--' on the 'Online' row. | [Country](country.md) _(business)_ |
| `CountryName` | varchar | attribute | `dim_contoso_store` | 9 measured values, one of which is 'Online' — a channel sitting in a country column (RUN.md Q7). Not corrected here: correcting it would invent a market for 41.8 % of the fact. | — |
| `State` | varchar | dimension | `dim_contoso_store` | — | — |
| `Description` | varchar | attribute | `dim_contoso_store` | Description — the outlet's display name, and the register's search key. | — |
| `OpenDate` | date | dimension | `dim_contoso_store` | DATE since 2026-09-19, cast in the transform from the landing's TIMESTAMP on the operator's ruling; lossless and measured, not assumed — 0 non-midnight over 74 of 74 rows immediately before the cast. main.store keeps TIMESTAMP. This is the version-ordering column of the SCD-2 dimension and the cast preserves the uniqueness claim exactly: (StoreCode, OpenDate) is 74 distinct pairs over 74 rows, re-measured after. | — |
| `CloseDate` | date | dimension | `dim_contoso_store` | null on 58/74 rows (P1 #5). DATE since 2026-09-19, same cast as OpenDate; lossless over the 16 of 74 non-null values (0 non-midnight), and a cast leaves the 58 nulls null. | — |
| `SquareMeters` | integer | measure | `dim_contoso_store` | null on 1/74 rows (the sentinel). | — |
| `Status` | varchar | dimension | `dim_contoso_store` | CLEANSED: the landing spells missing two ways, '' on 58 rows and NULL on 1 (P1 #5); the served column uses NULL for both. Whether '' meant 'operating' is an open ruling (Q7). | — |

_Declared per column, over 11 columns: description 10 of 11 · type 11 of 11 · joins → 3 of 11. An em dash is a column for which nothing is declared._

## Relationships

*3 join(s) out · 1 in — click a concept to open it.*

**Joins to** — this concept references:

- [Country](country.md) — joined on `CountryCode`
- [Region](geo_area.md) — joined on `GeoAreaKey`
- [Store Status](store_status.md) — joined on `StoreKey`

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `StoreKey`

## Source of record
- Full MAC concept: `store.yaml` — open the **YAML** tab for the complete typed definition.

## Data
- Source table: [store](../../data/sources/store.md)
