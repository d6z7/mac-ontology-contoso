---
type: Transform
title: 'Cleansing: dim_contoso_calendar_day'
description: Cleansing → contoso_served.dim_contoso_calendar_day
relation: contoso_served.dim_contoso_calendar_day
tags:
- CONTOSO
- transform
- lifecycle:draft
sql_file: data/transforms/dim_contoso_calendar_day.sql
---

Produces `contoso_served.dim_contoso_calendar_day` · grain: one row per Date — one calendar day

## Rules
## Open — needs SME
- **type_mismatch** Cast it to integer or drop it in favour of Date — NEITHER applied here. The dataset descriptor declares this column varchar, so retyping it in the transform would make the served relation contradict the seam the ontology binds to; changing a served type is a promotion decision. And WHICH column the calendar keys on is itself open.
 _(PROPOSED)_
- **type_mismatch** `d."WorkingDay" <> 0 AS WorkingDay` would serve it as a boolean — NOT applied, for the same reason as varchar-datekey: the dataset descriptor declares it integer, and a served type change belongs to the promotion step, not to this transform.
 _(PROPOSED)_
- **over_coverage** NONE — DO NOT TRIM. A calendar exists to carry days on which nothing happened; trimming it to the fact's span would make every 'no sales that day' question unanswerable and would silently change the served row count on every reload. This is a DISCLOSURE carried where the transform is read, not an impurity: what must be decided is what 'latest month' means, and that is a concept-level rule (P7/P9), not a line of SQL.
 _(PROPOSED)_

## Lineage
- Source: [date](../sources/date.md)
- Clean dataset: [dim_contoso_calendar_day](../datasets/dim_contoso_calendar_day.md)

## SQL realization
Realized by `dim_contoso_calendar_day.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.