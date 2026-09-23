---
type: Dataset
title: 'Clean: dim_contoso_calendar_day'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_contoso_calendar_day
tags:
- CONTOSO
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `Date` | date | primary_key |
| `DateKey` | varchar | value |
| `Year` | integer | discriminator |
| `YearQuarter` | varchar | discriminator |
| `YearQuarterNumber` | integer | value |
| `Quarter` | varchar | discriminator |
| `YearMonth` | varchar | discriminator |
| `YearMonthShort` | varchar | discriminator |
| `YearMonthNumber` | integer | value |
| `Month` | varchar | discriminator |
| `MonthShort` | varchar | discriminator |
| `MonthNumber` | integer | value |
| `DayofWeek` | varchar | discriminator |
| `DayofWeekShort` | varchar | discriminator |
| `DayofWeekNumber` | integer | value |
| `WorkingDay` | integer | discriminator |
| `WorkingDayNumber` | integer | value |