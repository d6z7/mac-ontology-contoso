---
type: Rule
title: Store GeoAreaKey -1 is the online channel, and it is a member
description: guarantee rule · binds GeoAreaKey
tags:
- mac.rule_kind.guarantee
- confidence:P
applies_to: ../geo_area.md
---

## Rule

- **Kind** — `guarantee`
- **Confidence** — P (proposed)
- **Binds** — `GeoAreaKey`
- **Rule id** — `geo_area.sentinel.online_has_no_region`

### When

reporting a store-side region breakdown

### Then — do (then)

include `{GeoAreaKey}` = -1 as its own row, labelled as the online channel, with the 93 550 of 223 974 lines behind it stated

### Never — don't (never)

filtering `{GeoAreaKey}` = -1 out as invalid, or resolving it through the register, which has no row for it

Applies to [Region](../geo_area.md).