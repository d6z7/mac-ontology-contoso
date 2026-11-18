---
type: Concept
title: Colour
description: 'The colour a product comes in — the one attribute that on its own makes a new SKU: "E400 Green" and "E400 Orange" are different products.'
tags:
- Contoso 5
- concept
resource: table://dim_product
rule_pages:
- ../rules/Color.one_spelling.md
---

The colour a product comes in — the one attribute that on its own makes a new SKU: "E400 Green" and "E400 Orange" are different products. The account is ontology/concepts/Color.md.

## Details

- **Label** — Colour
- **Table** — [`dim_product`](../../data/datasets/dim_product.md)
- **Counts** — `color`
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*1 rule(s) are about this concept, 1 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Color.one_spelling](../rules/Color.one_spelling.md) — **proposed** · parent · prose — not enforced (owner operator) — A colour is one member however the source spells its case: colour names are capitalised, so Blue and blue are one colour. A breakdown or count by colour never lists two spellings of one colour.

**Words**

*9 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| Colour | `concept:Color` | binds | — | — | — |
| colour | `dataset:dim_product.color` | binds | — | — | — |
| product id | `dataset:dim_product.product_key` | binds | — | — | — |
| blue | `rule:Color.one_spelling` | finds | — | — | — |
| case | `rule:Color.one_spelling` | finds | — | — | — |
| color | `rule:Color.one_spelling` | finds | — | — | — |
| colour | `rule:Color.one_spelling` | finds | — | — | — |
| fold | `rule:Color.one_spelling` | finds | — | — | — |
| spelling | `rule:Color.one_spelling` | finds | — | — | — |

## Grounded in

- [`dim_product`](../../data/datasets/dim_product.md) — served as `"contoso_served"."dim_product"`

## Grain

- One row of `dim_product` is identified by `product_key` (the dataset key).
- One Colour is one distinct `color` (`counts`, the instance).

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `color` | dimension | — | — | — | — | the product's colour. | — |
| `product_key` | identifier | — | — | — | — | the row key: one row per product. | — |

_Declared per column, over 2 served columns: is 2 of 2 · label 0 of 2 · measure 0 of 2 · names 0 of 2 · value set 0 of 2 · means 2 of 2 · joins → 0 of 2. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind |
|---|---|
| `color` | dimension |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

_No content available — the bundle declares nothing for this section._

## Source of record

- Declaration: `ontology/concepts/Color.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/Color.md`](../../../ontology/concepts/Color.md) — the authored account (X-3); this page cites it and never writes it.
