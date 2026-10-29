---
type: Rule
title: Customer.age
state: proposed
---

# Customer.age

> PROJECTED from `ontology/rules/Customer.age.yaml` by tools/mac_rules.py — do not edit; change the yaml.

An age is computed, never stored: a customer's age from the birth date and a store's age from its opening date, both measured at the sampling date rather than at today's date. Which age arithmetic is meant — completed years counting the birthday, or calendar year boundaries crossed — has not been ruled.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Customer, Store
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — age, average age, customer age, store age, birth date, opening date

## What was said

> *"and just as we can calculate average age of customers we can do the same with shops"* — operator, 2026-10-23 (`meaning-as-code#decisions/RULED-2026-10-23_the-sampling-date-is-the-newest-order.md`)
