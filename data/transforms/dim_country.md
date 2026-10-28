---
type: Transform
title: 'Cleansing: dim_country'
description: Cleansing → contoso_served.dim_country
relation: contoso_served.dim_country
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/dim_country.sql
---

Produces `contoso_served.dim_country` · grain: —

## Rules
## Lineage
- Source: [store](../sources/store.md)
- Clean dataset: [dim_country](../datasets/dim_country.md)

## SQL realization
Realized by `dim_country.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.dim_country` · kinds: passthrough + transform

| output column | ← from | rule | kind |
|---|---|---|---|
| `country_code` | `store.CountryCode` |  | passthrough |
| `country_name` | `store.CountryName` → _any_value(s.CountryName)_ |  | transform |