---
type: Dataset
title: 'Clean: contoso5_currency'
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

## Referenced by

- `dim_currency.currency_code` → `contoso5_currency.code`

## Rows

- The rows of this relation live in a FILE: format `csv` · `data/lookups/contoso5_currency.lookup.csv` · 5 row(s) measured.

| `code` |
|---|
| AUD |
| CAD |
| EUR |
| GBP |
| USD |

_All 5 row(s) — this IS the complete mapping._