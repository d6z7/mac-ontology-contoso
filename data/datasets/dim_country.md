---
type: Dataset
title: 'Clean: dim_country'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_country
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `country_code` | string | PK · FK | → `contoso5_country_code.code` |
| `country_name` | string | value |  |

## Foreign keys

- `country_code` → `contoso5_country_code.code`

## Referenced by

- `dim_customer.country_code` → `dim_country.country_code`
- `dim_location.country_code` → `dim_country.country_code`
- `dim_store.country_code` → `dim_country.country_code`
- `v_contoso5_sales_line.sale_country_code` → `dim_country.country_code`