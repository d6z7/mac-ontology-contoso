---
type: Rule
title: A bare total is net, and the reading is disclosed rather than silent
description: ambiguity rule · binds NetPrice, UnitPrice
tags:
- mac.rule_kind.ambiguity
- confidence:P
applies_to: ../net_sales_amount.md
---

## Rule

- **Kind** — `ambiguity`
- **Confidence** — P (proposed)
- **Binds** — `NetPrice`, `UnitPrice`
- **Rule id** — `net_sales_amount.ambiguity.gross_or_net`

### When

a question asks for a sales total without saying gross or net

### Then — do (then)

answer with NetSalesAmount and SAY SO in the answer, naming the discount as what was subtracted; offer the gross figure from `{UnitPrice}` alongside when the gap matters

### Never — don't (never)

choosing between `{NetPrice}` and `{UnitPrice}` silently — the two disagree on 136 913 of 223 974 lines, so an undisclosed choice is a different number with the same label

Applies to [Net Sales Amount](../net_sales_amount.md).