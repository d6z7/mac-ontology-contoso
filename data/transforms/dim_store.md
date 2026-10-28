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
| `store_key` | `store.StoreKey` |  | passthrough |
| `store_code` | `store.StoreCode` |  | passthrough |
| `store_name` | `store.Description` |  | passthrough |
| `country_code` | `store.CountryCode` |  | passthrough |
| `state` | `store.State` |  | passthrough |
| `open_date` | `store.OpenDate` → _CAST(s.OpenDate AS DATE)_ |  | transform |
| `close_date` | `store.CloseDate` → _CAST(s.CloseDate AS DATE)_ |  | transform |
| `square_metres` | `store.SquareMeters` |  | passthrough |
| `status_annotation` | _CASE WHEN ((s.CloseDate IS NULL)) THEN (s.Status) WHEN (("nullif"("trim"(s.Status), '') IS NOT NULL)) THEN (s.Status) WHEN (EXISTS(SELECT 1 FROM main.store AS l_ |  | computed |