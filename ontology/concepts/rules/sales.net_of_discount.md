---
type: Rule
title: sales.net_of_discount
description: aggregation rule · binds NetPrice, UnitPrice, Quantity
tags:
- mac.rule_kind.aggregation
applies_to: ../sales.md
---

## Rule

- **Kind** — `aggregation`
- **Binds** — `NetPrice`, `UnitPrice`, `Quantity`
- **Rule id** — `sales.net_of_discount`

### When

computing sales value from order lines

### Then — do (then)

use NET revenue = SUM(Quantity x NetPrice); report GROSS = SUM(Quantity x UnitPrice) only when explicitly asked, and disclose which

### Never — don't (never)

reporting gross as 'sales' without saying so — it overstates by the discount volume

Applies to [Sales (net revenue)](../sales.md).