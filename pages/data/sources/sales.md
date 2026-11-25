---
type: Source
title: sales
description: The data as it lands — address `main`
resource: source://main/sales
tags:
- Contoso 5
- source
---

- **Address** — `main` — its key in the connection's source map; transform SQL names the raw table only through it.
- **Account** — [`data/sources/sales.md`](../../../data/sources/sales.md) — the source's documentation (Y-4), authored; this page cites it and never writes it.

## Columns

| column | distinct | nulls | min | max |
|---|---:|---:|---|---|
| `OrderKey` | 93470 | 0 | 139000 | 3653084 |
| `LineNumber` | 7 | 0 | 0 | 6 |
| `OrderDate` | 3450 | 0 | 2016-05-18 00:00:00 | 2025-12-31 00:00:00 |
| `DeliveryDate` | 3498 | 0 | 2016-05-18 00:00:00 | 2026-01-06 00:00:00 |
| `CustomerKey` | 52189 | 0 | 15 | 2099697 |
| `StoreKey` | 64 | 0 | 10 | 999999 |
| `ProductKey` | 2517 | 0 | 1 | 2517 |
| `Quantity` | 10 | 0 | 1 | 10 |
| `UnitPrice` | 1760 | 0 | 0.95000 | 6247.50000 |
| `NetPrice` | 18407 | 0 | 0.81700 | 6247.50000 |
| `UnitCost` | 1955 | 0 | 0.48000 | 2069.92500 |
| `CurrencyCode` | 5 | 0 | — | — |
| `ExchangeRate` | 5862 | 0 | 0.67253 | 1.72530 |

_Measured (`data/profiles/sales.yaml`, 2026-11-18T03:16:04.376+01:00); a v3 source declares no columns._

## Read by

- [dim_currency](../transforms/dim_currency.md) — its SQL names this source
- [v_contoso5_sales_line](../transforms/v_contoso5_sales_line.md) — its SQL names this source

## Findings

_No finding or rule names this source._
