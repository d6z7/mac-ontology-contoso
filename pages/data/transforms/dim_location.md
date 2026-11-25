---
type: Transform
title: 'Transform: dim_location'
description: Produces dataset:dim_location
relation: dim_location
tags:
- Contoso 5
- transform
sql_file: data/transforms/dim_location.sql
---

Produces `dataset:dim_location` · driven by **proposed** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Source: [store](../sources/store.md)
- Produces: [dim_location](../datasets/dim_location.md)

## SQL realization

Realized by `data/transforms/dim_location.sql` — open it with the **SQL** button.
