---
type: Rule
title: store.online_is_not_a_market
description: exclusion rule · binds CountryName
tags:
- mac.rule_kind.exclusion
applies_to: ../store.md
---

## Rule

- **Kind** — `exclusion`
- **Binds** — `CountryName`
- **Rule id** — `store.online_is_not_a_market`

### When

producing a sales-by-country / by-market breakdown

### Then — do (then)

treat CountryName='Online' as a CHANNEL, not a country: separate it out and disclose, or exclude with a note

### Never — don't (never)

silently listing 'Online' as a country peer of Germany, France, etc.

Applies to [Store](../store.md).