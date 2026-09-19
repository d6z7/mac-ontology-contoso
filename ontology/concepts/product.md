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

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `ProductKey` | integer | key | `dim_contoso_product` (key) | ProductKey — the identity, and the column the fact joins on. | — |
| `ProductCode` | varchar | dimension | `dim_contoso_product` | measured unique today (2 517/2 517, P2 G5); whether it is the product's business identity is an open ruling (RUN.md Q10), so it is served as a value, not as the key. | — |
| `ProductName` | varchar | attribute | `dim_contoso_product` | measured unique today (2 517/2 517) — almost certainly convention, not law (Q10). | — |
| `Manufacturer` | varchar | attribute | `dim_contoso_product` | Manufacturer — 1:1 with Brand today (measured 0 brands with two manufacturers). | — |
| `Brand` | varchar | dimension | `dim_contoso_product` | 11 measured values; the scope's 'by brand' axis. Brand <-> Manufacturer is 1:1 today (P2), whether by law is unruled (Q13). | — |
| `Color` | varchar | dimension | `dim_contoso_product` | CLEANSED: the landing carries 17 spellings that fold to 16 (Blue 197 rows / blue 3) — a closed vocabulary drifting by case (P1 #7, S8). The served column carries one spelling per colour; the rule belongs to the transform (P4). | — |
| `WeightUnit` | varchar | dimension | `dim_contoso_product` | CLEANSED: '' in the landing on 222 rows becomes NULL (absence_semantics). 62 rows name a unit for a weight that is not there (P1 #6) — missing vs not-applicable is an open ruling (Q7), not something this promotion decides. | — |
| `Weight` | decimal(20,5) | measure | `dim_contoso_product` | null on 284/2 517 rows (P1). | — |
| `Cost` | decimal(20,5) | measure | `dim_contoso_product` | Cost — the catalogue cost. The cost actually booked is UnitCost on the order line. | — |
| `Price` | decimal(20,5) | measure | `dim_contoso_product` | Price — the catalogue list price. NOT the price a line sold at: the line carries its own UnitPrice and NetPrice, and a sales figure is computed from those, never from here. | — |
| `CategoryKey` | integer | key | `dim_contoso_product` | — | — |
| `CategoryName` | varchar | dimension | `dim_contoso_product` | — | — |
| `SubCategoryKey` | integer | key | `dim_contoso_product` | — | — |
| `SubCategoryName` | varchar | dimension | `dim_contoso_product` | — | — |

_Declared per column, over 14 columns: description 10 of 14 · type 14 of 14 · joins → 0 of 14. An em dash is a column for which nothing is declared._

## Relationships

*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `ProductKey`

## Source of record
- Full MAC concept: `product.yaml` — open the **YAML** tab for the complete typed definition.

## Data
- Source table: [product](../../data/sources/product.md)
