---
type: Source
title: product
description: The data as it lands — address `main`
resource: source://main/product
tags:
- Contoso 5
- source
---

- **Address** — `main` — its key in the connection's source map; transform SQL names the raw table only through it.
- **Account** — [`data/sources/product.md`](../../../data/sources/product.md) — the source's documentation (Y-4), authored; this page cites it and never writes it.

## Columns

| column | distinct | nulls | min | max |
|---|---:|---:|---|---|
| `ProductKey` | 2517 | 0 | 1 | 2517 |
| `ProductCode` | 2517 | 0 | — | — |
| `ProductName` | 2517 | 0 | — | — |
| `Manufacturer` | 11 | 0 | — | — |
| `Brand` | 11 | 0 | — | — |
| `Color` | 17 | 0 | — | — |
| `WeightUnit` | 4 | 0 | — | — |
| `Weight` | 296 | 284 | 0.17000 | 239.00000 |
| `Cost` | 480 | 0 | 0.48000 | 1060.22000 |
| `Price` | 426 | 0 | 0.95000 | 3199.99000 |
| `CategoryKey` | 8 | 0 | 1 | 8 |
| `CategoryName` | 8 | 0 | — | — |
| `SubCategoryKey` | 32 | 0 | 101 | 808 |
| `SubCategoryName` | 32 | 0 | — | — |

_Measured (`data/profiles/product.yaml`, 2026-11-18T03:16:04.145+01:00); a v3 source declares no columns._

## Read by

- [dim_product](../transforms/dim_product.md) — its SQL names this source

## Findings

- [DQ-DANGLINGKEY-CATEGORYKEY](../quality/DQ-DANGLINGKEY-CATEGORYKEY.md) — medium · open — nobody has ruled — `CategoryKey` is key-shaped and no relation in scope carries it as a key
- [DQ-DANGLINGKEY-SUBCATEGORYKEY](../quality/DQ-DANGLINGKEY-SUBCATEGORYKEY.md) — medium · open — nobody has ruled — `SubCategoryKey` is key-shaped and no relation in scope carries it as a key
