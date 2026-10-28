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

| column | type | role | reference |
|---|---|---|---|
| `product_key` | integer | PK |  |
| `product_code` | string | value | search: `like` |
| `product_name` | string | value | search: `like` |
| `manufacturer` | string | value |  |
| `brand` | string | value |  |
| `color` | string | value |  |
| `category_name` | string | value |  |
| `sub_category_name` | string | value |  |
| `weight` | decimal | value |  |
| `weight_unit` | string | value |  |

## Referenced by

- `v_contoso5_sales_line.product_key` → `dim_product.product_key`