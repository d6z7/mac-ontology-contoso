---
type: Rule
title: Order.rate_on_order_date
state: proposed
---

# Order.rate_on_order_date

> PROJECTED from `ontology/rules/Order.rate_on_order_date.yaml` by tools/mac_rules.py — do not edit; change the yaml.

An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a target currency alone does not pick a rate.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — ExchangeRate, Order
- **Formal** — **Escape hatch** — `mac.canon.composite_key_guard` with `confidence: P`, `code_column: to_currency`, `scope_columns: ['date_day', 'from_currency']`
- **Keywords** — exchange rate, conversion, currency, order date, fx
- **Formerly** — `order.resolution.rate_on_order_date`

## How and where it is implemented

```
  declared at   ontology/edges.yaml#order__converts_at__exchange_rate.resolved_by
  realized by   mac.canon.composite_key_guard  (kind resolution)   no default: asked
  executed by   canons/composite_key_guard.py — a parent-scoped code constrained or grouped without its scope column(s) is refused (serves context_dependent_meaning). Fired by 
  tested by     (nothing names a question)
```
