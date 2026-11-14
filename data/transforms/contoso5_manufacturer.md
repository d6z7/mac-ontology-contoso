---
type: Transform
title: 'Cleansing: contoso5_manufacturer'
description: Cleansing → contoso_served.contoso5_manufacturer
relation: contoso_served.contoso5_manufacturer
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_manufacturer.sql
---

Produces `contoso_served.contoso5_manufacturer` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_manufacturer](../datasets/contoso5_manufacturer.md)

## SQL realization
Realized by `contoso5_manufacturer.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_manufacturer` · kinds: computed

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | _DISTINCT manufacturer_ |  | computed |