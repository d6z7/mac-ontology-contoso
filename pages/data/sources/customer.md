---
type: Source
title: customer
description: The data as it lands — address `main`
resource: source://main/customer
tags:
- Contoso 5
- source
---

- **Address** — `main` — its key in the connection's source map; transform SQL names the raw table only through it.
- **Account** — [`data/sources/customer.md`](../../../data/sources/customer.md) — the source's documentation (Y-4), authored; this page cites it and never writes it.

## Columns

| column | distinct | nulls | min | max |
|---|---:|---:|---|---|
| `CustomerKey` | 104990 | 0 | 15 | 2099743 |
| `GeoAreaKey` | 608 | 0 | 1 | 616 |
| `StartDT` | 11305 | 0 | 1980-01-01 00:00:00 | 2010-12-30 00:00:00 |
| `EndDT` | 14711 | 0 | 2005-01-01 00:00:00 | 2045-12-30 00:00:00 |
| `Continent` | 3 | 0 | — | — |
| `Gender` | 2 | 0 | — | — |
| `Title` | 4 | 0 | — | — |
| `GivenName` | 9294 | 0 | — | — |
| `MiddleInitial` | 37 | 0 | — | — |
| `Surname` | 20325 | 0 | — | — |
| `StreetAddress` | 95854 | 0 | — | — |
| `City` | 34581 | 0 | — | — |
| `State` | 565 | 0 | — | — |
| `StateFull` | 610 | 0 | — | — |
| `ZipCode` | 40639 | 0 | — | — |
| `Country` | 8 | 0 | — | — |
| `CountryFull` | 8 | 0 | — | — |
| `Birthday` | 24147 | 0 | 1935-02-04 00:00:00 | 2002-02-20 00:00:00 |
| `Age` | 67 | 0 | 19 | 85 |
| `Occupation` | 2571 | 0 | — | — |
| `Company` | 1031 | 0 | — | — |
| `Vehicle` | 11760 | 0 | — | — |
| `Latitude` | 102773 | 0 | -43.34649 | 76.47497 |
| `Longitude` | 103894 | 0 | -170.22205 | 159.03845 |

_Measured (`data/profiles/customer.yaml`, 2026-11-18T03:16:03.274+01:00); a v3 source declares no columns._

## Read by

- [dim_customer](../transforms/dim_customer.md) — its SQL names this source
- [v_contoso5_sales_line](../transforms/v_contoso5_sales_line.md) — its SQL names this source

## Findings

- [DQ-DANGLINGKEY-GEOAREAKEY](../quality/DQ-DANGLINGKEY-GEOAREAKEY.md) — medium · open — nobody has ruled — `GeoAreaKey` is key-shaped and no relation in scope carries it as a key
