---
type: Source
title: store
description: The data as it lands — address `main`
resource: source://main/store
tags:
- Contoso 5
- source
---

- **Address** — `main` — its key in the connection's source map; transform SQL names the raw table only through it.
- **Account** — [`data/sources/store.md`](../../../data/sources/store.md) — the source's documentation (Y-4), authored; this page cites it and never writes it.

## Columns

| column | distinct | nulls | min | max |
|---|---:|---:|---|---|
| `StoreKey` | 74 | 0 | 10 | 999999 |
| `StoreCode` | 67 | 0 | -1 | 67 |
| `GeoAreaKey` | 67 | 0 | -1 | 616 |
| `CountryCode` | 9 | 0 | — | — |
| `CountryName` | 9 | 0 | — | — |
| `State` | 67 | 0 | — | — |
| `OpenDate` | 32 | 0 | 2005-03-04 00:00:00 | 2019-03-05 00:00:00 |
| `CloseDate` | 15 | 58 | 2013-12-05 00:00:00 | 2019-11-03 00:00:00 |
| `Description` | 67 | 0 | — | — |
| `SquareMeters` | 39 | 1 | 245 | 3500 |
| `Status` | 3 | 1 | — | — |

_Measured (`data/profiles/store.yaml`, 2026-11-18T03:16:04.582+01:00); a v3 source declares no columns._

## Read by

- [dim_country](../transforms/dim_country.md) — its SQL names this source
- [dim_location](../transforms/dim_location.md) — its SQL names this source
- [dim_store](../transforms/dim_store.md) — its SQL names this source
- [v_contoso5_sales_line](../transforms/v_contoso5_sales_line.md) — its SQL names this source

## Findings

_No finding or rule names this source._
