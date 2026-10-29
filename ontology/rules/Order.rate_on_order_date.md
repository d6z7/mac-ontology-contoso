---
type: Rule
title: Order.rate_on_order_date
state: proposed
---

# Order.rate_on_order_date

> PROJECTED from `ontology/rules/Order.rate_on_order_date.yaml` by tools/mac_rules.py — do not edit; change the yaml.

An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a target currency alone does not pick a rate.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Order, ExchangeRate
- **Formal** — **Escape hatch** — `mac.canon.composite_key_guard` with `confidence: P`, `code_column: to_currency`, `scope_columns: ['date_day', 'from_currency']`
- **Keywords** — exchange rate, conversion, currency, order date, fx
- **Formerly** — `order.resolution.rate_on_order_date`
