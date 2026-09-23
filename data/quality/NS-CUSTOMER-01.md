---
type: DQ Issue
title: 12 of the 24 customer columns measured, deliberately not served
description: 'Measured 2026-09-18. `main.customer` has 24 columns over 104 990 rows.
  The question scope this bundle declares (README: the contested total, by brand,
  by region country -> continent, by currency, gros'
tags:
- CONTOSO
- severity:low
- confidence:I
- lifecycle:draft
---

`NS-CUSTOMER-01` · severity **low** · confidence **I** · disposition **accepted · ruled by operator**

## Finding
Measured 2026-09-18. `main.customer` has 24 columns over 104 990 rows. The question scope this bundle declares (README: the contested total, by brand, by region country -> continent, by currency, gross vs net, by period) names geography and nothing else about a customer. 12 columns are served — CustomerKey, GeoAreaKey, StartDT, EndDT, Continent, CountryFull, Country, StateFull, State, City, ZipCode, Gender — including the only continent column in the whole delivery (`store` has none: 0 continent-like columns, S10) whose country -> continent map is a function over 8 countries with 0 countries carrying two continents (S11). The 12 NOT served are Title, GivenName, MiddleInitial, Surname, StreetAddress, Birthday, Age, Occupation, Company, Vehicle, Latitude, Longitude. `Age` is additionally measured STALE: year(Birthday) + Age is 2020 or 2021 on every row while the facts run to 2025-12-31 (P1 #8), so it answers as-of a year nobody asked about.


## Current handling
NOT PROMOTED. dim_contoso_customer serves the 12 columns above at one row per CustomerKey; the other 12 stay in the landing and in data/sources/customer.yaml, measured, unserved and unreferenced. Nothing is filtered: 104 990 rows in, 104 990 rows out (52 189 of them appear on an order, S13 — a dimension over-covering its fact is disclosed, not trimmed).


## Residual risk
A question that needs a customer attribute cannot be answered until the column is promoted; the refusal is not destructive and the fix is one line in the transform's projection. REVERSED IF: a question in scope names a demographic attribute (then the column is added, and `Age` only with a ruling on its as-of year); or the declared question scope changes. Deliberately NOT a privacy claim: this is MIT-licensed synthetic data and no such claim would be measurable.


## Sign-off required
operator — NAMED 2026-09-18, taking the seat run record Q5 left empty. Recorded as the ROLE rather than a personal name because this bundle is a public example; there is exactly one operator on this estate, so the role identifies them, and the vocabulary asks for "the named person or role — never 'the team', never a tool". Both rulings this entry needs — the as-of ruling on the derived age column, and the scope ruling — are theirs. Not yet ruled.


## Disposition

**accepted** — ruled by **operator**.

Ruled 2026-09-18 by the operator, this source's owner: the served customer row is ROLL-UP GEOGRAPHY plus gender plus the age band, and the ten identity / contact / free-demographic columns (Title, GivenName, MiddleInitial, Surname, StreetAddress, Occupation, Company, Vehicle, Latitude, Longitude) stay unserved, as does `Birthday` — consumed, never exposed.
THE SCOPE LINE IS ROLL-UP GEOGRAPHY IN, POINT GEOGRAPHY OUT, and that distinction is the whole ruling, because "geography" read literally would admit the coordinates. Measured 2026-09-18: `main.customer` carries 104 990 DISTINCT (Latitude, Longitude) pairs over 104 990 rows, so EVERY customer sits at a unique point — a perfect identifier, strictly stronger than ZipCode, which singles out 29 193 (DQ-CUSTOMER-02). Serving them would make every other generalisation in the served plane pointless. They are also useless for the declared questions, which aggregate to region and country: a point coordinate cannot roll up, and the geography chain already served is what answers those.
Nothing is filtered by the non-promotion: 104 990 rows in, 104 990 out, 52 189 of them appearing on an order — a dimension over-covering its fact, disclosed rather than trimmed. The refusal is not destructive and the fix is one line in the transform's projection. REVERSED IF a question in the declared scope names one of these attributes, or the scope changes. Deliberately NOT a privacy claim: MIT-licensed synthetic data, and no such claim would be measurable — see DQ-CUSTOMER-02 for the shape that does travel.

## Table
- [customer](../sources/customer.md)