---
type: Source
title: date
description: The data as it lands — address `main`
resource: source://main/date
tags:
- Contoso 5
- source
---

- **Address** — `main` — its key in the connection's source map; transform SQL names the raw table only through it.
- **Account** — [`data/sources/date.md`](../../../data/sources/date.md) — the source's documentation (Y-4), authored; this page cites it and never writes it.

## Columns

| column | distinct | nulls | min | max |
|---|---:|---:|---|---|
| `Date` | 4018 | 0 | 2016-01-01 00:00:00 | 2026-12-31 00:00:00 |
| `DateKey` | 4018 | 0 | — | — |
| `Year` | 11 | 0 | 2016 | 2026 |
| `YearQuarter` | 44 | 0 | — | — |
| `YearQuarterNumber` | 44 | 0 | 8065 | 8108 |
| `Quarter` | 4 | 0 | — | — |
| `YearMonth` | 132 | 0 | — | — |
| `YearMonthShort` | 132 | 0 | — | — |
| `YearMonthNumber` | 132 | 0 | 24193 | 24324 |
| `Month` | 12 | 0 | — | — |
| `MonthShort` | 12 | 0 | — | — |
| `MonthNumber` | 12 | 0 | 1 | 12 |
| `DayofWeek` | 7 | 0 | — | — |
| `DayofWeekShort` | 7 | 0 | — | — |
| `DayofWeekNumber` | 7 | 0 | 1 | 7 |
| `WorkingDay` | 2 | 0 | 0 | 1 |
| `WorkingDayNumber` | 2761 | 0 | 0 | 2760 |

_Measured (`data/profiles/date.yaml`, 2026-10-26T16:40:50+01:00); a v3 source declares no columns._

## Read by

_No transform's SQL names this source._

## Findings

- [DQ-ORPHAN-DATE](../quality/DQ-ORPHAN-DATE.md) — medium · open — nobody has ruled — raw landing `date` is consumed by no transformation
