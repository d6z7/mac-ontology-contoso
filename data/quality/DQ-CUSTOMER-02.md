---
type: DQ Issue
title: the served customer row is a quasi-identifier — ZipCode alone singles out 29
  193 of 104 990 customers, and the age band nearly doubles that
description: Measured 2026-09-18 over `main.customer` (104 990 rows), counting GROUPS,
  the SMALLEST group, and the groups of EXACTLY ONE row — the last being the population
  that a single combination of served valu
tags:
- CONTOSO
- severity:low
- confidence:I
- lifecycle:draft
- resolution:gap
---

`DQ-CUSTOMER-02` · severity **low** · confidence **I** · resolution **⚠ open gap** · disposition **accepted · ruled by operator**

## Finding
Measured 2026-09-18 over `main.customer` (104 990 rows), counting GROUPS, the SMALLEST group, and the groups of EXACTLY ONE row — the last being the population that a single combination of served values singles out. The age band is the 5-year band derived from `Birthday` as of 2025-12-31 that `dim_contoso_customer` now serves as `age_band_5y`:

  quasi-identifier              groups   smallest cell   groups of exactly one row
  age band alone                    15           1 396                           0
  ZipCode alone                 40 639               1                      29 193
  ZipCode + Gender              49 278               1                      35 894
  ZipCode + Gender + age band   86 052               1                      74 617

TWO FACTS, AND THEY POINT DIFFERENT WAYS. (a) The age band is a SOUND GENERALISATION ON ITS OWN: 15 bands over 104 990 rows, smallest cell 1 396, and ZERO customers singled out by it. (b) IN COMBINATION IT IS AN AMPLIFIER: adding it to ZipCode + Gender takes the uniquely identifiable population from 35 894 to 74 617 — it more than doubles it (x2.08) and brings it to 71 % of all rows. And the dominant identifier is NEITHER of those: ZIPCODE ALONE, WHICH THIS BUNDLE ALREADY SERVED BEFORE THIS STEP, singles out 29 193 customers by itself — 81 % of what ZipCode + Gender achieves together. The risk was already on the row; the band adds to it.


## Current handling
NOTHING IS GENERALISED, SUPPRESSED OR PERTURBED, and no transform rule resolves this entry — data/quality/impurity_resolution_map.yaml records it as `coverage: gap`, which is the honest word for deliberately untreated. `dim_contoso_customer` serves ZipCode (role `value`), Gender (role `discriminator`), City, State/StateFull, Country/CountryFull, Continent, and now `age_band_5y`. `Birthday` and the raw `Age` are both unserved (NS-CUSTOMER-01, DQ-CUSTOMER-01) — one because it is the identifier, the other because it is five years wrong — so the exact date of birth is not on the served row. REGISTERED AS A PATTERN RECORD, NOT AS AN EXPOSURE, and this is stated plainly rather than dressed up: this is the Contoso Data Generator V2 (SQLBI, MIT) — SYNTHETIC data about people who do not exist. There is no data subject here to re-identify. NS-CUSTOMER-01 already says that a privacy claim on this bundle "would not be measurable", and that stands: nothing measured above is evidence about any real person's privacy.


## Residual risk
WHAT THIS ENTRY IS ACTUALLY FOR: the SHAPE travels even though the data does not. A bundle built from this one as a worked example — the purpose it serves on this estate — would carry the same served column set against real customers, and then every number above is a live finding rather than an arithmetic curiosity. IF THAT EVER HAPPENS, THE ORDER OF OPERATIONS IS THE FINDING: ZipCode is the dominant identifier and generalising the age band (or dropping it) buys 35 894 -> 74 617 back while leaving 29 193 singled out by ZipCode alone. Treating the band and leaving ZipCode served would be the visible half of the work with most of the risk untouched. The measured candidates, in the order the numbers support them: generalise ZipCode (to a prefix, or to City, which is already served); then reconsider whether Gender and the band are both needed on the same row. NOT DONE HERE, AND NOT PROPOSED AS A RULE: which columns a question may group by is a scope and an ownership decision, not a transform's, and inventing a suppression on synthetic data would make the served plane answer fewer questions while protecting nobody. REVERSED IF: this bundle's data is ever replaced by, or this descriptor set is ever applied to, a delivery describing real people — at which point this stops being a pattern record, the severity is no longer `low`, and the register entry must be re-graded before the plane is served; or the question scope adds a demographic axis that widens the served column set (each added attribute can only increase the numbers above, never reduce them).


## Sign-off required
operator — NAMED 2026-09-18. What they must ratify is not the arithmetic, which is measured and reproducible from queries/p1_source_profiling.sql: it is whether a served customer row in THIS delivery may carry ZipCode, Gender and an age band at once, and what the rule becomes the day these descriptors are pointed at real customers. Recorded as the ROLE rather than a personal name because this bundle is a public example; there is exactly one operator on this estate. Not yet ruled.


## Disposition

**accepted** — ruled by **operator**.

Ruled 2026-09-18 by the operator, this source's owner: the measured quasi-identifier shape is accepted as it stands and NO treatment is applied to this bundle. There is nothing to protect — the data is synthetic, MIT-licensed, and about people who do not exist — so suppressing or generalising a served column here would make the served plane answer fewer questions while protecting nobody. Treatment is deferred to a delivery where there IS a data subject ("anonymization later"), and this entry exists to hand that delivery its starting numbers.
WHEN THAT TREATMENT COMES, THE NUMBERS SAY WHERE TO START AND IT IS NOT THE AGE BAND. ZipCode alone accounts for 29 193 of the 104 990 — 81 % of what ZipCode + Gender achieve together — and rolling geography up to Country takes uniqueness to ZERO. The 5-year age band is an amplifier, not a cause: sound alone (15 bands, smallest cell 1 396, 0 unique) and it takes ZipCode + Gender from 35 894 to 74 617 in combination. Treating the band and leaving ZipCode served would be the visible half of the work with most of the risk untouched.
`coverage: gap` STAYS, with `resolving_transforms: []`, because deferring is not treating and an empty transform list is the honest record of that rather than an omission.

## Resolution

**⚠ open gap** — NOTHING IS DONE, DELIBERATELY, AND THE EMPTY `resolving_transforms` IS THE HONEST RECORD OF THAT rather than an omission — no rule in this bundle generalises, suppresses or perturbs a served customer column, so there is no transform to name. `gap` is the coverage term for a finding that is documented and untreated.
WHY LEAVING IT IS SAFE HERE, said plainly and not dressed up: this is the Contoso Data Generator V2 (SQLBI, MIT) — synthetic data about people who do not exist. There is no data subject to re-identify, and NS-CUSTOMER-01 already records that a privacy claim on this bundle "would not be measurable". Nothing measured in DQ-CUSTOMER-02 is evidence about any real person's privacy. It is registered because the SHAPE travels even though the data does not: this bundle is a worked example, and a delivery built from it against real customers inherits the same served column set.
WHAT A FUTURE TREATMENT MUST GET RIGHT, because the numbers already say it: ZipCode is the DOMINANT identifier — 29 193 of 104 990 customers are singled out by ZipCode alone, which is 81 % of what ZipCode + Gender achieves together — and the age band is an AMPLIFIER, taking ZipCode + Gender from 35 894 uniquely identifiable to 74 617. Treating the band and leaving ZipCode served would be the visible half of the work with most of the risk untouched. NOT PROPOSED AS A RULE HERE: which columns a question may group by is a scope and ownership decision, not a transform's, and inventing a suppression on synthetic data would make the served plane answer fewer questions while protecting nobody.


_No transform in the copied gold dissolves this yet — an honest open gap._

## Table
- [customer](../sources/customer.md)