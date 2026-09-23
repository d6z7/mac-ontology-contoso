---
type: Enum
title: Store Status
description: 'The lifecycle event recorded against a store version: ''Closed'' (8 versions) or ''Restructured'' (7 versions).'
tags:
- CONTOSO
- enumeration
- confidence:I
resource: table://dim_contoso_store
rule_pages:
- rules/store_status.absence.operating_has_no_code.md
---

The lifecycle event recorded against a store version: 'Closed' (8 versions) or 'Restructured' (7 versions). Nothing else is recorded.
IT IS NOT A COMPLETE STATE MACHINE, and this is the point. There is NO CODE FOR AN OPERATING STORE. 59 of the 74 versions carry NULL, and 58 of those are versions with no CloseDate — still open. So "operating" exists only as the absence of a status, and the one remaining NULL is a version that IS closed by its dates and carries no status event at all.
IT IS ALSO NOT A FILTER ON THE STORE DIMENSION. Both coded members are served and so is the NULL; nothing is excluded by status anywhere in this bundle.

## Details

- **Identity** — code
- **Version** — 1.0
- **Schema version** — 0.1.14
- **Status** — draft
- **Owner** — operator
- **Governance owner** — operator
- **Last reviewed** — 2026-09-18

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
Both coded members, their labels, their search keys and their version counts are in data/lookups/contoso_store_status.lookup.csv, cut from the served plane and bound as this concept's value domain; the absence and what it means are declared in `null_semantics`; the operating test is `CloseDate IS NULL` on the same row. So a status word resolves offline, and a word that resolves to neither member (a question about 'active' or 'trading' stores) is answered from the declared absence rather than from an empty query.
```

## Grounded in

- `dim_contoso_store` — key `StoreKey`

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `StoreKey` | integer | key | `dim_contoso_store` (key) | — | — |
| `StoreCode` | integer | key | `dim_contoso_store` | the store's natural code; NOT unique (67 codes over 74 rows). (StoreCode, OpenDate) is measured unique (74/74) — the natural temporal key of the SCD-2 (P2 G6). | — |
| `Status` | varchar | dimension | `dim_contoso_store` | CLEANSED: the landing spells missing two ways, '' on 58 rows and NULL on 1 (P1 #5); the served column uses NULL for both. Whether '' meant 'operating' is an open ruling (Q7). | — |
| `CloseDate` | date | dimension | `dim_contoso_store` | null on 58/74 rows (P1 #5). DATE since 2026-09-19, same cast as OpenDate; lossless over the 16 of 74 non-null values (0 non-midnight), and a cast leaves the 58 nulls null. | — |

_Declared per column, over 4 columns: description 3 of 4 · type 4 of 4 · joins → 0 of 4. An em dash is a column for which nothing is declared._

## Relationships

*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Store](store.md) — on `Status`

## Source of record
- Full MAC concept: `store_status.yaml` — open the **YAML** tab for the complete typed definition.