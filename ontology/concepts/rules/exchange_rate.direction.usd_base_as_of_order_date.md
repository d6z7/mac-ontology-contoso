---
type: Rule
title: The direction is USD to the order's currency, on the order's day — measured, not inferred
description: resolution rule · binds FromCurrency, ToCurrency, Date, Exchange
tags:
- mac.rule_kind.resolution
- confidence:P
applies_to: ../exchange_rate.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — P (proposed)
- **Binds** — `FromCurrency`, `ToCurrency`, `Date`, `Exchange`
- **Rule id** — `exchange_rate.direction.usd_base_as_of_order_date`

### When

converting a line amount from `{v_contoso_order_line}` using `{v_contoso_fx_rate_day}`

### Then — do (then)

join on `{Date}` = the line's `{OrderDate}` AND `{FromCurrency}` = 'USD' AND `{ToCurrency}` = the line's `{CurrencyCode}`, and multiply the amount by `{Exchange}`

### Never — don't (never)

the reverse orientation (`{FromCurrency}` = the line's `{CurrencyCode}`, `{ToCurrency}` = 'USD'), which REPRODUCES 113 627 of 223 974 lines and therefore passes any USD-heavy sample while inverting every non-USD figure

Applies to [Exchange Rate](../exchange_rate.md).