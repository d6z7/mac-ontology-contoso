---
type: Rule
title: Order.is_the_purchase
state: ruled
---

# Order.is_the_purchase

> PROJECTED from `ontology/rules/Order.is_the_purchase.yaml` by tools/mac_rules.py — do not edit; change the yaml.

An order is the purchase: one customer buying at one store on one day in one currency. Its lines are not orders and not events of their own — a line borrows the when, the who and the where from its order and adds only which product and how many. Counting orders counts purchases, never lines.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — order, purchase, order line, sale, event, how many orders

## Examples

| Question | Reading |
|---|---|
| how many orders | distinct orders (purchases), not order lines |
