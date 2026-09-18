---
type: DQ Issue
title: the order header measured, deliberately not served as a relation of its own
description: 'Measured 2026-09-18. `main.orders` (93 470 rows, 6 columns) carries
  no measure: its columns are OrderKey, CustomerKey, StoreKey, DT, DeliveryDate, CurrencyCode.
  Every one of its 5 non-key columns is f'
tags:
- CONTOSO
- severity:low
- confidence:I
- lifecycle:draft
---

`NS-ORDERS-02` · severity **low** · confidence **I** · disposition **accepted · ruled by operator**

## Finding
Measured 2026-09-18. `main.orders` (93 470 rows, 6 columns) carries no measure: its columns are OrderKey, CustomerKey, StoreKey, DT, DeliveryDate, CurrencyCode. Every one of its 5 non-key columns is functionally determined by OrderKey (measured, P2) and every one of them is served on the line relation, so a header view would restate them at a coarser grain under a second name. Serving the line loses no order: 0 of the 93 470 headers have no line (S1), and the inner join keeps exactly the line population with no fan-out (223 974 joined rows = 223 974 orderrows rows; 93 470/93 470 distinct OrderKey in orders, so the join cannot multiply — S1, S2).


## Current handling
NOT PROMOTED as its own relation; CONSUMED as an input to v_contoso_order_line, where OrderKey is a degenerate dimension (the framework's degenerate_dimension pattern: a grouping key with no dimension table, modelled as a property of the fact rather than as a separate reference). Order- grain questions are answerable from the line relation by count(DISTINCT OrderKey) and by grouping on the header attributes it carries.


## Residual risk
An order-level FIGURE cannot be stored anywhere today. REVERSED IF: the delivery gains an order-level measure (freight, an order-level total, a header discount) — a line view can only repeat such a column, never hold it; or a question needs orders that have no lines (0 today, S1); or a header attribute stops being functionally determined by OrderKey. Any of those makes a second served relation at order grain the right answer, and it must then be promoted deliberately rather than by copying the line view.


## Sign-off required
operator — NAMED 2026-09-18, taking the seat run record Q5 left empty. Recorded as the ROLE rather than a personal name because this bundle is a public example; there is exactly one operator on this estate, so the role identifies them, and the vocabulary asks for "the named person or role — never 'the team', never a tool". They are the one who can say whether an order-level figure is expected in this delivery. Not yet ruled.


## Disposition

**accepted** — ruled by **operator**.

Ruled 2026-09-18 by the operator, this source's owner: the order header is consumed as an input to v_contoso_order_line and is NOT served as a relation of its own. Measured grounds, none of them in dispute: `main.orders` carries NO measure — nothing at order grain to sum; every one of its five non-key columns is functionally determined by OrderKey and every one is already served on the line; and 0 of its 93 470 headers has no line, so serving the line loses no order. A header view could therefore only restate the same values at a coarser grain under a second name, and `OrderKey` is served as a degenerate dimension so order-grain questions answer by count(DISTINCT OrderKey) and by grouping on the header attributes the line already carries.
THE ONE THING THIS SHAPE CANNOT DO, which is the whole reversal condition: an ORDER-LEVEL FIGURE has nowhere to live. A line view can repeat a header column but never hold one. So the day the delivery gains freight, a header discount or an order total, a second served relation at order grain becomes the right answer immediately — and it must then be promoted deliberately rather than by copying the line view. Also reversed if a question needs orders that have no lines (0 today), or if a header attribute stops being determined by OrderKey.

## Table
- [orders](../sources/orders.md)