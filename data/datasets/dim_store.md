---
type: Dataset
title: 'Clean: dim_store'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_store
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `store_key` | integer | PK |  |
| `store_code` | integer | FK | → `dim_location.location_code` |
| `store_name` | string | value |  |
| `country_code` | string | FK | → `dim_country.country_code` |
| `state` | string | value |  |
| `open_date` | date | value |  |
| `close_date` | date | value |  |
| `status_annotation` | string | value |  |
| `square_metres` | integer | value |  |

## Foreign keys

- `store_code` → `dim_location.location_code` (many:one, mandatory:mandatory)
- `country_code` → `dim_country.country_code` (many:one, mandatory:mandatory)

## Referenced by

- `v_contoso5_sales_line.store_key` → `dim_store.store_key`