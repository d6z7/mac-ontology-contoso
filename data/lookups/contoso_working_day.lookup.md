---
type: Lookup
title: contoso_working_day.lookup
source_yaml: data/lookups/contoso_working_day.lookup.csv
tags:
- CONTOSO
- lookup
---

Reference lookup · 2 rows · SSOT: `data/lookups/contoso_working_day.lookup.csv` (CSV).

| WorkingDay | label | search_key | source_view | confidence | note |
| --- | --- | --- | --- | --- | --- |
| 1 | working day | working day | dim_contoso_calendar_day | I | calendar days: 2760; of them on Sat/Sun: 0 |
| 0 | non-working day | non-working day | dim_contoso_calendar_day | I | calendar days: 1258; of them on Sat/Sun: 1148 |