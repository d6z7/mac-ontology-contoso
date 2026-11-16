---
type: Rule
title: Order.date
state: proposed
---

# Order.date

> PROJECTED from `ontology/rules/Order.date.yaml` by tools/mac_rules.py — do not edit; change the yaml.

An order's date is the day it was placed, not the day it was delivered. A question that says when, or names a period, without saying delivery is answered on the order date; a question that says delivered or shipped is answered on the delivery date.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — order date, delivery date, when, placed, delivered, shipped, period
- **Formerly** — `order.default.period_is_order_date`

## How and where it is implemented

```
  declared at   ontology/concepts/order.yaml#readings.date
  realized by   mac.canon.column_select  (kind default)   default: ordered
                ordered: column: order_date
                delivered: column: delivery_date
  executed by   canons/column_select.py + planner/columns.py — WHICH COLUMN OR JOIN PATH a named reading resolves to. The third member of the family population_select and ratio
  tested by     RC10  'How many orders were placed in 2024?'  board: pass (stale)
```
