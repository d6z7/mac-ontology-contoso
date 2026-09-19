---
type: Rule
title: Two levels are both called "category" — resolve to the one asked for and say which
description: ambiguity rule · binds CategoryKey, SubCategoryKey
tags:
- mac.rule_kind.ambiguity
- confidence:P
applies_to: ../product_category.md
---

## Rule

- **Kind** — `ambiguity`
- **Confidence** — P (proposed)
- **Binds** — `CategoryKey`, `SubCategoryKey`
- **Rule id** — `product_category.level.category_is_not_subcategory`

### When

a question says category, product group, or product type without naming a level

### Then — do (then)

resolve to THIS level (`{CategoryKey}`, 8 members) and say so; offer the `{SubCategoryKey}` level (32 members) when the question names a value that only exists there

### Never — don't (never)

answering a category question at subcategory grain or the reverse — 8 rows against 32 is a different answer to the same words, with no symptom in the result

Applies to [Product Category](../product_category.md).