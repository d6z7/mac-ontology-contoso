---
type: Transform
title: 'Cleansing: v_contoso_order_line'
description: Cleansing → contoso_served.v_contoso_order_line
relation: contoso_served.v_contoso_order_line
tags:
- CONTOSO
- transform
- lifecycle:draft
sql_file: data/transforms/v_contoso_order_line.sql
---

Produces `contoso_served.v_contoso_order_line` · grain: one row per (OrderKey, RowNumber) — one line of one order

## Rules
### duplicate_delivery — `one-delivery-of-the-line` · authored
- **defect** The delivery ships the same order line twice. main.sales (223 974 rows) carries the same line population at the same key and, joined line-for-line to orderrows x orders, differs on NOTHING: 223 974 matched lines and 0 differences across ProductKey, Quantity, UnitPrice, NetPrice, UnitCost, CustomerKey, StoreKey, OrderDate, DeliveryDate and CurrencyCode; its one extra column, ExchangeRate, reproduces the currencyexchange USD->CurrencyCode quote for the row's day with 0 differences on all 223 974 rows (T5; P1 R1-R4, P3 S4/S5 measured the same over the same denominator). Serving both would give every figure in this bundle two defensible answers.

- **rule** Build the line from the header/detail pair and do not read main.sales in any transform of this bundle. The rate is served at its own grain in v_contoso_fx_rate_day, where the whole grid exists (T12), instead of being repeated on the line as sales does.

- **guarantee** Every figure on this relation has exactly one home in the served plane: a consumer summing Quantity x NetPrice over this view counts the delivery's 223 974 lines once, and there is no second served relation it could have summed instead. No conversion rate is carried on the line, so a currency question must join the rate grid deliberately rather than inherit a single USD-based direction by accident.


###  — `rename-dt-to-orderdate` · authored
- **defect** 
- **rule** Project orders.DT under the name the same value carries in the sales delivery, OrderDate. It is the only renamed column in this bundle; every other served column keeps its landing name.

- **guarantee** The order event date is addressable under one name across the delivery. Measured identical to sales.OrderDate on 223 974/223 974 lines with 0 differing values and 0 nulls either side (T4), so the rename carries no value change — only the name.


###  — `attach-order-header` · authored
- **defect** 
- **rule** Carry the five header attributes onto each line of the order. All five are functionally determined by OrderKey (measured, P2), so the line grain loses nothing by holding them and the order header is not served as a relation of its own (NS-ORDERS-02); OrderKey is then a degenerate dimension on this fact.

- **guarantee** A line can be grouped by customer, store, currency, order date and delivery date without a second join, and the join can neither fan out nor drop a line: orders.OrderKey is unique 93 470/93 470, 0 of 223 974 lines are orphaned, 0 of 93 470 headers have no line, and the served relation is unique at its declared key — 223 974 rows / 223 974 distinct / 0 duplicates / 0 null key parts (T2a, T3).


## Open — needs SME
- **sequence_gaps** NONE a transform may apply. Renumbering would rewrite half of the cell key the fact is identified by, and the gaps may be cancelled or deleted lines that are legitimately absent. If a human rules that they are deletions, the honest fix is a declared note on the served column, not a renumbering.
 _(PROPOSED)_
- **duplicate_row_candidate** NO de-duplication. The other 252 colliding key groups differ on at least one figure and are genuinely distinct lines; collapsing on equality would delete 8 rows that may be real repeated lines, and the only thing that separates them is the key column itself.
 _(PROPOSED)_
- **sentinel_key** NOTHING on the fact. Filtering the sentinel would silently delete 41.8 % of the delivery, and rewriting 'Online' to a country would invent a market for it. If a human rules that Online is a channel rather than a store, the fix belongs on the store dimension as a declared channel attribute (see dim_contoso_store.yaml#open_transforms/sentinel-store-row), not here.
 _(PROPOSED)_

## Impurities dissolved
- ✓ resolved [NS-ORDERS-01](../quality/NS-ORDERS-01.md) — 

## Lineage
- Source: [orderrows](../sources/orderrows.md)
- Source: [orders](../sources/orders.md)
- Clean dataset: [v_contoso_order_line](../datasets/v_contoso_order_line.md)

## SQL realization
Realized by `v_contoso_order_line.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.