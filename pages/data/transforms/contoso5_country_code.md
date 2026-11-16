---
type: Transform
title: 'Cleansing: contoso5_country_code'
description: Cleansing → contoso_served.contoso5_country_code
relation: contoso_served.contoso5_country_code
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_country_code.sql
---

Produces `contoso_served.contoso5_country_code` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_country_code](../datasets/contoso5_country_code.md)

## SQL realization
Realized by `contoso5_country_code.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_country_code` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | `dim_country.country_code` |  | passthrough |
| `label` | `dim_country.country_name` |  | passthrough |