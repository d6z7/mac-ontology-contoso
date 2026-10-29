---
type: Rule
title: Currency.code_is_not_the_unit
state: proposed
---

# Currency.code_is_not_the_unit

> PROJECTED from `ontology/rules/Currency.code_is_not_the_unit.yaml` by tools/mac_rules.py — do not edit; change the yaml.

Every amount on a sale is in US dollars. A sale's currency is the currency the customer transacted in, not the unit of its amounts: filtering by that currency does not turn the amounts into it. Sales asked for in a named currency are converted through the exchange rate.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Currency, Order
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — currency, usd, dollars, euros, transaction currency, convert, amounts

## How and where it is implemented

```
  declared at   (nowhere — prose, stated in words only)
  tested by     (nothing names a question)
```

## Examples

| Question | Reading |
|---|---|
| revenue in euros | USD amounts converted to EUR, not the USD amounts of EUR sales |
