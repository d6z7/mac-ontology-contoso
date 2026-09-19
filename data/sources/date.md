---
type: Source
title: date
description: Raw landing of data/date.parquet, loaded verbatim by setup.sh (CREATE
  TABLE date AS SELECT * FROM read_parquet(...)); contents unmodified. What one row
  means, and whether this relation is served at all, are decided in P2/P3 — not claimed
  here.
resource: table://main.date
tags:
- CONTOSO
- source
- lifecycle:draft
- confidence:I
---

## Columns

| column | type | role |
|---|---|---|
| `Date` | timestamp | primary_key |
| `DateKey` | varchar | value |
| `Year` | integer | value |
| `YearQuarter` | varchar | value |
| `YearQuarterNumber` | integer | value |
| `Quarter` | varchar | value |
| `YearMonth` | varchar | value |
| `YearMonthShort` | varchar | value |
| `YearMonthNumber` | integer | value |
| `Month` | varchar | value |
| `MonthShort` | varchar | value |
| `MonthNumber` | integer | value |
| `DayofWeek` | varchar | value |
| `DayofWeekShort` | varchar | value |
| `DayofWeekNumber` | integer | value |
| `WorkingDay` | integer | value |
| `WorkingDayNumber` | integer | value |