---
type: Rule
title: The calendar is wider than the data — never take "latest" from this dimension
description: resolution rule · binds Date
tags:
- mac.rule_kind.resolution
- confidence:P
applies_to: ../calendar_day.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — P (proposed)
- **Binds** — `Date`
- **Rule id** — `calendar_day.extent.latest_comes_from_the_fact`

### When

resolving a relative period — latest, current, this year, year to date, the last N months

### Then — do (then)

take the anchor from the FACT's own date column in `{v_contoso_order_line}` and state the resolved window

### Never — don't (never)

anchoring on max(`{Date}`) of `{dim_contoso_calendar_day}`, which is 2026-12-31 — 359 days and almost twelve empty months past the newest order (2025-12-31) — so a year-to-date figure anchored here reports emptiness as a real result

Applies to [Calendar Day](../calendar_day.md).