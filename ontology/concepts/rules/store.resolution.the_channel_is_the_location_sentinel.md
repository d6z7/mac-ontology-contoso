---
type: Rule
title: store.resolution.the_channel_is_the_location_sentinel
description: resolution rule · binds store_code
tags:
- CONTOSO5
- mac.concept.rule.resolution
- confidence:P
applies_to: ../store.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — P (proposed)
- **Scope** — CONTOSO5
- **Binds** — `store_code`
- **Rule id** — `store.resolution.the_channel_is_the_location_sentinel`

> The clauses below are PROJECTED from `mac.canon.population_select` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a question counts, lists or filters this concept's rows

### Then — do (then)

2 named population(s) of one axis: `online`; `physical`. a question naming none of them takes `physical`, and the answer DISCLOSES that it did. this default holds only when the question is ABOUT this concept — a concept merely on the join path keeps none of it

### Never — don't (never)

mixing two readings of one axis in a single figure; reporting a count over all rows as a count of the default reading

Applies to [Store](../store.md).