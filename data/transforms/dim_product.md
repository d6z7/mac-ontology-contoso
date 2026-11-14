---
type: Transform
title: 'Cleansing: dim_product'
description: Cleansing → contoso_served.dim_product
relation: contoso_served.dim_product
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/dim_product.sql
---

Produces `contoso_served.dim_product` · grain: —

## Rules
## Lineage
- Source: [product](../sources/product.md)
- Clean dataset: [dim_product](../datasets/dim_product.md)

## SQL realization
Realized by `dim_product.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.dim_product` · kinds: passthrough + transform

| output column | ← from | rule | kind |
|---|---|---|---|
| `product_key` | `product."productkey"` |  | passthrough |
| `product_code` | `product."productcode"` |  | passthrough |
| `product_name` | `product."productname"` |  | passthrough |
| `manufacturer` | `product."manufacturer"` |  | passthrough |
| `brand` | `product."brand"` |  | passthrough |
| `color` | `product."color"` → _UPPER(SUBSTR(p."color", 1, 1)) || SUBSTR(p."color", 2)_ |  | transform |
| `category_name` | `product."categoryname"` |  | passthrough |
| `sub_category_name` | `product."subcategoryname"` |  | passthrough |
| `weight` | `product."weight"` |  | passthrough |
| `weight_unit` | `product."weightunit"` |  | passthrough |