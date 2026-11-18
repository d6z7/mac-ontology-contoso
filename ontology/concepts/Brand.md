# Brand

The account of concept Brand.

## Overview

Whose name a product is sold under: names carried as a column on the product row with no table and no key of their own. WHY IT IS A CONCEPT AT ALL. "Contoso products" is something a question says. As a column flag inside Product it resolves against nothing; as a concept, its names resolve offline from the column's own values — and, because Product grounds the same column, Product's own names are reached THROUGH it. IT IS NOT THE MANUFACTURER. Both are small sets of names on the same row and most names appear in both: a brand is what the customer sees, a manufacturer is who made it.

## Identity

Brand NAMES used as their own key — a closed set with no surrogate and no relation behind it.

## Grain

one member per brand name

## Brand.not_manufacturer

- **when** — a question asks who is behind a product
- **then** — decide whether it means the brand the customer buys or the manufacturer, and say which
- **never** — treat the two columns as interchangeable because their member sets overlap

## Cites

- `dataset:dim_product.brand`
- `dataset:dim_product.product_key`
- `rule:Brand.not_manufacturer`

## edge product__sold_under__brand, from Product

(no notes)
