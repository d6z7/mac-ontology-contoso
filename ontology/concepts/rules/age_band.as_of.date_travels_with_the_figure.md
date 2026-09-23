---
type: Rule
title: The band is as-of 2025-12-31 and says so in the answer
description: default rule · binds age_band_5y
tags:
- mac.rule_kind.default
- confidence:P
applies_to: ../age_band.md
---

## Rule

- **Kind** — `default`
- **Confidence** — P (proposed)
- **Binds** — `age_band_5y`
- **Rule id** — `age_band.as_of.date_travels_with_the_figure`

### When

reporting or grouping by `{age_band_5y}`

### Then — do (then)

state the as-of date 2025-12-31 with the figure, and read the band as the customer's age ON THAT DATE rather than now

### Never — don't (never)

presenting the band as a current age, or comparing bands across two loads without checking that both were derived as of the same date

Applies to [Age Band](../age_band.md).