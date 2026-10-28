---
type: DQ Issue
title: '`dim_customer.city` names individuals — 21,317 of 34,581 values are held by
  exactly one row'
description: 21,317 of 34,581 distinct values (62%) over 104,990 rows are held by
  exactly one row (mac_profile.py/6, one GROUPING SETS scan). A column most of whose
  values name one row is an identifier wearing a d
tags:
- CONTOSO5
- severity:medium
- confidence:?
- lifecycle:draft
---

`DQ-IDENTIFYING-DIM_CUSTOMER-CITY` · severity **medium** · confidence **?** · disposition **open — nobody has ruled**

## Finding
21,317 of 34,581 distinct values (62%) over 104,990 rows are held by exactly one row (mac_profile.py/6, one GROUPING SETS scan). A column most of whose values name one row is an identifier wearing a dimension's role: GROUP BY it returns one row per person, and the query succeeds.

## Current handling
—

## Residual risk
—

## Sign-off required
—

## Disposition

**open** — ruled by **nobody named**.

_No reason recorded. `accepted` and `wont_fix` both require one._

## Table
- [customer](../sources/customer.md)