---
type: DQ Issue
title: '`sales` re-delivers every line of `orderrows` — one fact, twice'
description: '223,974 rows each. `sales` carries all but 1 column of `orderrows` (RowNumber
  is spelled differently there), plus 7: CurrencyCode, CustomerKey, DeliveryDate,
  ExchangeRate, LineNumber, OrderDate, Store'
tags:
- CONTOSO5
- severity:medium
- confidence:?
- lifecycle:draft
---

`DQ-DUP-ORDERROWS-SALES` · severity **medium** · confidence **?** · disposition **open — nobody has ruled**

## Finding
223,974 rows each. `sales` carries all but 1 column of `orderrows` (RowNumber is spelled differently there), plus 7: CurrencyCode, CustomerKey, DeliveryDate, ExchangeRate, LineNumber, OrderDate, StoreKey. So `sales` answers at this grain with NO join, and `orderrows` cannot answer at all without a header relation. Only one is served, so the ambiguity is latent rather than live.

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
- [sales](../sources/sales.md)