---
type: Entity
title: Customer
description: A person on Contoso's customer register, each with a name, a birth date and a place — continent, country, state, city.
tags:
- CONTOSO5
- entity
- confidence:I
---

A person on Contoso's customer register, each with a name, a birth date and a place — continent, country, state, city. The register is not the buyer list: many registered customers have never ordered (rule Customer.register_not_buyers). The account is knowledge/customer.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.3.1-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-10-29

## How to answer

_No content available — the bundle declares nothing for this section._

## Grounded in

- `dim_customer` — key `customer_key` — semantics: [`ontology/relations/dim_customer.yaml`](../relations/dim_customer.md)

## Grain

- One row is one Customer, identified by `customer_key`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `customer_key` | integer | key | — | — | — | — | — | — |
| `customer_name` | string | dimension | — | — | label_of `customer_key` (common) | — | — | — |
| `continent` | string | dimension | — | — | — | — | — | — |
| `country_code` | string | dimension | — | — | finer_than `continent` | — | — | [Country](country.md) |
| `state` | string | dimension | — | — | scoped_by `country_code` | — | — | — |
| `city` | string | dimension | — | — | — | — | — | — |
| `gender` | string | dimension | — | — | — | — | — | — |
| `birth_date` | date | dimension | — | — | — | — | — | — |
| `valid_from` | date | housekeeping | — | — | — | — | — | — |
| `valid_to` | date | housekeeping | — | — | — | — | — | — |

_Declared per column, over 10 columns: type 10 of 10 · role 10 of 10 · identity 0 of 10 · measure 0 of 10 · rulings 3 of 10 · register 0 of 10 · description 0 of 10 · joins → 1 of 10. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind | fold |
|---|---|---|
| `birth_date` | time | — |
| `city` | categorical | — |
| `continent` | categorical | — |
| `country_code` | categorical | — |
| `customer_name` | categorical | — |
| `gender` | categorical | — |
| `state` | categorical | — |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*1 join(s) out · 1 in — click a concept to open it.*

**Joins to** — this concept references:

- [Country](country.md) — joined on `country_code`

**Referenced by** — these point at this concept:

- [Order](order.md) — on `customer_key`

## Source of record

- Full MAC concept: `customer.yaml` — open the **YAML** tab for the complete typed definition.
- Source table: [customer](../../data/sources/customer.md)
