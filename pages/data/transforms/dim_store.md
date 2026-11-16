---
type: Transform
title: 'Cleansing: dim_store'
description: Cleansing → contoso_served.dim_store
relation: contoso_served.dim_store
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/dim_store.sql
---

Produces `contoso_served.dim_store` · grain: —

## Rules
## Lineage
- Source: [store](../sources/store.md)
- Clean dataset: [dim_store](../datasets/dim_store.md)

## SQL realization
Realized by `dim_store.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.dim_store` · kinds: computed + passthrough + transform

| output column | ← from | rule | kind |
|---|---|---|---|
| `store_key` | `store."storekey"` |  | passthrough |
| `store_code` | `store."storecode"` |  | passthrough |
| `store_name` | `store."description"` |  | passthrough |
| `country_code` | `store."countrycode"` |  | passthrough |
| `state` | `store."state"` |  | passthrough |
| `open_date` | `store."opendate"` → _CAST(s."opendate" AS DATE)_ |  | transform |
| `close_date` | `store."closedate"` → _CAST(s."closedate" AS DATE)_ |  | transform |
| `square_metres` | `store."squaremeters"` |  | passthrough |
| `status_annotation` | _CASE WHEN s."closedate" IS NULL THEN s."status" WHEN NOT NULLIF(TRIM(s."status"), '') IS NULL THEN s."status" WHEN EXISTS(SELECT 1 AS "1" FROM main.store AS l W_ |  | computed |