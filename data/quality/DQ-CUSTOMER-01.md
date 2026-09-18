---
type: DQ Issue
title: '`customer.Age` is a derived attribute frozen five years before the facts it
  would describe'
description: 'Re-measured 2026-09-18 over `main.customer` (104 990 rows). `Age` is
  a STORED DERIVED value and it is stale: year(Birthday) + Age is 2020 on 94 990 rows
  and 2021 on 10 000, so the column is as-of one '
tags:
- CONTOSO
- severity:medium
- confidence:I
- lifecycle:draft
- resolution:partial
---

`DQ-CUSTOMER-01` · severity **medium** · confidence **I** · resolution **◐ partial** · disposition **accepted · ruled by operator**

## Finding
Re-measured 2026-09-18 over `main.customer` (104 990 rows). `Age` is a STORED DERIVED value and it is stale: year(Birthday) + Age is 2020 on 94 990 rows and 2021 on 10 000, so the column is as-of one of two years in the past, while the order facts run to 2025-12-31. ZERO rows are consistent with 2024, 2025 or 2026 — the staleness is total, not partial, and it is not drift around a current value. Two further measurements matter for what may be served instead: `Age` IS NOT BANDED as delivered — 67 distinct values from 19 to 85, of which only 21 833 of 104 990 rows (20.8 %) carry a multiple of 5 — and `Birthday` is NON-NULL on all 104 990 rows, so a correct age is derivable for every customer without a fallback. A consumer who filtered or grouped on the stored `Age` would be answering a question about 2020 in a delivery whose newest fact is five years younger, with nothing on the row to say so.


## Current handling
TWO RULES ON `dim_contoso_customer`, both cross-linked from data/quality/impurity_resolution_map.yaml:
  · `exclude-stale-derived-age` — the stored `Age` is NOT PROJECTED. The fix is an absence, so
    the rule quotes no SQL fragment and appears in no `consumes` map; the refusal is visible as
    the projection list in data/transforms/dim_contoso_customer.sql.
  · `derive-age-band-as-of` — a CORRECT age is derived from `Birthday` and served as
    `age_band_5y`, banded to 5 years, AS OF THE DATE THE RULE DECLARES (2025-12-31, the fact
    horizon). `Birthday` itself stays unserved: it is the identifier, and serving it would put
    the exact date of birth on the row the band exists to generalise.
So no age-based figure computable from the served plane is five years stale, and an age-band figure IS computable, which it was not before this step.


## Residual risk
THE STALENESS IS CONTAINED, NOT CURED, AND THE CONTAINMENT HAS ITS OWN AS-OF DATE. That is why the resolution map records this as `coverage: partial` rather than `resolved`, and why the status here is `open`:
1. THE SERVED BAND WILL GO STALE THE SAME WAY. `age_band_5y` is derived as of 2025-12-31 —
   a constant in the .sql, declared in the rule. When the delivery gains 2026 facts the fact
   horizon moves, the as-of date no longer matches it, and the band becomes a figure about a
   year nobody asked about: the identical defect class, one iteration later. NOTHING ENFORCES
   THE RE-DERIVATION — there is no acceptance property that compares the rule's as-of date to
   max(order date), and until there is, this is an unpoliced dependency on a hand-typed
   constant. FOLLOW-UP, named rather than implied: such a property.
2. PRECISION IS LOST BY CHOICE. The delivery carries single-year age (wrong); the served plane
   carries 5-year bands (right, coarser). A question that needs age to the year cannot be
   answered from the served plane at all. That is the operator's ruling of 2026-09-18 ("age is
   served as age and rounded to 5 years precision ... it is perfect candidate for some kind of
   PII handling like anonymization later") and it is a deliberate cost, not an oversight.
3. THE RAW COLUMN IS UNTOUCHED UPSTREAM. Nothing this bundle can do repairs `main.customer.Age`,
   and a reader of the landing still meets a column that is five years wrong with no marker.
REVERSED / CLOSABLE WHEN: the delivery starts computing `Age` as-of its own newest fact (then the stored column becomes servable and the derivation is redundant); or an acceptance property re-measures the as-of date against the fact horizon per load, at which point 1 stops being unpoliced and this entry can be dispositioned on evidence rather than on a promise.


## Sign-off required
operator — NAMED 2026-09-18, and they have already ruled on WHAT is served (age, banded to 5 years). What is still theirs to ratify is narrower and is not a modelling question: whether 2025-12-31 is the as-of date this delivery wants pinned, and who re-derives the band when the fact horizon moves past it. Recorded as the ROLE rather than a personal name because this bundle is a public example; there is exactly one operator on this estate.


## Disposition

**accepted** — ruled by **operator**.

Ruled 2026-09-18 by the operator, this source's owner: the served age is a 5-year band, not a single year — "age is served as age and rouded to 5 years precision. so 40,45,50,55, etc." The stored `Age` is refused (as-of 2020/2021 on 104 990 of 104 990 rows, 0 consistent with 2024-2026) and `Birthday` is consumed but never served, so the identifier does not reach the served plane. TWO RESIDUALS WERE ACCEPTED WITH IT, both recorded in residual_risk and neither cured: single-year age is no longer answerable from the served plane at all, a deliberate loss of precision; and the band's own as-of date is a constant in the transform SQL that nothing compares to the fact horizon, so it will go stale the same way unless the acceptance property named in residual_risk 1 is built. That is why the resolution map keeps `coverage: partial` — the treatment is partial, the ruling is not.

## Resolution

**◐ partial** — TWO RULES ON ONE TRANSFORM, and neither is sufficient alone. `exclude-stale-derived-age` refuses the stored `Age`, so no age figure computable from the served plane can be five years stale. `derive-age-band-as-of` derives the age from `Birthday` and serves it as the integer `age_band_5y`, banded to 5 years, AS OF 2025-12-31 — so an age-grouped question is answerable at all, which it was not before. Neither input is served: the stored `Age` is five years wrong, and `Birthday` is the exact date of birth, i.e. the identifier the band generalises.
`partial`, NOT `resolved`, AND THE COST AND THE REVERT CONDITION ARE THE REASON. THE COST: the delivery carries single-year age and the served plane carries 5-year bands, so a question that needs age to the year cannot be answered from the served plane at all. That is the operator's ruling of 2026-09-18 ("rounded to 5 years precision"), a deliberate loss of precision rather than an oversight — but it is a loss, and `resolved` would claim the defect was dissolved losslessly. THE REVERT / RE-DERIVE CONDITION: the as-of date is a CONSTANT in data/transforms/dim_contoso_customer.sql and nothing compares it to the warehouse's newest fact. When the fact horizon moves past 2025-12-31 the served band becomes as-of a year in the past — the identical defect class, one iteration on, and silently. So the containment carries its own staleness clock, which is exactly what `partial` is for. DQ-CUSTOMER-01 residual risk 1 names the acceptance property that would police it; that property does not exist yet. THE RAW COLUMN IS UNTOUCHED UPSTREAM: `main.customer.Age` is still as-of 2020/2021 on 104 990 of 104 990 rows and this bundle cannot repair it.
Evidence, re-measured read-only 2026-09-18 over main.customer with the exact SQL the rule ships: year(Birthday) + Age is 2020 on 94 990 rows and 2021 on 10 000, ZERO rows consistent with 2024/2025/2026; `Age` has 67 distinct values from 19 to 85 with only 21 833 of 104 990 a multiple of 5, so it is not the rounded age that was ruled servable either; `Birthday` is non-null on all 104 990 rows, so the derivation needs no fallback branch and none is written; and the derived band yields 15 bands (20 … 90), 0 nulls, smallest cell 1 396.


- Dissolved by [dim_contoso_customer](../transforms/dim_contoso_customer.md)

## Table
- [customer](../sources/customer.md)