---
type: Metric
title: Exchange Rate
description: 'What one currency was worth in another on one day: 100,450 quoted rates
  over a date and an ordered pair of currencies.'
tags:
- CONTOSO5
- measure
- confidence:I
timestamp: '2026-09-29'
---

# Exchange Rate

What one currency was worth in another on one day: 100,450 quoted rates over a date and an ordered pair of currencies. The account is knowledge/exchange_rate.md.

## Relationships

- inverse of **order__converts_at__exchange_rate** ← [Order](/Order.md) (grounded join `v_contoso5_sales_line.order_date = v_contoso5_fx_rate.date_day AND v_contoso5_sales_line.currency_code = v_contoso5_fx_rate.to_currency AND v_contoso5_fx_rate.from_currency = 'USD'`)
- **exchange_rate__quotes_from__currency** → [Currency](/Currency.md) (cardinality 1; grounded join `v_contoso5_fx_rate.from_currency = dim_currency.currency_code`)
- **exchange_rate__quotes_to__currency** → [Currency](/Currency.md) (cardinality 1; grounded join `v_contoso5_fx_rate.to_currency = dim_currency.currency_code`)

# Citations

1. MAC concept source of record: `concepts/exchange_rate.yaml` (schema_version 0.3.0-develop, confidence I).
