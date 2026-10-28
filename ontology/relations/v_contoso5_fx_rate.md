---
type: Relation
title: v_contoso5_fx_rate
description: semantic plane · 4 described column(s) · 1 binding concept(s)
tags:
- CONTOSO5
- relation
- semantic-plane
---

What a question may DO with each column of `v_contoso5_fx_rate` — the SEMANTIC plane of this relation. Its physical facts (types, measured distincts, where its rows live) are on the data-plane page; this says what the columns MEAN.

## Details

- **Schema version** — 0.3.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

## Key

- One row is identified by `date_day`, `from_currency`, `to_currency`.

## Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `date_day` | **key** | axis `time` | — | — |
| `from_currency` | **key** | axis `categorical` | — | — |
| `to_currency` | **key** | axis `categorical` | — | — |
| `rate` | — | aggregate intensive / to-currency per from-currency · extremum `min`, `max` | — | — |

_Declared per column, over 4 columns: offers 4 of 4 · references 0 of 4 · rulings 0 of 4. An em dash is a column for which nothing is declared._

## Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Exchange Rate](../concepts/exchange_rate.md) — serves `date_day`, `from_currency`, `to_currency`, `rate`

## Served as

- Kind — `view` · served by the warehouse.
- The same relation's PHYSICAL page: [`v_contoso5_fx_rate`](../../data/datasets/v_contoso5_fx_rate.md)
