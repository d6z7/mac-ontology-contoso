---
type: Rule
title: A quote is keyed by an ordered pair and a day — all three, or none
description: resolution rule · binds Date, FromCurrency, ToCurrency
tags:
- mac.rule_kind.resolution
- confidence:P
applies_to: ../exchange_rate.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — P (proposed)
- **Binds** — `Date`, `FromCurrency`, `ToCurrency`
- **Rule id** — `exchange_rate.pair.never_half_a_pair`

### When

filtering or joining `{v_contoso_fx_rate_day}`

### Then — do (then)

constrain all three key columns — `{Date}`, `{FromCurrency}` and `{ToCurrency}` — together

### Never — don't (never)

constraining `{FromCurrency}` or `{Date}` alone and aggregating what comes back: the grid is complete, so a half-specified filter returns 5 rows per day per currency and silently averages five different pairs

Applies to [Exchange Rate](../exchange_rate.md).