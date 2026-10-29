---
type: Enum
title: Currency
description: 'The money a sale is denominated in: five ISO codes, pointed at by every sale and by both ends of every exchange rate.'
tags:
- CONTOSO5
- enumeration
- confidence:I
---

The money a sale is denominated in: five ISO codes, pointed at by every sale and by both ends of every exchange rate. The account is knowledge/currency.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.3.1-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-29

## How to answer

_No content available — the bundle declares nothing for this section._

## Grounded in

- `dim_currency` — key `currency_code` — semantics: [`ontology/relations/dim_currency.yaml`](../relations/dim_currency.md)

## Grain

- One row is one Currency, identified by `currency_code`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `currency_code` | string | key | — | — | — | — | — | — |

_Declared per column, over 1 column: type 1 of 1 · role 1 of 1 · identity 0 of 1 · measure 0 of 1 · rulings 0 of 1 · register 0 of 1 · description 0 of 1 · joins → 0 of 1. An em dash is a column for which nothing is declared._

## Axes

_No content available — the bundle declares nothing for this section._

## Relationships


*0 join(s) out · 3 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Exchange Rate](exchange_rate.md) — on `currency_code`
- [Exchange Rate](exchange_rate.md) — on `currency_code`
- [Order](order.md) — on `currency_code`

## Source of record

- Full MAC concept: `currency.yaml` — open the **YAML** tab for the complete typed definition.
