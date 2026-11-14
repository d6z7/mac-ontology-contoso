---
type: Transform
title: 'Cleansing: contoso5_continent'
description: Cleansing → contoso_served.contoso5_continent
relation: contoso_served.contoso5_continent
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_continent.sql
---

Produces `contoso_served.contoso5_continent` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_continent](../datasets/contoso5_continent.md)

## SQL realization
Realized by `contoso5_continent.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_continent` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | `dim_customer.continent` |  | passthrough |