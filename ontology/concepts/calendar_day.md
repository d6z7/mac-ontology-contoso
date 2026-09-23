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

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `Date` | date | key | `dim_contoso_calendar_day` (key) | DATE since 2026-09-19, cast in the transform from the landing's TIMESTAMP on the operator's ruling. Lossless and measured, not assumed: every value was a timestamp at midnight (P1 V10), re-measured as 0 non-midnight over 4 018 of 4 018 rows immediately before the cast. main.date keeps TIMESTAMP; the served type is decided at the sources->datasets seam. The fact's OrderDate/DeliveryDate join this column by exact equality and were cast in the same change, so both sides are DATE — re-measured after: 3 450 of 4 018 ordered days, 3 498 of 4 018 delivered days, inclusion 1.0 over 223 974 rows, 0 orphans. DateKey is the same identity as varchar YYYYMMDD; which one the calendar keys on is still an open ruling (RUN.md Q11) — this descriptor keys on Date because the facts carry the day. | — |
| `DateKey` | varchar | key | `dim_contoso_calendar_day` | varchar YYYYMMDD on every row (P1 V9); bijective with Date (4 018/4 018, P2 G8). | — |
| `Year` | integer | dimension | `dim_contoso_calendar_day` | Year — 11 distinct values. | — |
| `YearQuarter` | varchar | dimension | `dim_contoso_calendar_day` | — | — |
| `YearQuarterNumber` | integer | attribute | `dim_contoso_calendar_day` | — | — |
| `Quarter` | varchar | dimension | `dim_contoso_calendar_day` | — | — |
| `YearMonth` | varchar | dimension | `dim_contoso_calendar_day` | — | — |
| `YearMonthShort` | varchar | attribute | `dim_contoso_calendar_day` | — | — |
| `YearMonthNumber` | integer | attribute | `dim_contoso_calendar_day` | — | — |
| `Month` | varchar | dimension | `dim_contoso_calendar_day` | — | — |
| `MonthShort` | varchar | attribute | `dim_contoso_calendar_day` | — | — |
| `MonthNumber` | integer | dimension | `dim_contoso_calendar_day` | — | — |
| `DayofWeek` | varchar | dimension | `dim_contoso_calendar_day` | — | — |
| `DayofWeekShort` | varchar | attribute | `dim_contoso_calendar_day` | — | — |
| `DayofWeekNumber` | integer | dimension | `dim_contoso_calendar_day` | — | — |
| `WorkingDay` | integer | dimension | `dim_contoso_calendar_day` | declared integer, used as a boolean (0/1 only, P1 V12). | — |
| `WorkingDayNumber` | integer | attribute | `dim_contoso_calendar_day` | — | — |

_Declared per column, over 17 columns: description 4 of 17 · type 17 of 17 · joins → 0 of 17. An em dash is a column for which nothing is declared._

## Relationships

*0 join(s) out · 2 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `Date`
- [Order Line](order_line.md) — on `Date`

## Source of record
- Full MAC concept: `calendar_day.yaml` — open the **YAML** tab for the complete typed definition.