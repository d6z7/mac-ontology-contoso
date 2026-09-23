---
type: Reference
title: NS-ORDERS-02 — the order header measured, deliberately not served as a relation of its own
tags: [reference, guardrail]
---

# NS-ORDERS-02

*low · confidence I*

**Finding.** Measured 2026-09-18. `main.orders` (93 470 rows, 6 columns) carries no measure: its columns are OrderKey, CustomerKey, StoreKey, DT, DeliveryDate, CurrencyCode. Every one of its 5 non-key columns is functionally determined by OrderKey (measured, P2) and every one of them is served on the line relation, so a header view would restate them at a coarser grain under a second name. Serving the line loses no order: 0 of the 93 470 headers have no line (S1), and the inner join keeps exactly the line population with no fan-out (223 974 joined rows = 223 974 orderrows rows; 93 470/93 470 distinct OrderKey in orders, so the join cannot multiply — S1, S2).


**Current handling.** NOT PROMOTED as its own relation; CONSUMED as an input to v_contoso_order_line, where OrderKey is a degenerate dimension (the framework's degenerate_dimension pattern: a grouping key with no dimension table, modelled as a property of the fact rather than as a separate reference). Order- grain questions are answerable from the line relation by count(DISTINCT OrderKey) and by grouping on the header attributes it carries.


**Residual risk.** An order-level FIGURE cannot be stored anywhere today. REVERSED IF: the delivery gains an order-level measure (freight, an order-level total, a header discount) — a line view can only repeat such a column, never hold it; or a question needs orders that have no lines (0 today, S1); or a header attribute stops being functionally determined by OrderKey. Any of those makes a second served relation at order grain the right answer, and it must then be promoted deliberately rather than by copying the line view.


**Resolution.** Not yet reconciled (newly harvested) — an honest open item.

