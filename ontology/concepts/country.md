---
type: Enum
title: Country
description: A country Contoso sells in — 8 of them, plus one `--` sentinel that is not a place.
tags:
- CONTOSO5
- enumeration
- confidence:I
---

A country Contoso sells in — 8 of them, plus one `--` sentinel that is not a place. The account is knowledge/country.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.3.1-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-30

## How to answer

_No content available — the bundle declares nothing for this section._

## Grounded in

- `dim_country` — key `country_code` — semantics: [`ontology/relations/dim_country.yaml`](../relations/dim_country.md)

## Grain

- One row is one Country, identified by `country_code`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `country_code` | string | key | — | — | — | — | — | — |
| `country_name` | string | dimension | — | — | label_of `country_code` (long) | — | — | — |

_Declared per column, over 2 columns: type 2 of 2 · role 2 of 2 · identity 0 of 2 · measure 0 of 2 · rulings 1 of 2 · register 0 of 2 · description 0 of 2 · joins → 0 of 2. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind | fold |
|---|---|---|
| `country_name` | categorical | — |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*0 join(s) out · 4 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Customer](customer.md) — on `country_code`
- [Location](location.md) — on `country_code`
- [Order](order.md) — on `country_code`
- [Store](store.md) — on `country_code`

## Source of record

- Full MAC concept: `country.yaml` — open the **YAML** tab for the complete typed definition.
