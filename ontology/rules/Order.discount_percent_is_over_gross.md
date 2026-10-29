---
type: Rule
title: Order.discount_percent_is_over_gross
state: ruled
---

# Order.discount_percent_is_over_gross

> PROJECTED from `ontology/rules/Order.discount_percent_is_over_gross.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A discount percentage is the money given away divided by the gross amount before discount — not by the net amount.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — discount, discount percentage, discount rate, gross, percent
- **Formerly** — `Order.discount_amount.percent`, `discount.aggregation.percent_is_over_gross`

## How and where it is implemented

```
  declared at   ontology/relations/v_contoso5_sales_line.yaml#columns.discount_amount.readings.percent
  realized by   mac.canon.ratio_select  (kind aggregation)   default: percent
                percent: denominator: gross_amount
  executed by   canons/ratio_select.py — WHICH DENOMINATOR a named ratio divides by. The twin of population_select: that one maps a word a reader says to the ROWS a concept has
  tested by     (nothing names a question)
```
