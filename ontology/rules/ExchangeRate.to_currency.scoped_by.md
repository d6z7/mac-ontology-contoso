---
type: Rule
title: ExchangeRate.to_currency.scoped_by
state: proposed
---

# ExchangeRate.to_currency.scoped_by

> PROJECTED from `ontology/rules/ExchangeRate.to_currency.scoped_by.yaml` by tools/mac_rules.py — do not edit; change the yaml.

An exchange rate's target currency means something only together with its source currency: the direction is part of the rate's identity, so a rate is never picked or grouped by its target currency alone.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — ExchangeRate, Currency
- **Formal** — **Symbolic** — declared at `ontology/relations/v_contoso5_fx_rate.yaml#columns.to_currency.rulings.scoped_by`
- **Keywords** — exchange rate, currency, direction, from currency, to currency, fx
- **Formerly** — `exchange_rate.exclusion.direction_is_part_of_the_key`
