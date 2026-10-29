---
type: Rule
title: Order.revenue_means_net
state: ruled
---

# Order.revenue_means_net

> PROJECTED from `ontology/rules/Order.revenue_means_net.yaml` by tools/mac_rules.py — do not edit; change the yaml.

"Revenue" or "sales" without "net" or "gross" means the net amount — what the customer was charged after discount — and the answer says so. "Gross revenue" means the amount before discount.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — revenue, sales, net, gross, turnover, net revenue, gross revenue
- **Formerly** — `Order.net_amount.surfaces`

## Implemented at

- `ontology/relations/v_contoso5_sales_line.yaml#columns.net_amount.rules`
