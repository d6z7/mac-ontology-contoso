---
type: Relation
title: dim_currency
description: semantic plane · 1 described column(s) · 1 binding concept(s)
tags:
- CONTOSO5
- relation
- semantic-plane
---

What a question may DO with each column of `dim_currency` — the SEMANTIC plane of this relation. Its physical facts (types, measured distincts, where its rows live) are on the data-plane page; this says what the columns MEAN.

## Details

- **Schema version** — 0.3.1-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

## Key

- One row is identified by `currency_code`.

## Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `currency_code` | **key** | — | — | — |

_Declared per column, over 1 column: offers 0 of 1 · references 0 of 1 · rulings 0 of 1. An em dash is a column for which nothing is declared._

## Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Currency](../concepts/currency.md) — serves `currency_code`

## Served as

- Kind — `view` · served by the warehouse.
- The same relation's PHYSICAL page: [`dim_currency`](../../data/datasets/dim_currency.md)
