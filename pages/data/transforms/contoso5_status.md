---
type: Transform
title: 'Transform: contoso5_status'
description: Produces dataset:contoso5_status
relation: contoso5_status
tags:
- Contoso 5
- transform
sql_file: data/transforms/contoso5_status.sql
---

Produces `dataset:contoso5_status` · driven by **undeclared** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Produces: [contoso5_status](../datasets/contoso5_status.md)

## SQL realization

Realized by `data/transforms/contoso5_status.sql` — open it with the **SQL** button.
