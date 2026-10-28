---
type: Relation
title: v_contoso5_sales_line
description: semantic plane · 19 described column(s) · 1 binding concept(s)
tags:
- CONTOSO5
- relation
- semantic-plane
---

What a question may DO with each column of `v_contoso5_sales_line` — the SEMANTIC plane of this relation. Its physical facts (types, measured distincts, where its rows live) are on the data-plane page; this says what the columns MEAN.

## Details

- **Schema version** — 0.3.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

## Key

- One row is identified by `order_key`, `line_number`.

## Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `order_key` | **key** | — | — | — |
| `line_number` | **key** | — | — | — |
| `order_date` | — | axis `time` · extremum `min`, `max` · **binds the period** | — | — |
| `delivery_date` | — | axis `time` · extremum `min`, `max` | — | — |
| `store_key` | — | axis `categorical` | `Store` | — |
| `customer_key` | — | axis `categorical` | `Customer` | — |
| `channel` | — | axis `categorical` | — | — |
| `sale_country_code` | — | axis `categorical` | `Country` | — |
| `product_key` | — | axis `categorical` | `Product` | — |
| `currency_code` | — | axis `categorical` | — | — |
| `gross_amount` | — | aggregate flow / USD · extremum `min`, `max` | — | — |
| `net_amount` | — | aggregate flow / USD · extremum `min`, `max` | — | — |
| `cost_amount` | — | aggregate flow / USD · extremum `min`, `max` | — | — |
| `margin_amount` | — | aggregate flow / USD · extremum `min`, `max` | — | — |
| `discount_amount` | — | aggregate flow / USD · extremum `min`, `max` | — | — |
| `quantity` | — | aggregate flow / units · extremum `min`, `max` | — | — |
| `unit_price` | — | aggregate intensive / USD · extremum `min`, `max` | — | — |
| `net_price` | — | aggregate intensive / USD · extremum `min`, `max` | — | — |
| `unit_cost` | — | aggregate intensive / USD · extremum `min`, `max` | — | — |

_Declared per column, over 19 columns: offers 17 of 19 · references 4 of 19 · rulings 0 of 19. An em dash is a column for which nothing is declared._

## Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Order](../concepts/order.md) — serves `order_key`, `line_number`, `order_date`, `delivery_date`, `customer_key`, `store_key`, `product_key`, `currency_code`, `quantity`, `net_amount`, `gross_amount`, `cost_amount`, `discount_amount`, `margin_amount`, `unit_price`, `net_price`, `unit_cost`

## Served as

- Kind — `view` · served by the warehouse.
- The same relation's PHYSICAL page: [`v_contoso5_sales_line`](../../data/datasets/v_contoso5_sales_line.md)
