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
| `country_code` | string | PK |  |
| `country_name` | string | value | register: `contoso5_country_code_label` |

## Registers

- `country_name` → `data/lookups/contoso5_country_code_label.lookup.csv`

## Referenced by

- `dim_customer.country_code` → `dim_country.country_code`
- `dim_location.country_code` → `dim_country.country_code`
- `dim_store.country_code` → `dim_country.country_code`
- `v_contoso5_sales_line.sale_country_code` → `dim_country.country_code`