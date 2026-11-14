---
type: Transform
title: 'Cleansing: contoso5_gender'
description: Cleansing → contoso_served.contoso5_gender
relation: contoso_served.contoso5_gender
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/contoso5_gender.sql
---

Produces `contoso_served.contoso5_gender` · grain: —

## Rules
## Lineage
- Clean dataset: [contoso5_gender](../datasets/contoso5_gender.md)

## SQL realization
Realized by `contoso5_gender.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.contoso5_gender` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `code` | `dim_customer.gender` |  | passthrough |