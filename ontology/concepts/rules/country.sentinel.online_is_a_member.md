---
type: Rule
title: The '--' store country is a channel, not missing geography
description: guarantee rule · binds CountryCode, CountryName
tags:
- mac.rule_kind.guarantee
- confidence:P
applies_to: ../country.md
---

## Rule

- **Kind** — `guarantee`
- **Confidence** — P (proposed)
- **Binds** — `CountryCode`, `CountryName`
- **Rule id** — `country.sentinel.online_is_a_member`

### When

reporting a store-side country breakdown

### Then — do (then)

include `{CountryCode}` = '--' as its own row and label it as the online channel, naming the 93 550 of 223 974 lines behind it

### Never — don't (never)

correcting `{CountryCode}` = '--' to a real country, which invents a market for 41.8 % of the fact; and never reading `{CountryName}` = 'Online' as a country name

Applies to [Country](../country.md).