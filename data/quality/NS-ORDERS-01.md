---
type: DQ Issue
title: '`sales` measured, deliberately not served — it is the served order line delivered
  a second time'
description: 'Measured 2026-09-18. `main.sales` (223 974 rows, 13 columns) carries
  the same line population as `main.orderrows` at the same cell key: (OrderKey, LineNumber)
  EXCEPT (OrderKey, RowNumber) returns 0 ro'
tags:
- CONTOSO
- severity:low
- confidence:I
- lifecycle:draft
- resolution:resolved
---

`NS-ORDERS-01` · severity **low** · confidence **I** · resolution **✓ resolved** · disposition **accepted · ruled by operator**

## Finding
Measured 2026-09-18. `main.sales` (223 974 rows, 13 columns) carries the same line population as `main.orderrows` at the same cell key: (OrderKey, LineNumber) EXCEPT (OrderKey, RowNumber) returns 0 rows in both directions (P2 G3, S4), so LineNumber and RowNumber are the same values. Joined line-for-line to `orderrows` x `orders`, it differs on NOTHING: 223 974 matched lines and 0 differences across ProductKey, Quantity, UnitPrice, NetPrice, UnitCost, CustomerKey, StoreKey, OrderDate, DeliveryDate and CurrencyCode (S5; P1 R1-R3 measured the same over the same denominator). It carries exactly one column the header/detail pair does not — ExchangeRate — and that column reproduces the currencyexchange USD->CurrencyCode quote for the row's day on 223 974/223 974 rows, 0 missing quotes, 0 differences (P1 R4).


## Current handling
NOT PROMOTED. No dataset descriptor, and no transform consumes it; its raw descriptor (data/sources/sales.yaml) and its profile stay, so the measurement is not lost. The served line relation is v_contoso_order_line, built from orders x orderrows at (OrderKey, RowNumber). ExchangeRate is not served on the line either: the rate is served at its own grain in v_contoso_fx_rate_day, where every pair a question can ask is present (100 450 = 4 018 x 5 x 5, complete; all 5 quotes out on 14 106/14 106 order-day-currency combinations — S16, S17), which is strictly more than the one USD-based direction sales carries. Serving both relations would give every figure in this bundle two defensible answers and the engine would pick by accident.


## Residual risk
RULED 2026-09-18 (operator): `v_contoso_order_line`, built from orders x orderrows at (OrderKey, RowNumber), IS the order line's fact of record; `main.sales` is measured, described and not served. That settles run record Q8, which the promotion step correctly declined to settle on its own. Protocol: decisions/0001-order-line-fact-of-record.md.
WHAT REMAINS OPEN, and it is not the modelling. The derivability this closure rests on is a fact about THIS SNAPSHOT and is enforced by nothing: an independent re-derivation on 2026-09-18 reconstructed all 13 sales columns from orders x orderrows x currencyexchange with 0 differences either way (multiset and full-outer-join formulations both), and in the same pass measured that this database declares ZERO constraints — no primary key, no foreign key, no unique — so nothing stops the next load from breaking the agreement. A one-time proof is not an invariant. FOLLOW-UP: an acceptance property that re-measures the agreement per load, so the reversal condition below is detected rather than assumed. Until that exists, this entry is closed on evidence that is true and unpoliced.
A SECOND SNAPSHOT-DEPENDENCY, in the FX join: the rate is matched on exact date equality, which works only because the quote grid is gapless and runs a year past the newest order (4 018 dates, 0 orders outside it today). An order dated off the grid yields a silent NULL. An as-of join (latest quote on or before the order date) would be robust where equality is not.
REVERSED IF: a reload makes the agreement non-zero, i.e. sales and the pair stop agreeing; or upstream retires `orderrows`/`orders`, making sales the only source of the line; or a human re-rules that `sales` is the fact of record (then the transform swaps its inputs and the served columns are unchanged — the values were measured identical). Note also that the data cannot say WHICH direction the dependency runs upstream: it shows the two are identical, not that `orderrows` is the original.


## Sign-off required
operator — NAMED 2026-09-18, taking the seat run record Q5 left empty. Recorded as the ROLE rather than a personal name because this bundle is a public example; there is exactly one operator on this estate, so the role identifies them, and the vocabulary asks for "the named person or role — never 'the team', never a tool". The delivery contract's owner is the operator, and they have ruled on this entry — see decisions/0001.


## Disposition

**accepted** — ruled by **operator**.

The delivery ships the order line twice and always will; this bundle serves one of them and describes the other. Ruled 2026-09-18 by the operator, who is this source's owner: the header/detail pair (orders x orderrows at OrderKey, RowNumber) is the order line's FACT OF RECORD and `main.sales` is measured, described and not served — settling run record Q8, which the promotion step correctly declined to settle on its own. Nothing is lost by the choice: `sales` is exactly reconstructible from orders x orderrows x currencyexchange, measured twice independently at 0 differences either way across all 13 columns. What is tolerated rather than fixed is the upstream redundancy itself. Evidence, reversal conditions and the two snapshot-dependencies this rests on: decisions/0001-order-line-fact-of-record.md.

## Resolution

**✓ resolved** — 

- Dissolved by [v_contoso_order_line](../transforms/v_contoso_order_line.md)

## Table
- [sales](../sources/sales.md)