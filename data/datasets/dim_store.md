---
type: Dataset
title: 'Clean: dim_store'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_store
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `store_key` | integer | PK |
| `store_code` | integer | FK |
| `store_name` | string | value |
| `country_code` | string | FK |
| `state` | string | value |
| `open_date` | date | value |
| `close_date` | date | value |
| `status_annotation` | string | value |
| `square_metres` | integer | value |

## Foreign keys

- `store_code` → `dim_location.location_code` (many:one, mandatory:mandatory)
- `country_code` → `dim_country.country_code` (many:one, mandatory:mandatory)

## Referenced by

- `v_contoso5_sales_line.store_key` → `dim_store.store_key`

## What a question may do

### Details

- **Schema version** — 0.3.1-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

### Key

- One row is identified by `store_key`.

### Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `store_key` | **key** | — | — | finer_than `store_code` |
| `store_code` | — | — | `Location` | — |
| `store_name` | — | axis `categorical` | — | label_of `store_code` (common) |
| `country_code` | — | axis `categorical` | — | — |
| `state` | — | axis `categorical` | — | — |
| `open_date` | — | axis `time` · extremum `min`, `max` | — | — |
| `close_date` | — | axis `time` · extremum `min`, `max` | — | — |
| `status_annotation` | — | axis `categorical` | — | — |
| `square_metres` | — | aggregate stock / m2 · extremum `min`, `max` | — | — |

_Declared per column, over 9 columns: offers 7 of 9 · references 1 of 9 · rulings 2 of 9. An em dash is a column for which nothing is declared._

### Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Store](../concepts/store.md) — serves `store_key`, `store_code`, `store_name`, `country_code`, `state`, `open_date`, `close_date`, `status_annotation`, `square_metres`
