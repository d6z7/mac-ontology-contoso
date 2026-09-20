# 0004 — The fold plane: one law was three, and the guard was pointed the wrong way

**Status:** PROPOSED — only the operator may ratify. A working prototype exists and is measured; no
part of it has landed. Two points ARE ruled, inline, and marked so.
**Audience:** whoever next reaches for `MeasureType` to say why a number must not be summed; anyone
adding a fourth home for what a column means; whoever wonders why the console offered
`Total Exchange Rate`.
**Author context:** the operator asked three questions in sequence — what properties carry these
values and at what level, how the planner handles the combinations, and what the complete set of
cases is. Then, on reading the matrix, observed that `average` repeats itself across `Intensive`'s
two axes and asked whether the categorisation might be "either incomplete and/or inconsistent". It
is both, and the reason is structural rather than a missing member. Eleven agents measured it; the
operator then ruled on `Target` and asked whether sort order belongs here too. It does.
**Relates to:** `decisions/0003-semantic-types-for-columns.md` (its Phase 0 diagnosis stands; its
class-gate test and its `_EXCLUSION_KIND` claim are measured wrong — §9) ·
`decisions/0002-answering-questions-about-the-model.md` (THE LINE; not restated) ·
`mac_vocabulary.yaml#MeasureType`, `#axis_kind`, `#aggregation_effect` (what this replaces) ·
`ontology/concepts/order/order_line.yaml` (the degenerate-dimension prose that has no term).

---

## 0. TL;DR

The fold law reads a field that is empty on **17 of 17** concepts, is stated at a grain coarser than
the thing it governs, and is consulted on the axes a question **preserves** rather than the axes it
**folds**. Measured over 18 enumerated cases across three bundles, the outcome is correct on
**3 of 18** and follows from a declaration the runtime actually read on **1 of 18**.

`MeasureType` is not incomplete. It is three different facts fused into one term at one grain:

| fused into `MeasureType` | is really | and belongs on the |
|---|---|---|
| Flow / Stock / Intensive | how a quantity behaves under folding | **COLUMN** |
| Precomputed | how the relation's rows came to exist | **RELATION** |
| Target | whether the figure is observed or planned | **CONCEPT** |

`Precomputed` and `Target` carry identical additivity rows — **2 of 10 cells with no information** —
precisely because neither was ever a statement about folding. Splitting the three planes makes the
redundancy disappear rather than papering over it with a sixth member.

A prototype of the split takes the 18 cases from **3 of 18 to 16 of 18** with **0 regressions** and
both suites at baseline (671 passed / 1 skipped; 758 passed / 2 skipped). The bundle's six
`aggregation` contract rules — prose the type system could not say — go from **2 of 6** expressible
as declarations to **6 of 6**, five of them also executable.

---

## 1. WHAT IS MEASURED, BEFORE ANY PROPOSAL

### 1.1 The guard is inert

`_check_additivity` reads `concept.semantics.additivity`. That dict is empty on **17 of 17**
concepts, so the read returns `None` and the guard answers "no violation" every time. It is not a
weak guard; it is an unreachable one. The data it needs is one field away and populated:
`measure_type` on **3 of 3** measures, `axis_kinds` on **3 of 3**.

### 1.2 The law is not in the runtime

`MeasureType` appears in **0 of 62** runtime source files. The matrix is authored in the framework
repository and mirrored nowhere the planner reads. The bundle's own `vocabulary.json` mirrors nine
namespaces — including the superseded two-term `concept.semantics.additivity` scale — and not
`MeasureType`, `axis_kind` or `aggregation_effect`.

### 1.3 The grain is coarser than the claim

One `measure_type` covers every measure column a concept declares. The bundle contradicts itself on
its own fact:

```
GrossSalesAmount   measure_type: Flow        columns: [Quantity, UnitPrice]
                   Flow = additive on both axes
  its own rule:    never "SUM(UnitPrice) x SUM(Quantity), or SUM(UnitPrice) alone
                   -- a price is per unit"
```

`Quantity` is a flow; `UnitPrice` is not. `OrderLine` declares **four** measure columns and no
`measure_type` at all. The type system says the fold is legal; the contract rule says it is wrong;
both are in the same file.

### 1.4 The guard is pointed the wrong way

`GROUP BY` **preserves** an axis. Folding happens on every axis a question does **not** group by.
Instrumented:

```
"total gross sales"  (bare)            consulted on []  ZERO axes      -> Plan
"gross sales by country"               consulted on ["country"]
"gross sales by country and product"   consulted on ["country","product"]
```

The check fires on the axes that survive and never on the axes that are collapsed. The bare total
folds **every** axis at once and is examined on none: **11 of 11** typed measures across three
bundles emit a plain `SUM` for a bare total, and **7 of 11** are measures the matrix itself says must
not be SUM-folded over time.

### 1.5 The score

Over 18 cases (§3): outcome-correct on **3 of 18**; governed by a declaration the runtime read on
**1 of 18** — and that one is governed by `field_role: key`, outside the additivity system entirely.

---

## 2. THE POSITION: FOUR PLANES, NOT ONE TERM

### 2.1 The property table

Grain is the load-bearing column. Tier counts are measured on this bundle.

| property | grain | vocabulary | tier here | authored by |
|---|---|---|---|---|
| `quantity_kind` | **column** | `extensive · intensive · indicator · ordinal · identifier` | 18 derived / 8 confirmed / 3 inferred of 29 | gate fills `identifier`; SME rules the rest |
| `per` (the extent) | column | a column on the same relation, or `__rows__` | 7 of 29, all confirmed | SME |
| `denominated_by` | column | a unit column (+ its distinct count) | 4 of 29 confirmed; the count derived | SME + profile |
| `grain_semantics` | **relation** | `event · observation · plan · precomputed` + `UNKNOWN` | 5 of 6 relations | gate proposes, SME rules |
| `observation{subject_key, observed_at}` | relation | two column names | **1 of 1, 0 authored — fully derived** | gate |
| `cell_key` | relation | the declared source key | 5 of 5 derived | gate |
| `counts_as` | concept | a column name | 1 of 17 confirmed | SME — the law refuses to pick |
| `modality` | concept | `observed · planned` — never a fold input | default `observed` | SME |
| `sentinel{column, member, share}` | axis | member + profile share | **0 of 17 machine-readable today** | SME (share derived) |
| `partition_role` / `ordered` | axis | `partitions · reobserves · revision` + `UNKNOWN` | derived from the relation facts | gate |
| `mac.fold_op` | framework | 10 operators, each with a stage and a `composes` flag | framework law | framework |
| `LAW[grain_semantics][quantity_kind]` | framework | **25 of 25 cells** | derived — a pure lookup | framework |
| `provenance_tier` | **every entry** | `derived · inferred · confirmed`; silence means `inferred` | 0 mandatory authoring | nobody |

`mac.axis_kind` is **not read**. It asked two questions at once and neither of them was temporality.

### 2.2 What is deleted, and what is only deprecated

**RULED (operator, 2026-09-20): `Target` is deleted as a fold class.** A monthly goal summing to an
annual goal is correct arithmetic. `Target` fused a provenance claim with a fold claim; a planned
quantity now declares `extensive` plus `modality: planned`, folds by `SUM`, and carries a mandatory
"this is a plan figure, not an observation" disclosure. Cases 9 and 10 are the only 2 of 10 matrix
cells this record contradicts, and the drift test records both as a DECLARED DIVERGENCE rather than
hiding them.

`Precomputed` likewise stops being a fold class and becomes `grain_semantics: precomputed`, a fact
about the relation. Its "never half a pair" content is already the declared `cell_key` and needs no
new property.

**`semantics.additivity` is deprecated, never deleted.** `ConceptSemantics` is `extra="forbid"` and
the schema is `additionalProperties: false`, so removing the field stops **13 of 13** files parsing
— and three of them are behind the armed ontology lock and may not be edited. The field stays
parsed, stays first, and stops being the law. `measure_type` and `axis_kinds` become unread
projections.

### 2.3 The corrected predicate

The law is consulted on `FOLDED = axes(FACT) \ (partitioned ∪ pinned)`, not on the axes a question
names. Measured: before, the guard sees 0–2 axes; after, 3–10. The bare total moves from **0 axes
for 11 of 11** typed measures to the maximal case, and **4 of 11** bare totals refuse where all 11
previously emitted a plain `SUM`.

---

## 3. THE EIGHTEEN CASES

Ten are the matrix's own cells; eight fall outside it, and six of those eight are this bundle's own
`aggregation` contract rules — prose the type system cannot say.

| # | case | before | after |
|---|---|---|---|
| 1 | extensive × time | SUM | SUM |
| 2 | extensive × categorical | SUM | SUM |
| 3 | level × time | SUM over every snapshot day | collapse to the end cell per subject, then fold |
| 4 | level × categorical | wrong refusal | **unchanged — held wrong by the precedence below** |
| 5 | intensive × time | SUM of durations | `AVG` + a non-composition disclosure |
| 6 | intensive × categorical | SUM of a rate | `SUM(x·w)/NULLIF(SUM(w),0)` |
| 7 | precomputed × time | SUM over 365 stored quotes | refuse: no stored cell at that grain |
| 8 | precomputed × categorical | SUM **+ an empty ON clause** | the same refusal, before invalid SQL is built |
| 9 | plan × time | SUM, no disclosure | SUM + the plan disclosure |
| 10 | plan × categorical | SUM, no disclosure | SUM + the plan disclosure |
| 11 | overlapping views | refused upstream for an unrelated reason | **unchanged — a join defect, not a fold defect** |
| 12 | incommensurable units | silent SUM across five units | refuse, naming pin / group / convert |
| 13 | flag as quantity | `SUM(flag)` | `COUNT(*) FILTER (WHERE flag = 1)` |
| 14 | entity-count identity | `SUM(floor_area)` | `COUNT(DISTINCT <the declared code>)` |
| 15 | ratio / derived | SUM of a ratio | `SUM(n)/NULLIF(SUM(d),0)` |
| 16 | identifier columns | governed already | unchanged |
| 17 | sentinel members | no fold-time disclosure | the member, its row share and its value share |
| 18 | republication collapse | partitions by the version key — a silent no-op | partitions by the declared subject key |

**Correct before: 3 of 18. Correct after: 16 of 18. Changed: 13 of 18. Regressed: 0 of 18.**

Three honesty notes, two of which move the number.

* The 18-case list as first written is **internally inconsistent**: cases 2 and 12 are the same
  question with opposite expectations. They are separated here by whether the unit axis is pinned.
  That was an error in the enumeration, not in the design.
* Case 3's predicate was changed from "never a SUM" to "resolve the end cell per subject, *then*
  fold". The literal original predicate would score this case failed even when correct, because
  collapse-then-sum is the right number across subjects. Under the original wording: 15 of 18.
* Cases 9 and 10 are scored strictly — the disclosure is required, not just the SUM. Scored
  leniently, before is 5 of 18 and after is still 16 of 18.

**Case 4 is held wrong by a constraint this record imposes** (§5). Lifting it gives 17 of 18.

---

## 4. SORT ORDER

The operator asked whether sort belongs in this discussion, having noticed that the design governs
`GROUP BY` and says nothing about `ORDER BY`. It belongs, in three of its four roles.

Measured first: the planner emits **no `ORDER BY`** in any outer query. `Intent` carries no sort and
no top-N. The single `ORDER BY` anywhere in the runtime is inside the reporting-cycle collapse — and
that one was, until 2026-09-20, iterating a scalar `order_by` into its individual letters, emitting
`ORDER BY O DESC, p DESC, e DESC, ...`. Sort already carries meaning in exactly one place, and
nothing governed it.

**Role 1 — order as truth-selection.** `ROW_NUMBER() OVER (PARTITION BY … ORDER BY … DESC)` does not
sort a result; it *chooses which row is true*. A wrong ordering column returns an arbitrary row per
cell with no symptom on the page. This is a declaration and belongs under the same discipline as the
partition it accompanies.

**Role 2 — order as the enabling condition for a family of operators.** `ordinal` is defined as
order without arithmetic: rankable, never summable, never averaged. `LAST`/`FIRST` (the end-of-period
cell), `MEDIAN`, `PERCENTILE`, running totals, moving averages and period-over-period deltas are all
folds that **cannot be expressed** without a declared order. An operator vocabulary that omits order
can express `SUM` and little else.

**Role 3 — axis orderedness.** Some categorical axes are ordered — an age band, a size, a severity —
and `mac.axis_kind` cannot say so, because it conflates ordered-ness with temporality. Orderedness
gates every cumulative fold and decides whether a breakdown is presented in its own sequence or
alphabetically. Derivable for temporal columns; declarable for ordered categoricals; absent for
nominal ones.

**Role 4 — result determinism — is DELIBERATELY EXCLUDED from the fold law, and recorded here as a
separate finding.** Which rows to show, in what sequence, and how many, is a question-and-
presentation concern. A fold law that starts asserting presentation order commits exactly the fusion
this record convicts `MeasureType` of. But the finding is real, and it is the same defect class as
the `declared[0]` bug fixed the same day:

| | picks one silently, by |
|---|---|
| `declared[0]` in the column choosers | the author's YAML ordering |
| a grouped result with no `ORDER BY` | parallel aggregation order — *measured to differ between processes on identical data* |
| a truncated result with no `ORDER BY` | storage order: an arbitrary subset |

The estate has already met the second and bought determinism from the engine rather than the plan —
the DuckDB adapter pins worker threads to one so that generated fixtures are byte-stable. `plan()`'s
docstring promises a byte-identical *plan*; nothing promises a stable *result*. That gap deserves its
own record.

---

## 5. WHAT IS RULED, WHAT IS OPEN

**RULED — `Target` is deleted as a fold class** (operator, 2026-09-20). §2.2.

**RULED — precedence is decided after this design is ratified** (operator, 2026-09-20). Until then
`semantics.additivity` is read FIRST and the fold law is consulted second, which is what keeps the
three lock-blocked fixtures untouched. Lifting it later costs **6 of 1429** named tests and moves
the score from 16 of 18 to 17 of 18.

Open, each answerable in a word:

**Q1 — what does an intensive quantity emit when no extent is declared?**
*Recommendation: make `per:` mandatory on every `intensive` column and CLARIFY when it is absent.*
The arithmetic forces it: a plain mean does not compose (32.000000 one-shot against 32.500000
staged on the same data), a weighted mean does (identical to six decimals). A silent plain mean is
a wrong number that looks like a right one.

**Q2 — may a measure that declares nothing be folded at all?**
*Recommendation: not yet.* Failing closed globally costs **142 of 1429** tests today. Ship
open-world with a disclosure and make closed-world a per-bundle opt-in, flipped once that bundle's
plane is complete.

**Q3 — which properties must be SME-confirmed rather than left inferred?**
*Recommendation: `quantity_kind` on every `field_role: measure` column, `per`, `denominated_by`,
`counts_as`, sentinel members, and any axis relation.* Measured: **0 of 9** measure columns get a
sound `quantity_kind` from any declared type or profile statistic. Leave derived and un-tokened:
`identifier`, the observation fact, `cell_key`, the profile shares.

**Q4 — add `no_fold_law` to `ReasonCode` and a `fold_disclosure` caveat kind?**
*Recommendation: yes.* The prototype smuggles seven sub-codes through a `missing[0]` prefix to keep
the golden schema test green. That is a workaround and should not survive into the landing.

**Q5 — which of the eight multi-column equivalence classes are one axis?**
*Irreducibly the operator's.* Two of the eight are demonstrably wrong to collapse: the data says
they are one and the bundle's own prose says the coincidence "is not declared to be law".

**Q6 — does `quantity_kind` need a sixth term?**
*Recommendation: no, and record why.* A cyclic quantity — an angle, a time of day — folds by
circular mean and is neither extensive nor intensive. Nothing in this estate has one. Adding a term
for an absent case is precisely the move that left `MeasureType` with five members and a header
miscounting its own cells.

---

## 6. THE AUTHORING COST

Zero mandatory. `provenance_tier` defaults to `inferred` on silence; the gate fills every derivable
entry. On this bundle the authored half is **83 non-comment lines** carrying 14 provenance tokens.

The one new obligation is honest rather than incidental: a `field_role: measure` column now wants a
`quantity_kind`, and **0 of 9** of them can be derived. That is 9 rulings on this bundle, each one
word, each recording a fact an SME already knows and the model currently cannot hold.

---

## 7. WHAT THIS DOES NOT BUY

Median and percentile share one mean family with no operator parameter. Time-weighted means cannot
be stated — `per:` names a column and an interval length is not one. Composite and scaled units
(thousands of a currency) are not expressible. No property is a function of the question's filters,
so conditional additivity is out. The law refuses, correctly, to pick between two declared count
candidates. At what share a sentinel invalidates rather than annotates is undecided — a 41.8 % share
is disclosed, never refused. Overlap *within* one axis's member set has no term. Fold order when two
independent re-observation axes meet is undefined.

And one boundary worth stating plainly: **no SQL was executed.** Every outcome measured is a plan or
a refusal, never a number. The emitted windows and distinct counts are syntactically right and
numerically unverified.

---

## 8. THE COMPLETENESS ORACLE

This bundle authors 28 contract rules, **28 of 28** carrying machine-readable `binds`; six are kind
`aggregation` and state in prose six things the type system cannot say. They are the test, because
they were written by someone who knew the domain and had nowhere structured to put it.

**Before: 2 of 6 are declarations** — and both of those reach the SQL through `derived_by_rule`, a
route with nothing to do with `MeasureType`. **After: 6 of 6 are declarations, 5 of 6 also
executable.** The one that is declarable but not executable is blocked by an unrelated join defect,
not by the fold law.

---

## 9. WHAT THIS CORRECTS IN 0003

0003's Phase 0 diagnosis stands and this record is built on it. Two of its specifics are measured
wrong and should not be carried forward:

* **The class gate.** 0003 specifies refusing any concept whose class is not `measure`. Measured
  across the framework's example bundles, that refuses a concept which declares
  `field_roles: {<column>: measure}` — the author *has* said what number it carries — while emitting
  "nothing declares a number it carries", a false statement on the wire. The gate must read both
  homes. This was corrected before landing.
* **Widening the exclusion kind.** 0003 calls it "the cheapest finding of the night" and names four
  facts it would activate. Measured, composed with the gate, it activates **0 of 17**; standalone it
  activates **1 of 6** aggregation rules, and as specified it converts four governed refusals into
  uncaught exceptions. It is not shippable in that form.

0003's central claim — that the role SELECTS and the type REFUSES, and that the type belongs on the
column — survives all of it, and is what §2 implements.

---

## 10. WHAT WOULD REVERSE THIS

* A bundle where `grain_semantics` at relation grain is sufficient for every measure sharing that
  relation. Measured here it mistypes **1 of 7**, which is what forced a per-column override — two
  homes for one fact, gated but real, and the weakest joint in §2.
* Evidence that a plain mean is acceptable where a weighted one is correct. Then `per:` need not be
  mandatory and Q1 dissolves.
* A second bundle adopting the plane. Every tier count here is n = 1.
* A ruling that presentation order belongs to the fold law after all. Then §4's role 4 comes back in
  and the plane count goes from four to five.

---

**Integrity.** Every figure was measured on 2026-09-19/20 by running the real parser, the real
planner and the real suites over three bundles, or by instrumenting the guard in process. Counts are
given with denominators throughout. The prototype ran from shadow copies; no repository file was
written by it, nothing was written under any `ontology/` directory, no lock marker was created,
moved or removed, and the warehouse was never opened for write.

---

## 11. AMENDMENT, 2026-09-20 — five options measured after this record was written

The operator asked for every option on the table to be re-analysed before any further
implementation, and proposed one of their own. Five were built as real planes and run. This section
records what changed; §1–§10 above stand except where named here.

**The suite denominator in §3 and §5 was stale.** This record quotes 758 passed / 2 skipped for the
runtime suite. The fold law's own test file added 3, so the figure is **761 passed / 2 skipped**, and
the estate is **1432 passed / 3 skipped of 1435**. Every count in this section uses 1435.

### 11.1 The authored minimum is 29 tokens, not 43

§6 put the honest minimum at 24 tokens for this bundle and the ladder stopped at 43 estate-wide.
Pushed further and re-run: **29 tokens estate-wide (11 on this bundle) holds 16 of 18**, with 0 of 30
answer signatures moved, 0 of 4 chips lost against the 52-token plane, and 0 of 1435 tests. Two
merges were tested and both REJECTED on evidence: folding `per` into `denominated_by` removes a term
and adds a token, and moving `modality` onto `grain_semantics` emits a FALSE plan disclosure on 5 of
30 measures.

### 11.2 The operator's fail-closed-on-ingest proposal: keep the term, reject the default

Proposed: at ingest, write a complete plane in which every column is closed, and let an SME open one
column at a time when a question needs it. **The operator's central insight is confirmed** — because
the plane EXISTS and is complete, nothing is absent, so it costs **0 of 1435 tests** and entirely
avoids the 142-failure bill that `MAC_FOLD_CLOSED_WORLD` pays. A positive control proves the null is
real: a plane that closes the suites' own dominant fixture relation fails 59 of 763.

Measured against it, and decisive:

* the closed skeleton with **0 SME rulings scores 1 of 18**, and **regresses 3 of 18** — cases 1, 2
  and 16 are legitimate sums it now refuses. Day one: **0 of 6 console chips, 0 of 3 bare totals**.
* refusal-driven authoring has a **hard ceiling**. A refusal names only **2 of 11** terms, so
  following the refusals reaches a fixpoint at **8 of 18** with 13 tokens. It cannot get to 16.
* the intermediate — skeleton plus the 6 rulings the console's own question corpus demands — scores
  6 of 18 and restores **6 of 6 chips**, but **12 of its 14 restored answers are undisclosed
  five-currency sums.** Refusal-driven authoring re-opens the defect the plane exists to close.

**KEEP: the `UNDECLARED` term and its own refusal lane** — "the ingest listed this column and nobody
has ruled how it folds", tier `inferred`. It changes 0 of 18 and 0 of 1435 and earns its keep in the
sentence an SME acts on. The alternative the proposal named, defaulting to `none`, states a
**falsehood on 7 of 8 relations**: `none` is the claim "resolve a stored row instead", and these
relations store no such row.

**REJECT: the complete closed skeleton as a shipping default**, on the regression and the ceiling.

### 11.3 Report mode is strictly dominated — §1.4's rollout question is closed

0003 §3.6 recommended report mode first, and §5 of this record left it open. Measured: report mode
scores **3 of 18 correct and 13 of 18 confidently wrong** — which is exactly today's runtime, plus
the cost of authoring a plane. And the footnote has no reader: `CaveatKind` is closed at
`dq | open_question | staleness`, and the presenter promotes only the applied-declaration prefix. It
is not a gentler rollout; it is the incumbent with extra steps.

### 11.4 The physical home: not `data/datasets`

This record named no home, which was an omission — the prototype's comments proposed `x-` keys on
`data/datasets/<relation>.yaml` on the grounds that the runtime already parses those files and they
sit outside the armed lock. **Measured, that home is unusable**: the ingest's own promotion stage
regenerates those files and destroys **9 of 9** such keys; the schema rejects **8 of 9**; the
grounding column model is `extra="forbid"` with four fields, so none reaches the parser; a gate
returns exit 1 on the keys; and a prior commit already removed 19 of 19 `x-` keys from these exact
files. There is also no concept plane there, so `counts_as` and `modality` have nowhere to sit —
**13 of 18**, not 16.

**Recommended and UNRULED: a new top-level `fold/<bundle>.fold.yaml`**, with a `FoldFile` definition
added to the schema first. Measured: exit 0 for an SME edit with and without an unlock marker, 0 of 3
digest moves, outside the projected surface, and touched by no generator.

### 11.5 Both boolean designs, built and scored

The operator proposed per-column booleans, then escalated to one boolean per operator. Built:
**two booleans score 4 of 18** (1 of 18 when the flag is flipped on the price columns, which is the
axis-dependence proof); **six booleans score 8 of 18** at 126 tokens, and a seventh regresses case 5.
Adding back the three pointer fields reaches 16 of 18 at **143 tokens — 2.75× the 52-token plane for
byte-identical behaviour.**

The instinct behind the proposal is nonetheless recorded as correct, and it changed how this design
is presented rather than what it is: the common case IS one word, 60 of 71 columns need nothing, and
a 13-row table at four grains was the wrong introduction. `is_sortable` is dropped — it would read
`yes` on **71 of 71** columns.

### 11.6 Three things nobody had proposed, all recommended, none needing any vocabulary

* **Fix the live SQL defects.** Two are pure construction bugs — a `JOIN` with an empty `ON` clause,
  reproduced live, and a collapse that partitions by a column already unique so 74 of 74 rows
  survive. Neither needs a declaration.
* **Wire `open_question_id`.** It is `None` at **15 of 15** construction sites and nothing sets it,
  while older refusals say the words "filing an open question" in their prose. This is what makes a
  refusal teach rather than merely stop.
* **Route fold refusals into the existing Clarification lane.** Measured as the only route from
  "0 of 3 bare totals answerable" back to answerable: a refusal that names ≤6 candidate repairs is a
  question the asker can settle, not a wall.

### 11.7 What this amendment does not change

Cases 4 and 11 are unreachable under **every** option measured. Case 4 needs the precedence ruling
(§5, still open: 6 of 1435 tests, 16 → 17 of 18). Case 11 is a missing edge — no plane, no boolean,
no home and no derivation reaches it.
