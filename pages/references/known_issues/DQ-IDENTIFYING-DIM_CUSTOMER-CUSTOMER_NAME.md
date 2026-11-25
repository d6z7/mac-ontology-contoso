---
type: Reference
title: DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME — `dim_customer.customer_name` names individuals — 94,488 of 99,200 values are held by exactly one row
tags: [reference, guardrail]
---

# DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME

*medium · open — nobody has ruled · filed under `dim_customer`*

**Finding.** `dim_customer.customer_name` names individuals — 94,488 of 99,200 values are held by exactly one row

**About.** `dataset:dim_customer`

**Blocks.** `dataset:dim_customer.customer_name` — a question reading it refuses while the finding is open.

**Needs.** a ruling on the concept that grounds `dim_customer.customer_name`: `rulings: {never_axis: privacy, evidence: DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME}` on the column, or a written reason the axis is safe to offer. Until then the planner has nothing to refuse with.

