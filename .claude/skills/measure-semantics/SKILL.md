---
name: measure-semantics
description: Classify a measure's additivity through the framework's single registry rather than restating it per concept. Use as step P8.
---

# P8 · Classify the measures — additivity is three facts, not one

Every measure concept must say what kind of quantity it is and what kind each of its axes is, so that
the framework can decide — for any axis, at any time — whether folding the measure along that axis is
a SUM, an average, or forbidden. Skip this and the bundle still compiles: the measures simply behave
as if everything were addable, and the first wrong number is a total that counts the same thing twice.
The failures here are quiet and plausible. A level measure summed over twelve months looks like a
bigger business; a share whose denominator was folded the wrong way comes out above 100% and gets
explained away as a data issue for a month. Do this step properly and the fold becomes a fact the
model holds, rather than an assumption whoever writes the next query makes.

## When

After P7 (the measure concepts exist, each grounded on a served dataset with a declared grain), before
P9. You need, for each measure: its declared grain from P2 — that is where its real axes come from —
and, if you intend to materialize a registry, the lookups plane from P6. Do not classify a measure
whose grain you have not declared; you will classify the axes you imagined instead of the ones it has.

## Do

1. **List every concept with `class: measure`.** These, and only these, get classified. A dimension
   concept has no additivity.

2. **Read the closed domain before choosing a type.** Open
   `meaning-as-code/mac_vocabulary.yaml#MeasureType` and read the members it actually declares today.
   Do not take the member list from a checker docstring or from an older bundle — at least one gate's
   own docstring lists a member set the domain has since grown past, and the gate reads the file at
   runtime while the docstring does not. Each member answers "what kind of quantity is this?":
   - **Flow** — accrues during a period and accumulates: orders placed, units shipped, revenue booked.
     Two periods add; two regions add.
   - **Stock** — a level observed at a moment: open orders standing, inventory on hand. Regions add;
     periods do **not** — an order open in March and April is one order, not two. A period reading is
     the level at the period's end, resolved, never summed.
   - **Intensive** — a per-entity magnitude meaningful only as an average: a duration, an age, a rate,
     a ratio, a signed deviation. A total of days-to-deliver is not a number anyone wants. The correct
     fold on *every* axis is a mean/median/percentile, which is not a weaker form of additive — the two
     disagree about whether the sum means anything at all.
   - **Precomputed** — the value exists only at the grains it was computed for; you locate the row
     matching the requested combination and read it. Nothing is derivable from narrower cells, on any
     axis. Weeks-of-cover published per aggregation level is the archetype.
   - **Target** — a planned level rather than an observed quantity. It behaves like a level over time
     *and* is not summable across entities: adding this quarter's regional targets is arithmetic the
     business never authorised.

3. **Write the type as a qualified reference** — `concept.semantics.measure_type: mac.MeasureType.<Member>`.
   Bare member names and invented spellings resolve to nothing.

4. **Declare `concept.semantics.axis_kinds` for every axis the measure is really keyed on**, mapping
   each to `mac.axis_kind.time` or `mac.axis_kind.categorical`. Take the axis names from the grain, not
   from the columns you find convenient. An axis you omit is an axis the law cannot speak about, and
   the model will honestly return "no statement" rather than a fold.

5. **Do not write `concept.semantics.additivity`.** The per-axis fold is *derived* from (type × axis
   kind) by the framework law, and the derived value carries the law's own provenance, so a reader can
   still see where it came from. This is the third fact, and it is the one you must not author. A
   measure that writes it authors both the premise and the conclusion, and they drift: a planning
   target once declared its type correctly and then wrote `additive` on its entity axis, and a
   downstream value anchor summed that target across product lines for weeks on the strength of it.
   You cannot contradict a value you do not write. The schema still accepts the block so legacy
   bundles validate — that is tolerance, not endorsement.

6. **Name the axes the law cannot rule on, in prose, where they belong.** Two cases recur:
   a *measure selector* — a discriminator column where changing the value selects a **different**
   measure, so no fold along it means anything; and a *restating axis* — a relation that carries both a
   rolled-up total row and the rows composing it, where summing across the column double-counts a large
   fraction of the volume. The second is a property of the **relation**, not of the measure: the measure
   may be a perfectly additive Flow and still be un-summable along that column. Say so in the grain and
   in a concept rule. Do not "fix" it by downgrading the measure's type — that lies about every other axis.

7. **If consumers need the fold without resolving the vocabulary, materialize a registry** — a lookup
   CSV carrying the three columns `measure_type`, `additivity_time`, `additivity_categorical`, one row
   per measure code (alongside whatever family/variant/source columns the register already has).
   **Generate the two additivity columns from the vocabulary in a build script; never type them.** The
   registry is a projection of the law, and a hand-typed projection is a second home for a fact.

8. **Write no per-measure aggregation rule at all.** An earlier version of this step asked for one
   rule per measure — *"when folding this measure along an axis, read the registered effect for that
   axis"* — citing the register and putting the prohibition in its `never`. **`check_cookbook_smells`
   rejects that shape, and the gate is right. The instruction was the defect; it is withdrawn.**

   MEASURED on five measure concepts each carrying exactly that rule and nothing else unusual: it fires
   **C6** — `rule shape 'aggregate.read_registered_effect' is written on 5 concepts — a law nobody has
   stated` — and **C2** — `then only reads additivity, which the concept already declares` — five
   witnesses each. Binding the rule to a canon (`realized_by`) silences C6 and leaves C2 firing on all
   five, so there is no spelling of this rule that comes out clean. Deleting the rules clears both.

   The rule was buying nothing it claimed. The fold is already derived from (`measure_type` ×
   `axis_kinds`) by the framework law — that is step 5's whole argument, and it applies here with the
   same force: a rule restating the fold is a second home for it, in prose, once per measure. And
   nothing *reads* it — `check_additivity_in_sql` enforces the fold from `mac_vocabulary.yaml#MeasureType`
   and the concept's own `axis_kinds`, never from `contract.rules`. The one-cell edit in the register
   already reaches every consumer; N rules announcing that it will are N copies that can drift from it.

   So: classify the measure (steps 3–4), project the register if consumers need it (step 7), and write
   no aggregation rule. The fold rules you *should* write are the ones in step 6 — the measure selector
   and the restating axis — because those state something the law cannot reach. They are per-relation,
   few, and specific. If even those reach five concepts, read C6's diagnosis: it names the columns your
   bundle types nowhere, and the answer is the missing declaration, not the rule.

   **Read the severity honestly.** Both findings are WARNINGs: `check_cookbook_smells` exits 0 on its
   own, and `mac-compile` returns non-zero only on error-severity findings. So these rules *ship green*
   while standing as a permanent MAC003 on every measure you own. That is exactly the green step 9
   tells you not to trust.

9. **Run the gates below, and read what they printed**, not just their exit codes.

## Produces

- `ontology/concepts/<Measure>.yaml` → `concept.semantics.measure_type` +
  `concept.semantics.axis_kinds.<axis>`, and **no** `concept.semantics.additivity` block.
- Optional but recommended: `data/lookups/<measures>.lookup.csv` with
  `code,…,measure_type,additivity_time,additivity_categorical`, plus the script that derives it
  (`data/lookups/<measures>.lookup.build.py`) and its `.md` companion.
- **No** per-measure aggregation rule (step 8). Only step 6's selector/restating-axis rules, where
  the relation carries something the law cannot rule on.

## Accepted by

- **`check_measure_additivity_registry <bundle-root>`** — recomputes every registry row from
  `mac_vocabulary.yaml#MeasureType` and asserts cell-for-cell equality. In my words: *you may project
  the law, you may not restate it*. It was written after a registry populated by hand drifted the same
  day it was written — a level measure's time axis spelled with a term from a different, coarser scale,
  and a target written additive across entities, which is the registry claiming the plan could be summed
  across regions. `mac-compile` files its failures as MAC004: two statements of one fact, disagreeing.
- **`check_additivity_in_sql <root>`** — static-analyzes the SQL in your acceptance properties and
  reports any `SUM` of a measure that crosses an axis the law says it cannot cross, unless that axis is
  pinned or grouped somewhere in the statement. In my words: *the rules you wrote about folding must
  hold in the queries you shipped*. Nothing about additivity is written in the gate — it reads the
  vocabulary and your `axis_kinds`, so changing the law changes what it rejects.
- **the fact-homes check inside `mac-compile`** (`tools/mac_checks_semantic.py#check_fact_homes`) —
  MAC003 when a fact is restated and the copies agree, MAC004 when they disagree. This is what catches
  an authored `additivity` block contradicting its own `measure_type`. Restated-and-agreeing is only a
  warning because nothing is wrong *today*; that is exactly the state the target-summing incident sat
  in before it became wrong.
- **`check_cookbook_smells`** (MAC003, warning) — C6 reports one rule SHAPE written on five or more
  concepts as "a law nobody has stated"; C2 reports a rule whose `then` only READS a slot the concept
  already declares (`measure_type`, `additivity`, `grain`, `closure`) with no derivation verb in it. The
  per-measure aggregation rule this step used to ask for trips both at once — see step 8. It warns, it
  never reds, which is why it ran for a long time without anyone acting on it.
- **`check_vocabulary_drift`** — MAC008 when a `mac.<vocabulary>.<term>` literal names a term its
  closed vocabulary does not define. **Read its scope honestly: it scans the framework's own
  `tools/**.py`, not your bundle.** It exists because a closed set's members were hand-copied into three
  Python files and one copy grew a member the vocabulary never had. The lesson transfers to your side
  even though the gate does not follow you there: re-listing a closed vocabulary anywhere is N homes
  for one fact.
- **Schema validation** — the measure template requires `measure_type` and `axis_kinds`; the per-axis
  `additivity` block is not required and is marked derived.

## Getting it right first time

- **Typing a market-size or population measure as a level because it "describes a state".** The tell is
  arithmetic: a ratio built on it exceeds 100%, or a yearly figure equals a single month's. Ask instead
  whether the underlying rows are *events counted during* the period. If they are, it is a Flow.
- **Typing a duration or a rate as a Flow because the column is numeric.** The tell is a total that no
  one would ever quote: "1.4 million delivery-days". That is Intensive.
- **Conflating a target with a level.** They fold identically over time, so the mistake survives the
  obvious test and shows up only when someone adds targets across entities. Keep them distinct types.
- **Writing the `additivity` block "for readability".** The tell is MAC003 on every measure/axis pair.
  Delete the block; the derived value renders in the projections anyway, carrying the law's provenance.
- **Writing a fold rule that says "read the register".** The prose form of the same mistake: it does not
  write `additivity`, it narrates it. The tell is MAC003 twice over — C6 on the shape, C2 on the `then` —
  with one witness per measure. Delete the rules; nothing downstream was reading them (step 8).
- **Guarding a rule on a token that exists in no vocabulary.** Eight copies of one aggregation rule once
  guarded on a spelling one character away from a real term, in a different scale. Every rule read fine
  and none of them ever fired. The tell: grep your rule prose for each value and confirm it appears in
  the register's real domain *or* in the framework vocabulary the column draws on.
- **Reading a green that means "did not run".** `check_additivity_in_sql` needs a SQL parser; without
  it, it prints that the canon is unavailable and exits 0. And the registry gate exits 0 with
  "nothing to project" when no lookup carries the three columns — which is also what it prints if you
  never built a registry at all. Read the last line, not the exit code.
- **Classifying axes the measure does not have.** Declaring an axis kind for a column that is not in the
  grain gives the SQL gate a name to look for and produces findings nobody can act on.

## What stays your judgment

No gate can tell you **which type a measure is**. The gates check that your classification is projected
consistently and obeyed in SQL; they cannot check that it is true. That judgment belongs to whoever
knows whether the rows are events or levels, and it must be surfaced for challenge rather than settled
by whoever was typing — write the classification down as a table a domain expert can read and contradict
without opening a YAML file, and record which calls you consider contestable.

Equally yours: whether an axis is genuinely a *selector* or genuinely a *dimension*; whether a restating
axis in the relation is a defect to fix upstream or a shape to guard against; and, for a Precomputed
measure, which stored row answers a given question. The law says only that no fold is valid; *which cell
to read* is a resolution decision your concept has to make and state.
