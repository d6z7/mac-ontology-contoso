---
type: Rule
title: '"Operating" is an absence here, not a code — read it from the dates'
description: resolution rule · binds Status, CloseDate
tags:
- mac.rule_kind.resolution
- confidence:P
applies_to: ../store_status.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — P (proposed)
- **Binds** — `Status`, `CloseDate`
- **Rule id** — `store_status.absence.operating_has_no_code`

### When

a question asks for open, operating, active or trading stores

### Then — do (then)

answer from `{CloseDate}` IS NULL — 58 of 74 versions — and say that the operating state is read from the validity window because the status column has no code for it

### Never — don't (never)

filtering `{Status}` for an 'Open' or 'Operating' value, which does not exist and returns nothing; and never reading `{Status}` IS NULL as "operating", because one of the 59 nulls is a version that IS closed by its dates

Applies to [Store Status](../store_status.md).