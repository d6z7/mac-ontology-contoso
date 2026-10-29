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

| column | type | role | reference |
|---|---|---|---|
| `currency_code` | string | PK · FK | → `contoso5_currency.code` |

## Foreign keys

- `currency_code` → `contoso5_currency.code`

## Referenced by

- `v_contoso5_fx_rate.from_currency` → `dim_currency.currency_code`
- `v_contoso5_fx_rate.to_currency` → `dim_currency.currency_code`
- `v_contoso5_sales_line.currency_code` → `dim_currency.currency_code`