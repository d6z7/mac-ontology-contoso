---
name: grain-and-identity
description: Declare what one row MEANS: the cell key that makes a row unique, with the evidence that it does. Use as step P2, after profiling and before promotion.
---

# P2 · GRAIN — declare what one row means

A fact relation is a pile of numbers until someone states the column tuple at which **exactly one row exists**. That tuple — the *cell key* — is what every later collapse partitions on, what every concept above the relation inherits its key from, and what decides whether a `SUM` counts each figure once or counts a restatement of it a second time. Skip this step and nothing errors: the bundle compiles, the answers come back, and they are quietly too large. The key is not a ruling and not a guess; it is **measured, and the measurement is kept with it**.

## When

After P1 · PROFILE (you need the column census — distinct counts, null rates, value domains) and before you author any concept, because a measure concept's key is *derived* from this and cannot be authored ahead of it. Do it once per fact relation. Dimension relations need it too whenever a measure concept grounds on them — `check_grain_declaration` requires a key for exactly those.

## Do

1. **Pick the measure column.** One column whose *value* is the figure the relation exists to carry (`quantity`, `amount`, `duration_days`). This is the one bit no tool supplies. Everything below is judged by whether omitting a column makes *this* value disagree, so a wrong choice here produces a confidently wrong key with full evidence attached.
2. **Pick a stratum.** If the source republishes — a weekly load, a monthly reporting cycle — confine the measurement to ONE round (`reporting_period = (SELECT max(reporting_period) FROM …)`). Measuring across rounds measures republication, not identity.
3. **Exclude the surrogates.** Hold out row ids, load batches, and any concatenated composite key. A surrogate that already encodes five axes wins every greedy search step by construction, and then every atomic axis it encodes measures as *dead*. Columns with one distinct value, or one distinct value per row, are not candidates at all.
4. **Grow a minimal key.** Add the column that most refines the group count; repeat until nothing refines it meaningfully. Then **shrink-confirm**: drop each key column in turn and check the group count actually moves. Growing alone leaves passengers in.
5. **Run the admission test — two probes, not one.**
   - *Discrimination* (leave-one-out): does removing this column split anything?
   - *Dependence* (functional): is this column determined by another column, and is that determination a **law** (structural — the dependent may leave the key) or a **convention** (true today; a key without it silently merges two things later)?
   No group count distinguishes those two, which is why both probes run. `tools/mac_admit_identity.py <root> <relation> --measure <col> [--stratum …] [--exclude …]` runs them in one pass.
6. **Classify by DISAGREEMENT, not by splitting.** For each candidate, omit it and ask how many collapsed groups now hold *two different values of the measure*.
   - **DEAD** — omitting changes nothing → excluded.
   - **IDENTITY** — omitting makes the measure disagree → included.
   - **COLLAPSIBLE** — omitting splits groups but the halves *agree* → **stop; this is a question for a human.** Same figure delivered twice.
   Uniqueness is the trap: adding a delivery column (`record_status`, `load_batch`) always makes the relation unique — and roughly doubles the figure count. At that point you have stopped identifying a *figure* and started identifying a *delivery of* a figure.
7. **Ask the residue as one closed question per column**, of an SME, and record the answer: *"Does a different `record_status` make it a DIFFERENT figure, or the SAME figure delivered again? [identity | delivery]"* Feed it back through the same tool (`--rule record_status=identity`) so the ruling and the evidence that prompted it live in one file. Do not rule columns the measurement already settled.
8. **Write it with its evidence**: the key, plus `measured_at`, the source's `source_watermark`, the `method`, the `measure`, the `stratum`, what was `excluded`, what was `ruled`, and the per-column group/split/disagree counts.
9. **Derive each concept's key — never declare one.** `concept key = measured grain − the column the concept pins to its own identity code, with any column substitutable by one that functionally determines it`. `tools/mac_inherit_grain.py` computes it; it only ever *adds* missing axes and reports declared columns the grain does not account for, because adding a missing axis is a mechanical repair while deleting a declared one is a modeling decision.
10. **Set `concept.identity.kind`** from the closed vocabulary (`mac.identity_kind`): `iso`, `code`, `namespace_code`, `fk_name`, `composite`, `resolved_axis`, `sme_pending`. Three of those are keyless-by-design on purpose — a fact grain is `composite`, an axis the served view pins is `resolved_axis`, and an identity nobody has ruled yet is `sme_pending`, carried as `__sme__` and never invented. The vocabulary exists so a concept can say *"I legitimately have no single-column key"* instead of being forced to fabricate one.
11. **Declare the identifiers that must be looked up**: `foreign_keys:` on the dataset descriptor, and lookup registers whose *first* column is the identifier. The fabricated-identifier gate reads exactly those two places — an identifier you never declared is one it cannot protect.

## Produces

- `data/profiles/<relation>.yaml#identity_evidence` — `key: [...]` plus `measured_at`, `source_watermark`, `method`, `measure`, `stratum`, `excluded`, `ruled`, `full_groups`, `columns[]` with each verdict.
- Column `role:` markings on the descriptor (`composite_key_part`, `delivery_axis`) and measured `profile.determined_by` lists.
- `ontology/concepts/<Name>.yaml#concept.identity.{kind, canonical_key}` (authored in P7, derived here).
- `data/datasets/<relation>.yaml#foreign_keys[]` naming the columns that are looked-up identifiers.

## Accepted by

- **`check_grain_declaration`** (MAC008) — the declaration must be *well-formed, complete and honest about its evidence*: a non-empty list of unique, non-blank names; every name a real column of the relation; no republication column inside a key that claims to exclude vintage; a key present for every relation a measure concept grounds on. Its fifth rule is the interesting one — a claim of "VERIFIED" with no date, or dated earlier than the descriptor's last edit, is flagged. It cannot prove the key is *right*; it proves the claim has not **outlived the thing it describes**.
- **`check_grain_key_consistency`** — every consumer that collapses the relation must partition on the declared key. It resolves positional `GROUP BY 1,2,3` ordinals, because that is exactly how the two real drifts were written. Severity is asymmetric on purpose: a consumer key that is a **subset** is an ERROR (it merges genuinely distinct rows, so every sum double-counts); a **superset** is a WARNING (over-partitioning can only fail to collapse, never double-count).
- **`check_no_fabricated_identifiers`** — an identifier that a register or foreign key declares may not be **built** by string concatenation and then compared or joined to a real column. Concatenation for labels, sort keys and messages is untouched; the gate fires on the *join*.
- **`check_relation_identity`** — one name for the relation across the dataset file stem, `table.name`, the concept's grounding tail, and any lookup's `source_view`. The grain is keyed on that name; if it diverges, the key silently stops being found and the two gates above go green by losing their subject.

## Getting it right first time

- **Searching for a minimal *unique* subset.** It succeeds and it is wrong. Tell: the last column you added multiplied the figure count by a small integer, and the column's name is about *when* or *how* the row arrived. That is a delivery axis, not identity.
- **Putting the reporting cycle inside the key.** Then every republication becomes its own group and the collapse collapses nothing. Tell: your "latest" partition returns as many rows as the raw relation.
- **Dropping a column because it splits nothing.** Discrimination alone justifies it and semantics forbid it. Run the dependence probe: if the column is determined only *by convention* (a naming scheme that happens to hold), it stays in the key — the day the convention breaks, a key without it merges two different things and nothing complains.
- **Retyping the key into a test or property SQL.** A retyped key is a key that is wrong eventually; this defect landed twice on one bundle, and the code comment left behind after the first did not prevent the second. Render it from the declaration; a comment is not a check.
- **Building an identifier from a pattern you inferred from three examples.** A concatenated code that does not exist returns zero rows, and *nothing finding nothing looks exactly like a clean result* — the property passes while testing nothing at all. Tell: an assertion whose expected answer is "0" or "does not exist". Resolve through the register instead.
- **Keying over raw column names after the transform renamed them.** The key is over the **served** relation's columns; a key naming columns that do not exist partitions nothing.
- **Writing "VERIFIED" in prose.** It is a sentence, not a test, and it goes stale the moment a new business status arrives. Record `measured_at` and the `source_watermark` instead — those age visibly.

## What stays your judgment

- **Which column is the measure.** No tool can choose it, and every classification below it inherits the choice.
- **The COLLAPSIBLE residue: identity or delivery.** Real cases have sat four significant figures apart on every statistic available, because the difference is not statistical — it is what the business *means* by the column. One closed question per column, answered once, by someone who owns the data.
- **Whether a pinned column leaves the concept's key.** If a concept identifies itself by a code and pins that column to a constant, is the column its identity or part of the figure's key inside it? That is a modeling ruling, not a measurement.
- **Whether a functional dependence is law or convention.** The probe measures that it holds *today*; only a human knows whether it is guaranteed to.
- **Whether the stratum is the right slice**, and whether the measurement is still true of the data now in front of you. The gates check the declaration is coherent and current-looking; only a warehouse sweep checks it is true.
