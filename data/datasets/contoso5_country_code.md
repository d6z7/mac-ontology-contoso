---
type: Dataset
title: 'Clean: contoso5_country_code'
description: AI-friendly clean shape the ontology binds to
relation: null
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `code` | string | PK |  |
| `label` | string | value |  |

## Referenced by

- `dim_country.country_code` → `contoso5_country_code.code`

## Rows

- The rows of this relation live in a FILE: format `csv` · `data/lookups/contoso5_country_code.lookup.csv` · 9 row(s) measured.

| `code` | `label` |
|---|---|
| -- | Online |
| AU | Australia |
| CA | Canada |
| DE | Germany |
| FR | France |
| GB | United Kingdom |
| IT | Italy |
| NL | Netherlands |
| US | United States |

_All 9 row(s) — this IS the complete mapping._