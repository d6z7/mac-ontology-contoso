---
type: Entity
title: Product
description: 'A thing Contoso sells, at the level the shelf knows it: a SKU.'
tags:
- CONTOSO5
- entity
- confidence:I
timestamp: '2026-09-29'
---

# Product

A thing Contoso sells, at the level the shelf knows it: a SKU. The account is knowledge/product.md.

## Relationships

- **product__sold_under__brand** → [Brand](/Brand.md) (cardinality 1; grounded join ``)
- **product__belongs_to__product_category** → [ProductCategory](/ProductCategory.md) (cardinality 1; grounded join ``)
- **product__comes_in__color** → [Color](/Color.md) (cardinality 1; grounded join ``)
- inverse of **order__of__product** ← [Order](/Order.md) (grounded join `v_contoso5_sales_line.product_key = dim_product.product_key`)

# Citations

1. MAC concept source of record: `concepts/product.yaml` (schema_version 0.3.0-develop, confidence I).
