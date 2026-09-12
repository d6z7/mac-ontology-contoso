---
type: Rule
title: margin.gross_basis_disclosed
description: aggregation rule · binds NetPrice, UnitCost, Quantity
tags:
- mac.rule_kind.aggregation
applies_to: ../margin.md
---

## Rule

- **Kind** — `aggregation`
- **Binds** — `NetPrice`, `UnitCost`, `Quantity`
- **Rule id** — `margin.gross_basis_disclosed`

### When

computing profit or margin

### Then — do (then)

compute GROSS profit = SUM(Quantity x (NetPrice - UnitCost) x ExchangeRate) and disclose that only cost of goods (UnitCost) is subtracted

### Never — don't (never)

presenting gross profit as NET profit — operating, logistics and overhead costs are not in this data

Applies to [Gross profit (gross margin)](../margin.md).