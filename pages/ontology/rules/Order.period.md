---
type: Rule
title: Order.period
state: ruled
---

# Order.period

> PROJECTED from `ontology/rules/Order.period.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A question that names no period covers all time. There is no implied "this year" and no implied latest month, and the answer states the window it covered.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — period, all time, no period, time window, unscoped, this year
- **Formerly** — `order.default.an_unscoped_question_covers_all_time`

## How and where it is implemented

```
  declared at   ontology/concepts/order.yaml#readings.period
  realized by   mac.canon.period_default  (kind default)   default: all_time
                all_time: unbounded: True
  executed by   canons/period_default.py + planner/period.py, consulted at planner/plan._period_window (step 4e, beside the population decision) — WHAT SILENCE ABOUT TIME MEANS
  tested by     AGG-01  'What is the total net revenue?'  board: pass (stale)
  tested by     ADV-22  'Total Revenue'  board: pass (stale)
```
