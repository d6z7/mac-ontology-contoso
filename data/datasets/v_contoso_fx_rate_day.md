---
type: Dataset
title: 'Clean: v_contoso_fx_rate_day'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.v_contoso_fx_rate_day
tags:
- CONTOSO
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `Date` | date | composite_key_part |
| `FromCurrency` | varchar | composite_key_part |
| `ToCurrency` | varchar | composite_key_part |
| `Exchange` | decimal(20,5) | value |

## Foreign keys
- `Date` → `dim_contoso_calendar_day.Date`