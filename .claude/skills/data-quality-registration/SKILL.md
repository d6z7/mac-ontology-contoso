---
name: data-quality-registration
description: Register a data defect so it is visible, dispositioned and cross-linked to the transform that fixes it — or honestly marked as not fixed. Use as step P10.
---

# P10 · DQ — register the defects as first-class artifacts

Every real ingestion meets data that is wrong: durations that run backwards, a key that is not unique, a code the dimension declares but nothing ever uses. You will cope with each of these somewhere in the transform. This step forces the coping to be *named*: the defect becomes a registered finding with an id, the transform rule that dissolves it cites that id, and a resolution map links the two back together. Without it, the only record of the defect is a `WHERE` clause. Six months later nobody can say whether that clause is a fix, a workaround, or a bug — and when the upstream is repaired, the clause silently keeps deleting good rows. **Silent workarounds are the failure mode this step exists to prevent.** A defect you registered is a defect someone can rule on; a defect you quietly filtered is one you now own forever without knowing it.

## When

After **P1 · PROFILE** — a finding without a measured number is an opinion — and interleaved with **P4 · AUTHOR THE TRANSFORM**: you write the register entry at the moment you write the SQL line that copes. Must already exist: the profile numbers; `data/transforms/<stem>.yaml` descriptors (the resolution map names transform **file stems**, not relation names); and settled served names from P5. Must happen before **P11 · COMPILE**, and before **P13 · GOVERN**, where the intervention ledger's `dq_ids` are checked against this register.

## Do

1. **Sweep for registrables.** Walk the profile output and your draft transform SQL and apply two tests. (a) *If I do nothing, can a consumer of the served data be confidently wrong?* Nulls that mean "not applicable" read as gaps; a non-unique key fans out a join; a duplicate row doubles a total. (b) *Does any line of my transform exist only because the raw data is defective?* If yes, that line has a defect behind it, and the defect is registrable. Test (b) is the one the gate can partially see, so it is the one you can never argue your way out of.
2. **Do not register cosmetics.** A rename, a cast you would have done anyway, a column you chose not to expose — none of these are findings. Registering everything is as useless as registering nothing: a register of 200 entries is read by no one, and the four that matter are lost in it.
3. **Write the register entry** in `data/quality/data_quality_register.yaml` under `issues:`. Required by schema: `id`, `title`, `finding`. Carry the rest — they are the point: `severity` (high/medium/low), `confidence` (`C` = measured live, and then *cite the number*; `I` = inferred from shape; `Q` = needs an SME), `current_handling`, `residual_risk`, `sme_owner` naming **what that person must ratify**, not just who they are.
4. **Put the number in `finding`, and describe the raw plane.** "`delivered_at` is earlier than `shipped_at` in 129,682 of 4.1M shipment rows (3.2%)" is a finding. "The shipment view filters negative durations" is not a finding — it is the fix, wearing the finding's clothes. If you catch yourself describing your own view, you have registered the wrong thing.
5. **Choose an id and never change it.** Shape: `DQ-<AREA>-<nn>-<slug>` (e.g. `DQ-ORDERS-03-duplicate-order-key`). Once written it is cited by transform rules, the resolution map, possibly an acceptance property, and the P13 ledger. Renaming it later breaks four places at once, and only two of them are gated.
6. **For each transform rule that copes with a registered defect**, in `data/transforms/<stem>.yaml` under `transforms:`, give the rule `impurity_class:` (a short class name — free text), `resolves: [DQ-…]`, plus `raw_defect`, `rule`, `sql`, `establishes_guarantee`, `status`. `raw_defect` says what was wrong; `establishes_guarantee` says what a downstream concept may now *rely on* — that sentence is what lets the ontology stop defending against the impurity.
7. **Things you have not done yet go in `open_transforms:`**, not `transforms:`. Same shape but `proposed_rule` and `status: PROPOSED`. The gate treats these as intentions: it checks only that any id they cite is registered, and does not demand a resolution-map entry. This is the correct home for "we know, we have not fixed it, here is what we would do."
8. **Add the matching resolution** in `data/quality/impurity_resolution_map.yaml` under `resolutions:`: `finding_id`, `coverage` (exactly one of `resolved` · `partial` · `gap`), `resolving_transforms: [<transform stem>, …]`, and a `guarantee` sentence.
9. **Choose `coverage` honestly — this is the resolved/worked-around distinction.**
   - `resolved` — the served dataset no longer exhibits the defect, losslessly, and no downstream consumer needs to know it existed. Deduplicating rows that are identical in every measure is resolved. So is deriving a correct value that the raw omitted.
   - `partial` — **contained, not cured.** You excluded a slice, quarantined rows behind a flag, or applied a fix that awaits ratification; the defect is untouched upstream. A `partial` guarantee must state **the cost** ("1,204 clean shipment rows are withheld along with the 87 ambiguous ones") and **the revert condition** ("remove once the upstream key is fixed"). A containment with no stated cost is a workaround that has learned to spell.
   - `gap` — deliberately untreated. Documented only. The guarantee explains why nothing is done *and why leaving it is safe*.
   Dropping rows is almost never `resolved`. If you removed data to make a number look right, it is `partial`, and the count you removed belongs in the guarantee.
10. **A deliberate non-decision is a finding too.** "This relation was profiled and is deliberately not served, because its grain cannot be reconciled with the order key" → register it, `coverage: gap`, `resolving_transforms: []`. In a comment it is lost; in the register the next operator can see it was a decision rather than an oversight.
11. **Run the gate**: `python3 tools/check_dq_resolution_sync.py <bundle-root>` (offline, structural, exit 0/1). Then re-run `validate_schema.py`, and at P13 make sure every `dq_ids` entry in `interventions/ledger.yaml` names a registered id.
12. **Project the readable pages; never author them twice.** Per-issue markdown and an issues overview are useful for humans, but they are a *rendering* of the register. Generate them. A hand-maintained issue page beside a register is the two-homes-for-one-fact shape that this whole plane exists to forbid.

## Produces

- `data/quality/data_quality_register.yaml` — `issues[]`, the defects.
- `data/quality/impurity_resolution_map.yaml` — `resolutions[]`, the cross-link finding → transform(s) + coverage + guarantee.
- `resolves:` / `impurity_class:` on rules inside `data/transforms/<stem>.yaml`, and any `open_transforms[]` proposals.
- Optional, generated: `data/quality/<DQ-ID>.md` per issue and an issues overview index, projected from the register.

## Accepted by

- **`check_dq_resolution_sync`** — the three planes must tell one story. ERROR when: a resolution's `finding_id` is not in the register (a fix for a problem nobody recorded); a resolution names a `resolving_transforms` entry with no such transform descriptor; `coverage` is anything other than `resolved`/`partial`/`gap`; a transform rule `resolves` an unregistered id; **or a rule declares `resolves` but the map has no entry linking that finding back to that transform** — the link must be two-way, because a one-way link means one of the two documents is lying by omission. WARN (exit 0, so existing bundles can migrate): a rule that declares an `impurity_class` but no `resolves` — i.e. *"this SQL is cleaning something; go say what."* That warning is the only automatic prompt you will ever get, so read the warnings.
- **`validate_schema`** — routes these two files to `DataQualityRegisterFile` and `ImpurityResolutionMapFile`: `issues:` and `resolutions:` are required, each issue needs `id`/`title`/`finding`, each resolution needs `finding_id`, and `severity`/`confidence` are closed enums. It cannot tell you the prose is true.
- **`check_intervention_ledger`** — every `dq_ids[]` an intervention cites must exist in this register, so a manual change justified by "a data-quality problem" must name which one.
- **`check_conformance`** — bundle files nothing references are reported as orphan registers. A loose findings note dropped into `data/quality/` and linked from nothing is exactly that shape.

## Getting it right first time

- **Naming the relation instead of the transform stem.** `resolving_transforms` is matched against `data/transforms/*.yaml` file stems. *Tell*: `names resolving_transform 'X' — no such transform descriptor` while the file plainly exists under a slightly different name.
- **Declaring `resolves` and forgetting the map.** The single commonest error. *Tell*: `resolves 'DQ-…' but the resolution map has no entry linking 'DQ-…' back to '<stem>'`. Write both halves in the same edit, always.
- **A duplicate id — and no gate catches it.** The checker collects ids into a set, so two findings sharing one id both "exist" and every check passes; the projected page for one silently overwrites the other. This has happened in a live register. Grep your ids for duplicates yourself.
- **`impurity_class` drift.** It is free text, and in one real tree both `orphan_value` and `orphan_values` exist as separate classes. Before inventing a class, grep the ones already used in the bundle and reuse the exact string.
- **Calling a containment `resolved`.** *Tell*: the guarantee sentence contains an exclusion, a filter, a quarantine flag, or the phrase "so no consumer sees" — while the raw source is untouched. That is `partial`. If a future upstream fix would require you to delete code, it is a containment.
- **Registering the fix rather than the defect.** *Tell*: `finding` describes a served view. Rewrite it against the raw relation and the number you measured in P1.
- **`confidence: C` with no number.** C means measured live; if the finding has no count or percentage in it, you meant `I`.
- **Assuming green means covered.** With no register file at all, the gate loads empty dicts and prints `✓ OK`. An empty quality plane is indistinguishable from a clean one *to this gate*. Coverage is on you.
- **A guarding property that cannot fail.** If you add an acceptance property to prove a resolution holds, make it read the warehouse. `check_vacuous_assertions` exists because a test that counts a list it wrote itself passes forever while checking nothing.

## What stays your judgment

The gate enforces **consistency**, never **coverage**. It cannot tell you that a defect exists, that you missed one, or that the one you registered matters. Specifically, no gate decides:

- whether an anomaly is a defect at all, or the data correctly reporting an ugly reality;
- `severity` and `confidence` — both are assertions about the world;
- whether `resolved` or `partial` is the honest word, and whether the cost you stated is the whole cost;
- whether the `guarantee` sentence is **true** — nothing executes it, so it is prose that the ontology is then entitled to trust;
- whether a residual risk is small enough to serve at all, or whether the relation should be withheld;
- what the SME must actually ratify, and by when.

State these where they can be seen — in `residual_risk`, in `sme_owner`, in an open item — rather than deciding them by typing. A defect that is registered, unresolved and owned is a finished piece of work. A defect that was quietly filtered out is not, even when everything is green.
