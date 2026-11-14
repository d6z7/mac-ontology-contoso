---
type: Dataset
title: 'Clean: dim_customer'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_customer
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `customer_key` | integer | PK |
| `customer_name` | string | value |
| `continent` | string | value |
| `country_code` | string | FK |
| `state` | string | value |
| `city` | string | value |
| `gender` | string | value |
| `birth_date` | date | value |
| `valid_from` | date | value |
| `valid_to` | date | value |

## Foreign keys

- `country_code` → `dim_country.country_code` (many:one, mandatory:optional)

## Referenced by

- `v_contoso5_sales_line.customer_key` → `dim_customer.customer_key`

## What a question may do

### Details

- **Schema version** — 0.4.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

### Key

- One row is identified by `customer_key`.

### Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `customer_key` | **key** | — | — | — |
| `customer_name` | — | axis `categorical` · suppressed `DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME` | — | label_of `customer_key` (common) |
| `continent` | — | axis `categorical` | — | — |
| `country_code` | — | axis `categorical` | — | finer_than `continent` |
| `state` | — | axis `categorical` | — | scoped_by `country_code` |
| `city` | — | axis `categorical` · suppressed `DQ-IDENTIFYING-DIM_CUSTOMER-CITY` | — | — |
| `gender` | — | axis `categorical` | — | — |
| `birth_date` | — | axis `time` · extremum `min`, `max` | — | — |
| `valid_from` | — | — | — | — |
| `valid_to` | — | — | — | — |

_Declared per column, over 10 columns: offers 7 of 10 · references 0 of 10 · rulings 3 of 10. An em dash is a column for which nothing is declared._

### Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Customer](../concepts/customer.md) — serves `customer_key`, `customer_name`, `continent`, `country_code`, `state`, `city`, `gender`, `birth_date`, `valid_from`, `valid_to`
