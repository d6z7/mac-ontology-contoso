---
type: Transform
title: 'Cleansing: contoso5_color'
description: Cleansing → contoso_served.contoso5_color
relation: contoso_served.contoso5_color
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_color.sql
---

Produces `contoso_served.contoso5_color` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_color](../datasets/contoso5_color.md)

## SQL realization
Realized by `contoso5_color.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_color` · kinds: computed

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | _DISTINCT color_ |  | computed |