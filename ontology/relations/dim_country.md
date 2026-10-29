---
type: Relation
title: dim_country
description: semantic plane · 2 described column(s) · 1 binding concept(s)
tags:
- CONTOSO5
- relation
- semantic-plane
---

What a question may DO with each column of `dim_country` — the SEMANTIC plane of this relation. Its physical facts (types, measured distincts, where its rows live) are on the data-plane page; this says what the columns MEAN.

## Details

- **Schema version** — 0.3.1-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

## Key

- One row is identified by `country_code`.

## Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `country_code` | **key** | — | — | — |
| `country_name` | — | axis `categorical` | — | label_of `country_code` (long) |

_Declared per column, over 2 columns: offers 1 of 2 · references 0 of 2 · rulings 1 of 2. An em dash is a column for which nothing is declared._

## Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Country](../concepts/country.md) — serves `country_code`, `country_name`

## Served as

- Kind — `view` · served by the warehouse.
- The same relation's PHYSICAL page: [`dim_country`](../../data/datasets/dim_country.md)
