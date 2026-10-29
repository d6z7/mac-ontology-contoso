---
type: Rule
title: Order.order_date.anchor
state: ruled
---

# Order.order_date.anchor

> PROJECTED from `ontology/rules/Order.order_date.anchor.yaml` by tools/mac_rules.py — do not edit; change the yaml.

"Now", for this data, is the date of the newest order — measured from the data, not taken from the clock. Relative periods such as "last month" are read against it, and it moves forward by itself when new orders arrive.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Symbolic** — declared at `ontology/relations/v_contoso5_sales_line.yaml#columns.order_date.offers.anchor`
- **Keywords** — anchor, now, today, sampling date, latest, newest order, last month, relative period
- **Decided in** — `meaning-as-code#decisions/RULED-2026-10-23_the-sampling-date-is-the-newest-order.md`
- **Formerly** — `order.resolution.the_anchor_is_the_newest_order`

## What was said

> *"but as the time move on ... we need to specify the sampling date lets say on 31.12.2025"* — operator, 2026-10-23 (`meaning-as-code#decisions/RULED-2026-10-23_the-sampling-date-is-the-newest-order.md`)
