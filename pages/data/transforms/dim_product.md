---
type: Transform
title: 'Transform: dim_product'
description: Produces dataset:dim_product
relation: dim_product
tags:
- Contoso 5
- transform
sql_file: data/transforms/dim_product.sql
---

Produces `dataset:dim_product` · driven by **proposed** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Source: [product](../sources/product.md)
- Produces: [dim_product](../datasets/dim_product.md)

## SQL realization

Realized by `data/transforms/dim_product.sql` — open it with the **SQL** button.
