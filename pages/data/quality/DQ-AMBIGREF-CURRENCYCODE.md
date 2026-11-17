---
type: DQ Issue
title: '`CurrencyCode` includes perfectly into 2 different keys — which is THE reference?'
description: '`CurrencyCode` includes perfectly into 2 different keys — which is THE
  reference?'
tags:
- Contoso 5
- severity:high
- disposition:open
---

`DQ-AMBIGREF-CURRENCYCODE` · severity **high** · disposition **open — nobody has ruled** · filed under [v_contoso5_fx_rate](../datasets/v_contoso5_fx_rate.md)

## Finding

`CurrencyCode` includes perfectly into 2 different keys — which is THE reference?

## About

- `source:currencyexchange`

## Needs

**Needs** — Which of currencyexchange.FromCurrency, currencyexchange.ToCurrency is THE reference for CurrencyCode? ANSWER ONE OF: currencyexchange.FromCurrency | currencyexchange.ToCurrency | both_are_real | neither. No recommendation is offered from the data because the data cannot carry one.

**Remedies**

- currencyexchange.FromCurrency: CurrencyCode references currencyexchange.FromCurrency, the reference to currencyexchange.ToCurrency is recorded as rejected-by-ruling, and questions convert FROM the order's currency. IF THE CHOICE IS WRONG THE NUMBERS DO NOT ERROR — they come back transformed the wrong way and still look plausible, which is the hardest defect to find later.
- currencyexchange.ToCurrency: CurrencyCode references currencyexchange.ToCurrency, the reference to currencyexchange.FromCurrency is recorded as rejected-by-ruling, and questions convert INTO the order's currency. IF THE CHOICE IS WRONG THE NUMBERS DO NOT ERROR — they come back transformed the wrong way and still look plausible, which is the hardest defect to find later.
- both_are_real: two references are drawn and every traversal must say which it used; a question that does not name a direction becomes ambiguous rather than wrong.
- neither: CurrencyCode stays an attribute, no line is drawn, and no question can traverse from it — the join must be written by hand each time, where it is visible.

**Recommended** — the endpoint the child is DENOMINATED IN — for an amount and an FX rate table, the child column is the `from` side

## Disposition

**open**.
- said by **mac_dq_findings.py/1**

## Repaired by

_No transform's `repairs` names this finding._

## Blocks and waives

_It blocks and waives nothing._

## Evidence

- measured on 4 reference(s) across 2 relation(s) (orders, sales): inclusion is 1.0 into every one of currencyexchange.FromCurrency, currencyexchange.ToCurrency, at the same key role and over the same rows. Value inclusion CANNOT separate them, so neither was drawn as the sole reference.
