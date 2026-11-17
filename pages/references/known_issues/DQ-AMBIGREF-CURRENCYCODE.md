---
type: Reference
title: DQ-AMBIGREF-CURRENCYCODE — `CurrencyCode` includes perfectly into 2 different keys — which is THE reference?
tags: [reference, guardrail]
---

# DQ-AMBIGREF-CURRENCYCODE

*high · open — nobody has ruled · filed under `v_contoso5_fx_rate`*

**Finding.** `CurrencyCode` includes perfectly into 2 different keys — which is THE reference?

**About.** `source:currencyexchange`

**Needs.** Which of currencyexchange.FromCurrency, currencyexchange.ToCurrency is THE reference for CurrencyCode? ANSWER ONE OF: currencyexchange.FromCurrency | currencyexchange.ToCurrency | both_are_real | neither. No recommendation is offered from the data because the data cannot carry one.

**Recommended.** the endpoint the child is DENOMINATED IN — for an amount and an FX rate table, the child column is the `from` side

