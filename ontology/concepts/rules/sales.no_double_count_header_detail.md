---
type: Rule
title: sales.no_double_count_header_detail
description: exclusion rule · binds OrderKey
tags:
- mac.rule_kind.exclusion
applies_to: ../sales.md
---

## Rule

- **Kind** — `exclusion`
- **Binds** — `OrderKey`
- **Rule id** — `sales.no_double_count_header_detail`

### When

choosing a table to sum sales from

### Then — do (then)

sum EITHER the denormalized `sales` table OR orders x orderrows — never both; they are the same order lines in two shapes

### Never — don't (never)

adding `sales` and orderrows totals together (doubles revenue)

Applies to [Sales (net revenue)](../sales.md).