---
type: Enum
title: Age Band
description: A customer's age in whole years, floored to a 5-year band and named by the band's lower bound, computed from the unserved `Birthday` AS OF 2025-12-31.
tags:
- CONTOSO
- enumeration
- confidence:I
resource: table://dim_contoso_customer
rule_pages:
- rules/age_band.precision.single_year_refused.md
- rules/age_band.as_of.date_travels_with_the_figure.md
---

A customer's age in whole years, floored to a 5-year band and named by the band's lower bound, computed from the unserved `Birthday` AS OF 2025-12-31. Fifteen bands, 20 through 90.
IT IS NOT AN AGE. The integer 40 is a band of five years, not a 40-year-old, and a mean of these codes is not a mean age. Single-year age is not answerable from the served plane at all — that is the ruling, not a gap.
IT IS NOT THE DELIVERY'S `Age` COLUMN EITHER. That column is stale by five years on every row and is not served; this band is derived instead.
AND IT IS AS-OF A DATE, NOT AS-OF NOW. The band is fixed at 2025-12-31 — the newest order date in the delivery. It does not age with the calendar, and when the fact horizon moves past that date the band must be re-derived. Nothing enforces that today.

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
The 15 members, their meanings and their populations are declared in this file; the column is `age_band_5y` on dim_contoso_customer; the as-of date is stated in every member's meaning. A question about single-year age, a birth date, or an age as-of today is refused from these declarations rather than from an empty query — there is nothing to probe for, because the columns that would answer it are not served.
```

## Grounded in

- `dim_contoso_customer` — key `CustomerKey`

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `CustomerKey` | integer | key | `dim_contoso_customer` (key) | — | — |
| `age_band_5y` | integer | dimension | `dim_contoso_customer` | DERIVED, NOT DELIVERED, AND IT CARRIES AN AS-OF DATE. The customer's age in whole years, floored to a 5-year band and served as the band's LOWER BOUND (20, 25, … 90 — an integer, so it sorts and compares as an age), derived from the unserved `Birthday` AS OF 2025-12-31. That date is the delivery's fact horizon (the newest order date) and is a CHOICE: the same three places must agree on it — the rule `derive-age-band-as-of` in data/transforms/dim_contoso_customer.yaml, the literal in the .sql, and this note. WHEN THE FACT HORIZON MOVES THE BAND MUST BE RE-DERIVED, and nothing enforces that (DQ-CUSTOMER-01, residual risk 1). Measured 2026-09-18: 15 bands, 0 nulls over 104 990 rows, smallest cell 1 396, no customer alone in a band. NOT SERVED alongside it: the stored `Age` (as-of 2020/2021 on every row, and unbanded) and `Birthday` (the identifier this band generalises) — see DQ-CUSTOMER-01 and NS-CUSTOMER-01. GROUPING ON IT IS LEGITIMATE AND HAS A MEASURED COST: the band alone singles out nobody, but added to ZipCode + Gender it takes the uniquely identifiable population from 35 894 to 74 617 of 104 990 (DQ-CUSTOMER-02, `coverage: gap`). | — |

_Declared per column, over 2 columns: description 1 of 2 · type 2 of 2 · joins → 0 of 2. An em dash is a column for which nothing is declared._

## Relationships

*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Customer](customer.md) — on `age_band_5y`

## Source of record
- Full MAC concept: `age_band.yaml` — open the **YAML** tab for the complete typed definition.