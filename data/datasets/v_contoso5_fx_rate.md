---
type: Dataset
title: 'Clean: v_contoso5_fx_rate'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.v_contoso5_fx_rate
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `date_day` | date | PK1 |  |
| `from_currency` | string | PK2 · FK | → `dim_currency.currency_code` |
| `to_currency` | string | PK3 · FK | → `dim_currency.currency_code` |
| `rate` | decimal | value |  |

## Foreign keys

- `from_currency` → `dim_currency.currency_code` (many:one, mandatory:mandatory)
- `to_currency` → `dim_currency.currency_code` (many:one, mandatory:mandatory)