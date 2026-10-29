---
type: Rule
title: Order.margin_ratio_is_named
state: ruled
---

# Order.margin_ratio_is_named

> PROJECTED from `ontology/rules/Order.margin_ratio_is_named.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A margin ratio can be stated two ways over the same profit, and the question must say which: margin percent is profit over net revenue, markup is profit over cost. A question naming neither is asked.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — margin, markup, margin percent, profit, margin on cost, net margin
- **Formerly** — `Order.margin_amount.ratio`, `margin.aggregation.two_named_ratios`

## How and where it is implemented

```
  declared at   ontology/relations/v_contoso5_sales_line.yaml#columns.margin_amount.readings.ratio
  realized by   mac.canon.ratio_select  (kind aggregation)   no default: asked
                margin_percent: denominator: net_amount
                markup_percent: denominator: cost_amount
  executed by   canons/ratio_select.py — WHICH DENOMINATOR a named ratio divides by. The twin of population_select: that one maps a word a reader says to the ROWS a concept has
  tested by     (nothing names a question)
```

## Examples

| Question | Reading |
|---|---|
| what is our margin percentage | profit over net revenue |
| what is our margin ratio | asked: margin percent or markup |
