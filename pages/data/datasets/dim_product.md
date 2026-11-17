---
type: Dataset
title: dim_product
description: dataset dim_product
relation: dim_product
tags:
- Contoso 5
- dataset
---

- **Served as** — `"contoso_served"."dim_product"`
- **Key** — `product_key`
- **Made by** — [dim_product](../transforms/dim_product.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `product_key` | identifier | PK | — | — | — | — | the row key: one row per product. |
| `product_code` | name | — | — | — | names `product_key` (code) | match=`pattern` | the product's code in the source system, unique across all rows. |
| `product_name` | name | — | — | — | names `product_key` (common) | match=`pattern` | the product's name as a reader would see it. |
| `manufacturer` | name | — | — | — | names `brand` (legal) | — | who made the product. |
| `brand` | dimension | — | — | — | — | — | the brand the product is sold under. Far fewer brands than products, so a question about brands wants the brands and not the products. |
| `color` | dimension | — | — | — | — | — | the product's colour. |
| `category_name` | dimension | — | — | — | — | — | the product's top-level category. |
| `sub_category_name` | dimension | — | — | — | — | parent=`category_name` | the product's sub-category, one level below `category_name`. Which of the two a question means is a declared ambiguity (ProductCategory.level). |
| `weight` | hidden | — | — | — | — | — | the product's weight as the source gives it, in the unit named by `weight_unit` on the same row. NOT OFFERED TO A QUESTION: the column holds weights in several units and is empty for some products, so a sum, an average or a comparison across products would add one unit to another. Bringing every weight to one unit is a transform's job that has not been done (evidence/MODELLING-LOG.md), so no concept serves it. |
| `weight_unit` | hidden | — | — | — | — | — | the unit the same row's `weight` is in, as the source spells it, blank where the source gives none. NOT OFFERED TO A QUESTION: it exists only to read `weight`, which is not offered until a transform brings every weight to one unit. |

## Checks

_This dataset declares no checks._

## Value sets

_No column of this dataset is linked to a value set, and none links to it._

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `product_key` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `product_code` | `name` | via `names` | via `names` | — | — | — | values; pattern for common / long / short | display (L13) |
| `product_name` | `name` | via `names` | via `names` | — | — | — | values; pattern for common / long / short | display (L13) |
| `manufacturer` | `name` | via `names` | via `names` | — | — | — | values; pattern for common / long / short | display (L13) |
| `brand` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `color` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `category_name` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `sub_category_name` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `weight` | `hidden` | — | — | — | — | — | — | — |
| `weight_unit` | `hidden` | — | — | — | — | — | — | — |

## Bound by

*4 concept(s) take rows from this dataset — a change to a column's declaration reaches every one of them.*

- [Brand](../../ontology/concepts/Brand.md) — serves `brand`, `product_key`
- [Colour](../../ontology/concepts/Color.md) — serves `color`, `product_key`
- [Product](../../ontology/concepts/Product.md) — serves `product_key`, `product_code`, `product_name`, `manufacturer`, `brand`, `color`, `category_name`, `sub_category_name`
- [ProductCategory](../../ontology/concepts/ProductCategory.md) — serves `category_name`, `sub_category_name`, `product_key`

## Findings

- [DQ-DANGLINGKEY-CATEGORYKEY](../quality/DQ-DANGLINGKEY-CATEGORYKEY.md) — medium · open — nobody has ruled — `CategoryKey` is key-shaped and no relation in scope carries it as a key
- [DQ-DANGLINGKEY-SUBCATEGORYKEY](../quality/DQ-DANGLINGKEY-SUBCATEGORYKEY.md) — medium · open — nobody has ruled — `SubCategoryKey` is key-shaped and no relation in scope carries it as a key
