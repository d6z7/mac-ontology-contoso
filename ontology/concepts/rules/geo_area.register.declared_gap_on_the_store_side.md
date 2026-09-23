---
type: Rule
title: Three store regions have no register row — say so rather than return nothing
description: resolution rule · binds GeoAreaKey, State
tags:
- mac.rule_kind.resolution
- confidence:P
applies_to: ../geo_area.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — P (proposed)
- **Binds** — `GeoAreaKey`, `State`
- **Rule id** — `geo_area.register.declared_gap_on_the_store_side`

### When

resolving a region word that the register does not contain

### Then — do (then)

check the store dimension's `{State}` for the 3 known store-only regions — `{GeoAreaKey}` 79, 291 and 519, carrying 6 708 of 223 974 lines — and say the resolution came from there; otherwise refuse

### Never — don't (never)

reading the register's silence as "no such region": the register is cut from `{dim_contoso_customer}` and 3 of the 67 store regions have no customer in them, so its coverage of the store side is 64 of 67 and not 67 of 67

Applies to [Region](../geo_area.md).