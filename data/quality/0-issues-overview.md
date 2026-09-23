---
type: Doc
title: Issues & inconsistencies
description: 6 findings — the full overview
tags:
- CONTOSO
- overview
---

Everything the harvest + reconciliation found for this source: **6 findings** across 8 tables.

- **Severity** — 0 high · 2 medium · 4 low
- **Resolution** — 1 ✓ resolved · 1 ◐ partial · 1 ⚠ open gap · 3 not yet reconciled (newly harvested)

## All findings

| severity | finding | table | impurity | resolution | disposition |
|---|---|---|---|---|---|
| medium | [`customer.Age` is a derived attribute frozen five years before t](DQ-CUSTOMER-01.md) | customer |  | ◐ partial `dim_contoso_customer` | accepted · ruled by operator |
| medium | [15 leftover views in the warehouse, measured, neither treated as](NS-SERVING-01.md) | — |  | not yet reconciled  | accepted · ruled by operator |
| low | [the served customer row is a quasi-identifier — ZipCode alone si](DQ-CUSTOMER-02.md) | customer |  | ⚠ open gap  | accepted · ruled by operator |
| low | [`sales` measured, deliberately not served — it is the served ord](NS-ORDERS-01.md) | sales |  | ✓ resolved `v_contoso_order_line` | accepted · ruled by operator |
| low | [the order header measured, deliberately not served as a relation](NS-ORDERS-02.md) | orders |  | not yet reconciled  | accepted · ruled by operator |
| low | [12 of the 24 customer columns measured, deliberately not served](NS-CUSTOMER-01.md) | customer |  | not yet reconciled  | accepted · ruled by operator |

## Open items — still need work

- ⚠ open gap [DQ-CUSTOMER-02](DQ-CUSTOMER-02.md) — NOTHING IS DONE, DELIBERATELY, AND THE EMPTY `resolving_transforms` IS THE HONEST RECORD OF THAT rather than an omission — no rule in this bundle generalises, suppresses or perturbs a served customer column, so there is no transform to name. `gap` is the coverage term for a finding that is documented and untreated.
WHY LEAVING IT IS SAFE HERE, said plainly and not dressed up: this is the Contoso Data Generator V2 (SQLBI, MIT) — synthetic data about people who do not exist. There is no data subject to re-identify, and NS-CUSTOMER-01 already records that a privacy claim on this bundle "would not be measurable". Nothing measured in DQ-CUSTOMER-02 is evidence about any real person's privacy. It is registered because the SHAPE travels even though the data does not: this bundle is a worked example, and a delivery built from it against real customers inherits the same served column set.
WHAT A FUTURE TREATMENT MUST GET RIGHT, because the numbers already say it: ZipCode is the DOMINANT identifier — 29 193 of 104 990 customers are singled out by ZipCode alone, which is 81 % of what ZipCode + Gender achieves together — and the age band is an AMPLIFIER, taking ZipCode + Gender from 35 894 uniquely identifiable to 74 617. Treating the band and leaving ZipCode served would be the visible half of the work with most of the risk untouched. NOT PROPOSED AS A RULE HERE: which columns a question may group by is a scope and ownership decision, not a transform's, and inventing a suppression on synthetic data would make the served plane answer fewer questions while protecting nobody.

- ◐ partial [DQ-CUSTOMER-01](DQ-CUSTOMER-01.md) — TWO RULES ON ONE TRANSFORM, and neither is sufficient alone. `exclude-stale-derived-age` refuses the stored `Age`, so no age figure computable from the served plane can be five years stale. `derive-age-band-as-of` derives the age from `Birthday` and serves it as the integer `age_band_5y`, banded to 5 years, AS OF 2025-12-31 — so an age-grouped question is answerable at all, which it was not before. Neither input is served: the stored `Age` is five years wrong, and `Birthday` is the exact date of birth, i.e. the identifier the band generalises.
`partial`, NOT `resolved`, AND THE COST AND THE REVERT CONDITION ARE THE REASON. THE COST: the delivery carries single-year age and the served plane carries 5-year bands, so a question that needs age to the year cannot be answered from the served plane at all. That is the operator's ruling of 2026-09-18 ("rounded to 5 years precision"), a deliberate loss of precision rather than an oversight — but it is a loss, and `resolved` would claim the defect was dissolved losslessly. THE REVERT / RE-DERIVE CONDITION: the as-of date is a CONSTANT in data/transforms/dim_contoso_customer.sql and nothing compares it to the warehouse's newest fact. When the fact horizon moves past 2025-12-31 the served band becomes as-of a year in the past — the identical defect class, one iteration on, and silently. So the containment carries its own staleness clock, which is exactly what `partial` is for. DQ-CUSTOMER-01 residual risk 1 names the acceptance property that would police it; that property does not exist yet. THE RAW COLUMN IS UNTOUCHED UPSTREAM: `main.customer.Age` is still as-of 2020/2021 on 104 990 of 104 990 rows and this bundle cannot repair it.
Evidence, re-measured read-only 2026-09-18 over main.customer with the exact SQL the rule ships: year(Birthday) + Age is 2020 on 94 990 rows and 2021 on 10 000, ZERO rows consistent with 2024/2025/2026; `Age` has 67 distinct values from 19 to 85 with only 21 833 of 104 990 a multiple of 5, so it is not the rounded age that was ruled servable either; `Birthday` is non-null on all 104 990 rows, so the derivation needs no fallback branch and none is written; and the derived band yields 15 bands (20 … 90), 0 nulls, smallest cell 1 396.


_Full narrative: [RECONCILIATION](RECONCILIATION.md)._