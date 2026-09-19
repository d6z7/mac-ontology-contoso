---
type: Rule
title: A weight unit does not imply a weight, and neither absence is a zero
description: guarantee rule · binds Weight, WeightUnit
tags:
- mac.rule_kind.guarantee
- confidence:P
applies_to: ../product.md
---

## Rule

- **Kind** — `guarantee`
- **Confidence** — P (proposed)
- **Binds** — `Weight`, `WeightUnit`
- **Rule id** — `product.weight.unit_and_weight_are_independent`

### When

reading, filtering or aggregating `{Weight}` or `{WeightUnit}`

### Then — do (then)

treat each absence as UNKNOWN and report the denominator — `{Weight}` is null on 284 of 2 517 rows, `{WeightUnit}` on 222 — and never compare weights across units without converting

### Never — don't (never)

reading a null `{Weight}` as 0, or inferring a weight exists because `{WeightUnit}` is present: 62 rows name a unit for a weight that is not there

Applies to [Product](../product.md).