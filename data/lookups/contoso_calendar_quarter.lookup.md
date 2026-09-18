---
type: Lookup
title: contoso_calendar_quarter.lookup
source_yaml: data/lookups/contoso_calendar_quarter.lookup.csv
tags:
- CONTOSO
- lookup
---

Reference lookup · 4 rows · SSOT: `data/lookups/contoso_calendar_quarter.lookup.csv` (CSV).

| Quarter | label | search_key | source_view | confidence | note |
| --- | --- | --- | --- | --- | --- |
| Q1 | Q1 | q1 | dim_contoso_calendar_day | I | member months: 1+2+3 |
| Q2 | Q2 | q2 | dim_contoso_calendar_day | I | member months: 4+5+6 |
| Q3 | Q3 | q3 | dim_contoso_calendar_day | I | member months: 7+8+9 |
| Q4 | Q4 | q4 | dim_contoso_calendar_day | I | member months: 10+11+12 |