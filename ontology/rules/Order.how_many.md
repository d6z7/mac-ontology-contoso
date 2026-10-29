---
type: Rule
title: Order.how_many
state: proposed
---

# Order.how_many

> PROJECTED from `ontology/rules/Order.how_many.yaml` by tools/mac_rules.py — do not edit; change the yaml.

How many is three questions. Purchases are counted as orders; items sold are the quantity summed; order lines are how the data is stored and are not a business quantity. "How many did we sell" asks for items, "how many times did we sell" or "how many orders" asks for purchases.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — how many, units sold, items, orders, lines, volume, quantity

## Examples

| Question | Reading |
|---|---|
| how many did we sell in 2024 | units: quantity summed over 2024 orders |
| how many orders did we get in 2024 | distinct orders placed in 2024 |
