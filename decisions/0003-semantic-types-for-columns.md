# 0003 — Semantic types for columns: the role SELECTS, the type REFUSES

**Status:** PROPOSED — only the operator may ratify. Nothing in this record has been built.
**Audience:** whoever next proposes a per-column field to make the model refuse a wrong operation;
anyone about to add a third home for what a column means.
**Author context:** the operator proposed a semantic type per column, from which legal operations
follow, reasoning by analogy to the RDBMS data dictionary — derived and never authored, queried in
the same language as the data, and carrying MEANING where Oracle's `SYS` carries only structure, so
that `SUM(varchar2)` is a type error the engine refuses rather than a mistake the author must avoid.
Five designs were argued, two phases measured, three judges ruled 2–1. This record is the position,
its cost and its limit.
**Relates to:** `decisions/0002-answering-questions-about-the-model.md` (THE LINE — §2, §3 item 1,
§3 item 2, §6.2; this record does not restate it) · `vocabulary.yaml` (the four role terms) ·
`ontology/concepts/store/store.yaml` (`STR-Q1`, now ruled) · `ontology/concepts/catalog/product.yaml`
(`PRD-Q1`) · `mac_vocabulary.yaml#MeasureType` (the fold law).

---

## 0. TL;DR

**The operator is right, and most of what they asked for is already authored and unwired. What is
missing is not a field. It is a SECOND AXIS and a READER.**

- A **role** answers *which column should I pick*. That is a preference order, and it cannot say
  "never" — a preference that reaches its third choice has not violated anything.
- A **type** answers *may this operation touch this column at all*. That is a prohibition.

One slot cannot carry both, and this estate proves it in code rather than in argument: sixteen
modules read `field_roles`, **0 of 16 refuse an operation on the strength of what a role means**,
while `mac.schema.json` has promised since v0.1.7 that *"the referenced role term implies the default
guardrail."*

The position: **add nothing per column.** Keep the 116 role assignments exactly as authored. DERIVE
a semantic type per (relation, column) — **71 rows for this bundle** — from declarations that already
exist, and let the operation table hang off the type. The fold is never owned by the type; it is
delegated to `mac_vocabulary.yaml#MeasureType × axis_kind`, which already holds the law and which
**nothing in the runtime can currently read**.

**Authoring delta: zero per column.** Two named framework changes, neither per column. And a Phase 0
that needs no type at all: **three guards and one class check take the rule-less measure route from
10 wrong answers of 17 concepts to 0, with no new declaration of any kind** (§3.5, reproduced
tonight).

---

## 1. WHAT IS ALREADY THERE

### 1.1 The layer is fully authored

`grounding.field_roles` is a FRAMEWORK slot (`mac.schema.json` §`field_roles`), not a bundle
invention. Its description already states the operator's thesis verbatim:

> "the WHITELIST of grounded columns that carry ontology meaning, each mapped to its analytical
> role … **The referenced role term implies the default guardrail**; behavioural specifics stay as
> typed `contract.rules`."

Measured on this bundle (re-measured tonight, denominators throughout):

| | measured |
|---|---|
| concepts declaring `grounding.field_roles` | **17 of 17** |
| column assignments | **116** — dimension 46 · key 37 · attribute 20 · measure 13 |
| distinct (relation, column) pairs those 116 resolve to | **71** |
| pairs given a CONFLICTING role by different concepts | **0 of 71** |
| assignments that restate a role already stated for the same physical column | **45 of 116 (38.8 %)** |
| assignments whose column is a member of its relation's declared cell key | **23 of 116** |
| `key` assignments that are NOT a cell-key member | **14 of 37** |

Two facts follow. **The authoring burden is already paid** — nothing below may add a second
per-column field. And **it is paid 1.63× over**: the role is a property of the COLUMN, not of the
concept-column pair, which is why the registry in §6 is 71 rows and not 116.

### 1.2 It is read for SELECTION, never for REFUSAL

Seventeen source readers, across three packages (excluding tests and worktrees): ten in the
framework repo, six in the runtime, one in the console.

| behaviour | count | what they do |
|---|---|---|
| refuse an operation because of what a role MEANS | **0 of 17** | — |
| refuse on an ADJACENT fact | 3 of 17 | the whitelisted column must exist (`check_shapes`, severity error) · the block must be non-empty (`authoring`) · the token must resolve (`check_references`) |
| select, project, count or hold | 14 of 17 | choosers, display surfaces, the vocabulary page, the console's ingest view |

`vocabulary.yaml` writes each guardrail out in words — `attribute`: *"the default guardrail is NEVER
filter or group on it"* — and the one reader that could honour it does the opposite: `sql.py`'s
`_display_column` iterates `("dimension", "attribute", "key")` and will GROUP BY an `attribute`.

### 1.3 The fold law exists, and the runtime cannot reach it

`mac_vocabulary.yaml#MeasureType` has **five** members, not four, and one of them is already the word
for this bundle's hardest columns:

> **Intensive** — "A per-entity magnitude that is meaningful only as an average, never a total (e.g.
> a duration, an age, a rate, a ratio …). Summing it across a population double-counts or is
> meaningless; the correct fold on ANY axis is a mean / median / percentile, not a SUM."

That is catalogue weight, cost, price and floor area exactly. Both bundles in the estate delegate to
this law correctly and neither restates it: **3 of 3** measures here declare `measure_type` +
`axis_kinds` + `unit`, and **0 of 17** concepts write an `additivity` block. The offline gate
`tools/check_additivity_in_sql.py` says so in its own docstring: *"THE LAW IS READ, NOT RETYPED …
nothing about additivity is written in this file."*

And then:

| | measured |
|---|---|
| references to `mac_vocabulary` / `MeasureType` / `aggregation_effect` anywhere in the runtime package | **0** |
| appearances of `measure_type` / `axis_kinds` in runtime source | **2 lines each** — the model field and the parser line. Read by nothing. |
| what `_check_additivity` actually reads | `semantics.additivity`, **empty on 3 of 3** measures here (correctly — authors are told not to write it) |
| measures estate-wide on which that guard can fire | **0 of 12** |

**So the operator's proposal is largely ALREADY DESIGNED.** Two fully-authored semantic layers — the
role guardrail and the fold law — and both are dead. The estate's demonstrated failure mode is not
"we lack a type." It is **"we author and do not wire."** A third authored layer inherits that.

---

## 2. WHAT THE FOUR TERMS CONFLATE

Every one of the 116 assignments, classified against what the column measurably IS. Declared role
across, real kind down; denominator **116 of 116**.

| | key | dimension | attribute | measure | **total** |
|---|---|---|---|---|---|
| identifier | 30 | 1 | · | · | **31** |
| additive fact | · | · | · | 3 | **3** |
| non-additive catalogue number | · | · | 1 | 10 | **11** |
| category label | · | 33 | 13 | · | **46** |
| free text | · | · | 4 | · | **4** |
| date | 3 | 7 | 2 | · | **12** |
| unit | 4 | 5 | · | · | **9** |
| **total** | **37** | **46** | **20** | **13** | **116** |

- **`measure` (13) is two incompatible kinds.** 3 are an additive fact on the event relation. **10 of
  13 name a column that must never be SUMmed**: per-product catalogue numbers, per-store floor area,
  a dimensionless ratio declared `Precomputed`, and the per-UNIT rates on the line — summing a unit
  price across lines is as meaningless as summing weight across products. One word covers both.
- **`dimension` (46) is four kinds** — 33 labels, 7 dates, 5 units, 1 identifier. The 5 units are the
  currency and weight-unit columns: calling the currency a slice loses the fact that two money
  figures in different currencies cannot be added at all.
- **`attribute` (20) is four kinds**, and only the 4 free-text ones match the term's written meaning.
- **`key` (37) is three kinds**, and 14 of 37 are not their relation's grain key.

**There is no term for `unit` (9 of 116), none for `date` (12 of 116), and none for the
additive/non-additive split inside `measure` (11 of 116 are non-additive).** That is **26 of 116**
where the declared role is a lossy cast, not a choice between right answers.

### 2.1 The worked case: `SUM(Weight)` is the planner OBEYING a declaration

Reproduced tonight against the real index (17 concepts, 3 rules, 17 edges):

    measure_column answers on 10 of 17 concepts — and 0 of 10 is defensible.
      Product          -> Weight          (1 of 3 declared measures)
      Store            -> SquareMeters    ExchangeRate -> Exchange (a Precomputed ratio)
      OrderLine        -> Quantity        (1 of 4)
      Gross/Net        -> Quantity        (1 of 2; each concept's own rule says Quantity × a price)
      ProductCategory  -> CategoryKey     Customer -> GeoAreaKey
      GeoArea          -> GeoAreaKey      StoreStatus -> StoreCode

The catalogue-weight answer is not the planner ignoring the model. `Product` declares `Weight`,
`Cost` and `Price` all as `measure`; `measure_column` takes the first declared with **no uniqueness
check**, while the same function's fallback path runs candidates through `_unique()` and refuses on
ambiguity. The planner obeyed a declaration that cannot say what it needs to say.

**The sharper half, and the best single argument for the operator's analogy:** the last four —
`SUM(CategoryKey)`, `SUM(GeoAreaKey)` twice, `SUM(StoreCode)` — came through `_unique()` with the
discipline **HOLDING**. Exactly one numeric column with descriptor role `value` existed, so exactly
one was returned, and it was a surrogate key. More refusal would not have caught it. Only a type that
knows an identifier is not a number catches it. **That is `SUM(varchar2)`, in this bundle, tonight.**

**One honest narrowing of the night's headline.** Both call sites of `measure_column` sit on the
RULE-LESS branch, and the two money measures declare `derived_by_rule` against rules that exist — so
they do not reach it when their rule resolves. The live defects are Product, Store, OrderLine,
ExchangeRate and the four identifier cases; "total sales answers with a unit count" is a property of
the function in isolation, not of the planner. It stays in the record because the function is public
and the branch is one refactor away.

---

## 3. THE POSITION: TWO AXES, AND THE TYPE IS DERIVED

### 3.1 Why not simply enrich the role vocabulary

Because this estate already retired a vocabulary for exactly that, and wrote down why.
`mac_vocabulary.yaml#aggregation_effect`, v0.1.15:

> "Every term names the OPERATION, so the set answers one question in one grammar … v0.1.15 REPLACED
> THE PREVIOUS FOUR. They answered the same question in three different grammars — `additive` named a
> property, `averageable` named a capability, `non_aggregable` named a negated capability, and
> `point_in_time` named a POINT IN TIME rather than any operation at all, leaving a reader to infer
> the fold."

`field_role` is that retired grammar still in service: `key` names a property, `dimension` a
capability, `attribute` a negated capability, `measure` a payload kind and no operation at all.
Adding five more nouns to it mixes the grammars again and buys a 38-token migration plus a namespace
rename. It also cannot fix the problem it is aimed at: a preference order that reaches its third
choice has violated nothing, so the prohibition has nowhere to live.

Note also that `field_role` is the **only** analytical classification in the estate that is
application-owned. `mac_vocabulary.yaml` defines `aggregation_effect`, `axis_kind`, `binding_mode`,
`MeasureType`, `rule_kind`, `canon`, `identity_kind` — and not `field_role`. It is also the only one
with no implementer. That is not a coincidence, and it is an argument for a framework-owned type
axis, not for nine framework-owned role terms.

### 3.2 The type set — eight types and a bottom

Derived per (relation, column). Ordered by operation-set inclusion, so the MEET of two candidate sets
is computable and ambiguity DEMOTES automatically instead of being special-cased.

| type | what it is |
|---|---|
| `identifier` | a value whose job is to equal another value |
| `categorical` | a repeating label |
| `unit` | a categorical that DENOMINATES a quantity (inherits categorical, adds a veto) |
| `ordinal` | discrete and ordered |
| `temporal` | ordinal with a calendar |
| `unique_text` | distinct per row, no reuse |
| `free_text` | natural language |
| `quantity` | arithmetic is meaningful — the FOLD is not stored here (see 3.3) |
| `⊥` | two authored planes contradict; display only, every operation refuses and names both planes |

### 3.3 The legal-operation table

EQ · RANGE · JOIN · GROUP · COUNTD (count distinct as an instance count) · MINMAX · SUM · AVG.
DISPLAY is always legal and is not listed.

| type | permitted |
|---|---|
| `identifier` | EQ JOIN GROUP COUNTD — **no SUM** |
| `categorical` | EQ GROUP COUNTD |
| `ordinal` | EQ RANGE GROUP COUNTD MINMAX |
| `temporal` | EQ RANGE JOIN GROUP COUNTD MINMAX |
| `unique_text` | EQ COUNTD (GROUP would equal rows) |
| `free_text` | DISPLAY and exact EQ |
| `quantity.Flow` | RANGE MINMAX SUM AVG |
| `quantity.Stock` | RANGE MINMAX AVG; SUM on a categorical axis only |
| `quantity.Intensive` | RANGE MINMAX AVG — **SUM is a type error** |
| `quantity.Precomputed` / `.Target` | RANGE MINMAX — no fold; resolve the stored row |
| `quantity` with no declared `measure_type` | RANGE MINMAX — SUM refuses, naming the missing declaration |
| `unit` | EQ GROUP COUNTD **+ vetoes** a fold of the quantity it denominates across differing values |
| `⊥` | nothing |

**The fold branch adds no vocabulary at all.** `Flow`, `Stock`, `Intensive`, `Precomputed`, `Target`
are the framework's own words and the law is `MeasureType × axis_kind → aggregation_effect`, read at
the point of use. A type that carried its own additivity would be the estate's standard two-homes
failure on the day it shipped — and the second home already exists (§1.3): it is the empty dict the
runtime reads. **Closing that is a prerequisite of this design, not a consequence of it.**

### 3.4 AUTHORING DELTA: zero per column, justified line by line

Every input is already declared, and I verified each one's coverage:

| input | coverage, measured |
|---|---|
| descriptor `{name, type, role, confidence}` per served column | **71 of 71**, all four fields present on all 71 |
| descriptor role vocabulary | discriminator 29 · value 28 · composite_key_part 5 · foreign_key 5 · primary_key 4 |
| physical types | varchar 33 · integer 22 · timestamp 8 · decimal(20,5) 7 · bigint 1 |
| declared cell key | 6 of 6 relations (`grounding.sources[].key`) |
| declared physical edges | 5 `join_rule`s of 17 edges |
| ontology `field_roles` | 116 assignments over 71 of 71 columns, **0 conflicting** |
| `measure_type` + `axis_kinds` + `unit` | 3 of 3 measures |
| derivation templates | 2 of 2 money measures declare `derived_by_rule` against rules that exist |
| typed contract rules carrying `binds` | **28 of 28** |

**No new per-column field. No change to any of the 116 assignments. No new role term. No `additivity`
block anywhere.**

**Two framework changes, both named, neither per column.** They must be named rather than smuggled:
`mac.schema.json` records that the `^x-` escape hatch was CLOSED in v0.1.14 — *"name the wall and
change the schema, which is now the only way to add a field."*

1. **`ReasonCode` needs a seventh member, `type_error`.** It is a closed six-member enum. A type
   refusal is not `ontology_gap` — nothing is missing; the declaration is present and says no — and
   not always `additivity_violation`. Without this, every refusal below has no code to return under.
2. **`concept.semantics.unit` must be able to NAME a column, not only describe one.** Today it is
   prose on 3 of 3 measures ("denominated in the order's own currency column"), which is why `unit`
   has **0 of 71** derivable occupants and the cross-currency prohibition reaches nothing.

### 3.5 PHASE 0 — what refuses BEFORE any type exists

Reproduced tonight against the real index. **Zero authoring, four edits, all on lines that already
exist.** Each step is independently shippable.

| step | what changes | measured effect |
|---|---|---|
| baseline | — | `measure_column` answers on **10 of 17** concepts; **0 of 10** defensible |
| **class gate** | `_resolve_measure` accepts any concept as the measure; there is no `class` test anywhere in the planner | 14 of 17 concepts leave the fold route by construction, before a column is chosen |
| **Guard A** | route the `field_roles` measure list through the `_unique()` that sits in the same file | refuses Product (3 declared), OrderLine (4), and both money measures (2 each) → **10 → 6** |
| **Guard B** | add to the descriptor path's `excluded` set every column ANY concept on that relation declares `field_role.key` | refuses the four identifier sums → **6 → 2** |
| **Guard C** | repoint `_check_additivity` from the empty `semantics.additivity` at `MeasureType × axis_kinds`; generalise: a `measure` column on a concept with no `measure_type` has no law, therefore no legal fold | refuses the `Precomputed` ratio and the floor area → **2 → 0** |

Two more that cost nothing and must land in the same commit:

- **`period_column` has the identical defect** and iterates role terms (`period`, `time`, `date`) the
  closed four-term vocabulary does not contain, so it falls through on 17 of 17 today. The moment a
  `temporal` type exists that loop starts RETURNING columns — on the event relation it would pick
  silently between two date columns, which is the choice `NSA-Q2` is already filed on.
- **Widen `_EXCLUSION_KIND` from `"exclusion"` to `{exclusion, aggregation}`.** This is the cheapest
  finding of the night. `unaggregatable_columns` ALREADY scans every concept on the relation, reads
  typed rules' `binds`, and either refuses naming the rule or pins a declared default and discloses
  it — filtered to one constant. The bundle authors **6 aggregation rules, 28 of 28 rules carrying
  `binds`**, and four of the six are exactly the facts every design called unsayable: the
  cross-currency prohibition, the working-day flag ("a SUM returns a count of working days under the
  name of a total"), the brand/category orthogonality, and *"count DISTINCT StoreCode, which is 67 …
  never DISTINCT StoreKey, which is 74."* Widening one constant activates them through machinery that
  already refuses. It also gives **0002 §3 item 1** its consumer.

**And a prerequisite that is not optional: wire `open_questions` into the index first.** A guard that
can file nothing teaches nobody (§6.3).

### 3.6 Rollout, stated honestly

Under the full type gate, **SUM is permitted on 0 of 71 columns** on day one. That is the bundle's
true state — nothing here declares that any COLUMN may be summed; the only summable objects are the
two rule-derived expressions, and `ontology/rules.yaml` says so itself ("SUM of a per-unit price is
not a money figure at all"). It is also a bundle that answers no numeric question. So: **report mode
first** (the MAC005 pattern, whose own docstring forbids ERROR), printing every refusal that WOULD
fire with its type and its evidence. Severity rises only after the two rule-derived measures are
answered through their templates and the `⊥` rows are filed.

---

## 4. DERIVABLE VERSUS CURATED

Applying **0002 §2.1**'s own test — every input a declared field or a closed term, prose quoted but
never parsed for a value, no ranking of rivals — mechanically, over all **116 of 116**:

| | count | what it is |
|---|---|---|
| **DERIVABLE** | **26 of 116 (22.4 %)** | 23 the column is a member of its relation's declared cell key (re-measured tonight: exactly 23) · 3 the column is named by a declared physical `join_rule` |
| **NOT DERIVABLE** | **90 of 116 (77.6 %)** | everything else |

**Of the 46 `dimension`, 20 `attribute` and 13 `measure` assignments, not one is derivable.** Zero.

The two independent passes split the 90 differently — one as 26 UNEXPRESSIBLE + 64 curation, the
other as 9 sound-only-by-naming-convention + 81 curation — and the disagreement is itself the finding:
**the residue's shape is not agreed, only its size.** The type axis expresses most of the
"unexpressible" class (dates become `temporal`, the non-additive numbers become `Intensive` /
`Precomputed`), leaving the unit cases; but that is a claim about a design that does not exist yet and
must be re-measured after it does, not asserted now (§8 Q6).

### 4.1 The irreducibly human part, worked

`ProductCode` is `dimension`. `ProductName` is `attribute`. Both VARCHAR, both 2 517 distinct over
2 517 rows, both 0 null, mutually bijective, both 1:1 with the key. **Nothing in the data
distinguishes them.** The concept's own note says why, and it is not a fact about the column at all:

> "`ProductName` IS `attribute` AND `ProductCode` IS `dimension`, even though both are measured
> unique today: the name is what a question says and the code is what a filter may safely use, so
> the name is resolved through the register and then never matched on again."

That is a ROUTE, not a prohibition — and it is the general case. Across the 71 columns, **26 pairs
are mutually bijective and 21 of the 26 carry different roles**: seven calendar spellings of one
fact, five code-vs-name pairs, six key-vs-label pairs. In one relation, four columns are mutually
bijective and carry three different roles. **No function of the data can separate them**, and the
type axis correctly has no opinion: it types both as the same thing and leaves the split on the role
axis where a human put it.

**14 of those 21 pairs already have an open question filed.** The bundle has already identified its
curation calls as curation. The 7 calendar pairs have none (§8 Q4).

### 4.2 The invariant that keeps this inside 0002's line

> **MEASUREMENT NEVER PROMOTES.** A measurement may NARROW a candidate set or VETO a declared type.
> It may never mint a type, an operation or an edge.

The estate's own counterexample proves the weaker rule unsafe: one dimension's area key (608 values)
includes TOTALLY into the product key (2 517 values, zero misses), so a derive-over-DATA catalog would
confidently mint a reference that `ontology/edges.yaml` records **rejecting by hand** ("2 candidate
parents measured, 0 admitted"). The data does not merely fail to supply the answer — it supplies a
wrong one confidently.

This is where the Oracle analogy has to be taken carefully. Oracle's catalog is derived because
`CREATE TABLE` is the authoring act. Here the authoring acts are the **grain declaration**, the
**descriptor role** and the **edge** — and those, not the data, are what the type reads. Any
distribution-shaped detector (dense integer ranges, bijections) is therefore a VETO only, and its
residue lands in the meet, which still refuses SUM. 0002 T3 forbids picking between rivals "because
they happen to agree today"; this invariant is that clause applied per column.

---

## 5. KEY-AS-ENUMERATOR — RULED

> "every object has a (primary) key … this is THE KEY to make the object enumerable in any
> situation. Specifying any column in this key will decide a filter … dimension is the column that
> can be used for filtering and measure is usually the outcome of aggregation over filtering."

**The mechanism is right. The operand is not one thing.** Counting, filtering and grouping really are
one operation at three bindings, and **composite keys do not disturb it** — the event relation's
two-part key is exactly unique over 223 974 rows and the FX grid's three-part key over 100 450: bind
all → one row, bind some → a filter, project some → a group.

Measured, concept by concept: `identity.canonical_key` agrees with the relation's declared cell key on
**4 of 17**, disagrees on **9 of 17**, and is absent on **4 of 17**.

**Where it holds — 4 of 17.** Product, Customer, CalendarDay, Store: the concept's key IS the
relation's grain key, and all three bindings are the same operation.

**Where it breaks — 13 of 17, in seven distinct ways.**

1. **The concept's key is not the relation's key — 9 of 17.** The groupings and enumerations ride a
   HOST relation: enumerating the relation's key counts products, not brands. And the declaration
   contradicts itself here — 6 of those concepts give their own canonical key the role `dimension`,
   not `key`.
2. **No key at all — 4 of 17** (the brief said 3; 0002 already records 4). For the three measures this
   is correct and permanent: a measure has no instance set. For the event concept the key exists and
   is unique — `identity.canonical_key` is **`"type": "string"`**, a scalar that cannot hold a
   composite, so the bundle's only composite-key concept omits it. The runtime meanwhile parses a
   tuple-shaped `cell_key`. **Two homes for "the key", one scalar and one tuple.**
3. **Instance identity ≠ row key.** 74 rows, 74 row keys, 67 business codes; six codes carry more
   than one version and one carries three. And the same key gives two further defensible answers:
   64 row keys and 63 codes appear in the fact. **Four numbers — 74 / 67 / 64 / 63 — one key.**
4. **One concept, two relations, two enumerations — 2 of 17.** Union, precedence and sentinel
   exclusion are all undeclared. Both already filed, both unreachable.
5. **A nullable enumerator.** One concept's key is null on 59 of 74 rows; "no status" is a member with
   no value.
6. **A degenerate key part.** One part of the event key has 7 distinct values over 223 974 rows.
   Binding it filters legally, projecting it groups legally, enumerating it answers "7" — a fact about
   line position and about no business object.
7. **One key, three populations.** The same key enumerates 104 990 in its dimension and 52 189 in the
   fact — half the customers have never ordered. Both readings are defensible; nothing ranks them.

**What the breaks share, in one sentence: the key enumerates a RELATION at the grain that relation
happens to have, while a question asks about a CONCEPT, and every break is a place those two differ.**

**So the word `key` covers four distinguishable things, and 37 of 116 assignments spell all four the
same way:** the **grain key** (derivable, 23 of 37) · the **instance identity**, which may be coarser
· the **foreign key**, which enumerates a population restricted by its host · the **grouping key**,
a non-key column of the host relation, which is what 9 of 17 concepts actually mean.

### 5.1 `STR-Q1`, and why it needs no new word

The operator has ruled: **a store is the CODE (67), not the version (74)** — *"the version is here
only to differentiate the same store before the restructuring and after."* Recorded.

That ruling needs a **READER**, not a term, and **0002 §3 item 2** already specifies the reader: a
five-branch precedence that resolves **17 of 17** concepts with **0** new fields, whose step 3 is
`grounding.realized_by.params.natural_key` — already declared as the store code in the concept file.
Ratification is a status change on `STR-Q1`.

But the record must say what no design said: **the ruling now has THREE homes, and nothing ranks
them.** `identity.canonical_key` says the row key; `realized_by.params.natural_key` says the code; and
a typed aggregation rule binds both and says *"count DISTINCT the code, which is 67 … never DISTINCT
the row key, which is 74."* Two say 67, one says 74. Worse, the slot carrying the ruling is one a
framework gate warns about — the concept's own note records that the parameter *"IS RETYPED ON PURPOSE
AND check_canon_binding WARNS ABOUT IT (MAC003)"*, because obeying the warning turns the collapse into
a no-op. **A MAC003 warning is load-bearing for the operator's ruling.** The precedence must be
declared and a gate must FAIL when the three disagree without one (§8 Q1).

### 5.2 And there is no COUNT route at all

`Intent` has one subject slot, typed `measure`, and there is **no `COUNT` anywhere in the planner** —
0 hits, re-confirmed tonight. The operator's unifying idea currently has nowhere to execute; "how many
products" bends through the fold route not because the role vocabulary is coarse but because the
runtime has exactly one aggregation route and it is a SUM. **0002 §6.10** already named the count
builder as the largest unpriced item in that record. It is still unpriced, and it is a prerequisite
for every enumeration claim in this one.

---

## 6. THE REGISTRY

### 6.1 Shape — 71 rows, derived, never authored

One row per (relation, column), because that is the grain at which the fact is true (§1.1):

    relation · column · physical_type · descriptor_role · field_role(s) · derived_type ·
    identity_backing {grain_key_member | edge_backed | asserted_only | none} ·
    fold_time · fold_categorical (or null WITH the reason) · legal_ops ·
    evidence (which planes voted, and what each voted) · confidence (C/I/Q) ·
    open_question_id · derived_on

**What is NOT stored on the row:** the permitted/refused operation set is a JOIN to the law register,
never a copy. Change the law once and every row's legality changes. Oracle's `SYS` says `NUMBER`; this
says *"may be folded, and here is how the fold is decided, and here is who has not yet ruled on it."*

### 6.2 The instrument already exists at three rows

`data/lookups/contoso_measure.lookup.csv` is a derived, queryable catalog with a build script beside
it, header:

    code,label,search_key,measure_type,additivity_time,additivity_categorical,
    axes_time,axes_categorical,concept_file,source_view,confidence,note

Nobody authored those additivity columns — a script projected the law onto the declarations, and each
row's note says so. **The proposal is to run that same instrument at 71 rows instead of 3.** Emit it
as CSV beside the other registers AND as a served view, so *"which columns may I group by"* is a
query over the warehouse in the same language as the data. That is the operator's requirement met
literally rather than by analogy.

The abstraction ladder they asked for, made concrete: **physical type** (71 of 71, authored in the
descriptor) → **descriptor role** (71 of 71) → **semantic type** (derived) → **permitted operations**
(joined from the law) → **fold** (delegated to `MeasureType × axis_kind`). Five rungs, four already
authored, one computed.

### 6.3 What it must carry that Oracle's never does: the unresolved ruling

| | measured |
|---|---|
| open questions filed | **29**, across **17 of 17** concepts — every concept has at least one |
| occurrences of `open_questions` in `objects.json` | **0** (also 0 for `field_roles`, `canonical_key`, `cell_key`; `measure_type` and `axis_kinds` do appear, 3 each) |
| occurrences in the runtime package | **0** — the single hit is a comment calling it an answer-store-level concept |
| `open_question_id` at the planner's construction sites | hard-coded `None` at every one |

This is **0002 §6.2**'s gap, and the registry is what makes closing it load-bearing rather than tidy.
A `⊥` row, an ambiguous label target, a key with no edge — each is a question a MACHINE can file, and
each needs an id that survives re-derivation. **Oracle's catalog has no column for "nobody has ruled
on this yet."** Ours must, or a refusal says "I don't know" where the truth is "nobody has told me" —
which **0002 §5** already bans.

### 6.4 What it answers that nothing answers today

- *May I sum this column, and if not, what is the correct fold?* — a join to the law, per column.
- *Which columns may I group by, and which are display-only?* — with the disagreement between the two
  authored planes visible as a column rather than invisible.
- *Which of these two columns is the axis and which is its spelling?* — with the twin, its denominator
  and its `measured_at`, or an open question id.
- *Why did that refuse?* — the type, the planes that voted for it, and the declaration that would
  change the answer.

---

## 7. WHAT THIS DOES NOT BUY

**7.1 It refuses more than it answers on day one.** SUM on 0 of 71 columns until the rule-derived
measures are routed through their templates. Report mode is not a nicety; it is the only shippable
first state.

**7.2 It does not resolve the curation majority — it relocates it.** 90 of 116 assignments are not
derivable and 0 of the 46 `dimension` + 20 `attribute` + 13 `measure` are. A better-shaped question is
progress; it is not an answer.

**7.3 Two types have zero derivable occupants here, and I say so plainly.** `unit` 0 of 71 (the slot
is prose) and `free_text` 0 of 71 (the "display only" columns all reuse values and derive to
`categorical`; only the product name has no reuse, and it derives identically to the product code).

**7.4 Sentinels are invisible to every type, verb and registry cell proposed.** The data plane records
a SERVED sentinel row — a sentinel row key, a sentinel area key, a sentinel country token — and
**41.8 % of the fact's lines point at it** (93 550 of 223 974). Every enumeration figure argued
tonight is silently sentinel-inclusive or not. No design has a column for it, no type expresses it, no
verb asks. **This is the largest unhandled correctness gap in the record**, in a system whose whole
premise is refusing confident wrong numbers.

**7.5 The display defect is not where everyone said it was.** `_display_column` tries the grounds
column, the code column, then the descriptor's `attribute`-subrole columns, then the descriptor's
`value` columns, and only THEN the `field_roles` loop. Traced over all 17 concepts: the descriptor
`value` branch fires on **12 of 17** and produces every bad grouping measured tonight; the
`field_roles` loop is reached on **5 of 17** and returns a `dimension` in all five. Any fix aimed at
the `field_roles` loop corrects none of the 12. And the highest-priority branch of the five is dead:
**0 of 71 descriptor entries carry a `subrole`**, so the runtime's first display preference is
unexercised and untested here.

**7.6 The bypass everyone called a defect is documented as deliberate.** The module docstring says
*"this module never picks … no preference order among equals."* The function docstring twelve lines
above the code says the opposite on purpose: *"Two homes, in order. `field_roles` wins when it names a
measure, because a concept that says so directly has said so."* Whoever lands Guard A is **reversing a
written decision**, and owes the record a line saying so — possibly by deleting that paragraph rather
than adding a check under it.

**7.7 One legitimate question starts refusing.** "How many units did we sell" is a SUM over the event
relation's quantity, and the event concept declares no `measure_type`, so Guard C and the type axis
both refuse it. The remedy is one concept-level declaration on an existing framework slot — not a
per-column write — but until it is written, the question refuses.

**7.8 The `Intensive` default is a default, not a proof.** Total floor area across stores is a
defensible figure and this design refuses it. The honest remedy is to DECLARE the measure concept with
`measure_type: Intensive` — the word already exists and the bundle uses 0 of 5 MeasureType members for
these columns — not to let a derivation guess.

**7.9 The unit prohibition's only machine-readable home binds the wrong operand.** The cross-currency
rule binds the currency column and the three per-unit prices. It does **not** bind the quantity, and
it does not bind the derived money expression — which is the figure the prohibition is actually about.

**7.10 One slot cannot hold two true facts — 8 of 116.** The two FX currency columns are members of
the grid's cell key AND the units of the ratio. The two date columns on the line are the time axis AND
declared physical foreign keys. Precedence resolves it; the other fact goes unstated in the token and
must live in the rule's `binds` or in the edge.

**7.11 Which plane wins when the two authored planes disagree is undecided — 23 of 116.** Ontology
`attribute` over descriptor `discriminator` (12), ontology `key` over descriptor `value` (11). This
design's answer is `⊥` — refuse and file — which is an outcome, not an adjudication. No gate compares
the two planes today; the registry's first output will be rows nobody has looked at.

**7.12 Everything here is measured on ONE bundle.** The mature bundle in the estate declares this
layer on **0 of 22** concepts, with the "offered and unused — 22 sites" warning live in its own
compile output. Every gate proposed here would report PASS over an empty denominator there. Per the
standing rule, a gate must print its adoption denominator and give "unadopted" a verdict distinct
from "clean". **0002 §4.5** already warns about designs fitted to n = 1.

**7.13 A derived registry served present-tense needs a watermark.** Every bijection, cardinality and
null rate is a snapshot of this delivery. **0002 §6.9** already ruled the shape: the value, its
`measured_at` and its `source_file` travel as one indivisible triple or not at all. The store profile
carries no source watermark today.

**7.14 The migration's blast radius is cross-repo and includes test fixtures.** Seventeen readers in
three packages, three of them refusing on adjacent facts (an error-severity shape, a reference check,
an authoring check). Any change to the token set or the namespace must land with the bundle
vocabulary, the reference index and the shape file in ONE commit, or the bundle fails its own gates
mid-migration. This is one more reason the position adds no token and retires none.

**7.15 The leak floor is an unpriced cost on exactly the most persuasive material.** The framework
repo is public at leak floor 0. Every worked example that makes this argument land is bundle-named. A
gate printing "11 of 37" is fine; a gate whose self-test fixture or docstring carries a real column
name is a leak. Budget the synthetic re-expression before any of this becomes framework prose.

---

## 8. OPEN QUESTIONS FOR THE OPERATOR

Each is answerable in one word. Each carries a recommendation, so silence is not required to mean
anything.

**Q1 — `STR-Q1` is ruled CODE (67). Which of its three homes is authoritative, and does a gate fail
when they disagree?**
*Recommendation: **`natural_key`** — the declared collapse is the ruling's home, `canonical_key` stays
the ROW key, and the typed rule quotes them both. Add the gate; its trigger is 1 of 17 today, which is
exactly why it must exist before a second concept acquires a collapse.*

**Q2 — Ship Phase 0 (§3.5) now, before any type exists?**
*Recommendation: **YES.** Zero authoring, 10 wrong answers of 17 to 0, on code that exists. Everything
else in this record lands on a runtime that already refuses, or it lands on one where the only SUM
guard is dead on 12 of 12 measures.*

**Q3 — Widen `_EXCLUSION_KIND` to `{exclusion, aggregation}`?**
*Recommendation: **YES**, excluding the two derivation rules. It activates the cross-currency, the
flag-not-quantity and the entity-count rules through machinery that already refuses and already
discloses, and it gives 0002 §3 item 1 its consumer.*

**Q4 — The seven calendar spelling-pairs have no open question filed. File them?**
*Recommendation: **YES**, one question per pair, owner operator. They are the only bijective pairs in
the bundle whose curation call is undocumented; leaving them is the difference between a residue and a
backlog nobody can see.*

**Q5 — When the two authored planes disagree (23 of 116), which wins?**
*Recommendation: **NEITHER** — the column lands at `⊥`, refuses everything but display, and files. An
adjudication rule would let one plane silently overwrite the other, which is the one-home rule
inverted.*

**Q6 — Does 0002's binary need a third class, UNEXPRESSIBLE?**
*Recommendation: **NO, NOT YET.** Two of the three kinds it names gain a term under this design;
re-measure the residue after the type axis exists and file what is left as a vocabulary defect report.
Amending the line on a pre-change count would bake in a category this design is meant to delete.*

**Q7 — Is a sentinel row a member of a concept's instance set?**
*Recommendation: **NO**, and the exclusion must be DECLARED per relation, never assumed by a reader.
Until it is, every count in this bundle carries a silent ±1 and the fact's sentinel share is 41.8 %.*

**Q8 — `ReasonCode` gains `type_error`, and `semantics.unit` becomes column-valued. Both are schema
changes. Approve?**
*Recommendation: **YES** to both, as named schema changes with a ruling each. They are the only two
things this design cannot do with what exists, and neither is per column.*

---

## 9. What would reverse this

- Evidence that a role CAN carry a prohibition without becoming unusable as a preference — i.e. a
  reader that refuses on a role and does not break the register routes the bundle documents. Then the
  second axis is unnecessary and the vocabulary should simply be enriched.
- The count route landing with a typed subject (0002 §3 item 4): several enumeration claims here stop
  being hypothetical and must be re-measured against a real route.
- A second bundle adopting `field_roles`: the derivation's hit rate here is n = 1, and on a bundle
  whose descriptor plane uses one term for three quarters of its columns it would produce far more
  `⊥` and far fewer resolved quantities.
- A ruling that the two authored planes have a precedence after all: §7.11's `⊥` class empties, and
  the registry loses its most useful column.

---

**Integrity.** Every figure above was re-measured tonight from YAML, JSON, Python source and the
schema, or reproduced by running the real parser and the real choosers over this bundle.
`contoso.duckdb` md5 `2f105860718aed0921ecf18be4f2fe3c` before and after — unchanged, never opened
for write. Nothing else in this repo was edited, nothing was committed, `CURRENT` was not bumped, and
`.ontology-unlocked` was not touched. The mature bundle was read for shape only; nothing was copied.
