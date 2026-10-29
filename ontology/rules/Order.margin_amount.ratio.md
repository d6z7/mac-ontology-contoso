---
type: Rule
title: Order.margin_amount.ratio
state: ruled
---

# Order.margin_amount.ratio

> PROJECTED from `ontology/rules/Order.margin_amount.ratio.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A margin ratio can be stated two ways over the same profit, and the question must say which: margin percent is profit over net revenue, markup is profit over cost. A question naming neither is asked.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Symbolic** — declared at `ontology/relations/v_contoso5_sales_line.yaml#columns.margin_amount.readings.ratio`
- **Keywords** — margin, markup, margin percent, profit, margin on cost, net margin
- **Formerly** — `margin.aggregation.two_named_ratios`

## Examples

| Question | Reading |
|---|---|
| what is our margin percentage | profit over net revenue |
| what is our margin ratio | asked: margin percent or markup |
