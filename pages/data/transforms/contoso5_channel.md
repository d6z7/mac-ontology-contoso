---
type: Transform
title: 'Transform: contoso5_channel'
description: Produces dataset:contoso5_channel
relation: contoso5_channel
tags:
- Contoso 5
- transform
sql_file: data/transforms/contoso5_channel.sql
---

Produces `dataset:contoso5_channel` · driven by **undeclared** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Produces: [contoso5_channel](../datasets/contoso5_channel.md)

## SQL realization

Realized by `data/transforms/contoso5_channel.sql` — open it with the **SQL** button.
