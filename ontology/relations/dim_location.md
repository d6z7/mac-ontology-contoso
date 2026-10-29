---
type: Relation
title: dim_location
description: semantic plane · 5 described column(s) · 1 binding concept(s)
tags:
- CONTOSO5
- relation
- semantic-plane
---

What a question may DO with each column of `dim_location` — the SEMANTIC plane of this relation. Its physical facts (types, measured distincts, where its rows live) are on the data-plane page; this says what the columns MEAN.

## Details

- **Schema version** — 0.3.1-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

## Key

- One row is identified by `location_code`.

## Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `location_code` | **key** | — | — | — |
| `country_code` | — | axis `categorical` | — | — |
| `country_name` | — | axis `categorical` | — | label_of `country_code` (long) |
| `state` | — | axis `categorical` | — | finer_than `country_code` |
| `units_ever_here` | — | aggregate precomputed / units · extremum `min`, `max` | — | — |

_Declared per column, over 5 columns: offers 4 of 5 · references 0 of 5 · rulings 2 of 5. An em dash is a column for which nothing is declared._

## Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Location](../concepts/location.md) — serves `location_code`, `country_code`, `country_name`, `state`, `units_ever_here`

## Served as

- Kind — `view` · served by the warehouse.
- The same relation's PHYSICAL page: [`dim_location`](../../data/datasets/dim_location.md)
