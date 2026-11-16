---
type: Enum
title: Product Category
description: 'How Contoso groups what it sells: categories, each over several sub-categories, both carried as names on the product row (rule ProductCategory.level).'
tags:
- CONTOSO5
- enumeration
- confidence:I
resource: table://dim_product
---

How Contoso groups what it sells: categories, each over several sub-categories, both carried as names on the product row (rule ProductCategory.level). The account is knowledge/product_category.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.4.0-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-29

## How to answer

_No content available — the bundle declares nothing for this section._

## Grounded in

- `dim_product` — key `product_key` — semantics: [`data/datasets/dim_product.yaml`](../../data/datasets/dim_product.md)

## Grain

- One row is one Product Category, identified by `product_key`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `category_name` | string | dimension | — | — | — | — | the product's top-level category. | — |
| `sub_category_name` | string | dimension | — | — | finer_than `category_name` | — | the product's sub-category, one level below `category_name`. Which of the two a question means is a declared ambiguity (product_category.ambiguity.which_level). | — |
| `product_key` | integer | key | -> Product | — | — | — | the row key: one row per product. | — |

_Declared per column, over 3 columns: type 3 of 3 · role 3 of 3 · identity 1 of 3 · measure 0 of 3 · rulings 1 of 3 · register 0 of 3 · description 3 of 3 · joins → 0 of 3. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind | fold |
|---|---|---|
| `category_name` | categorical | — |
| `sub_category_name` | categorical | — |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Product](product.md) — on `?`

## Source of record

- Full MAC concept: `product_category.yaml` — open the **YAML** tab for the complete typed definition.
