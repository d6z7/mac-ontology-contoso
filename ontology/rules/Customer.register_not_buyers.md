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

## How and where it is implemented

```
  declared at   ontology/relations/dim_customer.yaml#columns.customer_key.rules
  tested by     (nothing names a question)
```

## Examples

| Question | Reading |
|---|---|
| how many customers have bought something | customers with at least one order, said to be buyers and not the register |
