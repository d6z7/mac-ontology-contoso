---
type: Rule
title: A scope with no line has no gross figure — refuse, never report a zero
description: exclusion rule · binds Quantity, UnitPrice
tags:
- mac.rule_kind.exclusion
- confidence:P
applies_to: ../gross_sales_amount.md
---

## Rule

- **Kind** — `exclusion`
- **Confidence** — P (proposed)
- **Binds** — `Quantity`, `UnitPrice`
- **Rule id** — `gross_sales_amount.evidence.no_line_is_not_a_zero`

### When

a resolved scope has no line at all in `{v_contoso_order_line}` — measured today: 52 801 of 104 990 customers, 10 of 74 store versions and 568 of 4 018 calendar days carry no line

### Then — do (then)

REFUSE with an evidence-boundary answer naming the scope that was resolved and found empty — never guess, never estimate, and never substitute the Net Sales Amount figure for the missing gross one

### Never — don't (never)

returning 0, or an empty result framed as a real zero: an empty scope has no line, and no line is not an amount. And never reading the absence as a null VALUE — `{Quantity}` and `{UnitPrice}` are measured non-null on all 223 974 lines, so no resolved row carries a null to interpret and the only absence available here is the absent ROW

Applies to [Gross Sales Amount](../gross_sales_amount.md).