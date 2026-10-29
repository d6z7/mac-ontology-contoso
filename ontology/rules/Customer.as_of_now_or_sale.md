---
type: Rule
title: Customer.as_of_now_or_sale
state: proposed
---

# Customer.as_of_now_or_sale

> PROJECTED from `ontology/rules/Customer.as_of_now_or_sale.yaml` by tools/mac_rules.py — do not edit; change the yaml.

The customer register keeps history: a row is a version of a person, valid over a window. The customer as they are now and the customer a past sale was made to can be different rows, and reading one as the other moves old sales to new addresses. A question joining customers to sales over a period says which it means; neither reading is declared the default.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Customer, Order
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — customer, history, valid from, valid to, as of, moved, version

## How and where it is implemented

```
  declared at   (nowhere — prose, stated in words only)
  tested by     (nothing names a question)
```
