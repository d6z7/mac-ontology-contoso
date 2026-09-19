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

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `StoreKey` | key | `dim_contoso_store` (key) |  |  |
| `StoreCode` | key | `dim_contoso_store` |  |  |
| `GeoAreaKey` | key | `dim_contoso_store` |  |  |
| `CountryCode` | dimension | `dim_contoso_store` |  |  |
| `CountryName` | attribute | `dim_contoso_store` |  |  |
| `State` | dimension | `dim_contoso_store` |  |  |
| `Description` | attribute | `dim_contoso_store` |  |  |
| `OpenDate` | dimension | `dim_contoso_store` |  |  |
| `CloseDate` | dimension | `dim_contoso_store` |  |  |
| `SquareMeters` | measure | `dim_contoso_store` |  |  |
| `Status` | dimension | `dim_contoso_store` |  |  |

## Relationships

*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `StoreKey`

## Source of record
- Full MAC concept: `store.yaml` — open the **YAML** tab for the complete typed definition.

## Data
- Source table: [store](../../data/sources/store.md)
