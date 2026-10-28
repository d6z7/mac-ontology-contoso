---
type: Transform
title: 'Cleansing: dim_currency'
description: Cleansing → contoso_served.dim_currency
relation: contoso_served.dim_currency
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/dim_currency.sql
---

Produces `contoso_served.dim_currency` · grain: —

## Rules
## Lineage
- Source: [sales](../sources/sales.md)
- Clean dataset: [dim_currency](../datasets/dim_currency.md)

## SQL realization
Realized by `dim_currency.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.dim_currency` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `currency_code` | `sales.CurrencyCode` |  | passthrough |