---
type: Transform
title: 'Transform: v_contoso5_fx_rate'
description: Produces dataset:v_contoso5_fx_rate
relation: v_contoso5_fx_rate
tags:
- Contoso 5
- transform
sql_file: data/transforms/v_contoso5_fx_rate.sql
---

Produces `dataset:v_contoso5_fx_rate` · driven by **undeclared** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Source: [currencyexchange](../sources/currencyexchange.md)
- Produces: [v_contoso5_fx_rate](../datasets/v_contoso5_fx_rate.md)

## SQL realization

Realized by `data/transforms/v_contoso5_fx_rate.sql` — open it with the **SQL** button.
