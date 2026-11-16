---
type: Dataset
title: 'Clean: v_contoso5_fx_rate'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.v_contoso5_fx_rate
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `date_day` | date | PK1 |
| `from_currency` | string | PK2 · FK |
| `to_currency` | string | PK3 · FK |
| `rate` | decimal | value |

## Foreign keys

- `from_currency` → `dim_currency.currency_code` (many:one, mandatory:mandatory)
- `to_currency` → `dim_currency.currency_code` (many:one, mandatory:mandatory)

## What a question may do

### Details

- **Schema version** — 0.4.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

### Key

- One row is identified by `date_day`, `from_currency`, `to_currency`.

### Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `date_day` | **key** | axis `time` | — | — |
| `from_currency` | **key** | axis `categorical` | — | — |
| `to_currency` | **key** | axis `categorical` | — | scoped_by `from_currency` |
| `rate` | — | aggregate intensive / to-currency per from-currency · extremum `min`, `max` | — | — |

_Declared per column, over 4 columns: offers 4 of 4 · references 0 of 4 · rulings 1 of 4. An em dash is a column for which nothing is declared._

### Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Exchange Rate](../concepts/exchange_rate.md) — serves `date_day`, `from_currency`, `to_currency`, `rate`
