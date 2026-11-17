---
type: Concept
title: Product
description: 'A thing Contoso sells, at the level the shelf knows it: a SKU.'
tags:
- Contoso 5
- concept
resource: table://dim_product
rule_pages:
- ../rules/Brand.not_manufacturer.md
- ../rules/Product.price_is_dated.md
---

A thing Contoso sells, at the level the shelf knows it: a SKU. The account is pages/knowledge/product.md.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`dim_product`](../../data/datasets/dim_product.md)
- **Counts** — `product_key` (no `counts`: the dataset key)
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*2 rule(s) are about this concept, 2 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Brand.not_manufacturer](../rules/Brand.not_manufacturer.md) — **proposed** · names it · prose — not enforced (owner operator) — A brand is the name a customer buys a product under; a manufacturer is who made it. The two sets overlap in names but are two notions, and a question asking who is behind a product says which it means rather than treating them as interchangeable.
- [Product.price_is_dated](../rules/Product.price_is_dated.md) — **proposed** · parent · prose — not enforced (owner operator) — A product carries no standing price and no standing cost. A price changes over time, so every price and cost is the one on the sale, dated by the sale, and a product's price is reached through its sales. A product's current price is the regular unit price on its latest sale, stated with that sale's date where it matters. A question qualifying products by price — high-value products — selects products by that price and then counts all their sales, never qualifies individual sale lines.

**Words**

*18 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| label | `dataset:dim_product.brand` | binds | — | — | — |
| marque | `dataset:dim_product.brand` | binds | — | — | — |
| top category | `dataset:dim_product.category_name` | binds | — | — | — |
| colour | `dataset:dim_product.color` | binds | — | — | — |
| made by | `dataset:dim_product.manufacturer` | binds | — | — | — |
| maker | `dataset:dim_product.manufacturer` | binds | — | — | — |
| article number | `dataset:dim_product.product_code` | binds | — | — | — |
| sku | `dataset:dim_product.product_code` | binds | — | — | — |
| product id | `dataset:dim_product.product_key` | binds | — | — | — |
| name of the product | `dataset:dim_product.product_name` | binds | — | — | — |
| what it is called | `dataset:dim_product.product_name` | binds | — | — | — |
| lower category | `dataset:dim_product.sub_category_name` | binds | — | — | — |
| catalogue price | `rule:Product.price_is_dated` | finds | — | — | — |
| cost | `rule:Product.price_is_dated` | finds | — | — | — |
| current price | `rule:Product.price_is_dated` | finds | — | — | — |
| high-value products | `rule:Product.price_is_dated` | finds | — | — | — |
| list price | `rule:Product.price_is_dated` | finds | — | — | — |
| product price | `rule:Product.price_is_dated` | finds | — | — | — |

## Grounded in

- [`dim_product`](../../data/datasets/dim_product.md) — served as `"contoso_served"."dim_product"`

## Grain

- One row of `dim_product` is identified by `product_key` (the dataset key).
- One Product is one row — no `counts`, so the instance is the dataset key.

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `product_key` | identifier | — | — | — | — | the row key: one row per product. | ← [Order](Order.md) via `order__of__product` |
| `product_code` | name | — | — | names `product_key` (code) | — | the product's code in the source system, unique across all rows. | — |
| `product_name` | name | — | — | names `product_key` (common) | — | the product's name as a reader would see it. | — |
| `manufacturer` | name | — | — | names `brand` (legal) | — | who made the product. | — |
| `brand` | dimension | — | — | — | — | the brand the product is sold under. Far fewer brands than products, so a question about brands wants the brands and not the products. | — |
| `color` | dimension | — | — | — | — | the product's colour. | — |
| `category_name` | dimension | — | — | — | — | the product's top-level category. | — |
| `sub_category_name` | dimension | — | — | — | — | the product's sub-category, one level below `category_name`. Which of the two a question means is a declared ambiguity (ProductCategory.level). | — |

_Declared per column, over 8 served columns: is 8 of 8 · label 0 of 8 · measure 0 of 8 · names 3 of 8 · value set 0 of 8 · means 8 of 8 · joins → 1 of 8. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind |
|---|---|
| `brand` | dimension |
| `color` | dimension |
| `category_name` | dimension |
| `sub_category_name` | dimension |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

*0 edge(s) out · 1 in — the only joins (L7), walked in both directions.*

**Joined from** — edges into this concept:

- [Order](Order.md) — `order__of__product` on `product_key` = `product_key`

## Source of record

- Declaration: `ontology/concepts/Product.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/Product.md`](../../../ontology/concepts/Product.md) — the authored account (X-3); this page cites it and never writes it.
