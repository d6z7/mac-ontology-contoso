---
type: Transform
title: 'Cleansing: dim_contoso_store'
description: Cleansing → contoso_served.dim_contoso_store
relation: contoso_served.dim_contoso_store
tags:
- CONTOSO
- transform
- lifecycle:draft
sql_file: data/transforms/dim_contoso_store.sql
---

Produces `contoso_served.dim_contoso_store` · grain: one row per StoreKey — one store VERSION, not one store (see open_transforms/store-version-vs-store)

## Rules
### absence_semantics — `empty-string-is-missing` · authored
- **defect** Status spells missing two ways inside one 74-row relation: '' on 58 rows and NULL on 1 (the sentinel), leaving 8 'Closed' and 7 'Restructured' (T8; P1 #5). A consumer testing `IS NULL` finds 1 of the 59 rows that carry no status.

- **rule** Read '' as absent: nullif the empty string to NULL. It does NOT impute a meaning — nothing here rewrites '' to 'Open' or 'Operating' — because the meaning of the blank is unruled and the data argues against the obvious reading (see note).

- **guarantee** Missing has exactly one spelling — NULL on 59 of 74 rows — and the served vocabulary is exactly the 2 named values it measured (Closed, Restructured), so `count(DISTINCT Status)` returns 2 and `WHERE Status IS NULL` finds every row without one (T8).


## Open — needs SME
- **sentinel_key** Serve it as it is, and once a human rules what it is, add a declared channel attribute (e.g. an is_online flag or a channel column) so a question can separate the channel from the store estate. NOT a filter: dropping the row would silently delete 41.8 % of the fact. NOT a value correction: rewriting 'Online' to a country would invent a market for that 41.8 %.
 _(PROPOSED)_
- **scd_type_2_grain** A current-version projection (or a valid-from/valid-to collapse) beside this one, once 'what is a store' is ruled. Not applied here: the fact carries StoreKey, so the version grain is what a line joins, and collapsing it in this transform would break that join for every line.
 _(PROPOSED)_
- **over_coverage** NONE — DO NOT FILTER. A dimension legitimately over-covers its fact, and trimming it would make 'which stores had no sales' unanswerable and would change the served row count on every reload. Carried here as a DISCLOSURE so the number is visible where the transform is read; the count that a question needs is a fact-side count, which is a concept-level distinction (P7).
 _(PROPOSED)_
- **orphan_key** NONE — there is nothing to resolve it against. It is served because it is a measured column (and because P2 measured it determining State/Country/Continent on the customer side), but no join can be declared for it until the delivery gains a geography relation or a human states that it is an internal code with no dimension.
 _(PROPOSED)_

## Lineage
- Source: [store](../sources/store.md)
- Clean dataset: [dim_contoso_store](../datasets/dim_contoso_store.md)

## SQL realization
Realized by `dim_contoso_store.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.