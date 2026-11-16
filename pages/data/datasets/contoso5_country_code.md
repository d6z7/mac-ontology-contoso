---
type: Dataset
title: 'Clean: contoso5_country_code'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.contoso5_country_code
tags:
- CONTOSO5
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `code` | string | PK |
| `label` | string | value |

## Referenced by

- `dim_country.country_code` → `contoso5_country_code.code`

## What a question may do

### Details

- **Schema version** — 0.4.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

### Key

- One row is identified by `code`.

### Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `code` | **key** | — | — | — |
| `label` | — | axis `categorical` | — | label_of `code` (long) |

_Declared per column, over 2 columns: offers 1 of 2 · references 0 of 2 · rulings 1 of 2. An em dash is a column for which nothing is declared._

### Bound by

_No concept binds this relation through `grounding.bindings[]`, so nothing in the ontology reads these column facts._
