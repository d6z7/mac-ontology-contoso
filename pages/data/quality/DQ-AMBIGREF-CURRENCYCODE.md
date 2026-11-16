---
type: DQ Issue
title: '`CurrencyCode` includes perfectly into 2 different keys — which is THE reference?'
description: 'measured on 4 reference(s) across 2 relation(s) (orders, sales): inclusion
  is 1.0 into every one of currencyexchange.FromCurrency, currencyexchange.ToCurrency,
  at the same key role and over the same r'
tags:
- CONTOSO5
- severity:high
- confidence:?
- lifecycle:draft
---

`DQ-AMBIGREF-CURRENCYCODE` · severity **high** · confidence **?** · disposition **open — nobody has ruled**

## Finding
measured on 4 reference(s) across 2 relation(s) (orders, sales): inclusion is 1.0 into every one of currencyexchange.FromCurrency, currencyexchange.ToCurrency, at the same key role and over the same rows. Value inclusion CANNOT separate them, so neither was drawn as the sole reference.

## Current handling
—

## Residual risk
—

## Sign-off required
—

## Disposition

**open** — ruled by **nobody named**.

_No reason recorded. `accepted` and `wont_fix` both require one._

## Table
- [currencyexchange](../sources/currencyexchange.md)