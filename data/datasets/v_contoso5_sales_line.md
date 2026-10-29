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

| column | type | role | reference |
|---|---|---|---|
| `order_key` | integer | PK1 |  |
| `line_number` | integer | PK2 |  |
| `order_date` | date | value |  |
| `delivery_date` | date | value |  |
| `customer_key` | integer | FK | → `dim_customer.customer_key` |
| `store_key` | integer | FK | → `dim_store.store_key` |
| `product_key` | integer | FK | → `dim_product.product_key` |
| `channel` | string | value |  |
| `sale_country_code` | string | FK | → `dim_country.country_code` |
| `currency_code` | string | FK | → `dim_currency.currency_code` |
| `quantity` | integer | value |  |
| `net_price` | decimal | value |  |
| `unit_price` | decimal | value |  |
| `unit_cost` | decimal | value |  |
| `net_amount` | decimal | value |  |
| `gross_amount` | decimal | value |  |
| `cost_amount` | decimal | value |  |
| `discount_amount` | decimal | value |  |
| `margin_amount` | decimal | value |  |

## Foreign keys

- `customer_key` → `dim_customer.customer_key` (many:one, mandatory:optional)
- `store_key` → `dim_store.store_key` (many:one, mandatory:optional)
- `product_key` → `dim_product.product_key` (many:one, mandatory:mandatory)
- `sale_country_code` → `dim_country.country_code` (many:one, mandatory:optional)
- `currency_code` → `dim_currency.currency_code` (many:one, mandatory:mandatory)