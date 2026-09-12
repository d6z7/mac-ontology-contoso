---
type: Rule
title: sales.single_currency_basis
description: aggregation rule · binds NetPrice, ExchangeRate, CurrencyCode
tags:
- mac.rule_kind.aggregation
applies_to: ../sales.md
---

## Rule

- **Kind** — `aggregation`
- **Binds** — `NetPrice`, `ExchangeRate`, `CurrencyCode`
- **Rule id** — `sales.single_currency_basis`

### When

aggregating sales across rows that may span more than one CurrencyCode

### Then — do (then)

convert each line to the reporting base currency (Quantity x NetPrice x ExchangeRate) BEFORE summing, and disclose the base currency

### Never — don't (never)

summing NetPrice across mixed currencies as if AUD, CAD, EUR, GBP and USD were one unit — that total is meaningless

Applies to [Sales (net revenue)](../sales.md).