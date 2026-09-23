---
type: Rule
title: Amounts are store-local — a multi-currency sum needs a stated conversion
description: aggregation rule · binds CurrencyCode, UnitPrice, NetPrice, UnitCost
tags:
- mac.rule_kind.aggregation
- confidence:P
applies_to: ../order_line.md
---

## Rule

- **Kind** — `aggregation`
- **Confidence** — P (proposed)
- **Binds** — `CurrencyCode`, `UnitPrice`, `NetPrice`, `UnitCost`
- **Rule id** — `order_line.currency.no_bare_cross_currency_sum`

### When

summing `{UnitPrice}`, `{NetPrice}` or `{UnitCost}` across rows whose `{CurrencyCode}` differs

### Then — do (then)

either restrict to one `{CurrencyCode}` and say which, or convert through `{v_contoso_fx_rate_day}` in the direction the ExchangeRate concept declares, and disclose the choice with the figure

### Never — don't (never)

adding amounts denominated in different currencies as if they shared a unit — measured 5 currencies on the fact (USD 113 614, EUR 49 203, CAD 24 250, GBP 22 829, AUD 14 078), so a bare global SUM is a number with no unit

Applies to [Order Line](../order_line.md).