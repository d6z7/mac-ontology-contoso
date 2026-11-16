---
type: Event
title: Order
description: One customer's purchase on one date, counted by distinct `order_key`
  over the line relation.
tags:
- CONTOSO5
- event
- confidence:C
timestamp: '2026-09-30'
---

# Order

One customer's purchase on one date, counted by distinct `order_key` over the line relation. It is also THE FACT NODE of the sales line, one row per order line - every money and quantity measure (net, gross, cost, discount, margin, units, and the per-unit prices) is a column it serves, and every edge from the sale to a dimension starts here. The account is knowledge/order.md.

## Relationships

- **order__converts_at__exchange_rate** → [ExchangeRate](/ExchangeRate.md) (cardinality 1; grounded join `v_contoso5_sales_line.order_date = v_contoso5_fx_rate.date_day AND v_contoso5_sales_line.currency_code = v_contoso5_fx_rate.to_currency AND v_contoso5_fx_rate.from_currency = 'USD'`)
- **order__attributed_to__country** → [Country](/Country.md) (cardinality 1; grounded join `v_contoso5_sales_line.sale_country_code = dim_country.country_code`)
- **order__placed_by__customer** → [Customer](/Customer.md) (cardinality 1; grounded join `v_contoso5_sales_line.customer_key = dim_customer.customer_key`)
- **order__placed_at__store** → [Store](/Store.md) (cardinality 1; grounded join `v_contoso5_sales_line.store_key = dim_store.store_key`)
- **order__paid_in__currency** → [Currency](/Currency.md) (cardinality 1; grounded join `v_contoso5_sales_line.currency_code = dim_currency.currency_code`)
- **order__of__product** → [Product](/Product.md) (cardinality 0..N; grounded join `v_contoso5_sales_line.product_key = dim_product.product_key`)

# Citations

1. MAC concept source of record: `concepts/order.yaml` (schema_version 0.3.0-develop, confidence C).
