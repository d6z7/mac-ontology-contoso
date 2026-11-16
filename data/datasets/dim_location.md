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

| column | type | role |
|---|---|---|
| `location_code` | integer | PK |
| `country_code` | string | FK |
| `country_name` | string | value |
| `state` | string | value |
| `units_ever_here` | integer | value |
| `is_online` | boolean | value |

## Foreign keys

- `country_code` → `dim_country.country_code` (many:one, mandatory:mandatory)

## Referenced by

- `dim_store.store_code` → `dim_location.location_code`

## What a question may do

### Details

- **Schema version** — 0.4.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

### Key

- One row is identified by `location_code`.

### Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `location_code` | **key** | — | — | — |
| `country_code` | — | axis `categorical` | — | — |
| `country_name` | — | axis `categorical` | — | label_of `country_code` (long) |
| `state` | — | axis `categorical` | — | finer_than `country_code` |
| `units_ever_here` | — | aggregate precomputed / units · extremum `min`, `max` | — | — |
| `is_online` | — | — | — | — |

_Declared per column, over 6 columns: offers 4 of 6 · references 0 of 6 · rulings 2 of 6. An em dash is a column for which nothing is declared._

### Bound by

*1 concept(s) read this relation — a change to a column's `offers` or `rulings` reaches every one of them.*

- [Location](../concepts/location.md) — serves `location_code`, `country_code`, `country_name`, `state`, `units_ever_here`, `is_online`
