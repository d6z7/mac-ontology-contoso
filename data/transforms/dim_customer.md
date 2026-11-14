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
| `customer_key` | `customer."customerkey"` |  | passthrough |
| `continent` | `customer."continent"` |  | passthrough |
| `country_code` | `customer."country"` |  | passthrough |
| `state` | `customer."state"` |  | passthrough |
| `city` | `customer."city"` |  | passthrough |
| `gender` | `customer."gender"` |  | passthrough |
| `birth_date` | `customer."birthday"` → _CAST(c."birthday" AS DATE)_ |  | transform |
| `valid_from` | `customer."startdt"` → _CAST(c."startdt" AS DATE)_ |  | transform |
| `valid_to` | `customer."enddt"` → _CAST(c."enddt" AS DATE)_ |  | transform |
| `customer_name` | _c."givenname" || ' ' || c."surname"_ |  | computed |