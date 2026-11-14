---
type: Transform
title: 'Cleansing: contoso5_state'
description: Cleansing → contoso_served.contoso5_state
relation: contoso_served.contoso5_state
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_state.sql
---

Produces `contoso_served.contoso5_state` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_state](../datasets/contoso5_state.md)

## SQL realization
Realized by `contoso5_state.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_state` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | `dim_location.state` |  | passthrough |