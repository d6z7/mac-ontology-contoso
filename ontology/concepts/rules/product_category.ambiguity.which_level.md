---
type: Rule
title: product_category.ambiguity.which_level
description: ambiguity rule · binds category_name, sub_category_name
tags:
- CONTOSO5
- mac.concept.rule.ambiguity
- confidence:P
applies_to: ../product_category.md
---

## Rule

- **Kind** — `ambiguity`
- **Confidence** — P (proposed)
- **Scope** — CONTOSO5
- **Binds** — `category_name`, `sub_category_name`
- **Rule id** — `product_category.ambiguity.which_level`

> The clauses below are PROJECTED from `mac.canon.column_select` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a question names this concept and does not say which reading it means

### Then — do (then)

2 named reading(s): `category` (also called category; categories; product category; product categories); `sub_category` (also called sub category; sub-category; subcategories; sub-categories). `category` is `category_name`; `sub_category` is `sub_category_name`. a question naming none of them takes `category`, and the answer DISCLOSES that it did

### Never — don't (never)

answering on one column while reporting the other's name

Applies to [Product Category](../product_category.md).