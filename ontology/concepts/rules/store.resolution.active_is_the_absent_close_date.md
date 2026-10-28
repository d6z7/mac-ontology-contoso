---
type: Rule
title: store.resolution.active_is_the_absent_close_date
description: resolution rule · binds close_date, status_annotation
tags:
- CONTOSO5
- mac.concept.rule.resolution
- confidence:C
applies_to: ../store.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — C (confirmed)
- **Scope** — CONTOSO5
- **Binds** — `close_date`, `status_annotation`
- **Rule id** — `store.resolution.active_is_the_absent_close_date`

> The clauses below are PROJECTED from `mac.canon.population_select` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a question counts, lists or filters this concept's rows

### Then — do (then)

4 named population(s) of one axis: `active` (also called open; still open; trading; not closed; operating); `closed` (also called ceased; no longer trading; not active; inactive); `restructured` (also called rebuilt; replaced; closed and reopened); `shut` (also called shut down; shut for good; closed permanently; closed and not replaced). a question naming none of them takes `active`, and the answer DISCLOSES that it did. this default holds only when the question is ABOUT this concept — a concept merely on the join path keeps none of it. `active` is everything `closed` is not. `restructured` is a subset of `closed`; `shut` is a subset of `closed`

### Never — don't (never)

mixing two readings of one axis in a single figure; reporting a count over all rows as a count of the default reading

Applies to [Store](../store.md).