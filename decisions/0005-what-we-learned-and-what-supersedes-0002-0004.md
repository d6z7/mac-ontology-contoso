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

---

## 8. THE CHECK THIS RECORD ASKED FOR, AND WHAT IT FOUND

*Added 2026-09-24.* §6 ends on the claim that **you cannot enforce a document, only a check**, and
that a record's claims are worth exactly as much as the checks that fail today because of them.
This section supplies them for §1's fourth row — `params.natural_key`, *"declared deliberately with
a paragraph explaining why … read by nothing"*.

The operator asked for a corpus family around one concept: *"since store is complex concept … what
do you think of having few more question in corpus around it … to validate if the logic works
fine."* Seven questions (`STORE-01`…`STORE-07`), each with an anchor derived from the data by two
independent routes, neither of them the engine. Replayed through the real planner with hand-written
intents — so every failure below is the planner's and not an interpreter's.

| # | question | anchor | engine | |
|---|---|---|---|---|
| RC05 | how many stores do we have | 67 | **67** | correct |
| STORE-01 | how many stores are still open | 58 | *refused* `unresolved_term ['CloseDate']` | |
| STORE-02 | how many stores are not closed | 59 | **6** | **wrong** |
| STORE-03 | how many stores have been restructured | 0 | **6** | **wrong** |
| STORE-04 | when was the first store closed | 2013-12-05 | *refused* `unresolved_term ['CloseDate']` | |
| STORE-05 | total floor space in square metres | 99 300 | *refused* `unresolved_term ['SquareMeters']` | |
| STORE-06 | how many store versions are recorded | 74 | *refused* `unresolved_term ['StoreVersion']` | correctly — no such concept |
| STORE-07 | how many of our stores have closed | 8 | **8** | correct, and see below |

**One question in seven answers correctly and is not evidence of anything.** RC05's 67 is right
because `identity.counts_as: StoreCode` routes the distinct-count to the natural key. It masks the
defect below rather than avoiding it: the collapse it runs inside is a no-op, and the count is
correct only because it counts the right column over the wrong row set. STORE-07's 8 is right by
arithmetic accident — the eight closed versions happen to fall on eight distinct codes, and the one
multi-version code among them (46) happens to have its closed version last. Change one row of the
dimension and it is wrong with no code change.

### 8.1 The collapse runs and collapses nothing — as the bundle wrote down in advance

`store.yaml#grounding.realized_by` declares `params.natural_key: StoreCode` and spends a paragraph
on why, ending: *"Partitioning the collapse by it \[StoreKey] returns 74 of 74 rows: no collapse at
all, silently."*

The planner emits, measured today:

```sql
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY StoreKey ORDER BY OpenDate DESC) AS _mac_cycle_rank
      FROM contoso_served.dim_contoso_store) cycle
WHERE cycle._mac_cycle_rank = 1
```

74 of 74 rows survive. `snapshot.py#_SlotResolver._partition` derives the partition from the
relation's **measured identity** — `[StoreKey]`, the version surrogate, which is by construction
unique per row — minus the axes the fragment names as collapsed. It never reads `natural_key`. The
platform states this itself in `foldplane/planes.py`: *"the canon's own `params.natural_key` (read
by 0 of 62 runtime files today)"*.

**Three artefacts independently name the right column and the failure mode, and the fourth does the
wrong thing anyway.** That is §1's finding at its sharpest: not a missing declaration, not even an
unnoticed one — an unread one whose author predicted the consequence in the file the reader skips.

The guard that should have caught it is three lines above and checks the wrong thing: it subtracts
axes named in `collapses_over`, so it catches a partition containing the *collapse axis* and misses
a partition on a *surrogate that is unique per version*, which has the identical effect.

### 8.2 A wrong number that is not a refusal — the worst class

STORE-02 and STORE-03 both return **6**. Valid SQL, a plausible small integer, nothing in the
result to mark it. Two independent causes, and the corpus separates them:

* **STORE-03 (0 vs 6)** is the no-op collapse. Seven versions carry `Restructured`, over six codes;
  every one has since been superseded, so at entity grain the answer is 0. The engine counts codes
  that were *ever* restructured because the collapse never ran.
* **STORE-02 (59 vs 6)** is three-valued logic. `FilterOp.NE` renders `<>`, and 59 of the 67 current
  stores carry a NULL `Status` — they are precisely the stores the question asks for. `<>` discards
  every one. Recorded in the framework as `grammar/query_grammar.yaml#not_expressible:
  negation_over_nullable`, with `null_test` beside it for STORE-01.

### 8.3 Four refusals name a column the concept declares

`CloseDate`, `SquareMeters` are in `store.yaml#grounding.field_roles` — `dimension` and `measure`
respectively — and the term resolver reaches neither. This is §1's table again, one row further
down, and it is why STORE-01 cannot be answered at all: the bundle **rules** that operating stores
are read from `CloseDate IS NULL`, gives the reason no status code can serve, and the rule is
unreachable twice over — no null test in `FilterOp`, and the column unresolvable as a term.

### 8.4 What this section does and does not license

It does **not** license the `entity_key` / `versioned_by` redesign. The operator deferred that
pending more samples than one, and `counts_as` was named a hack by the same ruling; nothing here
changes the evidence base for a general pattern (*n* = 1 bundle).

It licenses exactly one thing: **the collapse should read `params.natural_key` when the bundle
declares it.** That is wiring an existing declaration, which is what §1 says this estate should be
doing instead of designing new ones, and it is independent of what the field ends up being called.
The seven questions above are the check that fails today and will say when it stops.

> **DONE 2026-09-24, and the site was not the one this section named.** An earlier revision said
> `snapshot.py#_SlotResolver._partition`. That is the FRAGMENT path, no fragment binds
> `dim_contoso_store`, and it never runs for this bundle — a fix was written there first and
> reverted, having changed nothing. The live path is
> `grounded_columns.py#reporting_cycle()`, which returned `partition=grounding.cell_key`; it now
> prefers the declared `natural_key`. A plausible fix in a plausible place that changes nothing is
> its own hazard, and it is recorded because §1's whole subject is declarations nobody traced to
> the code that reads them.
>
> Measured after, against the anchors: **STORE-02 6 → 59, STORE-03 6 → 0**, RC05 and STORE-07
> unchanged and correct. `FilterOp.NE` was fixed in the same pass — it rendered `<>`, which drops
> NULLs — and that is what moved STORE-02. Both are guarded by
> `meaning-as-code/invariants/planner_invariants.py`: 151 checks, 0 red.

A second, smaller item: the `SST-Q3` ruling. STORE-01 and STORE-02 are 58 and 59 and a business
reader hears one question. Both numbers are faithful to declarations this bundle already carries —
`"Closed stores" means Status = 'Closed'` and `operating means CloseDate IS NULL` — and they
disagree on exactly one store, the same row `store_status.yaml`'s INFORMATIONAL constraint has been
measuring as `59 - 58 = 1` since 2026-09-18. What a *negated* question should return was never
ruled on. Until it is, all three numbers are pinned so the ruling is visible when it lands.
