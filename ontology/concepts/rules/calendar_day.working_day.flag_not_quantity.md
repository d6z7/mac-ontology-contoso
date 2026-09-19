---
type: Rule
title: WorkingDay is a 0/1 flag — filter or group on it, never sum it
description: aggregation rule · binds WorkingDay, WorkingDayNumber
tags:
- mac.rule_kind.aggregation
- confidence:P
applies_to: ../calendar_day.md
---

## Rule

- **Kind** — `aggregation`
- **Confidence** — P (proposed)
- **Binds** — `WorkingDay`, `WorkingDayNumber`
- **Rule id** — `calendar_day.working_day.flag_not_quantity`

### When

using `{WorkingDay}` in a query

### Then — do (then)

filter on it, or group by it, reading 1 as a working day (2 760 of 4 018) and 0 as non-working (1 258)

### Never — don't (never)

summing `{WorkingDay}` or averaging `{WorkingDayNumber}`: the column is declared integer and measured boolean, so a SUM returns a count of working days under the name of a total

Applies to [Calendar Day](../calendar_day.md).