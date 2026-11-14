---
type: Entity
title: Customer
description: A person on Contoso's customer register, each with a name, a birth date and a place — continent, country, state, city.
tags:
- CONTOSO5
- entity
- confidence:I
resource: table://dim_customer
---

A person on Contoso's customer register, each with a name, a birth date and a place — continent, country, state, city. The register is not the buyer list: many registered customers have never ordered (rule Customer.register_not_buyers). The account is knowledge/customer.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.4.0-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-10-29

## How to answer

_No content available — the bundle declares nothing for this section._

## Grounded in

- `dim_customer` — key `customer_key` — semantics: [`data/datasets/dim_customer.yaml`](../../data/datasets/dim_customer.md)

## Grain

- One row is one Customer, identified by `customer_key`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `customer_key` | integer | key | — | — | — | — | the row key: one row per customer. The register is not the buyer list — many customers have never ordered (rule Customer.register_not_buyers). | — |
| `customer_name` | string | dimension | — | — | label_of `customer_key` (common) | — | the customer's name as registered. | — |
| `continent` | string | dimension | — | — | — | — | the continent the customer lives on. | — |
| `country_code` | string | dimension | — | — | finer_than `continent` | — | the country the CUSTOMER lives in. No customer carries the `--` online placeholder. This is the only column that can place an internet sale in a real country. | [Country](country.md) |
| `state` | string | dimension | — | — | scoped_by `country_code` | — | the state, province or region the customer lives in. | — |
| `city` | string | dimension | — | — | — | — | the city the customer lives in. | — |
| `gender` | string | dimension | — | — | — | — | the customer's recorded gender. | — |
| `birth_date` | date | dimension | — | — | — | — | the customer's date of birth. | — |
| `valid_from` | date | housekeeping | — | — | — | — | the day this customer record became valid — the start of the validity window that says whether a customer is active on a reference date. The register is kept as a history, so a sale could in principle be attributed to where the customer lived ON THE ORDER DATE — nothing in this bundle declares that it should be. | — |
| `valid_to` | date | housekeeping | — | — | — | — | the day this customer record stopped being valid — the end of the validity window. Paired with `valid_from`. | — |

_Declared per column, over 10 columns: type 10 of 10 · role 10 of 10 · identity 0 of 10 · measure 0 of 10 · rulings 3 of 10 · register 0 of 10 · description 10 of 10 · joins → 1 of 10. An em dash is a column for which nothing is declared._

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
