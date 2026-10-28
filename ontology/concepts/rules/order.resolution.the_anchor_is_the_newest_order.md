---
type: Rule
title: order.resolution.the_anchor_is_the_newest_order
description: resolution rule · binds order_date
tags:
- CONTOSO5
- mac.concept.rule.resolution
- confidence:C
applies_to: ../order.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — C (confirmed)
- **Scope** — CONTOSO5
- **Binds** — `order_date`
- **Rule id** — `order.resolution.the_anchor_is_the_newest_order`

> The clauses below are PROJECTED from `mac.canon.scoped_latest` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

an anchor for "now" is needed over this relation — a declared window pins its period to one, or the bundle's vintage is recorded from one

### Then — do (then)

resolve it to `MAX(order_date)` over the whole of `contoso_served.v_contoso5_sales_line`, this relation declaring no axis to pin — which the canon permits only where there is none, and DISCLOSE the date the answer anchored to

### Never — don't (never)

anchoring on the clock date instead of the latest date the data carries; leaving the anchor unscoped on a relation that does carry a plan, budget or scenario axis: an unscoped MAX returns the planning horizon, not the latest actual; lowering this anchor into a relative window on its own: the anchor is a DATE, the window it stands for needs a grain, and inventing one answers about a different span than the question asked

Applies to [Order](../order.md).