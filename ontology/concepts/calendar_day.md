---
type: Reference
title: Calendar Day
description: 'One calendar day, with the period labels a question groups by pre-computed on the row: year, quarter, month, day of week, and a working-day flag.'
tags:
- CONTOSO
- reference
- confidence:I
resource: table://dim_contoso_calendar_day
rule_pages:
- rules/calendar_day.extent.latest_comes_from_the_fact.md
- rules/calendar_day.working_day.flag_not_quantity.md
---

One calendar day, with the period labels a question groups by pre-computed on the row: year, quarter, month, day of week, and a working-day flag. 4 018 consecutive days, 2016-01-01 to 2026-12-31, with no gaps — a 4 018-day span carrying 4 018 rows.
IT IS NOT THE EXTENT OF THE DATA, and this is the trap. The calendar covers MORE than the facts do: 359 of its days fall after the last fact date (2026-01-06) and 568 days carry no sale at all. So max(Date) here is 2026-12-31 while the newest order is 2025-12-31 — the latest day in this relation is not the latest day of data, and "latest" must be resolved from the measure's own data rather than from this dimension.
IT IS ALSO NOT TWO DIMENSIONS. The fact carries two dates — OrderDate and DeliveryDate, both measured fully on this calendar (0 values off it) — and they are two ROLES of this one conformed calendar, not an order calendar and a delivery calendar.

## Details

- **Identity** — fk_name
- **Version** — 1.0
- **Schema version** — 0.1.14
- **Status** — draft
- **Owner** — operator
- **Governance owner** — operator
- **Last reviewed** — 2026-09-18

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
Every period label a question can name is a column of this row — year, quarter, month, weekday, working day — and the words resolve offline through data/lookups/contoso_calendar_month.lookup.csv (12 rows, each with its quarter), data/lookups/contoso_calendar_quarter.lookup.csv (4), data/lookups/contoso_calendar_weekday.lookup.csv (7) and data/lookups/contoso_working_day.lookup.csv (2). The grain is the declared key. Nothing here needs a probe, and a date outside 2016-01-01..2026-12-31 is a refusal derived from a measured gapless span.
```

## Grounded in

- `dim_contoso_calendar_day` — key `Date`

## Grain
one row = one calendar day — Date

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `Date` | key | `dim_contoso_calendar_day` (key) |  |  |
| `DateKey` | key | `dim_contoso_calendar_day` |  |  |
| `Year` | dimension | `dim_contoso_calendar_day` |  |  |
| `YearQuarter` | dimension | `dim_contoso_calendar_day` |  |  |
| `YearQuarterNumber` | attribute | `dim_contoso_calendar_day` |  |  |
| `Quarter` | dimension | `dim_contoso_calendar_day` |  |  |
| `YearMonth` | dimension | `dim_contoso_calendar_day` |  |  |
| `YearMonthShort` | attribute | `dim_contoso_calendar_day` |  |  |
| `YearMonthNumber` | attribute | `dim_contoso_calendar_day` |  |  |
| `Month` | dimension | `dim_contoso_calendar_day` |  |  |
| `MonthShort` | attribute | `dim_contoso_calendar_day` |  |  |
| `MonthNumber` | dimension | `dim_contoso_calendar_day` |  |  |
| `DayofWeek` | dimension | `dim_contoso_calendar_day` |  |  |
| `DayofWeekShort` | attribute | `dim_contoso_calendar_day` |  |  |
| `DayofWeekNumber` | dimension | `dim_contoso_calendar_day` |  |  |
| `WorkingDay` | dimension | `dim_contoso_calendar_day` |  |  |
| `WorkingDayNumber` | attribute | `dim_contoso_calendar_day` |  |  |

## Relationships

*0 join(s) out · 2 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `Date`
- [Order Line](order_line.md) — on `Date`

## Source of record
- Full MAC concept: `calendar_day.yaml` — open the **YAML** tab for the complete typed definition.