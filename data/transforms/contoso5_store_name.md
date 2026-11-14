---
type: Transform
title: 'Cleansing: contoso5_store_name'
description: Cleansing → contoso_served.contoso5_store_name
relation: contoso_served.contoso5_store_name
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_store_name.sql
---

Produces `contoso_served.contoso5_store_name` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_store_name](../datasets/contoso5_store_name.md)

## SQL realization
Realized by `contoso5_store_name.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_store_name` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | `dim_store.store_name` |  | passthrough |