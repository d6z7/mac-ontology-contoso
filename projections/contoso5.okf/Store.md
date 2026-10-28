---
type: Entity
title: Store
description: THE PREMISES Contoso sells from — a shop that stood on one place for
  one trading period, with its own name, floor area, opening date and closing date.
tags:
- CONTOSO5
- entity
- confidence:I
timestamp: '2026-09-30'
---

# Store

THE PREMISES Contoso sells from — a shop that stood on one place for one trading period, with its own name, floor area, opening date and closing date. It is what every sale is recorded against. A PLACE MAY HOLD A SUCCESSION OF PREMISES, so a store is NOT its place: see the Location concept for the place, and `dim_store.store_key#rulings.finer_than` for the declaration that one rolls up into the other. The account is knowledge/store.md. THIS DEFINITION CARRIES NO COUNTS, by the operator's ruling of 2026-10-24: "you are disclosing values that variy through the time as constnts?!?!?! this is no go ... you can decribe things without constants too". It used to say how many stores there were and how many were trading, which was a measurement of one day frozen into a sentence — and it disagreed with this concept's own `counts:` key, which is how one word came to name two grains. Counts belong where they can be re-measured: data/profiles/dim_store.yaml.

## Relationships

- **store__trades_in__country** → [Country](/Country.md) (cardinality 1; grounded join `dim_store.country_code = dim_country.country_code`)
- **store__sited_in__location** → [Location](/Location.md) (cardinality 1; grounded join `dim_store.location_code = dim_location.location_code`)
- inverse of **order__placed_at__store** ← [Order](/Order.md) (grounded join `v_contoso5_sales_line.store_key = dim_store.store_key`)

# Citations

1. MAC concept source of record: `concepts/store.yaml` (schema_version 0.3.0-develop, confidence I).
