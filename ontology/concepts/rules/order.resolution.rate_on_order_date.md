---
type: Rule
title: order.resolution.rate_on_order_date
description: resolution rule · binds order_date, currency_code
tags:
- CONTOSO5
- mac.concept.rule.resolution
- confidence:P
applies_to: ../order.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — P (proposed)
- **Scope** — CONTOSO5
- **Binds** — `order_date`, `currency_code`
- **Rule id** — `order.resolution.rate_on_order_date`

> The clauses below are PROJECTED from `mac.canon.composite_key_guard` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

`to_currency` is constrained, grouped on, or joined

### Then — do (then)

carry `date_day`; `from_currency` with it — the identity is (to_currency, date_day, from_currency), and a value of `to_currency` means different things under different date_day; from_currency

### Never — don't (never)

constraining or grouping on `to_currency` without `date_day`; `from_currency`; treating two rows with the same code and different scope as one thing

Applies to [Order](../order.md).