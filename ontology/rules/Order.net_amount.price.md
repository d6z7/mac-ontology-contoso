---
type: Rule
title: Order.net_amount.price
state: ruled
---

# Order.net_amount.price

> PROJECTED from `ontology/rules/Order.net_amount.price.yaml` by tools/mac_rules.py — do not edit; change the yaml.

An unqualified price means what the customer paid per article: the net amount divided by the number of units, both summed over the lines asked about — never an average of line prices.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Symbolic** — declared at `ontology/relations/v_contoso5_sales_line.yaml#columns.net_amount.readings.price`
- **Keywords** — price, average price, unit price, per article, per unit, net price
- **Formerly** — `net_revenue.default.a_price_is_revenue_per_article`
