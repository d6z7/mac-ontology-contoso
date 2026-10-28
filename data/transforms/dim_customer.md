---
type: Transform
title: 'Cleansing: dim_customer'
description: Cleansing → contoso_served.dim_customer
relation: contoso_served.dim_customer
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/dim_customer.sql
---

Produces `contoso_served.dim_customer` · grain: —

## Rules
## Lineage
- Source: [customer](../sources/customer.md)
- Clean dataset: [dim_customer](../datasets/dim_customer.md)

## SQL realization
Realized by `dim_customer.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.dim_customer` · kinds: computed + passthrough + transform

| output column | ← from | rule | kind |
|---|---|---|---|
| `customer_key` | `customer.CustomerKey` |  | passthrough |
| `continent` | `customer.Continent` |  | passthrough |
| `country_code` | `customer.Country` |  | passthrough |
| `state` | `customer.State` |  | passthrough |
| `city` | `customer.City` |  | passthrough |
| `gender` | `customer.Gender` |  | passthrough |
| `birth_date` | `customer.Birthday` → _CAST(c.Birthday AS DATE)_ |  | transform |
| `valid_from` | `customer.StartDT` → _CAST(c.StartDT AS DATE)_ |  | transform |
| `valid_to` | `customer.EndDT` → _CAST(c.EndDT AS DATE)_ |  | transform |
| `customer_name` | _((c.GivenName || ' ') || c.Surname)_ |  | computed |