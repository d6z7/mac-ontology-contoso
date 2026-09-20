# 0002 — Answering questions about the model: reflection is derived, never authored

> **SUPERSEDED IN APPROACH — see [0005](0005-what-we-learned-and-what-supersedes-0002-0004.md) (2026-09-20).** Its measurements stand; its proposal largely should not be built. The premise all three records share — that the model needs new declarations — was measured wrong: the facts are mostly declared already and the runtime does not read them.

**Status:** PROPOSED — only the operator may ratify. Nothing in this record has been built.
**Audience:** whoever next tries to make this model answer a question about itself; anyone tempted
to author a "count measure", a `countable: true` flag, or any other per-concept artifact whose only
job is to restate an identity the concept already declares.
**Author context:** the operator asked why the model cannot answer "how many different products do
you know", and rejected the proposal to hand-author a count per concept on the estate's own first
principle — a fact has ONE home. Four designs were argued and three judges ruled. This record is the
position, its cost and its limit.
**Relates to:** `ontology/concepts/store/store.yaml` (`STR-Q1`, `store.versions.entity_count_is_the_code`)
· `ontology/concepts/catalog/product.yaml` (`PRD-Q1`) · `check_answerability` (MAC011) ·
`decisions/0001-order-line-fact-of-record.md` (the same shape: the evidence existed; the ruling did not).

---

## 0. TL;DR

**The model already reflects on itself, twice, and throws both reflections away. Nothing per concept
needs authoring. What is missing is a route from the asker to a derivation that already runs.**

A count measure per concept would be a second — on one concept a **fourth** — home for a fact the
bundle already declares. The operator's objection stands unamended. But the opposite conclusion does
not follow either: the count is not simply "already available". Three things block it, all of them
platform-side, none of them per concept:

1. **The intent type has one subject slot and it is typed `measure`.** A question whose subject is a
   concept cannot be *represented*, let alone answered.
2. **The deriver that computes, per concept, how that concept would be answered reaches no route.**
   It runs in CI, its output is discarded, and the one function written to render it for a reader has
   zero callers.
3. **The refusal is a self-score,** and the information it would need to be honest was destroyed one
   layer earlier, in the prompt.

The deliverable of this record is not the count. It is **the line** (§2): which questions about
itself a model may answer without a human, and which require a human to decide something first.

---

## 1. What actually prevents it — mechanically

### 1.1 Introspection exists, and it is free

`GET /ask-capabilities/example/contoso`, live on 2026-09-19:

    ready: true   problems: []
    ontology: {concepts: 17, measures: 3, dimensions: 14, rules: 3, edges: 17}
    registers: {files: 2, entries: 7}     consent: {act: question, cost: billed}

`ask_engine.capabilities()` reads the bundle, derives those counts from the index, builds no client
and opens no connection. So reflection over declarations is already implemented and already costs
nothing. Two of its own published numbers are numerators (§6.7).

### 1.2 The question space is closed over measures BY TYPE, not by convention

`mac-runtime/src/mac_runtime/models.py:118-131`:

    class Intent(BaseModel):
        model_config = ConfigDict(extra="forbid", frozen=True)
        measure: str                     # required — the ONE subject slot
        slices / filters / period / stage / confidence

`Vocabulary.from_index` splits 17 concepts into 3 `MeasureTerm` and 14 `DimensionTerm`; a dimension
can only ever become `slices[].term`. Live: **6 of 6** suggestions carry a measure, **0 of 6** carry
a concept subject. With `extra="forbid"`, a concept subject cannot even be smuggled through.

### 1.3 The answer path refines rows; it never produces a scalar

`check_answerability.py:62` — `STEPS = ("read", "select", "resolve", "grain", "period")`. Every step
narrows WHICH ROWS. There is **no `COUNT` and no `COUNT(DISTINCT)` anywhere in `mac_runtime`**
(grep: 0 hits in `planner/`); the only aggregate on the rule-less path is `SUM` at `sql.py:538`.

### 1.4 The derivation for "why can't you answer that" already runs, and reaches nobody

`answer_path(doc, raw, shared)` (`check_answerability.py:81-138`) derives, per concept, the
declaration that supplies each of those five steps — or `None`. That is exactly the material an
honest refusal is made of. Measured reachability:

| question | measured |
|---|---|
| `answer_path` / `answerability` / `render_guarantee` referenced anywhere in `mac-platform/packages` | **0 hits** |
| callers of `render_guarantee()` (`check_answerability.py:300`), written to render a derived path FOR A READER | **0**, estate-wide |
| importers of `check_answerability` | **1** — `mac_compile.py:72`, the MAC011 build gate |
| derived paths surviving into `compile.json` | **0** — only the unfillable steps are kept as witnesses |

**Introspection is already pointed inward at CI. The whole ask is to also point it outward.**

### 1.5 The refusal cannot be honest, because of a type error one layer up

`interpret/prompt.py` instructs the interpreter to lower its confidence when the question is
"ambiguous, under-specified, **or names something outside this vocabulary**" — two unrelated facts,
one float. `interpret/gate.py:28,60-69` then compares that float to `DEFAULT_LOW_CONFIDENCE_THRESHOLD
= 0.5` (mirrored as `_CONFIDENCE_DEFAULT = 0.5`, `ask_engine.py:102`) and emits its single sentence:
*"…Could you rephrase it, naming the measure and any slice/filter/period you want?"* — asking for a
measure that cannot exist for this question. `interpret_or_clarify` returns `Intent | Clarification`
only, so the interpret step **can never reach a `Refusal` at all**.

No threshold fixes this. The two states — *"I did not follow you"* and *"I followed you exactly and
have no route"* — were merged into one number before the gate saw them.

### 1.6 The sharpest fact: the model is already told the answer

`Store.definition` contains, verbatim: *"a question about 'how many stores' means 67, not 74."* That
string is carried on `DimensionTerm.definition` and written into the interpreter's system prompt on
**every call**. The model reads it every time and cannot emit it, because the only output type it
has is an `Intent`.

### 1.7 And bending the measure route is not a safe shortcut

`Intent(measure="Product")` resolves **today**: `_resolve_measure` does a bare
`index.concepts.get(term)` with no class check (`plan.py:269-282`); the planner contains **0**
`ConceptClass`/`klass` guards (grep across `planner/`); `measure_column` returns
`_role_from_field_roles(concept, "measure")[0]` with no uniqueness check
(`grounded_columns.py:282-284`), and Product declares **three** measure roles — `Weight`, `Cost`,
`Price`. So "how many products" down the bent route emits `SUM(dim_contoso_product.Weight)`:
catalogue weight in mixed units, over a column NULL on **284 of 2 517** rows and carrying its own
open question (`PRD-Q2`). Full provenance, full confidence tier, **wrong in kind**.

The only thing standing between this estate and that number is the interpreter scoring such questions
under 0.5. **That is luck, not a safeguard.** A typed subject replaces luck with a type.

---

## 2. THE LINE — the deliverable

> **DERIVABLE** — the answer is a function (a read, a projection, or a deterministic count) over
> declarations that already exist in the bundle, evaluated by code, **where every choice the answer
> makes is itself declared**.
>
> **NEEDS A HUMAN** — answering requires choosing between readings the bundle has not ranked.

**Why the boundary is exactly there, and not somewhere more convenient:** the bundle is a set of
propositions, each with one home and one author. A projection of propositions adds none; a choice
between them adds one. **Adjudication is authoring.** A model that adjudicated would be writing into
a home it does not own — which is the one-home rule the operator invoked, turned on the model itself.

### 2.1 The operational test — three clauses, all must hold

| | test | the failure it forbids |
|---|---|---|
| **T1** | **CLOSED INPUT.** Every input is a declared field or a closed-vocabulary term (`identity.kind` 4 terms in use of 7; `class` 6; `mac.rule_kind` 6; `ConfidenceTier` C/I/Q). Prose may be **quoted**; it may never be **parsed for a value**. | Regexing `2 517` out of `identity.note`. That note is evidence for a human; the number must come from the relation via the declared key, or the answer has smuggled a second home into a comment and inherited its drift. |
| **T2** | **TOTAL FUNCTION.** Total over the declared domain, or it returns `None` and the route refuses. No default that guesses. | A count that falls back to `COUNT(*)` when no identity is declared. |
| **T3** | **NO RANKING OF RIVALS.** Where two declarations could both answer, either their precedence is itself declared, or the question needs a human. | Picking `StoreKey` over `StoreCode` — or picking silently between `ProductKey`, `ProductCode` and `ProductName` because they happen to agree today. |

A future author applies this to a question nobody has asked yet by naming the declaration that
supplies each step of the answer. **All resolve → derivable, and no human may be asked. One resolves
to `None` → that missing declaration IS the answer to "why can't you answer that."**

### 2.2 The seven candidates, ruled

| question | ruling | what supplies it | what it costs |
|---|---|---|---|
| **how many X do you know** — cardinality of a concept's instance set | **DERIVABLE** | `identity.canonical_key` (13 of 17) or a declared collapse `natural_key` (1 of 17) or `values.items` (1 of 17), over `grounding.sources[0].relation` (17 of 17). Must carry which identity it counted (§4). | the sixth step + the count builder. **0 of 17** concepts need a new field. For the **4 of 17** with no `canonical_key` — the 3 measures and `OrderLine` (kind `composite`) — it must refuse and offer the row count as an explicitly *different* question (§7 Q4). |
| **what can you answer** — the capability surface | **DERIVABLE** | already computed, already served, already free. | fixing two denominators it publishes (§6.7) and admitting its own shape: the subject slot is typed `measure`, so 14 of 17 concepts can never be a question's subject. |
| **why can't you answer that** — the honest refusal | **DERIVABLE**, and the highest value of the seven | `answer_path()`, which already derives it per concept and is discarded. | a seam, not a fact. It can only ever NARROW what the system asserts, which is why it should be built first. |
| **what does a measure mean** — a definition held as prose | **DERIVABLE, VERBATIM ONLY** | `concept.definition` (17 of 17), `semantics.purpose`, `semantics.measure_type`. | the route quotes and returns the file path. **A summarised definition is a second home for meaning, authored at read time by a model, with no owner.** Definition without additivity is also incomplete: two of three measures are `Flow`, one is `Precomputed`, and reading a `Precomputed` measure as summable produces a figure wrong by a factor of the period. |
| **how is X identified** — identity, declared | **DERIVABLE** | `identity.kind`, `identity.canonical_key`, `identity.note` (17 of 17). | must include the rivals and the open question, or it is a confident-wrong-number about identity itself. Cannot be answered through the interpret prompt: `Vocabulary` is never populated from `Concept.grounding` by construction (`vocabulary.py:59-66`) and a key is a column name. Post-interpret, deterministic, always. |
| **what changed since yesterday** — provenance / versioning | **NEEDS A HUMAN** (split) | derivable: *whether* anything changed (fingerprints, `governance.last_reviewed` 17 of 17), and which files moved (git). | NOT derivable: what changed semantically. No prior bundle state is retained to diff against; `governance.change_log` is authored prose recording what an author MEANT, which is a different fact from what moved; and `Concept` parses neither `governance` nor `version`. "Changed" also has four defensible readings — declarations, served data, registers, or the numbers an answer would now return — and nobody has chosen. Refuse, and name the absent home. |
| **how confident are you in this figure** — proof state | **DERIVABLE as proof state, NEVER as probability** | `ConfidenceTier` per concept (17 of 17, all tier I here) and per rule; `min_confidence` over every touched concept and rule already ships on the answer (`render.py:110-181`). | must never be answered from `Intent.confidence`. That float is a model's opinion of its own reading of a sentence; C/I/Q is the proof state of the declarations used. Two unrelated quantities sharing one word (§6.4). Rendering a tier as a percentage is a new semantic claim and must be refused. |

**Four bans follow from the line, and all four are unconditional:**

- **No paraphrase.** Quote prose verbatim with its path, or refuse.
- **No self-score as figure confidence.**
- **No bare count.** Carry which identity was counted, or refuse.
- **No refusal that asks the asker to rephrase.** Name what is missing and who owns it.

---

## 3. What to build — smallest first

Every item below reuses machinery that already runs. **Nothing here is authored per concept; all of
it is authored once, in the platform, and every future bundle inherits it.** That is where cost
belongs, and it is the operator's test passed.

**0 — Fix the denominators the surface already publishes.** *Reuses:* `capabilities()`. *Costs:*
three lines. It publishes `rules: 3` when the bundle declares **31** (3 in `ontology/rules.yaml` plus
**28** typed `contract.rules` across 17 of 17 concept files — including the one rule that rules on
counting stores), and `registers: {files: 2, entries: 7}` against **17** register files holding
**3 315** data rows, 15 skipped as undeclared. A new introspection answer inherits this habit unless
the habit is fixed first.

**1 — Give `mac.rule_kind.aggregation` a consumer, and gate the rest.** *Reuses:* the existing
exclusion/default consumer home (`grounded_columns.py:423,526-527`) and the resolution consumer
(`register_declarations.py:9`). *Costs:* one reader in one place. **Blocking.** Measured: this bundle
uses 6 rule kinds — resolution 7, aggregation 6, exclusion 6, guarantee 4, ambiguity 4, default 1
(28 total) — and the runtime consumes **3 of those 6**, so **14 of 28** authored rules are of a kind
nothing reads. `rule.when` has exactly one runtime use (`plan.py:513`), as a substring haystack for
choosing citation text — never as a trigger. **A declared kind with no consumer should be a build
FAIL with its denominator printed**, not a silent no-op.

**2 — `answer_path()` gains a sixth step: `aggregate`.** *Reuses:* the tuple that already runs, the
gate that already fires `D.empty_denominator` on zero concepts (`check_answerability.py:145`), and
`render_guarantee()`, which already renders a path. *Costs:* one key plus a precedence function.
Precedence, every input a declared field, no prose parsed:

    1. class == measure                       -> "already a scalar"; governed by semantics.measure_type
                                                 (Precomputed is read as stored, never folded)
    2. identity.kind == sme_pending           -> exempt (the existing refuse-stub exemption, verbatim)
    3. grounding.realized_by.params.natural_key -> COUNT(DISTINCT natural_key)   [the collapse says the
                                                 row is a VERSION]      Store -> StoreCode -> 67
    4. values.items                           -> len(items), no query at all     AgeBand -> 15
    5. identity.canonical_key                 -> COUNT(DISTINCT key) on sources[0].relation
                                                                                 Product -> 2 517
    6. else                                   -> None -> MAC011, and the route refuses

Measured against this bundle: steps 1-5 resolve for **17 of 17** concepts with **0** new fields. It
also closes a hole in the existing five: `grain` currently derives from the presence of
`snapshot_rule` with `realized_by.udf` defaulted to the literal string `"prose"`, so a
paragraph-only collapse PASSES today. `COUNT(DISTINCT ?)` cannot take a paragraph, so the sixth step
turns that into a finding.

**3 — The seam. This is the deliverable; item 2 is the cheap half.** *Reuses:* `OntologyIndex`,
already loaded by the console. *Costs:* moving the derivation to a runtime function over the index
rather than a CI function over raw YAML dicts, and serving it. Without this, CI gets a better gate
and the asker still gets "could you rephrase" — which is the failure mode every design named and
none avoided by itself.

**4 — A typed subject: `SubjectKind` + `ModelIntent` as a PEER of `Intent`.** *Reuses:* the existing
tool-call shape; `Interpreted = Intent | ModelIntent`; one `isinstance` at `ask.py:107-110`, between
interpret and plan. *Costs:* one new model and one branch. **Do not widen `Intent` in place.**
`measure: str` is required, frozen, `extra="forbid"`, and embedded in `AnswerObject.intent` and
`SemanticsApplied.measure` — making it optional silently retypes every stored answer, fixture and
replay recording, and makes `_resolve_measure`'s honest refusal unreachable. A peer type is also what
makes §1.7 impossible by construction rather than by luck.

**5 — `reflect()`: one deterministic responder.** *Reuses:* the shared rule reader from item 1, the
planner's existing refusal grammar (`Refusal.human_reason`, `missing[]`, the *"Nothing was executed /
Filing an open question"* form). *Costs:* one function and one SQL template. **It must CALL the rule
reader the planner calls, never re-implement it** — duplicating enforcement is a worse two-homes
defect than duplicating a fact. It composes nothing: it selects a subject and returns declarations.

**6 — Split the refusal (§5).** *Reuses:* `ReasonCode`, which already carries `ontology_gap`,
`unresolved_term` and `unsupported_intent` — the last of which is unreachable from interpret today.
*Costs:* `interpret_or_clarify` must be able to return a `Refusal`, and the prompt must stop saying
"naming the measure".

**7 — Let the parser keep what it already reads.** *Reuses:* `parse_profiles`. *Costs:* keep
`profile.rows`, per-column `distinct`/`nulls` and `measured_at` on `MeasuredIdentity`, and stop
`continue`-ing past a profile with no `identity_evidence`. Measured: **6 of 14** profile files are
skipped for that reason and the 6 are **exactly the served plane** every concept grounds on — so the
index today cannot see a single measured distinct count for any relation a concept actually uses.
**Take this for the DENOMINATOR and the evidence, not for the number** (§7 Q1). The parser's own
comment justifying the drop — "a reader that re-derived a key from them would be measuring" — is
sound for deriving a key and does not cover citing a dated measurement.

---

## 4. The identity ruling — how a count says WHICH identity it counted

### 4.1 Why this is the whole problem

Re-measured read-only on 2026-09-19, served plane, all 13 concepts that declare a `canonical_key`:

| relation rows vs DISTINCT canonical key | concepts | worst |
|---|---|---|
| row count IS the answer | **3 of 13** | — |
| row count is wrong by a declared ruling | **1 of 13** | Store: 74 rows, 74 `StoreKey`, **67 `StoreCode`** — a 10.4 % overstatement on a base of 67 |
| row count is wrong by an order of magnitude or more | **9 of 13** | 37× to **44 795×** (one concept: 223 974 rows, 5 members) |

`COUNT(DISTINCT canonical_key)` is right on 13 of 13. **The operator's store case is the mildest
error available in this bundle, not the worst.** And note the trap underneath: `grounding.cell_key`
is the RELATION's row identity, not the concept's instance identity — they coincide on only **4 of
17** concepts. Any implementation reaching for the cell key ships the 9-of-13 bug.

### 4.2 Finding the ruling — structurally, never by matching prose

A `contract.rules[]` entry whose `kind` is `mac.rule_kind.aggregation` **AND** whose `binds`
intersects the concept's identity columns — `{canonical_key, declared natural_key, cell key}` — in
**two or more** places is that concept's cardinality ruling.

Reproduced across all **6** aggregation rules on all **17** concepts:

| discriminator | selects | false positives |
|---|---|---|
| overlap ≥ 2 | `store.versions.entity_count_is_the_code` (binds `[StoreCode, StoreKey]` — two rival readings of one identity) | **0 of 6** |
| overlap ≥ 1 (the naive filter) | also a brand-axis orthogonality rule (binds one identity column plus a column belonging to another concept) | **1 of 6** |

`mac.rule_kind.aggregation` is about roll-up generally, not cardinality specifically, so **the kind
alone is not the discriminator** — identity-column overlap is. Matching the rule's natural-language
`when` clause is the other candidate and must be rejected for routing: it is a language judgment, it
would attach a rule id to a bad match and lend it authority, and the runtime has no such matcher.

### 4.3 The payload — a count is never returned bare

    the number        COUNT(DISTINCT <column>) — what was actually evaluated
    which identity    identity.canonical_key / the declared natural_key, plus identity.kind
    the ruling        the rule id, its `then` and `never` verbatim, and its confidence tier —
                      or, explicitly, "no aggregation rule is declared for this concept"
    the universe      the relation and grounding.grain
    the open items    EVERY open question on the concept — never a silent "none"
    the denominator   rows / distinct / duplicates, with measured_at and source_file

Worked, both derived, nothing authored:

> **67 stores.** `COUNT(DISTINCT StoreCode)` on `dim_contoso_store`, per
> `grounding.realized_by.params.natural_key`, because this relation is served at version grain —
> 74 rows, 74 distinct `StoreKey`. Ruling: `store.versions.entity_count_is_the_code` — *"count
> DISTINCT StoreCode, which is 67"*, never *"…DISTINCT StoreKey, which is 74 — the version count"*.
> **That ruling is provisional:** its confidence is `P`, and `STR-Q1` — *is the business entity the
> store CODE (67) or the store VERSION (74)?* — is `NEEDS_SME_CONFIRMATION`, owned by the operator.

> **2 517 products.** `COUNT(DISTINCT ProductKey)` on `dim_contoso_product`; 2 517 rows, 2 517
> distinct, 0 duplicates, measured on the served view. `ProductCode` and `ProductName` are **also**
> unique today (2 517 of 2 517 each) and are deliberately not the key. `PRD-Q1` — whether
> `ProductCode` is the business identity — is OPEN with the operator, so the three readings agree
> today and may not tomorrow.

### 4.4 The gate, so 74 cannot ship silently

A reject class in `check_answerability`, seeded as a `--self-test` mutant: **a concept with two or
more declared identity columns that disagree, and no aggregation rule binding two of them, FAILS at
warning** — the count is derivable but the reader would get a number with no statement of which
identity it counted.

**Its denominator, corrected.** Worded as "canonical key differs from cell key" it fires on **9 of
17** concepts and is wrong, because that conflates the relation's row identity with the concept's
instance identity. The correct trigger is a declared *rival* identity — a `natural_key` on a declared
collapse, or an identity-binding aggregation rule — which on this bundle is **1 of 17** (Store), and
Store already carries its ruling. The other 16 are unaffected because their readings coincide.

### 4.5 And the honest caveat on all of §4

**Every identity mechanism proposed here is fitted to n = 1.** Store is the only concept with a
`grounding.realized_by` (1 of 17) and the only one with an identity-overlapping aggregation rule
(1 of 6 rules, 1 of 17 concepts). Two ruling slots exist — `realized_by.params.natural_key` and the
aggregation rule — and on this bundle they agree, which is precisely the condition under which
choosing the wrong one ships undetected. **The route must read both and REFUSE if they name different
columns.** The mechanism is unfalsified, not validated; the gate in §4.4 is what would falsify it.

---

## 5. The honest refusal

Today, one sentence covers two unrelated states, blames the asker for both, and asks for a measure
that cannot exist. Replace the single threshold branch with a structural split — **self-score last**.

| state | what it means | what it returns |
|---|---|---|
| subject resolves, aggregate derives | answerable | the answer. No refusal. |
| subject resolves, aggregate is `None` | **the model's gap** | `ontology_gap`, naming the step, the slot, the file and the owner |
| subject is not in the vocabulary | unresolved term | `unresolved_term`, naming the register searched **and its population** |
| subject resolves, but the asked OPERATION has no route | **the model's shape** | `unsupported_intent`, describing the shape — not the wording |
| the subject itself is unreadable | genuinely not understood | the clarification stands — but it must quote what it DID understand and offer the capability surface, never demand "the measure" |

Replacement text for the case that started this, every clause derived:

> I understood you: you are asking how many distinct products I know. **The gap is mine, not your
> wording.** Every question this model can answer has a MEASURE as its subject — it holds 3 measures
> and 14 dimensions, and the dimensions appear only as breakdown terms. A question whose subject is a
> concept has no route here.
>
> Product IS one of my 14 dimensions, and I hold: its definition; its identity, `ProductKey`; its
> grounding relation; and a measurement of its size taken 2026-09-18. What I lack is the route from
> your question to that.
>
> `reason_code: unsupported_intent` · `missing: subject-kind-concept-has-no-route`

And the refusal for what reflection genuinely cannot do:

> I can tell you what I was declared to mean and how I was measured. I cannot tell you what you meant
> by a word nobody declared. "Margin" names no concept, no rule and no register here (17 concepts,
> 3 measures, 31 rule statements, 17 edges). That is not a gap in my reading of your sentence; it is
> **a decision no one has made.** Owner: operator.

**The hard rule: a refusal must never say "I don't know" where the truth is "nobody has told me."**
Those read the same and mean opposite things. One is a data gap; the other is an authoring gap, and
only the second has an owner who can fix it.

---

## 6. What this does NOT buy

**6.1 It is not self-awareness. It is reflection over declarations.** The model can read what it
declares and compute over it. It cannot invent a semantic it was never given, because there is
nothing to compute the invention FROM. It can say it knows 2 517 products and which key it counted;
it cannot say whether a product code arriving twice is a duplicate — `PRD-Q1` is OPEN, in the same
file the count came from. Knowing exactly which of its own questions are unanswered, and saying so
alongside the number, is the whole of what is on offer. A design promising the model will "just
understand" is the confident-wrong-number wearing a friendlier face.

**6.2 The disclosure everything above promises rests on a field the runtime does not carry.**
`ontology/caveats.py:4-19` states it outright: `open_questions` is an answer-store-level construct,
**not an ontology-index field**, and the caveat is APPROXIMATED from the concept's own
`ConfidenceTier` being `Q`. Every concept in this bundle is tier **I**, so `PRD-Q1`, `PRD-Q2` and
`STR-Q1` produce **no caveat today**. This bundle carries **29** open questions across **17 of 17**
concepts — every concept has at least one — so *"no open question to disclose"* must never be a
silent default, and until the index parses the construct, it silently is.

**6.3 The answer is not free, and nobody has ruled on what it costs.** `capabilities()` is free and
opens no connection. `COUNT(DISTINCT key)` on a served relation is a warehouse query, and the same
endpoint publishes `consent: {act: question, cost: billed}`. Classifying the subject also runs the
interpreter — a model call — *before* anything knows the question needs no warehouse. "Introspection
is already free" is true of the capability surface and false of the cardinality answer.

**6.4 `confidence: P` does not type-check against C/I/Q.** Every typed contract rule in this bundle
carries `confidence: P`; `render.py` computes `min_confidence` over touched concepts **and rules**.
`min(I, P)` is undefined across two vocabularies. So a derived count has no computable confidence
today, and any promise of "min over what it read" is a promise of an operation that does not run.

**6.5 `answer_path` already has a sixth key, and it is already invisible.** `path["default"] =
"contract.default_reading"` is set OUTSIDE the `STEPS` tuple, so any consumer iterating `STEPS`
drops it. Adding a seventh key to a structure whose sixth is already dropped repeats the defect.

**6.6 The `select` step is softer than its score suggests, exactly where a count needs it most.**
When `shared` is `False`, `select` returns *"a dedicated relation"* unconditionally — no declaration
is consulted. It can therefore only fail on a SHARED relation. But three concepts share one relation
with Product, and those are precisely the concepts where a row count is wrong by 79× to 315×. A count
over a shared relation is the case that most needs the select step, and it is the one case the step
actually tests. `aggregate` must report unusable whenever ANY earlier step is `None`.

**6.7 The estate's own introspection surface publishes numerators.** `rules: 3` of 31; `registers
{files: 2, entries: 7}` against 17 files and 3 315 rows. Both live right now. Nobody has proposed the
obvious enforcement — **a check that fails any published introspection field lacking its
denominator**, seeded with a mutant per class. The standing rule (never quote a PASS without its
denominator) applies to the model's description of itself, and is currently unenforced in the one
introspection surface that works.

**6.8 Which relation a multi-source concept counts is unruled.** "The concept's relation" is already
forked four ways across the estate (first source, first non-empty key, alphabetically first, any
grounded). Every design here writes `sources[0]` without noticing it is choosing a fork.

**6.9 A dated measurement served present-tense is a new species of confident-wrong-number.** The
profiles carry `measured_at`; the store profile carries **no** `source_watermark`. A number that is
right-when-measured and indistinguishable from a live read is worse than either. If a profile figure
is served at all, the value, its `measured_at` and its `source_file` travel as one indivisible triple
or not at all.

**6.10 The count SQL is the largest unpriced item in this record.** There is no `COUNT` builder in
the runtime. How a count Plan obtains the same rule application, caveat propagation and
`min_confidence` the `SUM` path gets is not specified here, and should not be hand-waved when it is.

**6.11 The acceptance-oracle grammar is a specification, not a seam.** The mature bundle's
`must_pin` / `must_not` / `must_surface_any` contract is the right shape for carrying a ruling to a
reader — and it has **no runtime reader on either bundle**. Treating it as existing machinery
overstates what is built.

---

## 7. Open questions for the operator

Each is answerable in one word. Each carries a recommendation, so silence is not required to mean
anything.

**Q1 — Where does the number come from: the warehouse, or the dated profile?**
They are different facts with different failure modes ("2 517 now" vs "2 517 as of 2026-09-18").
*Recommendation: **BOTH** — count the relation for the NUMBER, cite the profile for the DENOMINATOR
and its `measured_at`, and say which is which.*

**Q2 — Does asking a question about the model bill?**
Classifying the subject is a model call even when the answer needs no warehouse.
*Recommendation: **DISCLOSE** — classification is billed and says so; the answer itself declares
whether it touched the warehouse. No silent free/paid ambiguity.*

**Q3 — `STR-Q1`: is a store the CODE (67) or the VERSION (74)?**
This is the one genuine semantic decision in the whole record, it is already filed, and it changes
every store count in the bundle. Until it is ruled, every derived store count must say "provisional".
*Recommendation: **CODE** (67), which is what the concept, the rule and the default reading already
assume — ratifying it costs one status change and removes a standing caveat.*

**Q4 — The 4 of 17 concepts with no `canonical_key` (3 measures + one composite event): refuse, or
count the cell key?**
*Recommendation: **REFUSE**, and offer the row count as an explicitly different question. A line
count wearing an entity count's label is the exact defect §4 exists to prevent.*

**Q5 — When all identity readings coincide (Product: 2 517 three ways), may the disclosure be
omitted?**
*Recommendation: **NO.** The disclosure must fire on agreement too, or it will be missing exactly
when divergence begins.*

**Q6 — Is the sixth step also a build gate, or only a route?**
*Recommendation: **GATE**, at warning first — this estate turns rules worth enforcing into a check
with seeded reject classes, not a promise.*

**Q7 — Which home owns the derivation: the framework's CI tool, or the runtime?**
It currently lives in a CI tool over raw YAML, in a different repo from the index it describes.
*Recommendation: **RUNTIME** — derive over `OntologyIndex`, and have the CI check call it. One home,
and it is the same move that closes the seam in §3 item 3.*

---

## 8. What would reverse this

- A ruling on `STR-Q1` that makes the version the business entity: §4's worked answer changes from
  67 to 74 and the precedence in §3 item 2 inverts. The mechanism survives; the number does not.
- A concept acquiring a second identity that disagrees with the first without a ruling: §4.4's gate
  fires, and what must then be authored is **the ruling** — which identity is the business entity —
  never a count.
- Evidence that `mac.rule_kind.aggregation` is consumed somewhere outside `mac_runtime`: item 1 of §3
  stops being blocking.
- A second concept acquiring a declared collapse: §4.5's n = 1 becomes n = 2, and the mechanism
  becomes falsifiable for the first time.
