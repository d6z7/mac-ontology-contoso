---
type: Rule
title: Customer.register_not_buyers
state: proposed
---

# Customer.register_not_buyers

> PROJECTED from `ontology/rules/Customer.register_not_buyers.yaml` by tools/mac_rules.py — do not edit; change the yaml.

The customer register is wider than the buyers: a customer is a person on the register, and many registered customers have never bought anything. This is by design of the source, not a defect. "Customers" and "buyers" are two populations, and an answer counting customers says which one it counted.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Customer
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — customer, buyer, register, count customers, never bought, population

## Implemented at

- `ontology/relations/dim_customer.yaml#columns.customer_key.rules`

## Examples

| Question | Reading |
|---|---|
| how many customers do we have | states whether it counted the register or the customers who bought, and which |
