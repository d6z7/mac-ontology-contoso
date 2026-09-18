---
type: Doc
title: SME questions — data & data quality
description: 4 sign-offs + 14 proposed changes awaiting SME
tags:
- CONTOSO
- sme-questions
---

The open **SME sign-offs** the data + data-quality work surfaces — 4 from the quality register plus proposed transform changes awaiting ratification. Prioritised by severity; each links to the finding it unblocks. This list is projected from the register + transforms, so it stays in sync.

## Medium priority — 1 question(s)

| ask | owner | on (finding) | status | table |
|---|---|---|---|---|
| it is their warehouse file and their console mount; no modelling ruling is involved. | The operator of this c | [15 leftover views in the warehouse, measured, neither tr](NS-SERVING-01.md) | unreconciled | — |

## Low priority — 3 question(s)

| ask | owner | on (finding) | status | table |
|---|---|---|---|---|
| NAMED 2026-09-18, taking the seat run record Q5 left empty. Recorded as the ROLE rather than a personal name because this bundle i | operator | [`sales` measured, deliberately not served — it is the se](NS-ORDERS-01.md) | ✓ resolved | sales |
| NAMED 2026-09-18, taking the seat run record Q5 left empty. Recorded as the ROLE rather than a personal name because this bundle i | operator | [the order header measured, deliberately not served as a ](NS-ORDERS-02.md) | unreconciled | orders |
| NAMED 2026-09-18, taking the seat run record Q5 left empty. Recorded as the ROLE rather than a personal name because this bundle i | operator | [12 of the 24 customer columns measured, deliberately not](NS-CUSTOMER-01.md) | unreconciled | customer |

## Proposed data-model changes awaiting SME ratification

| transform | class | proposed change |
|---|---|---|
| [dim_contoso_calendar_day](../transforms/dim_contoso_calendar_day.md) | type_mismatch | Cast it to integer or drop it in favour of Date — NEITHER applied here. The dataset descriptor declares this column varchar, so retyping it in the tra |
| [dim_contoso_calendar_day](../transforms/dim_contoso_calendar_day.md) | type_mismatch | `d."WorkingDay" <> 0 AS WorkingDay` would serve it as a boolean — NOT applied, for the same reason as varchar-datekey: the dataset descriptor declares |
| [dim_contoso_calendar_day](../transforms/dim_contoso_calendar_day.md) | over_coverage | NONE — DO NOT TRIM. A calendar exists to carry days on which nothing happened; trimming it to the fact's span would make every 'no sales that day' que |
| [dim_contoso_customer](../transforms/dim_contoso_customer.md) | degenerate_interval | NONE. 'Never valid', 'valid for one instant' and 'a data entry error' imply different SQL (drop the row, keep it, or correct a date), and nothing in t |
| [dim_contoso_customer](../transforms/dim_contoso_customer.md) | over_coverage | NONE — DO NOT FILTER. A dimension legitimately over-covers its fact; trimming it would make 'customers who never bought' unanswerable and would change |
| [dim_contoso_customer](../transforms/dim_contoso_customer.md) | orphan_key | NONE — there is nothing to resolve it against. The geography a question can actually use is the Continent/Country/State/City columns served on this ro |
| [dim_contoso_product](../transforms/dim_contoso_product.md) | contradictory_pair | NONE until the meaning is ruled. If the weight is MISSING, the unit is a promise the data cannot keep and both columns should read absent; if it is NO |
| [dim_contoso_store](../transforms/dim_contoso_store.md) | sentinel_key | Serve it as it is, and once a human rules what it is, add a declared channel attribute (e.g. an is_online flag or a channel column) so a question can  |
| [dim_contoso_store](../transforms/dim_contoso_store.md) | scd_type_2_grain | A current-version projection (or a valid-from/valid-to collapse) beside this one, once 'what is a store' is ruled. Not applied here: the fact carries  |
| [dim_contoso_store](../transforms/dim_contoso_store.md) | over_coverage | NONE — DO NOT FILTER. A dimension legitimately over-covers its fact, and trimming it would make 'which stores had no sales' unanswerable and would cha |
| [dim_contoso_store](../transforms/dim_contoso_store.md) | orphan_key | NONE — there is nothing to resolve it against. It is served because it is a measured column (and because P2 measured it determining State/Country/Cont |
| [v_contoso_order_line](../transforms/v_contoso_order_line.md) | sequence_gaps | NONE a transform may apply. Renumbering would rewrite half of the cell key the fact is identified by, and the gaps may be cancelled or deleted lines t |
| [v_contoso_order_line](../transforms/v_contoso_order_line.md) | duplicate_row_candidate | NO de-duplication. The other 252 colliding key groups differ on at least one figure and are genuinely distinct lines; collapsing on equality would del |
| [v_contoso_order_line](../transforms/v_contoso_order_line.md) | sentinel_key | NOTHING on the fact. Filtering the sentinel would silently delete 41.8 % of the delivery, and rewriting 'Online' to a country would invent a market fo |
