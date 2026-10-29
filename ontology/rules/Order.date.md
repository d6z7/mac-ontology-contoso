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

## Implemented at

- `ontology/concepts/order.yaml#readings.date`
