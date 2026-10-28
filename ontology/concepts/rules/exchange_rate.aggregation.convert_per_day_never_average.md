---
type: Rule
title: exchange_rate.aggregation.convert_per_day_never_average
description: aggregation rule · binds rate
tags:
- CONTOSO5
- mac.concept.rule.aggregation
- confidence:P
applies_to: ../exchange_rate.md
---

## Rule

- **Kind** — `aggregation`
- **Confidence** — P (proposed)
- **Scope** — CONTOSO5
- **Binds** — `rate`
- **Rule id** — `exchange_rate.aggregation.convert_per_day_never_average`

> The clauses below are PROJECTED from `mac.canon.additivity_guard` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

`rate` is aggregated across an axis

### Then — do (then)

across a categorical axis it is none; across a time axis it is average. It may not be summed across ANY declared axis. Apply the declared effect and say which was applied

### Never — don't (never)

summing `rate` across a categorical or time axis; weighting every member of an axis equally when the declaration says otherwise

Applies to [Exchange Rate](../exchange_rate.md).