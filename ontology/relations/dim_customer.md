---
type: Relation
title: dim_customer
description: semantic plane · 10 described column(s) · 1 binding concept(s)
tags:
- CONTOSO5
- relation
- semantic-plane
---

What a question may DO with each column of `dim_customer` — the SEMANTIC plane of this relation. Its physical facts (types, measured distincts, where its rows live) are on the data-plane page; this says what the columns MEAN.

## Details

- **Schema version** — 0.3.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

## Key

- One row is identified by `customer_key`.

## Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `customer_key` | **key** | — | — | — |
| `customer_name` | — | axis `categorical` · suppressed `DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME` | — | label_of `customer_key` (common) |
| `continent` | — | axis `categorical` | — | — |
| `country_code` | — | axis `categorical` | — | finer_than `continent` |
| `state` | — | axis `categorical` | — | scoped_by `country_code` |
| `city` | — | axis `categorical` · suppressed `DQ-IDENTIFYING-DIM_CUSTOMER-CITY` | — | — |
| `gender` | — | axis `categorical` | — | — |
| `birth_date` | — | axis `time` · extremum `min`, `max` | — | — |
| `valid_from` | — | — | — | — |
| `valid_to` | — | — | — | — |

_Declared per column, over 10 columns: offers 7 of 10 · references 0 of 10 · rulings 3 of 10. An em dash is a column for which nothing is declared._

## Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Customer](../concepts/customer.md) — serves `customer_key`, `customer_name`, `continent`, `country_code`, `state`, `city`, `gender`, `birth_date`, `valid_from`, `valid_to`

## Served as

- Kind — `view` · served by the warehouse.
- The same relation's PHYSICAL page: [`dim_customer`](../../data/datasets/dim_customer.md)
