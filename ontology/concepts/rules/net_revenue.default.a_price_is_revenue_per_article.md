---
type: Rule
title: net_revenue.default.a_price_is_revenue_per_article
description: default rule · binds net_amount
tags:
- CONTOSO5
- mac.concept.rule.default
- confidence:C
applies_to: ../order.md
---

## Rule

- **Kind** — `default`
- **Confidence** — C (confirmed)
- **Scope** — CONTOSO5
- **Binds** — `net_amount`
- **Rule id** — `net_revenue.default.a_price_is_revenue_per_article`

> The clauses below are PROJECTED from `mac.canon.ratio_select` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a rate, share or percentage over this measure is asked for

### Then — do (then)

1 named ratio(s): `price_per_article` (also called price; average price; price per unit; per unit; price per article; per article). `price_per_article` divides by quantity. a question naming none of them takes `price_per_article`, and the answer DISCLOSES that it did

### Never — don't (never)

dividing by a figure this bundle has not declared

Applies to [Order](../order.md).