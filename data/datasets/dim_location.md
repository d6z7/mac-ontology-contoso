---
type: Dataset
title: 'Clean: dim_location'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_location
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `location_code` | integer | PK |  |
| `country_code` | string | FK | → `dim_country.country_code` |
| `country_name` | string | value | register: `contoso5_country_code_label` |
| `state` | string | value |  |
| `units_ever_here` | integer | value |  |

## Foreign keys

- `country_code` → `dim_country.country_code` (many:one, mandatory:mandatory)

## Registers

- `country_name` → `data/lookups/contoso5_country_code_label.lookup.csv`

## Referenced by

- `dim_store.store_code` → `dim_location.location_code`