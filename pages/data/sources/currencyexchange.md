---
type: Source
title: currencyexchange
description: The data as it lands — address `main`
resource: source://main/currencyexchange
tags:
- Contoso 5
- source
---

- **Address** — `main` — its key in the connection's source map; transform SQL names the raw table only through it.
- **Account** — [`data/sources/currencyexchange.md`](../../../data/sources/currencyexchange.md) — the source's documentation (Y-4), authored; this page cites it and never writes it.

## Columns

| column | distinct | nulls | min | max |
|---|---:|---:|---|---|
| `Date` | 4018 | 0 | 2016-01-01 00:00:00 | 2026-12-31 00:00:00 |
| `FromCurrency` | 5 | 0 | — | — |
| `ToCurrency` | 5 | 0 | — | — |
| `Exchange` | 31512 | 0 | 0.47908 | 2.08733 |

_Measured (`data/profiles/currencyexchange.yaml`, 2026-11-18T03:16:02.987+01:00); a v3 source declares no columns._

## Read by

- [v_contoso5_fx_rate](../transforms/v_contoso5_fx_rate.md) — its SQL names this source

## Findings

- [DQ-AMBIGREF-CURRENCYCODE](../quality/DQ-AMBIGREF-CURRENCYCODE.md) — high · open — nobody has ruled — `CurrencyCode` includes perfectly into 2 different keys — which is THE reference?
