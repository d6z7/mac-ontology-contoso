---
type: Transform
title: 'Cleansing: contoso5_brand'
description: Cleansing → contoso_served.contoso5_brand
relation: contoso_served.contoso5_brand
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_brand.sql
---

Produces `contoso_served.contoso5_brand` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_brand](../datasets/contoso5_brand.md)

## SQL realization
Realized by `contoso5_brand.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_brand` · kinds: computed

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | _DISTINCT brand_ |  | computed |