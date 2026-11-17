---
type: Transform
title: 'Transform: dim_country'
description: Produces dataset:dim_country
relation: dim_country
tags:
- Contoso 5
- transform
sql_file: data/transforms/dim_country.sql
---

Produces `dataset:dim_country` · driven by **ruled** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Source: [store](../sources/store.md)
- Produces: [dim_country](../datasets/dim_country.md)

## SQL realization

Realized by `data/transforms/dim_country.sql` — open it with the **SQL** button.
