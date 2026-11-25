---
type: Source
title: orderrows
description: The data as it lands — address `main`
resource: source://main/orderrows
tags:
- Contoso 5
- source
---

- **Address** — `main` — its key in the connection's source map; transform SQL names the raw table only through it.
- **Account** — [`data/sources/orderrows.md`](../../../data/sources/orderrows.md) — the source's documentation (Y-4), authored; this page cites it and never writes it.

## Columns

| column | distinct | nulls | min | max |
|---|---:|---:|---|---|
| `OrderKey` | 93470 | 0 | 139000 | 3653084 |
| `RowNumber` | 7 | 0 | 0 | 6 |
| `ProductKey` | 2517 | 0 | 1 | 2517 |
| `Quantity` | 10 | 0 | 1 | 10 |
| `UnitPrice` | 1760 | 0 | 0.95000 | 6247.50000 |
| `NetPrice` | 18407 | 0 | 0.81700 | 6247.50000 |
| `UnitCost` | 1955 | 0 | 0.48000 | 2069.92500 |

_Measured (`data/profiles/orderrows.yaml`, 2026-11-18T03:16:03.714+01:00); a v3 source declares no columns._

## Read by

_No transform's SQL names this source._

## Findings

- [DQ-DUP-ORDERROWS-SALES](../quality/DQ-DUP-ORDERROWS-SALES.md) — medium · open — nobody has ruled — `sales` re-delivers every line of `orderrows` — one fact, twice
- [DQ-ORPHAN-ORDERROWS](../quality/DQ-ORPHAN-ORDERROWS.md) — medium · open — nobody has ruled — raw landing `orderrows` is consumed by no transformation
