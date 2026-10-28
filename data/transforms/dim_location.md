---
type: Transform
title: 'Cleansing: dim_location'
description: Cleansing → contoso_served.dim_location
relation: contoso_served.dim_location
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/dim_location.sql
---

Produces `contoso_served.dim_location` · grain: —

## Rules
## Lineage
- Source: [store](../sources/store.md)
- Clean dataset: [dim_location](../datasets/dim_location.md)

## SQL realization
Realized by `dim_location.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.dim_location` · kinds: computed + passthrough + transform

| output column | ← from | rule | kind |
|---|---|---|---|
| `location_code` | `store.StoreCode` |  | passthrough |
| `country_code` | `store.CountryCode` → _any_value(s.CountryCode)_ |  | transform |
| `country_name` | `store.CountryName` → _any_value(s.CountryName)_ |  | transform |
| `state` | `store.State` → _any_value(s.State)_ |  | transform |
| `units_ever_here` | _count_star()_ |  | computed |