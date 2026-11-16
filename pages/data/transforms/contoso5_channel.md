---
type: Transform
title: 'Cleansing: contoso5_channel'
description: Cleansing → contoso_served.contoso5_channel
relation: contoso_served.contoso5_channel
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_channel.sql
---

Produces `contoso_served.contoso5_channel` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_channel](../datasets/contoso5_channel.md)

## SQL realization
Realized by `contoso5_channel.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_channel` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | `v_contoso5_sales_line.channel` |  | passthrough |