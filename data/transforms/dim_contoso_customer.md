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
- **defect** Age is as-of 2020/2021, not as-of now: year(Birthday) + Age is 2020 or 2021 on every one of the 104 990 rows (2 distinct as-of years, min 2020, max 2021) while orders run to 2025 (T11e; P1 #8). A consumer filtering on it would be answering a question about a year nobody asked about.

- **rule** The column is not projected. The fix is an ABSENCE — which is why this rule quotes no SQL fragment and appears in no `consumes` map: there is no served column for it to resolve onto. It is visible in the .sql as the 12-column projection list, and the refusal is registered with the other 11 unserved columns as NS-CUSTOMER-01.

- **guarantee** No age-based figure can be computed from the served plane at all, so none can be silently five years stale. If age is needed, it must be derived from a birth date as-of a stated date — which requires promoting Birthday deliberately (a promotion decision, not a transform's).


## Open — needs SME
- **degenerate_interval** NONE. 'Never valid', 'valid for one instant' and 'a data entry error' imply different SQL (drop the row, keep it, or correct a date), and nothing in the data distinguishes them. Dropping one customer to make a window look sensible would be a silent deletion of a real key.
 _(PROPOSED)_
- **over_coverage** NONE — DO NOT FILTER. A dimension legitimately over-covers its fact; trimming it would make 'customers who never bought' unanswerable and would change the served row count on every reload. Carried as a DISCLOSURE so the number is visible where the transform is read.
 _(PROPOSED)_
- **orphan_key** NONE — there is nothing to resolve it against. The geography a question can actually use is the Continent/Country/State/City columns served on this row; GeoAreaKey is served because it was measured to determine them (P2), not because it can be joined.
 _(PROPOSED)_

## Lineage
- Source: [customer](../sources/customer.md)
- Clean dataset: [dim_contoso_customer](../datasets/dim_contoso_customer.md)

## SQL realization
Realized by `dim_contoso_customer.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.dim_contoso_customer` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `StateFull` | `customer.StateFull` | trim-padded-region-label | passthrough |
| `State` | `customer.State` | trim-padded-region-label | passthrough |
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