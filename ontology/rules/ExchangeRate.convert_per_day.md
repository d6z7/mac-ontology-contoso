---
type: Rule
title: ExchangeRate.convert_per_day
state: proposed
---

# ExchangeRate.convert_per_day

> PROJECTED from `ontology/rules/ExchangeRate.convert_per_day.yaml` by tools/mac_rules.py — do not edit; change the yaml.

An amount is converted at its own day's rate, never at a rate averaged over a period. A rate is not a quantity to add up: over time it can at most be averaged, and across currency pairs it is not combined at all.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — ExchangeRate
- **Formal** — **Escape hatch** — `mac.canon.additivity_guard` with `confidence: P`, `measure_column: rate`, `axis_effects: {'time': 'mac.concept.aggregation_effect.average', 'categorical': 'mac.concept.aggregation_effect.none'}`
- **Keywords** — exchange rate, average rate, daily rate, conversion, fx, additivity
- **Formerly** — `exchange_rate.aggregation.convert_per_day_never_average`

## How and where it is implemented

```
  declared at   (NOWHERE)
  realized by   mac.canon.additivity_guard  (kind aggregation)   no default: asked
  executed by   canons/additivity_guard.py — SUM of a measure across an axis whose fold-law cell is not `additive` is refused unless the axis is pinned or grouped (serves semi_
  tested by     (nothing names a question)
```
