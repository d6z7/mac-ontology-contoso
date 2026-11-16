---
type: Dataset
title: 'Clean: v_contoso5_sales_line'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.v_contoso5_sales_line
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `order_key` | integer | PK1 |
| `line_number` | integer | PK2 |
| `order_date` | date | value |
| `delivery_date` | date | value |
| `customer_key` | integer | FK |
| `store_key` | integer | FK |
| `product_key` | integer | FK |
| `channel` | string | value |
| `sale_country_code` | string | FK |
| `currency_code` | string | FK |
| `unit_currency` | string | value |
| `quantity` | integer | value |
| `net_price` | decimal | value |
| `unit_price` | decimal | value |
| `unit_cost` | decimal | value |
| `net_amount` | decimal | value |
| `gross_amount` | decimal | value |
| `cost_amount` | decimal | value |
| `discount_amount` | decimal | value |
| `margin_amount` | decimal | value |

## Foreign keys

- `customer_key` → `dim_customer.customer_key` (many:one, mandatory:optional)
- `store_key` → `dim_store.store_key` (many:one, mandatory:optional)
- `product_key` → `dim_product.product_key` (many:one, mandatory:mandatory)
- `sale_country_code` → `dim_country.country_code` (many:one, mandatory:optional)
- `currency_code` → `dim_currency.currency_code` (many:one, mandatory:mandatory)

## What a question may do

### Details

- **Schema version** — 0.4.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

### Key

- One row is identified by `order_key`, `line_number`.

### Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `order_key` | **key** | — | — | — |
| `line_number` | **key** | — | — | — |
| `order_date` | — | axis `time` · extremum `min`, `max` · **binds the period** · anchor: `latest` | — | — |
| `delivery_date` | — | axis `time` · extremum `min`, `max` | — | — |
| `customer_key` | — | axis `categorical` | `Customer` | — |
| `store_key` | — | axis `categorical` | `Store` | — |
| `product_key` | — | axis `categorical` | `Product` | — |
| `channel` | — | axis `categorical` | — | — |
| `sale_country_code` | — | axis `categorical` | `Country` | — |
| `currency_code` | — | axis `categorical` | — | — |
| `unit_currency` | — | — | — | — |
| `quantity` | — | aggregate flow / units · extremum `min`, `max` | — | — |
| `net_price` | — | aggregate intensive / USD · extremum `min`, `max` | — | — |
| `unit_price` | — | aggregate intensive / USD · extremum `min`, `max` | — | — |
| `unit_cost` | — | aggregate intensive / USD · extremum `min`, `max` | — | — |
| `net_amount` | — | aggregate flow / USD / **default** · extremum `min`, `max` | — | — |
| `gross_amount` | — | aggregate flow / USD · extremum `min`, `max` | — | — |
| `cost_amount` | — | aggregate flow / USD · extremum `min`, `max` | — | — |
| `discount_amount` | — | aggregate flow / USD · extremum `min`, `max` | — | — |
| `margin_amount` | — | aggregate flow / USD · extremum `min`, `max` | — | — |

_Declared per column, over 20 columns: offers 17 of 20 · references 4 of 20 · rulings 0 of 20. An em dash is a column for which nothing is declared._

### Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Order](../concepts/order.md) — serves `order_key`, `line_number`, `order_date`, `delivery_date`, `customer_key`, `store_key`, `product_key`, `currency_code`, `quantity`, `net_amount`, `gross_amount`, `cost_amount`, `discount_amount`, `margin_amount`, `unit_price`, `net_price`, `unit_cost`
