---
type: Transform
title: 'Cleansing: dim_contoso_customer'
description: Cleansing → contoso_served.dim_contoso_customer
relation: contoso_served.dim_contoso_customer
tags:
- CONTOSO
- transform
- lifecycle:draft
sql_file: data/transforms/dim_contoso_customer.sql
---

Produces `contoso_served.dim_contoso_customer` · grain: one row per CustomerKey — one customer, with one validity window

## Rules
### padded_label — `trim-padded-region-label` · authored
- **defect** 4 of 104 990 rows carry a trailing space in StateFull and the same 4 in State — 'Birmingham ' on 3 rows and 'Bradford ' on 1 — and the trimmed form of each already exists as its own value ('Birmingham' 38 rows, 'Bradford' 35). The landing therefore spells two regions two ways: 565 State spellings fold to 563 and 610 StateFull spellings to 608 (T13a). It reaches the fact: 13 order lines belong to those customers (T13c), so the question scope's 'by region' axis would report Birmingham twice.

- **rule** Trim both region label columns. The fold is safe to make here because it merges spellings of ONE region rather than two regions: the padded rows carry the identical GeoAreaKey, Country and Continent as their unpadded twins (Birmingham 93/GB/Europe, Bradford 102/GB/Europe — T13b).

- **guarantee** One spelling per region label: 608 StateFull and 563 State values served, 104 990 rows in and 104 990 out, and the functional dependence P2 measured (StateFull -> State, GeoAreaKey, Country, Continent) still holds with 0 violations after the trim, exactly as it did before (T13c). A GROUP BY on either column cannot split a region into a padded and an unpadded group.


### stale_derived_attribute — `exclude-stale-derived-age` · authored
- **defect** Age is as-of 2020/2021, not as-of now: year(Birthday) + Age is 2020 or 2021 on every one of the 104 990 rows (2 distinct as-of years, min 2020, max 2021) while orders run to 2025 (T11e; P1 #8). Re-measured 2026-09-18: 2020 on 94 990 rows, 2021 on 10 000, and ZERO rows consistent with 2024, 2025 or 2026. A consumer filtering on it would be answering a question about a year nobody asked about. The column is additionally NOT BANDED as delivered — 67 distinct values from 19 to 85, only 21 833 of 104 990 rows carrying a multiple of 5 — so it is not the rounded age the operator ruled should be served either.

- **rule** The column is not projected. The fix is an ABSENCE — which is why this rule quotes no SQL fragment and appears in no `consumes` map: there is no served column for it to resolve onto. It is visible in the .sql as the projection list, and the refusal is registered with the other 11 unserved columns as NS-CUSTOMER-01. `Birthday` is not projected either, and for a DIFFERENT reason: it is not wrong, it is the identifier — see `derive-age-band-as-of` below, which reads it and serves only a band over it.

- **guarantee** No STORED age can reach the served plane, so no age figure computed from it can be silently five years stale. This is HALF of what DQ-CUSTOMER-01 needs and it is the half that is a pure absence; the other half — an age that IS answerable, and correct as-of a declared date — is `derive-age-band-as-of`. Before that rule existed this guarantee read "no age-based figure can be computed from the served plane at all", which was true and is now false: the two rules must be read together or the guarantee overstates the refusal.


### stale_derived_attribute — `derive-age-band-as-of` · authored
- **defect** The SAME defect the rule above refuses, seen from the other side: the delivery carries no usable age at all. `Age` is stale by five years on 104 990 of 104 990 rows and unbanded (67 distinct values, 19 to 85), and the only other age-bearing column is `Birthday` — non-null on all 104 990 rows, and an exact date of birth, which is an identifier rather than an attribute. So an age-grouped question was unanswerable from the served plane without either serving a wrong number or serving a date of birth.

- **rule** DERIVE the age from `Birthday` and serve it BANDED TO 5 YEARS, as of a DECLARED as-of date, and serve neither input.
THE AS-OF DATE IS 2025-12-31, AND IT IS DECLARED HERE BECAUSE IT IS A CHOICE, NOT A FACT. It is the delivery's FACT HORIZON: the newest order date in the warehouse (main.orders DT / orderrows, whose facts run to 2025-12-31). An age is meaningless without an as-of date — that is exactly what is wrong with the stored `Age`, which is as-of 2020/2021 and says so nowhere — so this one travels in three places that must agree: this rule, the `AS OF` comment block in the .sql, and the `notes` on the served column in data/datasets/dim_contoso_customer.yaml.
THE CONSEQUENCE, STATED RATHER THAN LEFT TO BE DISCOVERED: WHEN THE FACT HORIZON MOVES, THE BAND MUST BE RE-DERIVED. The as-of date is a constant in the .sql and nothing compares it to max(order date). A delivery that gains 2026 facts therefore serves an age band that is as-of a year in the past — the identical defect class, one iteration on — and it will do so silently. Registered as residual risk 1 on DQ-CUSTOMER-01, where the missing acceptance property that would police it is named as a follow-up.
THE BAND IS THE LOWER BOUND OF A 5-YEAR BUCKET (20, 25, ... 90), per the operator's ruling of 2026-09-18: "age is served as age and rounded to 5 years precision. so 40,45,50,55, etc." It is an INTEGER, not a label, so it sorts and compares as an age.
THE ARITHMETIC IS EXACT, NOT BOUNDARY-COUNTING. `date_diff('year', ...)` counts year boundaries crossed, which equals the true age only when the as-of date falls on or after the birthday in that year. It does today — the as-of date is 31 December — but that is an accident of THIS as-of date, and a re-derivation to a mid-year horizon would silently over-count every customer whose birthday has not yet passed. The month-day correction term is therefore written into the SQL now, while it is a no-op and provably so, rather than after it has become a defect.

- **guarantee** An age-grouped question is answerable from the served plane, and every figure it returns is as-of 2025-12-31 — not as-of 2020. Measured over main.customer on 2026-09-18, read-only, with the exact SQL above: 15 bands, 20 to 90 in steps of 5, 0 nulls over 104 990 rows (Birthday is non-null on all of them, so there is no fallback branch and none is written), and the band population is 1 725 at 20, 1 396 at 90 and between 7 740 and 7 983 in each of the 13 bands between. The smallest cell is 1 396 and NO customer is alone in a band — so the band ALONE is a sound generalisation. In COMBINATION with columns this bundle already serves it is not: see DQ-CUSTOMER-02, which measures that adding it to ZipCode + Gender takes the uniquely identifiable population from 35 894 to 74 617, and that ZipCode alone already singles out 29 193. That is registered as a `gap` — this rule does not treat it and does not claim to. NEITHER INPUT IS SERVED: `Birthday` is not projected (it is the identifier the band generalises) and the stored `Age` is not projected (it is five years wrong). A consumer cannot recover a date of birth or a single-year age from the served row.


## Open — needs SME
- **degenerate_interval** NONE. 'Never valid', 'valid for one instant' and 'a data entry error' imply different SQL (drop the row, keep it, or correct a date), and nothing in the data distinguishes them. Dropping one customer to make a window look sensible would be a silent deletion of a real key.
 _(PROPOSED)_
- **over_coverage** NONE — DO NOT FILTER. A dimension legitimately over-covers its fact; trimming it would make 'customers who never bought' unanswerable and would change the served row count on every reload. Carried as a DISCLOSURE so the number is visible where the transform is read.
 _(PROPOSED)_
- **orphan_key** NONE — there is nothing to resolve it against. The geography a question can actually use is the Continent/Country/State/City columns served on this row; GeoAreaKey is served because it was measured to determine them (P2), not because it can be joined.
 _(PROPOSED)_

## Impurities dissolved
- ◐ partial [DQ-CUSTOMER-01](../quality/DQ-CUSTOMER-01.md) — TWO RULES ON ONE TRANSFORM, and neither is sufficient alone. `exclude-stale-derived-age` refuses the stored `Age`, so no age figure computable from the served plane can be five years stale. `derive-age-band-as-of` derives the age from `Birthday` and serves it as the integer `age_band_5y`, banded to 5 years, AS OF 2025-12-31 — so an age-grouped question is answerable at all, which it was not before. Neither input is served: the stored `Age` is five years wrong, and `Birthday` is the exact date of birth, i.e. the identifier the band generalises.
`partial`, NOT `resolved`, AND THE COST AND THE REVERT CONDITION ARE THE REASON. THE COST: the delivery carries single-year age and the served plane carries 5-year bands, so a question that needs age to the year cannot be answered from the served plane at all. That is the operator's ruling of 2026-09-18 ("rounded to 5 years precision"), a deliberate loss of precision rather than an oversight — but it is a loss, and `resolved` would claim the defect was dissolved losslessly. THE REVERT / RE-DERIVE CONDITION: the as-of date is a CONSTANT in data/transforms/dim_contoso_customer.sql and nothing compares it to the warehouse's newest fact. When the fact horizon moves past 2025-12-31 the served band becomes as-of a year in the past — the identical defect class, one iteration on, and silently. So the containment carries its own staleness clock, which is exactly what `partial` is for. DQ-CUSTOMER-01 residual risk 1 names the acceptance property that would police it; that property does not exist yet. THE RAW COLUMN IS UNTOUCHED UPSTREAM: `main.customer.Age` is still as-of 2020/2021 on 104 990 of 104 990 rows and this bundle cannot repair it.
Evidence, re-measured read-only 2026-09-18 over main.customer with the exact SQL the rule ships: year(Birthday) + Age is 2020 on 94 990 rows and 2021 on 10 000, ZERO rows consistent with 2024/2025/2026; `Age` has 67 distinct values from 19 to 85 with only 21 833 of 104 990 a multiple of 5, so it is not the rounded age that was ruled servable either; `Birthday` is non-null on all 104 990 rows, so the derivation needs no fallback branch and none is written; and the derived band yields 15 bands (20 … 90), 0 nulls, smallest cell 1 396.


## Lineage
- Source: [customer](../sources/customer.md)
- Clean dataset: [dim_contoso_customer](../datasets/dim_contoso_customer.md)

## SQL realization
Realized by `dim_contoso_customer.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.dim_contoso_customer` · kinds: passthrough · rename

| output column | ← from | rule | kind |
|---|---|---|---|
| `StateFull` | `customer.StateFull` | trim-padded-region-label | passthrough |
| `State` | `customer.State` | trim-padded-region-label | passthrough |
| `age_band_5y` | `customer.Birthday` | derive-age-band-as-of | rename |
| `CustomerKey` | `customer.CustomerKey` | None | passthrough |
| `GeoAreaKey` | `customer.GeoAreaKey` | None | passthrough |
| `StartDT` | `customer.StartDT` | None | passthrough |
| `EndDT` | `customer.EndDT` | None | passthrough |
| `Continent` | `customer.Continent` | None | passthrough |
| `Gender` | `customer.Gender` | None | passthrough |
| `City` | `customer.City` | None | passthrough |
| `ZipCode` | `customer.ZipCode` | None | passthrough |
| `Country` | `customer.Country` | None | passthrough |
| `CountryFull` | `customer.CountryFull` | None | passthrough |