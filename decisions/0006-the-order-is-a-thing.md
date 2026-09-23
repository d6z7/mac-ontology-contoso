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

No table is built, no view is added, no transform is written. An order is the group of lines that
share an OrderKey, and counting it is `COUNT(DISTINCT OrderKey)`.

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

## 3. THE EVIDENCE, AND WHY IT LICENSES AN `event` RATHER THAN A GROUPING

An order is **atomic** in this delivery. Measured 2026-09-24 over the served relation, per axis,
independently:

| axis | orders carrying more than one value |
|---|---|
| CustomerKey | **0** of 93 470 |
| StoreKey | **0** |
| OrderDate | **0** |
| CurrencyCode | **0** |
| DeliveryDate | **0** |

93 470 orders over 223 974 lines — minimum 1 line, mean 2.4, maximum 7, and 0 null OrderKey.

That is the whole basis for the class. A concept whose axes disagree with themselves would be a
derived grouping needing a collapse before anything could be read from it. This one does not: the
line's own CustomerKey **is** the order's, so `order__placed_by__customer` joins on the line's
column and the partition is total. The measurement is the edge's licence, which is why each edge's
`resolved_by` points at the atomicity rule rather than at a resolution rule.

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

**No claim that delivery is part of the order.** An order agrees on `DeliveryDate` today, measured.
Whether that is law or a property of this snapshot is **ORD-Q2**: an order that shipped in two
parts would drop `DeliveryDate` from the atomicity rule and leave the lifecycle without a single
phase.

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

1. no order disagrees with itself on any of the five axes — the basis for the `event` class;
2. no served line carries a null OrderKey — a null would be a line no order owns, silently dropped
   by the distinct count.

Gates at adoption: `validate_schema` 0 findings on the new files, `check_references` 0 errors,
`check_shapes` OK over 9 shapes × 20 concepts.
