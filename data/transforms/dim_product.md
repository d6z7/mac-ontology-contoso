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
| `product_key` | `product.ProductKey` |  | passthrough |
| `product_code` | `product.ProductCode` |  | passthrough |
| `product_name` | `product.ProductName` |  | passthrough |
| `manufacturer` | `product.Manufacturer` |  | passthrough |
| `brand` | `product.Brand` |  | passthrough |
| `color` | `product.Color` → _(upper(substr(p.Color, 1, 1)) || substr(p.Color, 2))_ |  | transform |
| `category_name` | `product.CategoryName` |  | passthrough |
| `sub_category_name` | `product.SubCategoryName` |  | passthrough |
| `weight` | `product.Weight` |  | passthrough |
| `weight_unit` | `product.WeightUnit` |  | passthrough |