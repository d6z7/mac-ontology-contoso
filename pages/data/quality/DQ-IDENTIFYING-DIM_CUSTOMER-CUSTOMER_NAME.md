---
type: DQ Issue
title: '`dim_customer.customer_name` names individuals — 94,488 of 99,200 values are
  held by exactly one row'
description: '`dim_customer.customer_name` names individuals — 94,488 of 99,200 values
  are held by exactly one row'
tags:
- Contoso 5
- severity:medium
- disposition:open
---

`DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME` · severity **medium** · disposition **open — nobody has ruled** · filed under [dim_customer](../datasets/dim_customer.md)

## Finding

`dim_customer.customer_name` names individuals — 94,488 of 99,200 values are held by exactly one row

## About

- `dataset:dim_customer`

## Needs

**Needs** — a ruling on the concept that grounds `dim_customer.customer_name`: `rulings: {never_axis: privacy, evidence: DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME}` on the column, or a written reason the axis is safe to offer. Until then the planner has nothing to refuse with.

## Disposition

**open**.
- said by **mac_dq_findings.py/1**

## Repaired by

_No transform's `repairs` names this finding._

## Blocks and waives

- blocks `dataset:dim_customer.customer_name` — an open finding that blocks an address makes a question reading it refuse (L14)

## Evidence

- 94,488 of 99,200 distinct values (95%) over 104,990 rows are held by exactly one row (mac_profile.py/6, one GROUPING SETS scan). A column most of whose values name one row is an identifier wearing a dimension's role: GROUP BY it returns one row per person, and the query succeeds.
