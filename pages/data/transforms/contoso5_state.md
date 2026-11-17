---
type: Transform
title: 'Transform: contoso5_state'
description: Produces dataset:contoso5_state
relation: contoso5_state
tags:
- Contoso 5
- transform
sql_file: data/transforms/contoso5_state.sql
---

Produces `dataset:contoso5_state` · driven by **undeclared** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Produces: [contoso5_state](../datasets/contoso5_state.md)

## SQL realization

Realized by `data/transforms/contoso5_state.sql` — open it with the **SQL** button.
