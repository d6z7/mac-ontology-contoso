---
type: Rule
title: The online sentinel is a real member carrying 41.8 % of the fact
description: guarantee rule · binds StoreKey, CountryCode, CountryName
tags:
- mac.rule_kind.guarantee
- confidence:P
applies_to: ../store.md
---

## Rule

- **Kind** — `guarantee`
- **Confidence** — P (proposed)
- **Binds** — `StoreKey`, `CountryCode`, `CountryName`
- **Rule id** — `store.sentinel.online_is_served`

### When

filtering, counting or breaking a figure down by store

### Then — do (then)

include `{StoreKey}` 999999 as its own row, labelled as the online channel

### Never — don't (never)

excluding it as invalid geography, or repairing `{CountryCode}` '--' and `{CountryName}` 'Online' into a real country: 93 550 of 223 974 lines point at it, so excluding it removes 41.8 % of the fact and repairing it invents a market for the same share

Applies to [Store](../store.md).