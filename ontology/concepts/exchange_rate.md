---
type: Metric
title: Exchange Rate
description: 'What one currency was worth in another on one day: 100,450 quoted rates over a date and an ordered pair of currencies.'
tags:
- CONTOSO5
- measure
- confidence:I
---

What one currency was worth in another on one day: 100,450 quoted rates over a date and an ordered pair of currencies. The account is knowledge/exchange_rate.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.3.1-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-29

## How to answer

_No content available — the bundle declares nothing for this section._

## Grounded in

- `v_contoso5_fx_rate` — key `date_day`, `from_currency`, `to_currency` — semantics: [`ontology/relations/v_contoso5_fx_rate.yaml`](../relations/v_contoso5_fx_rate.md)

## Grain

- One row is one Exchange Rate, identified by `date_day`, `from_currency`, `to_currency`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `date_day` | date | key | — | — | — | — | — | — |
| `from_currency` | string | key | — | — | — | — | — | [Currency](currency.md) |
| `to_currency` | string | key | — | — | scoped_by `from_currency` | — | — | [Currency](currency.md) |
| `rate` | decimal | measure | — | intensive · to-currency per from-currency | — | — | — | — |

_Declared per column, over 4 columns: type 4 of 4 · role 4 of 4 · identity 0 of 4 · measure 1 of 4 · rulings 1 of 4 · register 0 of 4 · description 0 of 4 · joins → 2 of 4. An em dash is a column for which nothing is declared._

## Axes

Measure type: `intensive`.

| axis | axis kind | fold |
|---|---|---|
| `date_day` | time | average |
| `from_currency` | categorical | average |
| `to_currency` | categorical | average |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*2 join(s) out · 1 in — click a concept to open it.*

**Joins to** — this concept references:

- [Currency](currency.md) — joined on `from_currency`
- [Currency](currency.md) — joined on `to_currency`

**Referenced by** — these point at this concept:

- [Order](order.md) — on `from_currency = 'USD'`

## Source of record

- Full MAC concept: `exchange_rate.yaml` — open the **YAML** tab for the complete typed definition.
