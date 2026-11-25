---
type: Transform
title: 'Transform: v_contoso5_sales_line'
description: Produces dataset:v_contoso5_sales_line
relation: v_contoso5_sales_line
tags:
- Contoso 5
- transform
sql_file: data/transforms/v_contoso5_sales_line.sql
---

Produces `dataset:v_contoso5_sales_line` · driven by **proposed** (`-- mac.transform.driven_by:` on the `.sql`; absent = undeclared, trusted as generated)

## Repairs

_This transform declares no `repairs`._

## Lineage

- Source: [customer](../sources/customer.md)
- Source: [sales](../sources/sales.md)
- Source: [store](../sources/store.md)
- Produces: [v_contoso5_sales_line](../datasets/v_contoso5_sales_line.md)

## SQL realization

Realized by `data/transforms/v_contoso5_sales_line.sql` — open it with the **SQL** button.
