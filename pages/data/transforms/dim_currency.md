---
type: Transform
title: 'Transform: dim_currency'
description: Produces dataset:dim_currency
relation: dim_currency
tags:
- Contoso 5
- transform
sql_file: data/transforms/dim_currency.sql
---

Produces `dataset:dim_currency` · driven by **undeclared** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Source: [sales](../sources/sales.md)
- Produces: [dim_currency](../datasets/dim_currency.md)

## SQL realization

Realized by `data/transforms/dim_currency.sql` — open it with the **SQL** button.
