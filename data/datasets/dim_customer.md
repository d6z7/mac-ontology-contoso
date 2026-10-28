---
type: Dataset
title: 'Clean: dim_customer'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_customer
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `customer_key` | integer | PK |  |
| `customer_name` | string | value | search: `like` |
| `continent` | string | value |  |
| `country_code` | string | FK | → `dim_country.country_code` |
| `state` | string | value |  |
| `city` | string | value | search: `like` |
| `gender` | string | value |  |
| `birth_date` | date | value |  |
| `valid_from` | date | value |  |
| `valid_to` | date | value |  |

## Foreign keys

- `country_code` → `dim_country.country_code` (many:one, mandatory:optional)

## Referenced by

- `v_contoso5_sales_line.customer_key` → `dim_customer.customer_key`