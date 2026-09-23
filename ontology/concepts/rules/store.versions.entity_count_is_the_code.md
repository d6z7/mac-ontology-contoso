---
type: Rule
title: Counting stores counts codes, not rows — 67, never 74
description: aggregation rule · binds StoreCode, StoreKey
tags:
- mac.rule_kind.aggregation
- confidence:P
applies_to: ../store.md
---

## Rule

- **Kind** — `aggregation`
- **Confidence** — P (proposed)
- **Binds** — `StoreCode`, `StoreKey`
- **Rule id** — `store.versions.entity_count_is_the_code`

### When

counting stores, or reporting how many outlets there are

### Then — do (then)

count DISTINCT `{StoreCode}`, which is 67

### Never — don't (never)

counting rows of `{dim_contoso_store}` or DISTINCT `{StoreKey}`, which is 74 — the version count, inflated by the 6 codes that have more than one version and the one that has three

Applies to [Store](../store.md).