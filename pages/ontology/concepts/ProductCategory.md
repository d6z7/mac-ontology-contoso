---
type: Concept
title: ProductCategory
description: 'How Contoso groups what it sells: categories, each over several sub-categories, both carried as names on the product row (rule ProductCategory.level).'
tags:
- Contoso 5
- concept
resource: table://dim_product
rule_pages:
- ../rules/ProductCategory.level.md
---

How Contoso groups what it sells: categories, each over several sub-categories, both carried as names on the product row (rule ProductCategory.level). The account is ontology/concepts/ProductCategory.md.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`dim_product`](../../data/datasets/dim_product.md)
- **Counts** — `category_name`
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*1 rule(s) are about this concept, 1 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [ProductCategory.level](../rules/ProductCategory.level.md) — **proposed** · parent · choice over `category`, `sub_category` — default `category` — A product category is the top level of the product hierarchy. A question saying category is answered on the category; one saying sub-category is answered on the sub-category.

**Words**

*17 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| Product Category | `concept:ProductCategory` | binds | — | — | — |
| top category | `dataset:dim_product.category_name` | binds | — | — | — |
| product id | `dataset:dim_product.product_key` | binds | — | — | — |
| lower category | `dataset:dim_product.sub_category_name` | binds | — | — | — |
| category | `rule:ProductCategory.level` | finds | — | — | — |
| hierarchy | `rule:ProductCategory.level` | finds | — | — | — |
| level | `rule:ProductCategory.level` | finds | — | — | — |
| product category | `rule:ProductCategory.level` | finds | — | — | — |
| sub-category | `rule:ProductCategory.level` | finds | — | — | — |
| categories | `rule:ProductCategory.level.category` | binds | — | — | — |
| category | `rule:ProductCategory.level.category` | binds | — | — | — |
| product categories | `rule:ProductCategory.level.category` | binds | — | — | — |
| product category | `rule:ProductCategory.level.category` | binds | — | — | — |
| sub category | `rule:ProductCategory.level.sub_category` | binds | — | — | — |
| sub-categories | `rule:ProductCategory.level.sub_category` | binds | — | — | — |
| sub-category | `rule:ProductCategory.level.sub_category` | binds | — | — | — |
| subcategories | `rule:ProductCategory.level.sub_category` | binds | — | — | — |

## Grounded in

- [`dim_product`](../../data/datasets/dim_product.md) — served as `"contoso_served"."dim_product"`

## Grain

- One row of `dim_product` is identified by `product_key` (the dataset key).
- One ProductCategory is one distinct `category_name` (`counts`, the instance).

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `category_name` | dimension | — | — | — | — | the product's top-level category. | — |
| `sub_category_name` | dimension | — | — | — | — | the product's sub-category, one level below `category_name`. Which of the two a question means is a declared ambiguity (ProductCategory.level). | — |
| `product_key` | identifier | — | — | — | — | the row key: one row per product. | — |

_Declared per column, over 3 served columns: is 3 of 3 · label 0 of 3 · measure 0 of 3 · names 0 of 3 · value set 0 of 3 · means 3 of 3 · joins → 0 of 3. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind |
|---|---|
| `category_name` | dimension |
| `sub_category_name` | dimension |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

_No content available — the bundle declares nothing for this section._

## Source of record

- Declaration: `ontology/concepts/ProductCategory.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/ProductCategory.md`](../../../ontology/concepts/ProductCategory.md) — the authored account (X-3); this page cites it and never writes it.
