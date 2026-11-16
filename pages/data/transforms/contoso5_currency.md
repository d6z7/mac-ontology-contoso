---
type: Transform
title: 'Cleansing: contoso5_currency'
description: Cleansing → contoso_served.contoso5_currency
relation: contoso_served.contoso5_currency
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_currency.sql
---

Produces `contoso_served.contoso5_currency` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_currency](../datasets/contoso5_currency.md)

## SQL realization
Realized by `contoso5_currency.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_currency` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | `dim_currency.currency_code` |  | passthrough |