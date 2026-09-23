# 0006 — The order is a thing, and the bundle only modelled its lines

**Status:** ADOPTED — operator ruling, 2026-09-24 ("do ... but protocol decision").
**Date:** 2026-09-24
**Depends on:** [0001](0001-order-line-fact-of-record.md) (the line is the fact of record) · [0005](0005-what-we-learned-and-what-supersedes-0002-0004.md) (the runtime does not read what is declared)
**Supersedes:** nothing. 0001 stands unchanged — this is a second, coarser grain over the same rows.

---

## 1. THE DECISION

Declare `Order` as an `event` concept over `v_contoso_order_line`, with
`identity.canonical_key: OrderKey`, and three edges: to its lines, to the customer who placed it,
and to the store it was placed at.

No table is built, no view is added, no transform is written. An order is counted as
`COUNT(DISTINCT OrderKey)` over the served line relation.

> **CORRECTION 2026-09-24, operator finding.** An earlier revision of this record said *"there is
> no order table and none should be built"*. **That is false.** `main.orders` exists in the
> landing — 93 470 rows, exactly this concept's member count, carrying OrderKey, CustomerKey,
> StoreKey, DT, DeliveryDate and CurrencyCode. The bundle has always known: the served view's own
> transform names it in its INPUTS line as *"the header"*. What is true is narrower and is what
> this decision actually rests on: **nothing SERVED is at order grain**, so the concept grounds on
> the line relation it can reach. A served order header would be the better home and §8 records
> that as open.

## 2. WHAT FORCED IT

The corpus asks *"How many orders were placed in 2024?"*. The bundle could not answer it — not
because the data is missing, but because nothing declared that an order is a thing. The refusal
read `OrderLine.measure_column`, which is a true statement about the line and an unhelpful one
about the question.

**The error it prevents is not a refusal, it is a wrong number.** Before this concept existed, the
nearest answerable question was the line count:

| | 2024 |
|---|---|
| orders (`COUNT(DISTINCT OrderKey)`) | **15 899** |
| lines (`COUNT(*)`) | 38 109 |
| | **2.40×** |

Both are plausible. Neither carries a symptom. A reader handed 38 109 for "how many orders" has no
way to know.

The same factor sits under every per-order average. *"Average order value"* divided by the line
count is 2.40× too small — and the corpus asks that too (ADV-08, ADV-09).

## 3. WHY AN ORDER IS ATOMIC — AND WHY THE FIRST VERSION OF THIS SECTION PROVED NOTHING

An order carries one customer, one store, one date, one currency and one delivery date. Measured
2026-09-24 over the served relation, per axis, independently:

| axis | orders carrying more than one value |
|---|---|
| CustomerKey | **0** of 93 470 |
| StoreKey | **0** |
| OrderDate | **0** |
| CurrencyCode | **0** |
| DeliveryDate | **0** |

93 470 orders over 223 974 lines — minimum 1 line, mean 2.4, maximum 7, and 0 null OrderKey.

**THOSE ZEROES WERE A TAUTOLOGY AND ARE KEPT ONLY TO SAY SO.** The served relation is
`main.orderrows JOIN main.orders ON OrderKey`. All five of those columns come from the ORDERS
row — one row per order — so every line of an order inherits them by construction. Measuring that
they agree measures that a join on a unique key yields constant values. It could not have come out
any other way, and a measurement that cannot fail is not evidence.

**The real basis is structural, and it is stronger.** Those five columns live on an order header
that holds exactly one row per order. The atomicity is not a property of this delivery that might
lapse; it is what the landing's shape means. That is what licenses `event` and what licenses
`order__placed_by__customer` joining on the line's column — the line's CustomerKey *is* the
header's, because the view put it there.

The constraint in §7 is kept, with its purpose corrected: it no longer claims to establish
atomicity. It detects the day the served view stops being that join.

## 4. WHY THIS IS NOT THE MISTAKE 0005 WARNS ABOUT

0005's finding is that this estate proposes **new declarations** where it should wire the ones it
has. That test was applied here before anything was written, and the answer is that nothing
existing carries this:

* `OrderLine.identity.canonical_key` is deliberately absent — its grain is the two-column cell key
  `(OrderKey, RowNumber)`, with measured evidence and a paragraph saying why no single column is
  the identity. **That declaration is correct and is left untouched.** It is a statement about the
  line, and it cannot also be a statement about the order.
* No rule, edge, register or field role names an order as a countable thing.

So the fact was genuinely undeclared rather than declared-and-unread. The distinction is the one
0005 exists to force, and it is recorded here because the next concept proposed should have to
pass the same test.

## 5. WHAT IS DELIBERATELY NOT DECLARED

**No order-level money measure.** A per-order total is a line sum grouped by OrderKey. Whether that
deserves to be a named measure — with its own default reading and currency disclosure — or stays a
grouping of `NetSalesAmount` is a modelling decision nobody has made. Recorded as **ORD-Q1**, and
it blocks *"average order value"* alongside the engine's missing division.

**No line measures on the Order concept.** `Quantity`, `UnitPrice`, `NetPrice` and `UnitCost` are
not in its grounding. They belong to the line, and summing them under an order's name is a question
about lines wearing the wrong label.

**No claim that delivery is part of the order.** `DeliveryDate` sits on the order header, so an
order has exactly one — by the landing's shape, not by measurement (§3). Whether a business order
CAN ship in two parts, and the landing simply cannot express it, is **ORD-Q2**. That is a question
about the source system, not about this data, and no query here can answer it.

## 6. CONSEQUENCES

* *"How many orders were placed in 2024"* and *"...in euros during Q1 2024"* answer, at the grain
  asked — 15 899, not 38 109.
* *"Orders by customer country"* works with no further declaration: the planner walks
  `order__placed_by__customer` then `customer__resides_in__country`, which is the edge earning its
  place on the day it was written.
* The corpus's two `sme:no-order-concept` rows are closed.
* `ADV-08` / `ADV-09` are **not** closed. They now have a correct denominator available and still
  need the engine to divide, which it cannot — that is the planner's gap, recorded in the
  framework's `grammar/query_grammar.yaml`, not this bundle's.

## 7. HOW IT IS ENFORCED

Two machine-executable constraints on the concept, both out-of-set queries that go non-zero the
moment the claim stops being true:

1. no order disagrees with itself on any of the five axes. **Not evidence of atomicity** — see
   §3 — but a tripwire: it goes non-zero the day the served view stops being a join to a
   one-row-per-order header, which is the day this concept's grain claim would quietly stop
   holding;
2. no served line carries a null OrderKey — a null would be a line no order owns, silently dropped
   by the distinct count.

Gates at adoption: `validate_schema` 0 findings on the new files, `check_references` 0 errors,
`check_shapes` OK over 9 shapes × 20 concepts.

## 8. WHY THE HEADER IS NOT SERVED — and it is a RULING, not an omission

`main.orders` is the header and it is deliberately not promoted. The bundle decided that on
2026-09-18 and wrote it down: **register NS-ORDERS-02**, cited by the line dataset's own `OrderKey`
column, which calls it *"a DEGENERATE DIMENSION here: the order header is not served as a relation
of its own"*.

Its reasoning, and it is good:

* `main.orders` **carries no measure** — OrderKey, CustomerKey, StoreKey, DT, DeliveryDate,
  CurrencyCode and nothing else.
* Every non-key column is functionally determined by OrderKey and is **already served on the line
  relation**, so a header view would restate the same facts at a coarser grain under a second name.
* Serving the line loses no order: 0 of 93 470 headers have no line, and the join cannot fan out.
* The prescribed handling is exactly what this concept does: *"Order-grain questions are answerable
  from the line relation by count(DISTINCT OrderKey) and by grouping on the header attributes it
  carries."*

**THE REGISTER NAMES ITS OWN REVERSAL CONDITIONS, AND ALL THREE FAIL TODAY** (re-measured
2026-09-24): no order-level measure exists; 0 orders have no line; 0 orders disagree with
themselves on any header attribute. So the ruling stands, and this concept is the shape it
prescribes rather than a workaround around it.

> **CORRECTION 2026-09-24.** An earlier revision of this section offered cutting
> `v_contoso_order_header` as an open alternative "not large, and out of scope". That was wrong
> twice: it was already ruled against, and it was written without reading the register the line
> dataset points at from the very column in question. The view was in fact cut and then reverted
> when the register was found. What reverses NS-ORDERS-02 is one of its three conditions being
> met — not a preference about which relation reads more naturally.

### What the concept pays for that ruling, visibly

* the sample's `population` is 223 974 — the host ROWS the concept claims, not its 93 470 members.
  Consistent with every key-grain concept (`Currency` records the same number for the same reason).
  The sampler now leads its line with the MEMBER count, so the first number a reader meets is
  93 470.
* the grain claim depends on the served view remaining a join to a one-row-per-order header, which
  is what the §7 tripwire watches.

Both are the cost of a degenerate dimension, which is a named pattern with known ergonomics — not
a defect to be designed away.

### And the delivery this bundle deliberately does not read

`main.sales` holds the same 223 974 lines flat, keyed `(OrderKey, LineNumber)`, carrying the
header's columns and `ExchangeRate` besides. The transform names it and refuses it: *"the DOUBLE
DELIVERY … repeats these 223 974 lines with 0 differences over 10 columns … one figure, one home"*
(register NS-ORDERS-01). `LineNumber` and `orderrows.RowNumber` are the SAME ordinal — both range
0..6 and agree on all 223 974 rows — so a reader who knows this source as `(OrderKey, LineNumber)`
is describing the same key `OrderLine` declares as `(OrderKey, RowNumber)`. The name differs
because the bundle serves the normalised pair and not the flat one.
