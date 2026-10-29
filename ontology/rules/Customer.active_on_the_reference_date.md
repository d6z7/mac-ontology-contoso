---
type: Rule
title: Customer.active_on_the_reference_date
state: ruled
---

# Customer.active_on_the_reference_date

> PROJECTED from `ontology/rules/Customer.active_on_the_reference_date.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A customer is active on a reference date when that date falls inside the customer's validity window — on or after the day the record became valid and on or before the day it stopped being valid. The reference date is the date the question states, else the data's own "now", and the answer says which. "Customers" with no other word means the active customers; "registered" customers are every customer on the register, whether valid on that date or not. Active customers are not the same set as customers who have bought something — each can hold people the other does not.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Customer
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — customer, active, registered, valid, reference date, stichtag, as of, how many customers

## How and where it is implemented

```
  declared at   ontology/concepts/customer.yaml#readings.population
                ontology/relations/dim_customer.yaml#columns.valid_from.rules
                ontology/relations/dim_customer.yaml#columns.valid_to.rules
  realized by   mac.canon.population_select  (kind resolution)   default: active
                active: valid_from <= @as_of AND valid_to >= @as_of
                registered: every row
  takes         as_of — the reference date (Stichtag) the reading is evaluated on
  depends on    the question's date, else the anchor v_contoso5_sales_line.order_date (rule Order.now_is_the_newest_order) = 2025-12-31 (recorded vintage)
  executed by   planner/populations.py — WHICH ROWS a concept has. Named populations as structured predicates (planner/predicates.py), one marked `default`, and the rule's own 
  tested by     RC04  'How many customers do we have as of 31.12.2025?'  board: pass (stale)
```

## What was said

> *"it is differentitaion between active custoomers and registered customers"* — operator, 2026-10-29

> *"you have SCD for this ... customer valid from data to valid to date . if the reference date like now() or some specific date in past is gt then valid to date ... then the customer is valid. this can be a superset of customer who bot something. we need to refine question statig stichtag to be 31.12.2025"* — operator, 2026-10-29

> *"active customers is meant"* — operator, 2026-10-29


## Examples

| Question | Reading |
|---|---|
| how many registered customers do we have | every customer on the register, no date applied |
