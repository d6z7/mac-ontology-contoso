---
name: ontology-shared-facts
description: Facts every ontology ingestion step needs: the canonical relation name and its five homes, the C/I/Q confidence vocabulary, closed-vocabulary rules, register id conventions, and which step owns which artifact. Read FIRST, and read it once — the other ontology skills cite it rather than restating it.
---

# SHARED — facts every skill reads, and none restates

These are the facts more than one step needs. They live here **once**, and the skills reference
them rather than repeating them.

That is not tidiness. It is the rule the framework enforces on the ontologies you build —
`check_measure_additivity_registry` refuses a bundle that restates the additivity law instead of
projecting it; `check_vocabulary_drift` refuses one that re-lists a closed vocabulary's members in
code; `check_common_rules` refuses a concept that restates a law the framework already states.
A kit that preached single-homing while stating one fact six different ways would have taught the
opposite of its own method, which is exactly what the first draft of these skills did.

**If you are writing a skill: a fact needed by two steps belongs here, not in both.**

---

## The kit ROUTES; the framework INSTRUCTS

The framework ships its own modeling instrument: **`reference_manual/patterns/`** (22 named
patterns — role-playing dimensions, degenerate dimensions, bridges, SCD, bitemporal, supertype /
subtype, and more) and **`MODELLERS_COOKBOOK.md`** (the anti-patterns `check_cookbook_smells`
enforces).

**Read them. These skills do not replace them and must never be used as a substitute.**

This is not a courtesy. It was measured: three operators with these skills produced 5, 12 and
16-never-written edges over an identical inventory, while two operators *without* them produced 8
and 8 — by reading the pattern index, which no kit-equipped operator opened even once. The kit
displaced a better instrument and the result got worse. Where a skill here and the framework's own
material disagree, **the framework is right and the skill has a bug**.

---

## When the kit and a gate disagree, the GATE wins

A skill may describe a shape a checker rejects. When that happens:

1. **The gate wins.** It is the executable statement of the rule; the skill is a description of it.
2. **Record the collision** — as a data-quality issue or a note in the bundle, naming the skill,
   the gate, and what you did. Do not silently obey one and forget the other.
3. **It is a kit defect.** Report it so the skill can be fixed, rather than each operator deciding
   privately.

Measured: two such collisions were each found independently by three operators and resolved three
different ways — one obeyed the gate, one obeyed the skill, one split the difference. Three
operators, one instruction, three ontologies. Adjudicating the conflict *in the kit* is worth more
than either answer.

---

## Source-agnostic KIT, source-specific BUNDLE

These are two different artifacts and they take **opposite** rules. Reading a rule written for one
as if it governed the other is a measured failure, not a hypothetical: in the naming experiment one
operator read the kit's source-agnostic rule below, concluded that a *served relation* must not
carry a source marker either, rejected the naming gate's convention on that basis, and produced a
name set with **zero overlap** with every one of its peers.

| artifact | rule | why |
| --- | --- | --- |
| **the KIT** — these skills, their examples, the identifier conventions they define | **source-agnostic.** It ships naming no source. | It is handed unchanged to every ingestion. A source's identity baked into it is wrong for every bundle but the one it came from. |
| **a BUNDLE** — the ontology you are building: its descriptors, its registers, its served relation names | **source-SPECIFIC.** Its served relations *should* carry its own marker. | It exists to serve exactly one source, into an estate shared with others, where its relations have to be addressable as **its**. |

So `<AREA>` in a kit identifier convention is a subject area because **the kit cannot know your
source**. A served relation name carries your source's marker because **the bundle is the one thing
that does**. *"The kit never carries a source identity"* is a rule about the kit, and it is **not**
an argument against a bundle naming its own source — it is the reason the bundle has to.

Which rule applies is settled by which artifact you are writing. Never by which reads tidier.

---

## The canonical relation name — one string, five places

For every served relation there is exactly ONE name, appearing in all five of:

1. the `data/datasets/<name>.yaml` **file stem**
2. its **`table.name`**
3. its **physical view** — `<view_schema>.<name>`
4. the concept's **`grounding.sources[].relation`** tail
5. any lookup's **`source_view`**

**This section owns WHERE the name appears. It does not own what the name SPELLS.** The spelling is
owned by **`check_served_name_distinct`**, which publishes the convention in its own failure
message, derived from *your* bundle. Run it, read the refusal, use the name it hands you. Do not
copy that convention into a skill, a bundle README or a decision record — a copy is a second home
and it does not move when the gate moves. Measured: every operator who read that gate converged on
names, including two who had no method document at all and still produced identical name sets from
the gate alone. The one operator who took a kit paraphrase instead of the gate diverged from all of
its peers. Reading the gate is not diligence here; it is the mechanism that actually transmits.

The one part worth knowing before you run it: **a served name may never equal a raw source name.**
Everything else — including what to do when the raw relation is *already* a clean business noun — is
in the refusal text, which is the case that gate was rewritten to answer.

> **A prose collision you will meet.** `check_relation_identity`'s *docstring* also describes a
> naming rule ("the raw table's base name, no `_clean`/`clean_`"). Its *code* checks only that the
> stem equals `table.name`. Two gates' prose disagreeing is a framework defect worth reporting, and
> until it is fixed the gate that actually judges a served name is `check_served_name_distinct` —
> so per *When the kit and a gate disagree*, record the collision rather than quietly picking a side.

**What is actually checked, and where.** `check_relation_identity` is offline and pure-structural,
so it verifies places 1, 2, 4 and 5. **Place 3 — that the physical view really exists — is not
checked by any gate**, deliberately: gates stay free of warehouse access so they run anywhere. It
is verified by the materialize step, live, at the moment the view is created.

Say "five places, four of them checked offline". Saying "four places" hides a real obligation;
saying "the gate checks five" claims a guarantee that does not exist.

---

## `confidence: C | I | Q` — what the letter asserts

A closed three-member vocabulary. It records **how the value was arrived at**, not how sure you
feel.

| letter | means | the test |
| --- | --- | --- |
| **C** | Confirmed | measured against live data, and you can cite the number |
| **I** | Inferred | derived from structure, naming or documentation — plausible, unmeasured |
| **Q** | Question | needs a human who knows the business; you cannot settle it from the data |

**`Q` is a first-class outcome, not a failure.** An open question written down is work routed to
the person who can answer it; the same question answered by guessing is a fabrication that will
pass every gate. The gates cannot tell a confident wrong answer from a right one — that asymmetry
is the whole reason the letter exists.

Machine-authored content is capped at `I`. Only a human may raise a field to `C`.

---

## Closed vocabularies — read them, never re-list them

`mac_vocabulary.yaml` in the framework holds the closed member lists: measure types, identity
kinds, edge levels, column roles, provenance and confidence values.

**Read the members from there at the time you need them.** Do not copy the list into a skill, a
prompt, a comment or a code branch. `check_vocabulary_drift` exists precisely because a copied
list is a second home for the fact, and the copy does not move when the vocabulary does.

The one place a member list legitimately appears is the vocabulary file itself.

---

## Identifier conventions for the registers

One prefix per register, so an id tells you which register it came from:

| register | id shape | example |
| --- | --- | --- |
| data-quality issues | `DQ-<AREA>-<nn>` | `DQ-ORDERS-03` |
| deliberate non-promotions | `NS-<AREA>-<nn>` | `NS-STAGING-01` |
| interventions (authored deviations) | per the ledger's own convention | — |

`<AREA>` is the subject area, not the source name — the kit never carries a source's identity.
**This is a rule about KIT identifiers.** It says nothing about what a bundle's served
relations are called; see *Source-agnostic KIT, source-specific BUNDLE* above, and do not
cite this row as grounds for stripping a source marker off a served relation name.

---

## Which skill owns which artifact

Two skills producing the same artifact is the same defect as two homes for one fact. Ownership:

| artifact | owned by |
| --- | --- |
| `data/profiles/<stem>.yaml` | P1 · source-profiling |
| grain declaration, `identity_evidence` | P2 · grain-and-identity |
| the promotion decision, the non-promotion register | P3–P5 · dataset-promotion |
| `data/transforms/<name>.yaml` **and** `.sql` | **P4 · transformation-authoring** |
| `data/datasets/<name>.yaml` | P3–P5 · dataset-promotion |
| `data/lookups/<x>.lookup.csv` | P6 · lookup-pre-resolution |
| `ontology/concepts/<Name>.yaml` | P7 · concept-authoring |
| measure classification | P8 · measure-semantics |
| `data/quality/<ID>.md` | P10 · data-quality-registration |

**dataset-promotion decides *whether and at what grain* a relation is served; transformation-authoring
writes the transform that serves it.** The promotion skill names the transform as a consequence of
its decision; it does not specify the transform's shape.
