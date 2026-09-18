# 0001 — The order line's fact of record: serve the header/detail pair, not `sales`

**Status:** RULED — the operator ruled on 2026-09-18; this record protocols the ruling and closes
`NS-ORDERS-01`.
**Audience:** whoever next reads `data/quality/data_quality_register.yaml` and wonders why a
high-severity entry is now low and closed; any agent authoring the ontology over this source.
**Author context:** the ingestion's promotion step (P3) registered the non-promotion and measured it;
the operator asked for the analysis to be protocolled, the criticality degraded and the case closed.
**Relates to:** `NS-ORDERS-01` · `NS-ORDERS-02` (the header, still open) ·
`data/datasets/v_contoso_order_line.yaml` · `data/datasets/v_contoso_fx_rate_day.yaml` ·
run record Q8 (the provenance ruling this record makes).

---

## 0. TL;DR

**The source delivers the order line twice. We serve the normalised pair and do not serve the
flattened copy. That is now a ruling, not an unresolved observation.**

`main.sales` and `main.orders` × `main.orderrows` are the same fact at the same grain, in exact
agreement. The pipeline measured this before the question was asked. What was missing was not
evidence — it was a human deciding **which one is the fact of record**, which is the one thing the
pipeline is not allowed to decide for itself. That decision is recorded here.

## 1. What the source ships

    main.orders      93,470 rows   OrderKey, CustomerKey, StoreKey, DT, DeliveryDate, CurrencyCode
    main.orderrows  223,974 rows   OrderKey, RowNumber, ProductKey, Quantity, UnitPrice, NetPrice, UnitCost
    main.sales      223,974 rows   OrderKey, LineNumber, OrderDate, DeliveryDate, CustomerKey, StoreKey,
                                   ProductKey, Quantity, UnitPrice, NetPrice, UnitCost, CurrencyCode,
                                   ExchangeRate

`sales` is the header joined onto the detail, flattened, plus one column — `ExchangeRate`.

## 2. What was measured

Measured by the promotion step (S4, S5) and by the source profiling (P1 R1–R4); the queries are
written out in full, with their answers, in `queries/p1_source_profiling.sql` and
`queries/p3_dataset_promotion.sql`. Independently re-derived on 2026-09-18 by a second reader
against the same database, with different SQL formulations.

| question | result |
|---|---|
| line keys in `orderrows` absent from `sales`, and the reverse | **0 and 0**, over 223,974 each way |
| joined lines disagreeing on ProductKey, Quantity, UnitPrice, NetPrice, UnitCost | **0** of 223,974 |
| `sales` lines with no header in `orders` | **0** |
| joined lines where `sales`' denormalised CustomerKey / StoreKey / CurrencyCode disagree with `orders` | **0** |
| `sales.ExchangeRate` reproduced from `currencyexchange` as USD → order currency, on the order's day | **223,974 of 223,974** |
| `sales.OrderDate` vs `orders.DT` (exact timestamp; `DT` carries no time component) | **0** disagreements |
| `sales.DeliveryDate` vs `orders.DeliveryDate` | **0** disagreements |
| all 13 `sales` columns reconstructed from `orders` × `orderrows` × `currencyexchange` | **0** rows differing, either direction |

Three things the independent re-derivation checked that the first pass did not, each of which could
have made the conclusion mean something else:

- **Both key sets are genuinely unique** — 223,974 distinct keys of 223,974 rows on each side, 0
  NULLs in the key columns. Without that, "0 rows differ either way" would not have meant what it
  looks like.
- **The FX join does not fan out.** `(Date, FromCurrency, ToCurrency)` is unique across
  `currencyexchange`'s 100,450 rows — a complete 25-pair × 4,018-date grid — and the join preserves
  cardinality exactly (223,974 in, 223,974 out). So the 100% is not an artifact of multiplication.
- **The comparison is NULL-safe.** Tested with `IS DISTINCT FROM`, and separately there are zero
  NULLs in any compared column on either side, so nothing could hide behind a NULL-blind `<>`.

**Nothing in `sales` is unavailable from those three relations.** Note the *three*: twelve of its
thirteen columns come from `orders` × `orderrows`, and `ExchangeRate` does not. "Serving the narrow
pair loses nothing" is only true because the rate is also served, at its own grain, in
`v_contoso_fx_rate_day` — with the USD-base, as-of-order-date convention written down (§4). Drop
that third relation and the claim is false.

## 3. The ruling

1. **`v_contoso_order_line`, built from `orders` × `orderrows` at (OrderKey, RowNumber), is the
   order line's FACT OF RECORD.** `main.sales` is measured, described and not served. This settles
   run record Q8, which the promotion step correctly declined to settle on its own.
2. **`NS-ORDERS-01` severity: `high` → `low`.** It never described a defect. It describes a
   redundancy in the delivery that has been resolved by choosing, with zero disagreement between
   the two candidates. A non-defect parked at `high` misreports this source's condition, and —
   under the rule that the ontology pipeline may not start until open issues are at an acceptable
   minimum — a non-defect at `high` would block the ontology indefinitely on bookkeeping rather
   than on data.
3. **`NS-ORDERS-01` status: `open` → `accepted`**, with `ruled_by` and `reason`, which
   `mac.dq_status.accepted` requires: *"A NAMED HUMAN EXAMINED IT AND CHOSE TO LIVE WITH IT."* The
   thing being lived with is the duplicate delivery upstream, which this bundle cannot fix and does
   not need to.
4. **The FX rule keeps its direction stated.** `ExchangeRate` is not served on the line. The rate is
   served at its own grain in `v_contoso_fx_rate_day`, which carries all five quotes on
   14,106/14,106 order-day-currency combinations — strictly more than the single USD-based direction
   `sales` carries.

## 4. Why the direction is stated and not left to be re-derived

Testing the *opposite* FX direction — order currency → USD — reproduces **113,627** of 223,974 rows.
Separately, exactly **113,627** lines carry `ExchangeRate = 1.0`. **These two sets are identical** —
the symmetric difference is 0 — because a rate of 1.0 is the same in both directions.

Say it that way and not "those are the USD orders", which is what the first pass said and is wrong
by thirteen lines. There are **113,614** lines on USD orders. The other 13 are five **EUR** orders
all dated **2022-08-31**, the one order date on which the source itself carries EUR→USD = 1.00000
and USD→EUR = 1.00000 — a par crossing. (The table holds exactly two par dates; the other, 2026-03-24,
has no orders.) The set that defeats direction-testing is "the lines whose rate is 1.0", which is a
property of the *rate*, not of the currency.

**So the wrong direction looks right on 51% of the data, and on 100% of any USD-only sample.** Per
currency the correct direction reproduces everything and the wrong one almost nothing:

| currency | lines | USD→ccy reproduced | of those, rate = 1.0 |
|---|---|---|---|
| USD | 113,614 | 113,614 | 113,614 |
| EUR | 49,203 | 49,203 | 13 |
| CAD | 24,250 | 24,250 | 0 |
| GBP | 22,829 | 22,829 | 0 |
| AUD | 14,078 | 14,078 | 0 |

The test is discriminating rather than a property of a smooth rate table: the same join taken as of
the *delivery* date reproduces only 181,680 rows, and as of order-date + 1 day only 155,788.

Anyone who re-derives this rule from a sample — or from a slice that happens to be USD-heavy — will
invert the rate on every non-USD order and get plausible, wrong numbers with no error anywhere. That
is why the direction is written down as a rule with its measurement attached, rather than left as a
column somebody copies.

## 5. What this closure rests on that is TRUE BUT UNPOLICED

The independent re-derivation returned one finding that nothing above would have surfaced, and it is
the most important sentence in this record:

> **This database declares zero constraints.** `duckdb_constraints()` returns 0 rows — no primary
> key, no foreign key, no unique. Every property in §2 is a fact about *this snapshot*, not an
> enforced invariant. Nothing stops the next load from breaking the agreement.

So the severity downgrade rests on a derivability that **is not gated**. A one-time proof is not an
invariant, and the reversal condition in the register ("a reload makes the agreement non-zero") is
currently something nobody would notice.

**Follow-up, named rather than assumed: an acceptance property that re-measures the agreement per
load.** `acceptance/` already exists in this bundle. Until that property exists, this case is closed
on evidence that is true and unpoliced — which is a different thing from closed on evidence that
will stay true, and the difference is written here so nobody has to guess which was meant.

A second snapshot-dependency, smaller but real: the FX rule matches on **exact date equality**. That
works only because the quote grid is gapless — 4,018 distinct dates over a 4,018-day span — and runs
to 2026-12-31 while orders stop at 2025-12-31. Today 0 orders fall outside it, with about a year of
headroom. An order dated off the grid, or a gap day, yields a silent NULL. An *as-of* join (latest
quote on or before the order date) would be robust where equality is not; that is a transform change,
not a ruling, and it is not made here.

## 6. What this does NOT close

- **`NS-ORDERS-02` — the order header.** It reads "the order header measured, deliberately not served
  as a relation of its own", and §3.1 above serves the header as an input to the line. Whether the
  header is *also* served as a relation in its own right is a separate modelling decision and is not
  ruled here. Note that `contoso_served.order_header` exists as a view in the warehouse, but
  `connection.yaml` records the seven views in that schema as leftovers of a deleted run — so that
  view is **not** evidence that this run served a header.
- **The SME owner.** `NS-ORDERS-01` records `sme_owner: UNNAMED — no owner is declared for any
  relation of this source`. The disposition is now ruled; the ownership is still nobody's.
- **Which direction the dependency runs upstream.** The data shows the two relations are identical.
  It cannot show whether `orderrows` is the original and `sales` the flattened copy, or the reverse.
  "Derivable" is true either way; the modelling story would be inverted.

- **What would reverse this.** Unchanged from the register and worth repeating: a reload that makes
  the agreement non-zero; upstream retiring `orders`/`orderrows`, which would make `sales` the only
  source of the line; or a ruling that `sales` is the delivery's fact of record — in which case the
  transform swaps its inputs and **the served values do not change**, because they were measured
  identical.

## 7. This entry was first closed as `resolved`, and that was wrong

**Corrected the same day. The error is kept here rather than edited away, because it is a worked
example of the exact failure the estate's dispositions exist to prevent — and the agent that made it
is the one the rule is aimed at.**

`resolved` was chosen for two stated reasons, and a third unstated one. The stated reasons: a
transform genuinely does dissolve the impurity, and `resolved` rests on a gate-checked cross-link
rather than on an unverifiable claim that somebody looked. The unstated one, which should have been a
warning rather than an attraction: it required no human name, which suited a bundle that is a public
example.

**The category error.** `mac.dq_status.resolved` means *a defect was dissolved by a transform*. An
`NS-` entry is a relation measured and deliberately not served. It was never a defect, so nothing
dissolved it. The transform's guarantee is real and the `resolves:` cross-link stays — but a
cross-link records what a transform guarantees, not that a defect existed and is gone.

**The hole it opened, which is the serious half.** `resolved` is the one term in the closed
vocabulary carrying `requires: []` — no `ruled_by`, no `reason`, nothing naming a human. The register
and the resolution map are both agent-writable. So an agent can close every entry in any register
with a word that names nobody. Under the rule that the ontology pipeline may not start until the
registered issues are dispositioned, that means **an agent could open its own gate** — and this entry
was that hole, standing open, with the coming gate cited in its own comment as the justification.

Three independent reviewers found it while designing that gate. It is now reject class
`resolved_on_non_defect` in `check_data_plane_approved`, which refuses `resolved` on any `NS-` id and
says why. The entry is `accepted`, `ruled_by: operator`, with the reason recorded — the disposition
that claims a human acted, carrying the evidence that one did.

The severity edit in §3.2 is left standing but it bought nothing: the gate reads **no severity at
all**. Its threshold is per-issue human coverage. A non-defect parked at `high` was never the thing
that could block the ontology; an undispositioned issue was.

## 8. A schema gap noticed on the way

`mac.dq_status` is a closed vocabulary with four terms. `accepted` and `wont_fix` mean "a NAMED HUMAN
examined it and chose to live with it" and **require `ruled_by` and `reason`**, because they are the
two terms that claim a human acted. `resolved` means "the defect is gone, dissolved by a transform
that says so", evidenced by the cross-link rather than by a ruling — which is why it requires no
`ruled_by`.

This entry takes `accepted` (§7). The `resolves:` cross-link is separate and stands on its own:
`one-delivery-of-the-line` always did establish one home per figure in the served plane, and it
withheld its `resolves:` for exactly one stated reason — Q8 — while `check_dq_resolution_sync` warned
about the missing link on **every run since**. Settling Q8 made the link declarable. What the link
records is what the transform guarantees; it is not, and was never, evidence that a defect existed
and is gone.

**The schema gap.** `mac.schema.json#$defs/DataQualityRegisterFile` declares an issue's properties as
`id, title, severity, confidence, finding, current_handling, residual_risk, sme_owner` — it declares
neither `status`, nor `ruled_by`, nor `reason`. Those keys validate only because
`additionalProperties` is unset. The vocabulary's requirement is nonetheless enforced, but by the
**gate** (`check_dq_resolution_sync`, reject class `ruling-missing`, reading the `requires:` list off
`mac_vocabulary.yaml#dq_status`) rather than by the schema. So an `accepted` with no `ruled_by`
passes schema validation and fails the gate — the law is honoured, in one place and not the other.

Registered here rather than fixed silently: it belongs to the framework schema, not to this bundle.
