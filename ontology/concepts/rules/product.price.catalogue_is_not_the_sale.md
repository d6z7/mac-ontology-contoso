---
type: Rule
title: The catalogue price is not the sold price — sales figures come from the line
description: exclusion rule · binds Price, Cost
tags:
- mac.rule_kind.exclusion
- confidence:P
applies_to: ../product.md
---

## Rule

- **Kind** — `exclusion`
- **Confidence** — P (proposed)
- **Binds** — `Price`, `Cost`
- **Rule id** — `product.price.catalogue_is_not_the_sale`

### When

computing any sales, revenue or discount figure

### Then — do (then)

read `{UnitPrice}` and `{NetPrice}` from `{v_contoso_order_line}`, which are the prices the line actually carried

### Never — don't (never)

multiplying `{Price}` or `{Cost}` from `{dim_contoso_product}` by a quantity: these are current catalogue values on an unversioned dimension, so using them re-prices ten years of history at today's list

Applies to [Product](../product.md).