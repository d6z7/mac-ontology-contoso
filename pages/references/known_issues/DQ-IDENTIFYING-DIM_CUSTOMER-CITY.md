---
type: Reference
title: DQ-IDENTIFYING-DIM_CUSTOMER-CITY — `dim_customer.city` names individuals — 21,317 of 34,581 values are held by exactly one row
tags: [reference, guardrail]
---

# DQ-IDENTIFYING-DIM_CUSTOMER-CITY

*medium · confidence ?*

**Finding.** 21,317 of 34,581 distinct values (62%) over 104,990 rows are held by exactly one row (mac_profile.py/6, one GROUPING SETS scan). A column most of whose values name one row is an identifier wearing a dimension's role: GROUP BY it returns one row per person, and the query succeeds.

**Current handling.** —

**Residual risk.** —

**Resolution.** Not yet reconciled (newly harvested) — an honest open item.

