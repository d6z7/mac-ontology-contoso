---
type: Rule
title: margin.net_revenue_side
description: aggregation rule · binds NetPrice, UnitPrice
tags:
- mac.rule_kind.aggregation
applies_to: ../margin.md
---

## Rule

- **Kind** — `aggregation`
- **Binds** — `NetPrice`, `UnitPrice`
- **Rule id** — `margin.net_revenue_side`

### When

taking the revenue side of profit

### Then — do (then)

use NET revenue (NetPrice, post-discount), consistent with Sales > net_sales_base_currency

### Never — don't (never)

subtracting cost from GROSS (list-price) revenue — that overstates profit by the discount volume

Applies to [Gross profit (gross margin)](../margin.md).