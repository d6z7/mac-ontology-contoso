---
type: Rule
title: discount.aggregation.percent_is_over_gross
description: aggregation rule · binds discount_amount
tags:
- CONTOSO5
- mac.concept.rule.aggregation
- confidence:C
applies_to: ../order.md
---

## Rule

- **Kind** — `aggregation`
- **Confidence** — C (confirmed)
- **Scope** — CONTOSO5
- **Binds** — `discount_amount`
- **Rule id** — `discount.aggregation.percent_is_over_gross`

> The clauses below are PROJECTED from `mac.canon.ratio_select` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a rate, share or percentage over this measure is asked for

### Then — do (then)

1 named ratio(s): `percent` (also called discount percentage; discount rate; discount %; discount as a percentage). `percent` divides by gross_amount. a question naming none of them takes `percent`, and the answer DISCLOSES that it did

### Never — don't (never)

dividing by a figure this bundle has not declared

Applies to [Order](../order.md).