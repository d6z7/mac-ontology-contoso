---
type: Dataset
title: 'Clean: dim_product'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_product
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `product_key` | integer | PK |
| `product_code` | string | value |
| `product_name` | string | value |
| `manufacturer` | string | value |
| `brand` | string | value |
| `color` | string | value |
| `category_name` | string | value · FK |
| `sub_category_name` | string | value |
| `weight` | decimal | value |
| `weight_unit` | string | value |

## Foreign keys

- `category_name` → `contoso5_category_name.code`

## Referenced by

- `v_contoso5_sales_line.product_key` → `dim_product.product_key`

## What a question may do

### Details

- **Schema version** — 0.4.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

### Key

- One row is identified by `product_key`.

### Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `product_key` | **key** | — | `Product` | — |
| `product_code` | — | axis `categorical` | — | label_of `product_key` (code) |
| `product_name` | — | axis `categorical` | — | label_of `product_key` (common) |
| `manufacturer` | — | axis `categorical` | — | label_of `brand` (legal) |
| `brand` | — | axis `categorical` | — | — |
| `color` | — | axis `categorical` | — | — |
| `category_name` | — | axis `categorical` | — | — |
| `sub_category_name` | — | axis `categorical` | — | finer_than `category_name` |

_Declared per column, over 8 columns: offers 7 of 8 · references 1 of 8 · rulings 4 of 8. An em dash is a column for which nothing is declared._

### Bound by

*4 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Brand](../concepts/brand.md) — serves `brand`, `product_key`
- [Colour](../concepts/color.md) — serves `color`, `product_key`
- [Product](../concepts/product.md) — serves `product_key`, `product_code`, `product_name`, `manufacturer`, `brand`, `color`, `category_name`, `sub_category_name`
- [Product Category](../concepts/product_category.md) — serves `category_name`, `sub_category_name`, `product_key`
