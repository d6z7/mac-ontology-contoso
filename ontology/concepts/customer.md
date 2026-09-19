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

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `CustomerKey` | key | `dim_contoso_customer` (key) |  |  |
| `GeoAreaKey` | key | `dim_contoso_customer` |  |  |
| `StartDT` | attribute | `dim_contoso_customer` |  |  |
| `EndDT` | attribute | `dim_contoso_customer` |  |  |
| `Continent` | dimension | `dim_contoso_customer` |  |  |
| `CountryFull` | attribute | `dim_contoso_customer` |  |  |
| `Country` | dimension | `dim_contoso_customer` |  |  |
| `StateFull` | attribute | `dim_contoso_customer` |  |  |
| `State` | dimension | `dim_contoso_customer` |  |  |
| `City` | attribute | `dim_contoso_customer` |  |  |
| `ZipCode` | attribute | `dim_contoso_customer` |  |  |
| `Gender` | dimension | `dim_contoso_customer` |  |  |
| `age_band_5y` | dimension | `dim_contoso_customer` |  |  |

## Relationships

*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `CustomerKey`

## Source of record
- Full MAC concept: `customer.yaml` — open the **YAML** tab for the complete typed definition.

## Data
- Source table: [customer](../../data/sources/customer.md)
