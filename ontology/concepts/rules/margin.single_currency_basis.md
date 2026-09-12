---
type: Rule
title: margin.single_currency_basis
description: aggregation rule · binds NetPrice, UnitCost, ExchangeRate, CurrencyCode
tags:
- mac.rule_kind.aggregation
applies_to: ../margin.md
---

## Rule

- **Kind** — `aggregation`
- **Binds** — `NetPrice`, `UnitCost`, `ExchangeRate`, `CurrencyCode`
- **Rule id** — `margin.single_currency_basis`

### When

aggregating profit across rows that may span more than one CurrencyCode

### Then — do (then)

convert each line's profit to the base currency via ExchangeRate BEFORE summing, and disclose the base currency

### Never — don't (never)

summing (NetPrice - UnitCost) across mixed currencies as if they were one unit

Applies to [Gross profit (gross margin)](../margin.md).