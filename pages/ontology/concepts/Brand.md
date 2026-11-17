---
type: Concept
title: Brand
description: 'Whose name a product is sold under: eleven names, carried as a column on the product row with no table and no key of their own.'
tags:
- Contoso 5
- concept
resource: table://dim_product
rule_pages:
- ../rules/Brand.not_manufacturer.md
---

Whose name a product is sold under: eleven names, carried as a column on the product row with no table and no key of their own. The account is pages/knowledge/brand.md.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`dim_product`](../../data/datasets/dim_product.md)
- **Counts** — `brand`
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*1 rule(s) are about this concept, 1 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Brand.not_manufacturer](../rules/Brand.not_manufacturer.md) — **proposed** · parent · prose — not enforced (owner operator) — A brand is the name a customer buys a product under; a manufacturer is who made it. The two sets overlap in names but are two notions, and a question asking who is behind a product says which it means rather than treating them as interchangeable.

**Words**

*9 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| label | `dataset:dim_product.brand` | binds | — | — | — |
| marque | `dataset:dim_product.brand` | binds | — | — | — |
| product id | `dataset:dim_product.product_key` | binds | — | — | — |
| brand | `rule:Brand.not_manufacturer` | finds | — | — | — |
| label | `rule:Brand.not_manufacturer` | finds | — | — | — |
| made by | `rule:Brand.not_manufacturer` | finds | — | — | — |
| maker | `rule:Brand.not_manufacturer` | finds | — | — | — |
| manufacturer | `rule:Brand.not_manufacturer` | finds | — | — | — |
| who makes | `rule:Brand.not_manufacturer` | finds | — | — | — |

## Grounded in

- [`dim_product`](../../data/datasets/dim_product.md) — served as `"contoso_served"."dim_product"`

## Grain

- One row of `dim_product` is identified by `product_key` (the dataset key).
- One Brand is one distinct `brand` (`counts`, the instance).

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `brand` | dimension | — | — | — | — | the brand the product is sold under. Far fewer brands than products, so a question about brands wants the brands and not the products. | — |
| `product_key` | identifier | — | — | — | — | the row key: one row per product. | — |

_Declared per column, over 2 served columns: is 2 of 2 · label 0 of 2 · measure 0 of 2 · names 0 of 2 · value set 0 of 2 · means 2 of 2 · joins → 0 of 2. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind |
|---|---|
| `brand` | dimension |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

_No content available — the bundle declares nothing for this section._

## Source of record

- Declaration: `ontology/concepts/Brand.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/Brand.md`](../../../ontology/concepts/Brand.md) — the authored account (X-3); this page cites it and never writes it.
