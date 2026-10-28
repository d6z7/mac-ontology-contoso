---
type: Rule
title: margin.aggregation.two_named_ratios
description: aggregation rule · binds margin_amount
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
- **Binds** — `margin_amount`
- **Rule id** — `margin.aggregation.two_named_ratios`

> The clauses below are PROJECTED from `mac.canon.ratio_select` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a rate, share or percentage over this measure is asked for

### Then — do (then)

2 named ratio(s): `margin_percent` (also called margin %; margin percentage; margin rate; net margin; margin on net); `markup_percent` (also called markup; markup %; markup percentage; margin on cost). `margin_percent` divides by net_amount; `markup_percent` divides by cost_amount. a question naming none of them is ASKED BACK, with every reading offered

### Never — don't (never)

choosing between denominators the question did not name; dividing by a figure this bundle has not declared

Applies to [Order](../order.md).