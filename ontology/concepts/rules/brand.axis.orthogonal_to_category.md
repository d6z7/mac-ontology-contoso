---
type: Rule
title: Brand and category are two axes — neither rolls up into the other
description: aggregation rule · binds Brand, CategoryName
tags:
- mac.rule_kind.aggregation
- confidence:P
applies_to: ../brand.md
---

## Rule

- **Kind** — `aggregation`
- **Confidence** — P (proposed)
- **Binds** — `Brand`, `CategoryName`
- **Rule id** — `brand.axis.orthogonal_to_category`

### When

a question combines brand with the category hierarchy

### Then — do (then)

group by both independently: `{Brand}` and `{CategoryName}` are separate axes of the same product row, so the cross-product is the answer

### Never — don't (never)

treating `{Brand}` as a level of the category hierarchy, or a category as a level of brand — a brand's products span categories and a category's products span brands

Applies to [Brand](../brand.md).