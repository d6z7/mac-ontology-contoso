---
type: Entity
title: Location
description: THE PLACE a store stands on — a country and a state, and nothing that
  belongs to the shop itself.
tags:
- CONTOSO5
- entity
- confidence:I
timestamp: '2026-09-29'
---

# Location

THE PLACE a store stands on — a country and a state, and nothing that belongs to the shop itself. Floor area, opening and closing dates are properties of PREMISES and live on Store; what a place owns is where it is. ONE PLACE MAY HOLD A SUCCESSION OF PREMISES over time, which is the fact this concept exists to keep separate from Store: `dim_store.store_key` declares `finer_than: location_code`, so premises roll UP into a place and a place never divides down into one. Summing a per-premises measure over a place that has been re-let counts it once per tenancy. A PLACE IS NOT A CITY IN THIS BUNDLE. Its finest geography is `state`, which in France means regions and overseas territories; `main.store` carries no city or town column. City exists only on the customer, as where a customer lives, and is declared personally identifying. No counts here, by the ruling of 2026-10-24 — they belong in data/profiles/dim_location.yaml where they can be re-measured. The account is knowledge/location.md.

## Relationships

- **location__in__country** → [Country](/Country.md) (cardinality 1; grounded join `dim_location.country_code = dim_country.country_code`)
- inverse of **store__sited_in__location** ← [Store](/Store.md) (grounded join `dim_store.location_code = dim_location.location_code`)

# Citations

1. MAC concept source of record: `concepts/location.yaml` (schema_version 0.3.0-develop, confidence I).
