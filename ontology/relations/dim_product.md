---
type: Relation
title: dim_product
description: semantic plane · 8 described column(s) · 4 binding concept(s)
tags:
- CONTOSO5
- relation
- semantic-plane
---

What a question may DO with each column of `dim_product` — the SEMANTIC plane of this relation. Its physical facts (types, measured distincts, where its rows live) are on the data-plane page; this says what the columns MEAN.

## Details

- **Schema version** — 0.3.1-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

## Key

- One row is identified by `product_key`.

## Columns

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

## Bound by

*4 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Brand](../concepts/brand.md) — serves `brand`, `product_key`
- [Colour](../concepts/color.md) — serves `color`, `product_key`
- [Product](../concepts/product.md) — serves `product_key`, `product_code`, `product_name`, `manufacturer`, `brand`, `color`, `category_name`, `sub_category_name`
- [Product Category](../concepts/product_category.md) — serves `category_name`, `sub_category_name`, `product_key`

## Served as

- Kind — `view` · served by the warehouse.
- The same relation's PHYSICAL page: [`dim_product`](../../data/datasets/dim_product.md)
