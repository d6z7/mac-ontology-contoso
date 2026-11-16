---
type: Index
title: CONTOSO5 landing plane
tags:
- CONTOSO5
- sources
- overview
---


8 relation(s) · 753,467 row(s) measured · 96 column(s) · 0 declared reference(s) · 0 register pointer(s)

| relation | rows | columns | key | references | registers |
|---|---:|---:|---|---:|---:|
| [currencyexchange](currencyexchange.md) | 100450 | 4 | `Date` + `FromCurrency` + `ToCurrency` | 0 | 0 |
| [customer](customer.md) | 104990 | 24 | `CustomerKey` | 0 | 0 |
| [date](date.md) | 4018 | 17 | `Date` | 0 | 0 |
| [orderrows](orderrows.md) | 223974 | 7 | `OrderKey` + `RowNumber` | 0 | 0 |
| [orders](orders.md) | 93470 | 6 | `OrderKey` | 0 | 0 |
| [product](product.md) | 2517 | 14 | `ProductKey` | 0 | 0 |
| [sales](sales.md) | 223974 | 13 | `OrderKey` + `LineNumber` | 0 | 0 |
| [store](store.md) | 74 | 11 | `StoreKey` | 0 | 0 |
