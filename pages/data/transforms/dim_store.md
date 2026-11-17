---
type: Transform
title: 'Transform: dim_store'
description: Produces dataset:dim_store
relation: dim_store
tags:
- Contoso 5
- transform
sql_file: data/transforms/dim_store.sql
---

Produces `dataset:dim_store` · driven by **undeclared** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Source: [store](../sources/store.md)
- Produces: [dim_store](../datasets/dim_store.md)

## SQL realization

Realized by `data/transforms/dim_store.sql` — open it with the **SQL** button.
