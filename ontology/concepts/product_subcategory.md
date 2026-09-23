---
type: Grouping
title: Product Subcategory
description: 'The lower level of the catalogue hierarchy: the 32 narrow groups a product belongs to, each inside exactly one of the 8 categories — MP4&MP3 and Bluetooth Headphones inside Audio, Televisions and Home Theater System…'
tags:
- CONTOSO
- grouping
- confidence:I
resource: table://dim_contoso_product
rule_pages:
- rules/product_subcategory.parent.read_the_column_not_the_key.md
---

The lower level of the catalogue hierarchy: the 32 narrow groups a product belongs to, each inside exactly one of the 8 categories — MP4&MP3 and Bluetooth Headphones inside Audio, Televisions and Home Theater System inside TV and Video, and so on.
IT IS NOT THE CATEGORY. 32 members against 8; a category question answered here returns four times the rows with the same column heading.
IT IS NOT A SEPARATE HIERARCHY BRANCH EITHER. Every subcategory has exactly one parent category (measured, 0 subcategories carrying two), so this level and its parent are one hierarchy read at two grains, not two axes.

## Details

- **Identity** — fk_name
- **Version** — 1.0
- **Schema version** — 0.1.14
- **Status** — draft
- **Owner** — operator
- **Governance owner** — operator
- **Last reviewed** — 2026-09-18

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
All 32 members, their keys, their search keys, their product counts and their PARENT category key are in data/lookups/contoso_product_subcategory.lookup.csv, cut from the served plane; the exploded membership is in data/lookups/dim_contoso_product.lookup.csv, and the 8 parent labels are in data/lookups/contoso_product_category.lookup.csv. So a subcategory word resolves offline, the roll-up to its category resolves offline, and a subcategory the delivery does not carry is a refusal derived from a closed 32-member register.
```

## Grounded in

- `dim_contoso_product` — key `ProductKey`

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `ProductKey` | integer | key | `dim_contoso_product` (key) | — | — |
| `SubCategoryKey` | integer | key | `dim_contoso_product` | — | — |
| `SubCategoryName` | varchar | dimension | `dim_contoso_product` | — | — |
| `CategoryKey` | integer | key | `dim_contoso_product` | — | — |

_Declared per column, over 4 columns: description 0 of 4 · type 4 of 4 · joins → 0 of 4. An em dash is a column for which nothing is declared._

## Relationships

*0 join(s) out · 0 in — click a concept to open it.*

**Groups** → **Product** — the leaf concept this rolls up.

## Source of record
- Full MAC concept: `product_subcategory.yaml` — open the **YAML** tab for the complete typed definition.