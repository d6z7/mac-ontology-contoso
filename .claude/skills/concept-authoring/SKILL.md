---
name: concept-authoring
description: Author an ontology concept that binds meaning to a served dataset and can be answered from without a probe. Use as step P7.
---

# P7 · CONCEPT — author the meaning

Everything before this step measured, moved or named data. This step says what it **means**: one business
notion, its definition, how it is identified, which served relation carries it, and the contract an agent
may rely on. Rushed, the bundle still compiles — it becomes a schema with prose stapled on, and the failure
surfaces later as an answer that is fluent, grounded in a real column, and about the wrong thing. Three
agents given no method all certified a bundle here, and all three drew the concept boundaries differently.

## When

After P1–P6, not before. You need: the served dataset descriptor with its column list (P5), the declared
grain and its evidence (P2), the transform producing the relation (P4), and a lookup register for every
dimension a question might name in words (P6). A concept grounded on a raw landing, or whose
`no_probe_guarantee` cites a register nobody built, is rejected — both produce wrong answers confidently.

## Do

1. **Decide it is a concept at all.** A relation BETWEEN two named notions is an edge; a *computed* value is
   a rule; a column's type is physical. Only the meaning, structure or values of one thing is a concept. Two
   consequences newcomers miss: a pure mapping/bridge table is **not** a notion — it dissolves into an edge
   on the notions it relates; and a notion may exist with **no table of its own** (a perspective, a plan
   stage, a roll-up), grounded on whichever relation carries its discriminating column.
2. **Fix the mapping, which is M:N.** One concept may ground on several relations (`grounding.sources` is a
   list); one relation may serve several concepts, and grounding on it does not consume it; some relations
   back no concept. If you are writing one concept per served table, stop — you are modeling the warehouse.
3. **Choose the class first, and write its required block.** The vocabulary is closed — `entity · event ·
   measure · enumeration · reference · grouping · meta` — and a seventh is a rejection, not a discussion.
   If you would `SUM` it, `measure`; if you would `JOIN` to it, `reference`. A leaf dimension is `reference`,
   something with members below it (region over country) is `grouping`. A small coded set with no attributes
   of its own is `enumeration`; a keyed table with several attribute columns is `reference`. `entity` is the
   residual — reach for it last. Each class dictates one mandatory block: `measure` → `concept.semantics`
   with `measure_type` + `axis_kinds`; `enumeration` → top-level `values` with `closure` + `items`; `event`
   → `lifecycle`; `grouping` → `members` with a required `over:`. Placement matters: `semantics` nests under
   `concept:`, the other three are siblings of it.
4. **Write the canonical definition — 2 to 4 sentences a domain expert would sign.** Say what one row is, at
   what grain, and — the sentence people skip — what it *excludes*: the neighboring notion a reader would
   otherwise assume it covers ("shipments dispatched in the period; one booked but not yet dispatched is not
   counted here"). That clause stops the next author re-modeling the same notion under a second name.
5. **Declare identity.** `identity.kind` from the closed set (`code`, `iso`, `namespace_code`, `fk_name`,
   `composite`, `resolved_axis`, `sme_pending`) plus `canonical_key`, which is a **single column name, a
   string**. If the grain is a composite of several columns — typical for a fact — set `kind: composite` and
   **omit** `canonical_key` rather than making it a list. Never build an identifier by concatenation (P2);
   a fabricated key reads downstream as a real absence.
6. **Ground on the served dataset, in the relation's own spelling.** `grounding.sources[].relation` equals
   the dataset name exactly (P5); `key` / `columns` must be columns of *that* relation. Inherit the key from
   the measured grain rather than declaring a fresh one, and record where it came from. Add
   `grounding.field_roles`: a whitelist mapping each meaningful column to key / dimension / attribute /
   measure. Columns you omit carry no ontology meaning — that is the point: it declares what you ignore.
7. **For a measure, choose `measure_type` deliberately, then stop.** `Flow` accrues and sums over time;
   `Stock` is a level read at a point in time; `Intensive` is meaningful only as an average (a duration, a
   rate); `Precomputed` exists only at the grains it was computed for; `Target` is planned, not observed.
   **Do not write an `additivity:` block** — how the measure folds is derived from `measure_type × axis_kind`
   by the framework's law (P8). Writing it out authors both premise and conclusion, and they drift: one
   concept declared `Target` and wrote `additive` on a categorical axis, and a tool summed a planning target
   across products for weeks on the strength of it.
8. **Write the contract as declarations, not prose.** `contract.default_reading` says what to assume when the
   question is silent — which variant, which perspective, which period reading. Silence is the commonest
   question shape, and an undeclared default is decided at random. For rules: **where the framework has a
   canon for the shape, bind it** — supply `realized_by: {udf: …, params: {…}}` and omit `when`/`then`/`never`,
   which are rendered. The params are the part only you know; the most valuable names the *confusable*
   neighbors a tired reader would substitute when this one is empty. An empty actual answered with the
   target is worse than no answer.
9. **Make `no_probe_guarantee` derivable, not sworn.** It states what an agent needs *only*, to use the
   concept without asking the warehouse anything. Five steps must each have a declaration behind them:
   **read** (`sources[0]` with columns/key), **select** (how this concept's rows are picked out of a shared
   relation), **resolve** (the register that turns a name into a code, or in-file `values.items`), **grain**
   (the key, or a `snapshot_rule` where the relation republishes cells), **period** (for a measure,
   `measure_type × axis_kinds`). A step with no declaration means the concept is incomplete — supply the
   declaration; never write a sentence promising the step happens.
10. **A notion you cannot ground yet is still authored**, as `identity.kind: sme_pending`: it exists so a
    question about it gets a grounded refusal instead of an invention, and is exempt from the completeness
    gate by design. That is how an open question stays visible instead of becoming a silence. Then set
    `confidence` honestly (`C` confirmed / `I` inferred / `Q` needs an expert) — everything `C` with nothing
    ever run is the commonest false green.

## Produces

- `ontology/concepts/<name>.yaml` — **one concept per file**, keys in canonical order:
  `metadata → concept → ⟨class block⟩ → grounding → contract → constraints → governance → open_questions`.
- Optionally a sibling `ontology/concepts/<name>.md` — a *projection*, regenerated in P12, never hand-edited.

## Accepted by

- **`check_concept_columns_exist`** — every column a concept names must be a column of the relation it grounds
  on. Written after five concepts named columns that did not exist and nobody noticed for months: the sources
  spelled the same thing two ways (prefixed on the dimension, bare on the fact, inconsistently within one
  view), so a concept written against one relation's spelling and grounded on the other looks right to every
  human reader. Only a machine catches it.
- **`check_answerability` (MAC011)** — the five answer-path steps must be **derivable from declarations**.
  Written after hand-written guarantees were walked clause by clause and found to contain nothing not already
  declared elsewhere — and to have gone stale three times in one session as declarations moved, because prose
  is not checked. Two deliberate exemptions: a concept that is the sole user of its relation is selected *by*
  that relation and needs no discriminator; an `sme_pending` stub is authored to be unanswerable.
- **`check_common_rules` (MAC003 / MAC005)** — a concept rule restating a law the framework already states for
  its class is a copy, not a contract. Thirteen concepts once each wrote their own version of one refusal law:
  thirteen wordings, one promising an answer it could not produce. A rule that only carries *parameters* to a
  common law is legitimate, and is reported as information rather than a defect.
- **`check_cookbook_smells`** — C6: the same rule *shape* on five or more concepts is a law nobody has stated,
  and the check names the columns those copies bind that no concept declares, because the right home is
  usually not a new rule but an existing **declaration slot nobody filled** — an empty slot is invisible to
  every query that returns what is present. C2: a rule whose `then` only *reads* something the concept
  already declares (measure type, grain, closure) is a second home for that fact.
- **`check_ontology_grounds_on_datasets`** — a concept may bind only a served dataset, never a raw landing.
- **`check_lookups`** — every register your guarantee cites must exist, be non-empty, and name a real relation.
- **`mac_checks_adoption` (MAC005)** — warns where the framework offers a mechanism you did not use
  (`field_roles`, register delegation, a canon). Never an error: declining one can be correct, and a toolchain
  that blocked on it would be dictating your design.

## Getting it right first time

- **One concept per served table.** Tell: concept count equals dataset count. Re-run step 2.
- **Two orthogonal axes fused into one concept** — a variant and a reporting cycle, a status and a stage.
  Tell: the definition needs the word "and", or the guarantee pins two unrelated columns. If the cross-product
  is real, they are two concepts.
- **Splitting a concept per filter value.** Tell: several files identical but for one code, same grain, same
  refusal behavior. That is one concept with an alias map and a `default_reading`.
- **A guarantee that reads like instructions.** Tell: it contains "the agent should". Rewrite each clause as
  the declaration it wants to be; if there is nothing to point at, the concept is incomplete.
- **A key copied from the fact's obvious columns.** Tell: it omits a column the profile measured as part of
  the grain — typically a role/perspective or a republication marker. Every aggregate then double-counts,
  and nothing is red.
- **`additivity` written next to `measure_type`.** Tell: both present. Delete the derived one.
- **A physical column used as a YAML key.** Tell: a snake_case key that is also a column name. Physical names
  are always *values* (`relation:`, `canonical_key:`, `grounds_column:`).
- **`closure: closed` on a set you did not enumerate from the register.** Tell: `closure_why` missing or
  "appears stable". An honest open set costs nothing; a false closed set makes a real value unanswerable.

## What stays your judgment

No gate decides **where one concept ends and the next begins.** The gates prove your columns exist, that your
rows can be selected, that your guarantee derives — never that you carved the business into the right notions.
The working test is a person's: would someone asking for A be *misled* by being handed B? If yes, two concepts;
if they would merely be surprised by the default, one concept with a declared `default_reading`.

Nor can any gate decide the name a business would recognize; whether the definition is *true*; whether
`measure_type` is the right claim about the world (only that you made one); whether a code set is genuinely
closed; which neighbor belongs in `confusable`; or whether a rule says what the business means.
`confidence: C` is a claim you make, not a verdict the compiler reached — green means well-formed, never
correct. Leave genuinely open items as `sme_pending` concepts and recorded open questions, where someone can
see them, rather than deciding them quietly because you were the one typing.
