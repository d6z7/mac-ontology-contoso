---
type: Rule
title: Geography rolls up — the point location is not served and not derivable
description: exclusion rule · binds City, ZipCode, Continent, Country, State, GeoAreaKey
tags:
- mac.rule_kind.exclusion
- confidence:P
applies_to: ../customer.md
---

## Rule

- **Kind** — `exclusion`
- **Confidence** — P (proposed)
- **Binds** — `City`, `ZipCode`, `Continent`, `Country`, `State`, `GeoAreaKey`
- **Rule id** — `customer.geography.rollup_only`

### When

a question asks where a customer is, or asks to map, cluster or locate customers

### Then — do (then)

answer from the roll-up chain this row serves — `{Continent}`, `{Country}`, `{State}`, `{GeoAreaKey}` — and refuse the point, naming NS-CUSTOMER-01 as the ruling

### Never — don't (never)

treating `{City}` or `{ZipCode}` as a location axis to group by, or implying a coordinate exists on this row: the landing's 104 990 distinct (Latitude, Longitude) pairs over 104 990 rows are a perfect identifier and are deliberately not served

Applies to [Customer](../customer.md).