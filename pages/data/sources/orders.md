---
type: Source
title: orders
description: The data as it lands — address `main`
resource: source://main/orders
tags:
- Contoso 5
- source
---

- **Address** — `main` — its key in the connection's source map; transform SQL names the raw table only through it.
- **Account** — [`data/sources/orders.md`](../../../data/sources/orders.md) — the source's documentation (Y-4), authored; this page cites it and never writes it.

## Columns

| column | distinct | nulls | min | max |
|---|---:|---:|---|---|
| `OrderKey` | 93470 | 0 | 139000 | 3653084 |
| `CustomerKey` | 52189 | 0 | 15 | 2099697 |
| `StoreKey` | 64 | 0 | 10 | 999999 |
| `DT` | 3450 | 0 | 2016-05-18 00:00:00 | 2025-12-31 00:00:00 |
| `DeliveryDate` | 3498 | 0 | 2016-05-18 00:00:00 | 2026-01-06 00:00:00 |
| `CurrencyCode` | 5 | 0 | — | — |

_Measured (`data/profiles/orders.yaml`, 2026-10-26T16:40:51+01:00); a v3 source declares no columns._

## Read by

_No transform's SQL names this source._

## Findings

- [DQ-ORPHAN-ORDERS](../quality/DQ-ORPHAN-ORDERS.md) — medium · open — nobody has ruled — raw landing `orders` is consumed by no transformation
