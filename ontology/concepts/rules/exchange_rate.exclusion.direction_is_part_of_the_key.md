---
type: Rule
title: exchange_rate.exclusion.direction_is_part_of_the_key
description: exclusion rule · binds from_currency, to_currency
tags:
- CONTOSO5
- mac.concept.rule.exclusion
- confidence:P
applies_to: ../exchange_rate.md
---

## Rule

- **Kind** — `exclusion`
- **Confidence** — P (proposed)
- **Scope** — CONTOSO5
- **Binds** — `from_currency`, `to_currency`
- **Rule id** — `exchange_rate.exclusion.direction_is_part_of_the_key`

> The clauses below are PROJECTED from `mac.canon.composite_key_guard` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

`to_currency` is constrained, grouped on, or joined

### Then — do (then)

carry `from_currency` with it — the identity is (to_currency, from_currency), and a value of `to_currency` means different things under different from_currency

### Never — don't (never)

constraining or grouping on `to_currency` without `from_currency`; treating two rows with the same code and different scope as one thing

Applies to [Exchange Rate](../exchange_rate.md).