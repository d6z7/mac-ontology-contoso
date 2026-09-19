---
type: Rule
title: A subcategory's parent is read from the row, never parsed out of its key
description: resolution rule · binds SubCategoryKey, CategoryKey
tags:
- mac.rule_kind.resolution
- confidence:P
applies_to: ../product_subcategory.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — P (proposed)
- **Binds** — `SubCategoryKey`, `CategoryKey`
- **Rule id** — `product_subcategory.parent.read_the_column_not_the_key`

### When

rolling a subcategory up to its category

### Then — do (then)

read `{CategoryKey}` from the same `{dim_contoso_product}` row, or `parent_category_key` from data/lookups/contoso_product_subcategory.lookup.csv

### Never — don't (never)

deriving the parent from the digits of `{SubCategoryKey}` — 101 and 104 do sit under category 1 in this delivery, but that is an observed encoding and not a declared rule, and a key like 1001 would break it silently

Applies to [Product Subcategory](../product_subcategory.md).