---
type: Rule
title: Country.where_we_have_customers
state: ruled
---

# Country.where_we_have_customers

> PROJECTED from `ontology/rules/Country.where_we_have_customers.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A question asking for the countries where we have customers asks for countries: the countries at least one customer lives in, one answer row per country, never one row per customer. Country is the subject and Customer the restriction. The same reading holds for other existence phrasings — countries that have a customer, with any customer — and the question must be answered, not refused.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Country, Customer
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — countries, where we have customers, customer country, list countries, existence

## What was said

> *"this question must be answerable: where we have customers. it can be usnerstood by you and can be understood by 2nd generation of LLM. i dont accept bullshit that it cannot be answered. what i might accept is that it needs to be reformulated in a way to contain werbs aubject and predicated and make it stylistic more correct."* — operator, 2026-10-19 (`meaning-as-code#decisions/FINDINGS-2026-10-19_slots-versus-object-sets-operator-rulings.md`)


## Examples

| Question | Reading |
|---|---|
| List all countries where we have customers | the countries referenced by at least one customer, one row each, by name |
