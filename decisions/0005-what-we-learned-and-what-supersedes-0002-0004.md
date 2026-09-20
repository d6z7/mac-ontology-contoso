# 0005 — What was learned, and what it supersedes in 0002–0004

**Status:** RECORD OF FINDINGS. It supersedes the *approach* of 0002, 0003 and 0004 without
discarding their measurements. Little of what those three propose should now be built.
**Audience:** whoever picks this up next. Read this before reading 0002, 0003 or 0004 — each of
those is a design argument built on a premise this record contradicts.
**Author context:** written 2026-09-20 at the end of a long session, at the operator's instruction,
so the thread can be resumed. The operator's verdict on the session's method was that it oscillated
and substituted scores for explanation. That verdict was correct and its cause is recorded in §2.

---

## 1. THE FINDING THAT CHANGES THE APPROACH

**The estate's defect is not a model that lacks declarations. It is a runtime that does not read the
declarations it has.** Measured, repeatedly, from independent directions:

| the bundle declares | on | read by |
|---|---|---|
| `identity.canonical_key` | **14 of 17** concepts | the counting route reads none of it |
| `contract.rules[].binds` | **28 of 28** rules | the runtime acts on very few |
| `contract.rules[].realized_by` — the seam to an executable body | available on all 28 | **2 of 28** use it |
| `params.natural_key`, declared deliberately with a paragraph explaining why | the store concept | nothing |
| `semantics.axis_kinds` | 3 of 3 measures | nothing outside the parser |
| `members.over`, a declared roll-up | 4 concepts | the route-finder reads only `edges.yaml` |

Every time this session met one of those, it proposed a NEW declaration instead of wiring the
existing one. That is the through-line of 0003 and 0004 and it is why they should not be built as
written.

## 2. THE COUNTING RESULT, WHICH MAKES THE POINT CONCRETE

The operator's claim: *"to figure out # of customers a system needs to know a key and enumerate it
by the key. it is as easy as that."*

Tested by constructing one derivation rule per concept — `template: COUNT(DISTINCT <the key the
concept already declares>)` — and planning it through the **real** planner, then executing the SQL
read-only against the warehouse:

```
Customer  104,990   CalendarDay 4,018   Product 2,517   GeoArea 608
ProductSubcategory 32   Brand 11   Country 8   ProductCategory 8   Currency 5   Continent 3 ...
13 of 13 countable concepts, zero new code, zero new vocabulary
```

`counts_as` — the per-concept parameter 0004 proposes — is therefore unnecessary. The key is already
declared and `derived_by_rule` already renders arbitrary SQL into the SELECT expression.

**Store is not a counter-example.** Its grain is composite, and 74 (all versions) is a correct
answer; 67 is the count of distinct business codes; an `active` filter selects among them. The
question has to say which. No declaration is wrong and nothing needs correcting.

**The one thing that blocks this end to end** is a single condition in
`interpret/vocabulary.py:83-85`: the interpreter builds its subject list from
`concept.klass == ConceptClass.MEASURE`, so only **3 of 17** concepts can ever be the subject of a
question. The planner can answer "how many customers". The question cannot be formed.

## 3. THE PROSE-RULE RESULT

The goal was never zero prose. It is: derive what is derivable, keep prose exactly where meaning is
irreducible, and shrink that set as parametrization is learned (operator, 2026-09-20).

The operator's reframe — a prose rule is like a **trigger**: at design time you bind it to a concept
and its columns; its behaviour is a body, and a body can be code. The framework already has that
seam (`realized_by: {udf, params}`, with a canon catalogue at `reference_manual/canon/`). Measured:

```
28 contract rules · 28 declare what they bind · 2 have a body
   aggregation 6, bodies 0      resolution 7, bodies 0     exclusion 6, bodies 2
   ambiguity   4, bodies 0      guarantee  4, bodies 0     default   1, bodies 0
```

**0004 built a type vocabulary for the six aggregation rules. Those six could have had six function
bodies through a mechanism that already exists and is 7% used.** Writing bodies is the hypothesis to
test next; it needs no new vocabulary at any level.

## 4. WHAT THIS MEANS FOR 0002, 0003 AND 0004

* **0002** — its central distinction (what is derivable versus what a human must rule) survives and
  is the most useful thing in the three. Its inventory of what the runtime can answer is stale.
* **0003** — "the role selects, the type refuses" is a good sentence. Its Phase 0 diagnosis of the
  fold guard is correct and was fixed. Its class gate and its `_EXCLUSION_KIND` claim were measured
  wrong (see 0004 §9), and its central proposal — a semantic type per column — is superseded by §1:
  the facts it wants to add are largely already declared elsewhere.
* **0004** — the diagnosis stands and is worth keeping: the old fold guard read a field empty on 17
  of 17 concepts, and it was consulted on the axes a question *preserves* rather than the axes it
  *folds*. Two small fixes landed from it and should stay. The four-plane vocabulary should not be
  built. `counts_as` is unnecessary (§2); the aggregation half is better served by rule bodies (§3);
  and a column-level type cannot express a fact that is grain-relative — one measured case settles
  it: a 0/1 flag correctly sums to 2,760 at calendar grain and wrongly to 160,273 at line grain.
  **One column, two grains, two correct behaviours. No column-level type can say that.**

**What landed and should stay** (all committed, all inert or bug-fixes):
`fix(planner): a scalar order_by was iterated into its letters` · `feat(planner): refuse to fold a
concept that declares no number` · `fix(planner): both choosers take declared[0]` · the fold plane
module, which is inert because no bundle declares a plane.

## 5. TWO OPEN DECISIONS

**D1 — how the count route is wired.** The operator's stated preference is (b), and asked for the
cost and the peril.

*(a) generate a derivation rule per concept* from the declared key. No code change at all; proven in
§2. Cost: 13 generated rules in the bundle, which must be regenerated when concepts change.

*(b) teach the planner to read `canonical_key` directly* when the subject is a non-measure concept.
**Cost: small** — one branch in the measure-column path plus the interpreter condition in §2.
**Peril, stated honestly:** it is an *implicit* behaviour, and this estate's whole discipline is that
nothing happens unless something declares it; it silently picks `canonical_key` where a composite
grain admits several defensible answers (Store: 74, 67, or active-only); and it creates a second
route to an aggregate beside the rule path, so two mechanisms emit SQL. **Mitigation:** make it
disclose the key it counted, in the answer, every time.

**D2 — rule bodies.** Test whether the six aggregation rules can be written as canon bodies bound
through `realized_by`. Smallest falsifying measurement: write one body for one rule and see whether
it refuses the case the prose forbids. If it does, the vocabulary route is dead and 22 more rules
have a path.

## 6. HOW ANY OF THIS GETS ENFORCED

The session's own failure is the argument. Six declarations were found that nothing reads, and no
gate noticed, because the estate's 37 gates check that artifacts *exist* and are *well-formed* —
none checks that a declared fact is *consumed*.

**The proposal: a declared-but-unread gate.** For every field in the schema and in the parsed
models, assert that some module outside the parser reads it — or that it appears in a register of
deliberately-unread fields, each with a reason. A crude version was run today: over 42 fields of 4
models it found 3 with no reader outside the parser, `semantics.axis_kinds` among them. It is
crude — a substring match — and it is the right shape. Run properly it would have caught every row
of §1's table before any of this session's work began.

This is the answer to "how do we enforce that what is defined will be read": **you cannot enforce a
document, only a check.** A decision record's claims are enforceable exactly insofar as each carries
a named check that fails today — the estate's own acceptance discipline. 0002, 0003 and 0004 carry
none, which is why three records could stand while the thing they describe was never wired.

## 7. WHERE TO PICK UP

1. Rule the count route, D1 above.
2. Run D2 — one rule body, one measurement.
3. Build the declared-but-unread gate; it is small and it protects everything else.
4. The Knowledge section of the console is a nav entry and a route filter with **no view and no
   producer**. The reverse-engineering already done for columns, tables and concepts is not emitted
   as knowledge objects, which is why the shelf is empty. That is wiring, not design.

**Integrity.** Every figure here was measured on 2026-09-19/20 against the real bundle, the real
planner and a read-only connection to the warehouse. Counts carry their denominators. No repository
file was written by any subagent, nothing was written under any `ontology/` directory, and no lock
marker was created, moved or removed.
