---
type: Transform
title: 'Cleansing: contoso5_status'
description: Cleansing → contoso_served.contoso5_status
relation: contoso_served.contoso5_status
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_status.sql
---

Produces `contoso_served.contoso5_status` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_status](../datasets/contoso5_status.md)

## SQL realization
Realized by `contoso5_status.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_status` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | `dim_store.status_annotation` |  | passthrough |