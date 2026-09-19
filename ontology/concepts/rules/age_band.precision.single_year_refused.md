---
type: Rule
title: Single-year age is not served — the answer is a refusal naming the ruling
description: exclusion rule · binds age_band_5y
tags:
- mac.rule_kind.exclusion
- confidence:P
applies_to: ../age_band.md
---

## Rule

- **Kind** — `exclusion`
- **Confidence** — P (proposed)
- **Binds** — `age_band_5y`
- **Rule id** — `age_band.precision.single_year_refused`

### When

a question needs age to the year — average age, everyone aged 42, a birth date, age today

### Then — do (then)

REFUSE and say which precision IS available: `{age_band_5y}` in 5-year bands as of 2025-12-31, naming DQ-CUSTOMER-01 as the ruling that set it

### Never — don't (never)

treating the band code as a single-year age — averaging `{age_band_5y}` to report a mean age, or reading 40 as a 40-year-old — and never reaching for the delivery's `Age` column, which is stale on 104 990 of 104 990 rows and is not served

Applies to [Age Band](../age_band.md).