---
type: Dataset
title: 'Clean: dim_currency'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_currency
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `currency_code` | string | PK · FK |

## Foreign keys

- `currency_code` → `contoso5_currency.code`

## Referenced by

- `v_contoso5_fx_rate.from_currency` → `dim_currency.currency_code`
- `v_contoso5_fx_rate.to_currency` → `dim_currency.currency_code`
- `v_contoso5_sales_line.currency_code` → `dim_currency.currency_code`

## What a question may do

### Details

- **Schema version** — 0.4.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

### Key

- One row is identified by `currency_code`.

### Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `currency_code` | **key** | — | — | — |

_Declared per column, over 1 column: offers 0 of 1 · references 0 of 1 · rulings 0 of 1. An em dash is a column for which nothing is declared._

### Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Currency](../concepts/currency.md) — serves `currency_code`
