---
type: Rule
title: Order.no_lifecycle_state
state: proposed
---

# Order.no_lifecycle_state

> PROJECTED from `ontology/rules/Order.no_lifecycle_state.yaml` by tools/mac_rules.py — do not edit; change the yaml.

An order has no state beyond its two dates: it was placed on one day and delivered on another. Nothing records a cancellation or a return, so a question about either has no answer in this business's data and says so; an absent state is never read as zero.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — order status, cancelled, returned, cancellation, return, lifecycle

## How and where it is implemented

```
  declared at   (nowhere — prose, stated in words only)
  tested by     (nothing names a question)
```

## Examples

| Question | Reading |
|---|---|
| how many orders were cancelled | unanswerable: no cancellation is recorded |
