---
type: Grouping
title: Product Category
description: 'The upper level of the catalogue hierarchy: the eight broad groups every product belongs to — Audio, TV and Video, Computers, Cameras and camcorders, Cell phones, Music Movies and Audio Books, Games and Toys, Home…'
tags:
- CONTOSO
- grouping
- confidence:I
resource: table://dim_contoso_product
rule_pages:
- rules/product_category.level.category_is_not_subcategory.md
---

The upper level of the catalogue hierarchy: the eight broad groups every product belongs to — Audio, TV and Video, Computers, Cameras and camcorders, Cell phones, Music Movies and Audio Books, Games and Toys, Home Appliances.
IT IS NOT THE SUBCATEGORY. The two levels are separate concepts because they are different grains — 8 members against 32 — and someone asking for a category breakdown would be MISLED by a 32-row answer, not merely surprised. The subcategory rolls up into this level, and that roll-up is a function (measured, 0 subcategories with two parents).
IT IS NOT A BRAND AXIS EITHER. Brand cuts across the hierarchy; the two are orthogonal.

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
All 8 members, their keys, their search keys and their product counts are in data/lookups/contoso_product_category.lookup.csv, cut from the served plane; the exploded membership is in data/lookups/dim_contoso_product.lookup.csv. So a category word resolves offline, membership needs no probe, and a category the delivery does not carry is a refusal derived from a closed 8-member register rather than from an empty query.
```

## Grounded in

- `dim_contoso_product` — key `ProductKey`

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `ProductKey` | key | `dim_contoso_product` (key) |  |  |
| `CategoryKey` | key | `dim_contoso_product` |  |  |
| `CategoryName` | dimension | `dim_contoso_product` |  |  |

## Relationships

*0 join(s) out · 0 in — click a concept to open it.*

**Groups** → **Product** — the leaf concept this rolls up.

## Source of record
- Full MAC concept: `product_category.yaml` — open the **YAML** tab for the complete typed definition.