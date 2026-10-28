---
type: Rule
title: order.default.an_unscoped_question_covers_all_time
description: default rule · binds order_date
tags:
- CONTOSO5
- mac.concept.rule.default
- confidence:C
applies_to: ../order.md
---

## Rule

- **Kind** — `default`
- **Confidence** — C (confirmed)
- **Scope** — CONTOSO5
- **Binds** — `order_date`
- **Rule id** — `order.default.an_unscoped_question_covers_all_time`

> The clauses below are PROJECTED from `mac.canon.period_default` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a question neither names a window nor constrains this axis's own period column(s)

### Then — do (then)

1 named window(s): `all_time`. `all_time` is unbounded — no period predicate at all. a question naming none of them takes `all_time`, and the answer DISCLOSES that it did

### Never — don't (never)

reporting a defaulted answer without disclosing the extent it covered, which is indistinguishable from a guess; applying a default to a question that has already constrained this axis's own period column — its statement governs, and nothing is disclosed about it

Applies to [Order](../order.md).