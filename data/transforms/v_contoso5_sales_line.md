---
type: Transform
title: 'Cleansing: v_contoso5_sales_line'
description: Cleansing → contoso_served.v_contoso5_sales_line
relation: contoso_served.v_contoso5_sales_line
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/v_contoso5_sales_line.sql
---

Produces `contoso_served.v_contoso5_sales_line` · grain: —

## Rules
## Lineage
- Source: [customer](../sources/customer.md)
- Source: [sales](../sources/sales.md)
- Source: [store](../sources/store.md)
- Clean dataset: [v_contoso5_sales_line](../datasets/v_contoso5_sales_line.md)

## SQL realization
Realized by `v_contoso5_sales_line.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.v_contoso5_sales_line` · kinds: computed + passthrough + transform

| output column | ← from | rule | kind |
|---|---|---|---|
| `order_key` | `sales.OrderKey` |  | passthrough |
| `line_number` | `sales.LineNumber` |  | passthrough |
| `order_date` | `sales.OrderDate` → _CAST(s.OrderDate AS DATE)_ |  | transform |
| `delivery_date` | `sales.DeliveryDate` → _CAST(s.DeliveryDate AS DATE)_ |  | transform |
| `customer_key` | `sales.CustomerKey` |  | passthrough |
| `store_key` | `sales.StoreKey` |  | passthrough |
| `product_key` | `sales.ProductKey` |  | passthrough |
| `channel` | `sales.StoreKey` → _CASE WHEN ((s.StoreKey = 999999)) THEN ('online') ELSE 'physical' END_ |  | transform |
| `currency_code` | `sales.CurrencyCode` |  | passthrough |
| `quantity` | `sales.Quantity` |  | passthrough |
| `net_price` | `sales.NetPrice` |  | passthrough |
| `unit_price` | `sales.UnitPrice` |  | passthrough |
| `unit_cost` | `sales.UnitCost` |  | passthrough |
| `sale_country_code` | _CASE WHEN ((s.StoreKey = 999999)) THEN ((SELECT c.Country FROM main.customer AS c WHERE (c.CustomerKey = s.CustomerKey))) ELSE (SELECT st.CountryCode FROM main._ |  | computed |
| `net_amount` | _(s.Quantity * s.NetPrice)_ |  | computed |
| `gross_amount` | _(s.Quantity * s.UnitPrice)_ |  | computed |
| `cost_amount` | _(s.Quantity * s.UnitCost)_ |  | computed |
| `discount_amount` | _(s.Quantity * (s.UnitPrice - s.NetPrice))_ |  | computed |
| `margin_amount` | _(s.Quantity * (s.NetPrice - s.UnitCost))_ |  | computed |