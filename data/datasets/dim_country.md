---
type: Dataset
title: 'Clean: dim_country'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_country
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `country_code` | string | PK · FK |
| `country_name` | string | value |
| `is_placeholder` | boolean | value |

## Foreign keys

- `country_code` → `contoso5_country_code.code`

## Referenced by

- `dim_customer.country_code` → `dim_country.country_code`
- `dim_location.country_code` → `dim_country.country_code`
- `dim_store.country_code` → `dim_country.country_code`
- `v_contoso5_sales_line.sale_country_code` → `dim_country.country_code`

## What a question may do

### Details

- **Schema version** — 0.4.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

### Key

- One row is identified by `country_code`.

### Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `country_code` | **key** | — | — | — |
| `country_name` | — | axis `categorical` | — | label_of `country_code` (long) |
| `is_placeholder` | — | — | — | — |

_Declared per column, over 3 columns: offers 1 of 3 · references 0 of 3 · rulings 1 of 3. An em dash is a column for which nothing is declared._

### Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Country](../concepts/country.md) — serves `country_code`, `country_name`, `is_placeholder`
