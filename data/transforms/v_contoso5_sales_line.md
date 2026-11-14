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
| `order_key` | `sales."orderkey"` |  | passthrough |
| `line_number` | `sales."linenumber"` |  | passthrough |
| `order_date` | `sales."orderdate"` → _CAST(s."orderdate" AS DATE)_ |  | transform |
| `delivery_date` | `sales."deliverydate"` → _CAST(s."deliverydate" AS DATE)_ |  | transform |
| `customer_key` | `sales."customerkey"` |  | passthrough |
| `store_key` | `sales."storekey"` |  | passthrough |
| `product_key` | `sales."productkey"` |  | passthrough |
| `channel` | `sales."storekey"` → _CASE WHEN s."storekey" = 999999 THEN 'online' ELSE 'physical' END_ |  | transform |
| `currency_code` | `sales."currencycode"` |  | passthrough |
| `quantity` | `sales."quantity"` |  | passthrough |
| `net_price` | `sales."netprice"` |  | passthrough |
| `unit_price` | `sales."unitprice"` |  | passthrough |
| `unit_cost` | `sales."unitcost"` |  | passthrough |
| `sale_country_code` | _CASE WHEN s."storekey" = 999999 THEN (SELECT c."country" AS "country" FROM main.customer AS c WHERE c."customerkey" = s."customerkey") ELSE (SELECT st."countryc_ |  | computed |
| `net_amount` | _s."quantity" * s."netprice"_ |  | computed |
| `gross_amount` | _s."quantity" * s."unitprice"_ |  | computed |
| `cost_amount` | _s."quantity" * s."unitcost"_ |  | computed |
| `discount_amount` | _s."quantity" * (s."unitprice" - s."netprice")_ |  | computed |
| `margin_amount` | _s."quantity" * (s."netprice" - s."unitcost")_ |  | computed |