---
type: Reference
title: Store
description: A point of sale, identified by StoreKey, located in a CountryName.
tags:
- CONTOSO
- reference
- confidence:C
resource: table://store
rule_pages:
- rules/store.online_is_not_a_market.md
---

A point of sale, identified by StoreKey, located in a CountryName. NOTE: 'Online' appears as a CountryName alongside real countries (Germany, France, ...) — it is a sales CHANNEL, not a market. Treat it as such and disclose when it is included in a by-country breakdown.

## Details

- **Identity** — fk_name
- **Version** — 0.1
- **Schema version** — 0.1.9
- **Status** — draft
- **Owner** — demo-team
- **Governance owner** — demo-team
- **Last reviewed** — 2026-07-19

## Grounded in

- `store` — key `StoreKey`

## Grain
one row per store

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `CountryName` | — | `store` |  |  |
| `State` | — | `store` |  |  |

## Relationships

*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Sales (net revenue)](sales.md) — on `StoreKey`

## Source of record
- Full MAC concept: `store.yaml` — open the **YAML** tab for the complete typed definition.