---
type: Transform
title: 'Transform: dim_customer'
description: Produces dataset:dim_customer
relation: dim_customer
tags:
- Contoso 5
- transform
sql_file: data/transforms/dim_customer.sql
---

Produces `dataset:dim_customer` · driven by **undeclared** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Source: [customer](../sources/customer.md)
- Produces: [dim_customer](../datasets/dim_customer.md)

## SQL realization

Realized by `data/transforms/dim_customer.sql` — open it with the **SQL** button.
