---
type: Enumeration
title: Currency
description: 'The money a sale is denominated in: five ISO codes, pointed at by every
  sale and by both ends of every exchange rate.'
tags:
- CONTOSO5
- enumeration
- confidence:I
timestamp: '2026-09-29'
---

# Currency

The money a sale is denominated in: five ISO codes, pointed at by every sale and by both ends of every exchange rate. The account is knowledge/currency.md.

## Relationships

- inverse of **exchange_rate__quotes_from__currency** ← [ExchangeRate](/ExchangeRate.md) (grounded join `v_contoso5_fx_rate.from_currency = dim_currency.currency_code`)
- inverse of **exchange_rate__quotes_to__currency** ← [ExchangeRate](/ExchangeRate.md) (grounded join `v_contoso5_fx_rate.to_currency = dim_currency.currency_code`)
- inverse of **order__paid_in__currency** ← [Order](/Order.md) (grounded join `v_contoso5_sales_line.currency_code = dim_currency.currency_code`)

# Citations

1. MAC concept source of record: `concepts/currency.yaml` (schema_version 0.3.0-develop, confidence I).
