---
type: Rule
title: order.default.period_is_order_date
description: default rule · binds order_date, delivery_date
tags:
- CONTOSO5
- mac.concept.rule.default
- confidence:P
applies_to: ../order.md
---

## Rule

- **Kind** — `default`
- **Confidence** — P (proposed)
- **Scope** — CONTOSO5
- **Binds** — `order_date`, `delivery_date`
- **Rule id** — `order.default.period_is_order_date`

> The clauses below are PROJECTED from `mac.canon.column_select` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a question names this concept and does not say which reading it means

### Then — do (then)

2 named reading(s): `delivered` (also called delivered; delivery date; shipped; when it arrived); `ordered` (also called ordered; order date; placed; when it was ordered). `delivered` is `delivery_date`; `ordered` is `order_date`. a question naming none of them takes `ordered`, and the answer DISCLOSES that it did

### Never — don't (never)

answering on one column while reporting the other's name

Applies to [Order](../order.md).