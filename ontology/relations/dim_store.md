---
type: Relation
title: dim_store
description: semantic plane · 9 described column(s) · 1 binding concept(s)
tags:
- CONTOSO5
- relation
- semantic-plane
---

What a question may DO with each column of `dim_store` — the SEMANTIC plane of this relation. Its physical facts (types, measured distincts, where its rows live) are on the data-plane page; this says what the columns MEAN.

## Details

- **Schema version** — 0.3.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

## Key

- One row is identified by `store_key`.

## Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `store_key` | **key** | — | — | finer_than `store_code` |
| `store_code` | — | — | `Location` | — |
| `store_name` | — | axis `categorical` | — | label_of `store_code` (common) |
| `country_code` | — | axis `categorical` | — | — |
| `state` | — | axis `categorical` | — | — |
| `open_date` | — | axis `time` · extremum `min`, `max` | — | — |
| `close_date` | — | axis `time` · extremum `min`, `max` | — | — |
| `status_annotation` | — | axis `categorical` | — | — |
| `square_metres` | — | aggregate stock / m2 · extremum `min`, `max` | — | — |

_Declared per column, over 9 columns: offers 7 of 9 · references 1 of 9 · rulings 2 of 9. An em dash is a column for which nothing is declared._

## Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Store](../concepts/store.md) — serves `store_key`, `store_code`, `store_name`, `country_code`, `state`, `open_date`, `close_date`, `status_annotation`, `square_metres`

## Served as

- Kind — `view` · served by the warehouse.
- The same relation's PHYSICAL page: [`dim_store`](../../data/datasets/dim_store.md)
