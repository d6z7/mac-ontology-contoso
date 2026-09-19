---
type: Entity
title: Customer
description: 'A person who can place an order, served as the GEOGRAPHY they belong to plus two generalised demographics: continent, country, state, city, postal code, gender, and a 5-year age band.'
tags:
- CONTOSO
- entity
- confidence:I
resource: table://dim_contoso_customer
rule_pages:
- rules/customer.geography.rollup_only.md
---

A person who can place an order, served as the GEOGRAPHY they belong to plus two generalised demographics: continent, country, state, city, postal code, gender, and a 5-year age band. One row per customer.
IT IS NOT A PERSON RECORD. No name, no address line, no occupation, no company, no vehicle and no coordinates are served — twelve of the landing's twenty-four columns are deliberately withheld (NS-CUSTOMER-01), and `Birthday` is consumed to derive the age band without ever reaching this row.
IT IS ALSO NOT A BUYER LIST. The dimension over-covers the fact by half: 52 189 of the 104 990 customers appear on an order, so a count of customers is not a count of buyers, and the difference is disclosed here rather than filtered away.

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
Read dim_contoso_customer at CustomerKey; the geography words resolve offline through data/lookups/contoso_country.lookup.csv (9 rows, carrying the continent so the country-to-continent roll-up needs no probe) and data/lookups/contoso_geo_area.lookup.csv (608 rows, the delivery's only region key); gender through data/lookups/contoso_gender.lookup.csv (2 rows); the age band through the AgeBand concept's own closed value set. Nothing here needs a warehouse probe, and no register is cut for City or ZipCode because neither is an axis.
```

## Grounded in

- `dim_contoso_customer` — key `CustomerKey`

## Grain
one row = one customer — CustomerKey

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `CustomerKey` | integer | key | `dim_contoso_customer` (key) | CustomerKey — the identity, and the column the fact joins on. | — |
| `GeoAreaKey` | integer | key | `dim_contoso_customer` | 608 distinct values and no geography relation to join (P1 O9); determines Country and Continent (measured, P2). | [Region](geo_area.md) _(business)_ |
| `StartDT` | date | attribute | `dim_contoso_customer` | validity window start. DATE since 2026-09-19, cast in the transform from the landing's TIMESTAMP on the operator's ruling; lossless and measured, not assumed — 0 non-midnight over 104 990 of 104 990 rows immediately before the cast. main.customer keeps TIMESTAMP. No customer is restated today (1 row each, P2 G7) — whether a restatement can arrive is an open ruling (Q12). One customer has StartDT = EndDT. | — |
| `EndDT` | date | attribute | `dim_contoso_customer` | validity window end. DATE since 2026-09-19, same cast and same evidence as StartDT: 0 non-midnight over 104 990 of 104 990 rows. | — |
| `Continent` | varchar | dimension | `dim_contoso_customer` | 3 measured values; the only continent column in the delivery (S10/S11). | — |
| `CountryFull` | varchar | attribute | `dim_contoso_customer` | 8 measured values. | — |
| `Country` | varchar | dimension | `dim_contoso_customer` | 8 measured values; covers every store country except the sentinel '--' (S11, S12). | [Country](country.md) _(business)_ |
| `StateFull` | varchar | attribute | `dim_contoso_customer` | — | — |
| `State` | varchar | dimension | `dim_contoso_customer` | — | — |
| `City` | varchar | attribute | `dim_contoso_customer` | — | — |
| `ZipCode` | varchar | attribute | `dim_contoso_customer` | — | — |
| `Gender` | varchar | dimension | `dim_contoso_customer` | 2 measured values. | — |
| `age_band_5y` | integer | dimension | `dim_contoso_customer` | DERIVED, NOT DELIVERED, AND IT CARRIES AN AS-OF DATE. The customer's age in whole years, floored to a 5-year band and served as the band's LOWER BOUND (20, 25, … 90 — an integer, so it sorts and compares as an age), derived from the unserved `Birthday` AS OF 2025-12-31. That date is the delivery's fact horizon (the newest order date) and is a CHOICE: the same three places must agree on it — the rule `derive-age-band-as-of` in data/transforms/dim_contoso_customer.yaml, the literal in the .sql, and this note. WHEN THE FACT HORIZON MOVES THE BAND MUST BE RE-DERIVED, and nothing enforces that (DQ-CUSTOMER-01, residual risk 1). Measured 2026-09-18: 15 bands, 0 nulls over 104 990 rows, smallest cell 1 396, no customer alone in a band. NOT SERVED alongside it: the stored `Age` (as-of 2020/2021 on every row, and unbanded) and `Birthday` (the identifier this band generalises) — see DQ-CUSTOMER-01 and NS-CUSTOMER-01. GROUPING ON IT IS LEGITIMATE AND HAS A MEASURED COST: the band alone singles out nobody, but added to ZipCode + Gender it takes the uniquely identifiable population from 35 894 to 74 617 of 104 990 (DQ-CUSTOMER-02, `coverage: gap`). | [Age Band](age_band.md) _(business)_ |

_Declared per column, over 13 columns: description 9 of 13 · type 13 of 13 · joins → 3 of 13. An em dash is a column for which nothing is declared._

## Relationships

*3 join(s) out · 1 in — click a concept to open it.*

**Joins to** — this concept references:

- [Age Band](age_band.md) — joined on `age_band_5y`
- [Country](country.md) — joined on `Country`
- [Region](geo_area.md) — joined on `GeoAreaKey`

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `CustomerKey`

## Source of record
- Full MAC concept: `customer.yaml` — open the **YAML** tab for the complete typed definition.

## Data
- Source table: [customer](../../data/sources/customer.md)
