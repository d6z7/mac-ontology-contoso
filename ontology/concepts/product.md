---
type: Reference
title: Product
description: 'A sellable item in the catalogue: one row per product, carrying its code, name, manufacturer, brand, colour, weight, cost, list price and its place in the two-level category hierarchy.'
tags:
- CONTOSO
- reference
- confidence:I
resource: table://dim_contoso_product
rule_pages:
- rules/product.price.catalogue_is_not_the_sale.md
- rules/product.weight.unit_and_weight_are_independent.md
---

A sellable item in the catalogue: one row per product, carrying its code, name, manufacturer, brand, colour, weight, cost, list price and its place in the two-level category hierarchy.
IT IS NOT A PRODUCT VERSION. This dimension is not versioned — 2 517 rows over 2 517 keys, one row each — so a price on this row is the current list price and there is no history to read. The price actually charged is on the order line, not here.
IT IS ALSO NOT THE FULL CATALOGUE OF WHAT SOLD. Every ProductKey on the fact resolves here (0 orphans measured over 223 974 lines), but this dimension may carry products with no sale.

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
All 2 517 products are in data/lookups/dim_contoso_product.lookup.csv, cut from the served plane, with a search key, the product code, the brand and both hierarchy keys — so a product word resolves offline and so does its brand and category. The colour, weight-unit, category and subcategory value sets are in data/lookups/contoso_color.lookup.csv, data/lookups/contoso_weight_unit.lookup.csv, data/lookups/contoso_product_category.lookup.csv and data/lookups/contoso_product_subcategory.lookup.csv. Nothing here needs a probe, and a product name that does not resolve is a refusal derived from a complete register.
```

## Grounded in

- `dim_contoso_product` — key `ProductKey`

## Grain
one row = one product — ProductKey

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `ProductKey` | key | `dim_contoso_product` (key) |  |  |
| `ProductCode` | dimension | `dim_contoso_product` |  |  |
| `ProductName` | attribute | `dim_contoso_product` |  |  |
| `Manufacturer` | attribute | `dim_contoso_product` |  |  |
| `Brand` | dimension | `dim_contoso_product` |  |  |
| `Color` | dimension | `dim_contoso_product` |  |  |
| `WeightUnit` | dimension | `dim_contoso_product` |  |  |
| `Weight` | measure | `dim_contoso_product` |  |  |
| `Cost` | measure | `dim_contoso_product` |  |  |
| `Price` | measure | `dim_contoso_product` |  |  |
| `CategoryKey` | key | `dim_contoso_product` |  |  |
| `CategoryName` | dimension | `dim_contoso_product` |  |  |
| `SubCategoryKey` | key | `dim_contoso_product` |  |  |
| `SubCategoryName` | dimension | `dim_contoso_product` |  |  |

## Relationships

*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `ProductKey`

## Source of record
- Full MAC concept: `product.yaml` — open the **YAML** tab for the complete typed definition.

## Data
- Source table: [product](../../data/sources/product.md)
