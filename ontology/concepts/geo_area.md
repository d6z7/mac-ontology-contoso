---
type: Reference
title: Region
description: A sub-national region — a state, province, territory or county — identified by an integer key the delivery carries on both the customer and the store row.
tags:
- CONTOSO
- reference
- confidence:I
resource: table://dim_contoso_customer
rule_pages:
- rules/geo_area.register.declared_gap_on_the_store_side.md
- rules/geo_area.sentinel.online_has_no_region.md
---

A sub-national region — a state, province, territory or county — identified by an integer key the delivery carries on both the customer and the store row. 608 regions across the 8 countries, named from the customer dimension.
IT HAS NO TABLE. There is no geography relation anywhere in this delivery to join the key to, so the names live in a register cut from the customer dimension rather than in a dimension of their own. A key is never presented bare.
THE REGISTER DOES NOT COVER THE STORE SIDE COMPLETELY, and this is the sharp edge. Measured 2026-09-18: 3 of the 67 store regions have NO customer in them and therefore NO row in the register — GeoAreaKey 79 (GB, Ayrshire), 291 (GB, North Down) and 519 (IT, Pesaro), carrying 6 708 of 223 974 lines between them. Those three resolve by the store row's own `State` column and by nothing else.
IT IS NOT A CONTINENT OR A COUNTRY. This is the leaf below country; the roll-up above it is Country, then Continent.

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
All 608 customer-side regions are in data/lookups/contoso_geo_area.lookup.csv, cut from the served plane, each with a search key, its state abbreviation and its country — so a region word resolves offline and the roll-up to country needs no probe. The 3 store-only regions named in the definition are the register's declared gap, resolvable from the store row's own `State` column, which is declared above. A region word that resolves to neither is a refusal derived from the register plus that declared gap, rather than from an empty query.
```

## Grounded in

- `dim_contoso_customer` — key `CustomerKey`
- `dim_contoso_store` — key `StoreKey`

## Grain
one row = one region key, in the dimension that carries it

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `CustomerKey` | integer | key | `dim_contoso_customer` (key) | — | — |
| `GeoAreaKey` | integer | key | `dim_contoso_customer`, `dim_contoso_store` | 608 distinct values and no geography relation to join (P1 O9); determines Country and Continent (measured, P2). | — |
| `State` | varchar | dimension | `dim_contoso_customer`, `dim_contoso_store` | — | — |
| `StateFull` | varchar | attribute | `dim_contoso_customer` | — | — |
| `Country` | varchar | dimension | `dim_contoso_customer` | 8 measured values; covers every store country except the sentinel '--' (S11, S12). | — |
| `StoreKey` | integer | key | `dim_contoso_store` (key) | — | — |
| `CountryCode` | varchar | dimension | `dim_contoso_store` | 9 measured values, one of which is the sentinel '--' on the 'Online' row. | — |

_Declared per column, over 7 columns: description 3 of 7 · type 7 of 7 · joins → 0 of 7. An em dash is a column for which nothing is declared._

## Relationships

*0 join(s) out · 2 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Customer](customer.md) — on `GeoAreaKey`
- [Store](store.md) — on `GeoAreaKey`

## Source of record
- Full MAC concept: `geo_area.yaml` — open the **YAML** tab for the complete typed definition.