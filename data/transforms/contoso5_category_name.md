---
type: Transform
title: 'Cleansing: contoso5_category_name'
description: Cleansing → contoso_served.contoso5_category_name
relation: contoso_served.contoso5_category_name
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_category_name.sql
---

Produces `contoso_served.contoso5_category_name` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_category_name](../datasets/contoso5_category_name.md)

## SQL realization
Realized by `contoso5_category_name.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_category_name` · kinds: computed

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | _DISTINCT category_name_ |  | computed |