---
type: Rule
title: country.exclusion.sentinel_is_not_a_country
description: exclusion rule · binds country_code
tags:
- CONTOSO5
- mac.concept.rule.exclusion
- confidence:P
applies_to: ../country.md
---

## Rule

- **Kind** — `exclusion`
- **Confidence** — P (proposed)
- **Scope** — CONTOSO5
- **Binds** — `country_code`
- **Rule id** — `country.exclusion.sentinel_is_not_a_country`

> The clauses below are PROJECTED from `mac.canon.population_select` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a question counts, lists or filters this concept's rows

### Then — do (then)

2 named population(s) of one axis: `real`; `sentinel`. a question naming none of them takes `real`, and the answer DISCLOSES that it did. this default holds only when the question is ABOUT this concept — a concept merely on the join path keeps none of it

### Never — don't (never)

mixing two readings of one axis in a single figure; reporting a count over all rows as a count of the default reading

Applies to [Country](../country.md).