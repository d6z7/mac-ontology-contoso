---
name: lookup-pre-resolution
description: Build the name-to-code registers that let an engine answer from declarations instead of probing the warehouse. Use as step P6.
---

# P6 · LOOKUPS — the name-to-code registers

A question arrives in words ("shipments to Germany", "orders in the Express category") and the data
holds codes (`DE`, `CAT-07`). Something has to turn one into the other. Do it at build time, once,
into a committed register, and the runtime resolves offline before it emits a single query. Skip
this step and the engine resolves at answer time by probing the warehouse — and a probe that finds
nothing is indistinguishable from a real thing with no data. That is why probing is *wrong* and not
merely slow: `WHERE country_name = 'Deutschland'` against a table storing `DE` returns zero rows,
and zero rows reads as "Germany has no shipments" rather than "I looked in the wrong place". The
same failure has a worse sibling: an engine that did not know a depot's real code assembled one as
`country_code || '_' || 'MAIN'`, asked the fact whether it existed, got nothing, and recorded the
depot as having no activity. Nothing errored. `check_no_fabricated_identifiers` exists because of
that class of silence, and this step is what removes the need to guess in the first place.

## When

After P5 (datasets declared, canonical names fixed, views materialized) and **before P7** — a
concept's `contract.no_probe_guarantee` cites registers, so the registers must exist first. You need:
the P1 profile (distinct values and cardinality per candidate column), the served relations actually
queryable, and the canonical relation names from P5.

## Do

1. **List the columns a question can name in words.** The test is: *could a user type the human name
   of this thing?* Category and status codes, entity codes with a display name, unit/measure codes,
   geography, anything whose stored spelling differs from how people say it. Skip free-text and
   high-cardinality identifiers no one names aloud (an invoice number needs no register).
2. **Decide what each register is for**, because the shape follows the job:
   *resolution* (name → code), *description* (code → attributes, one row per code),
   *membership* (group → members, **exploded**: one row per `(group, member)`), or
   *registry* (code → a governing fact, e.g. a measure's additivity — see P8).
3. **Cut it from the SERVED dataset, never the raw table, and never from memory.** One query,
   `SELECT … ORDER BY <key>`, and commit the result verbatim as a snapshot. Values recalled from a
   column description are how registers come to hold tokens the data has never contained.
4. **Write it as `data/lookups/<x>.lookup.csv`** — a header row plus at least one data row. First
   column is the code, **spelled exactly as the column is spelled on the dataset it joins to**; then
   the display name; then a normalized search key if you need one; then `confidence` (`C` confirmed /
   `I` inferred / `Q` needs-SME) and a free `note`.
5. **Name the origin in a `source_view` column** when the register is a snapshot of a relation, using
   the **canonical stem from P5** — not the physical view name, not schema-qualified raw.
6. **Keep the unresolved rows**, stamped `Q` with a note saying what is missing. Dropping a row you
   could not resolve reintroduces exactly the false absence this step exists to prevent.
7. **Put the provenance beside the register, never inside it.** The CSV is data and nothing else:
   line 1 is the header, every other line is a row. The query, the date, the row count and any known
   defect in the values go in the `.lookup.md` twin and in the `.lookup.build.py` that cut it; per-row
   provenance goes in the row, in the `source_view`, `confidence` and `note` columns.
   **Never open the register with leading `#` comment lines.** MEASURED on a two-row register carrying
   two real defects — a dangling `source_view`, and a level measure's row claiming it could be summed
   over time: with no comment lines `check_lookups` and `check_measure_additivity_registry` both exit 1
   and name both defects. Adding two `#` provenance lines above the header, changing nothing else,
   turns **both** gates green. Neither strips comments: `csv.DictReader` takes line 1 as the header, so
   the field names become the words of your comment, none of the columns the gates look for
   (`source_view`, `measure_type`, `additivity_time`, `additivity_categorical`) are among them, and each
   gate concludes there is nothing of its kind here to check. The non-empty rule does not save you — it
   counts non-blank lines, and a comment is a non-blank line, so a commented header-only file still
   reads as populated. A register that fails silently is worse than no register: it certifies the
   guarantee while resolving nothing.
8. **Declare the plane** in `mac.project.yaml`: `lookups: data/lookups` — a first-class manifest key
   ("the value registers a concept may delegate to"). A CSV on disk in an undeclared directory is a
   file; a declared plane is an artifact of the bundle.
9. **Cite it from the concept in P7, by literal path.** `contract.no_probe_guarantee` must contain the
   string `data/lookups/<x>.lookup.csv`. The gate scans that text with a regex — "resolved via the
   category register" cites nothing and is checked by nothing.
10. **Delegate closed enumerations instead of retyping them**: `values.realized_by: {udf:
    mac.canon.enum_from_register, params: {register: <stem>, key_column: code}}` and omit
    `values.items`. The membership twin is `mac.canon.grouping_from_register` on `members.realized_by`.
    Holding the domain in both places creates two copies that will disagree.
11. **Re-cut when the dataset changes.** A register is a dated snapshot, and a snapshot with no date
    is a claim with no expiry.

## Produces

- `data/lookups/<x>.lookup.csv` — the SSOT, one per register
- `data/lookups/<x>.lookup.build.py` (the exact cut) and/or `<x>.lookup.md` (the readable twin) —
  at least one of the two, because this is where the provenance lives (step 7), not in the CSV
- `lookups: data/lookups` in `mac.project.yaml`
- the citations themselves, later, in `ontology/concepts/*.yaml`

## Accepted by

- **`check_lookups`** (MAC008) — two rules. (A) Every `data/lookups/….csv` path appearing in any
  concept's `no_probe_guarantee` must exist **and be non-empty** (header + ≥1 data row): a guarantee
  citing an absent or placeholder register is a promise nothing keeps. (B) Every distinct `source_view`
  value in any lookup CSV must resolve to a real `data/datasets` relation — by file stem or by declared
  `table.name`. Both rules read the file with `csv.DictReader`, so line 1 must be the header —
  see step 7. Offline and purely structural; it never touches the warehouse.
- **`check_relation_identity`** (MAC008) — a lookup's `source_view` is one of the five places one
  relation name must be spelled identically. Naming the physical view where the canonical stem belongs
  reds here, not in `check_lookups`.
- **`check_enumeration_closure`** (MAC006) — a closed value set may delegate to a register instead of
  listing members, but the register must actually resolve under `data/lookups/`; a closed set pointing
  at a missing register promises an exhaustive domain and names nothing.
- **`check_answerability`** (MAC011) — for a `reference` or `enumeration` concept it **derives** the
  `resolve` step from the register paths in the concept file, falling back to inline `values.items`.
  Neither present ⇒ that step is underivable ⇒ error. It also renders the guarantee from the
  declarations, so a hand-written one cannot drift away from what the bundle actually holds.
- **`check_no_fabricated_identifiers`** (MAC008) — an identifier a register declares may not be built
  by concatenation and compared or joined against a declared key. Look it up.

## Getting it right first time

- **Values recalled rather than pulled.** Tell: the register holds a token that appears nowhere in the
  profile, and downstream guards keyed on it never fire.
- **Citing a register in prose.** Tell: the gate prints `0 cited lookup(s)` while your concepts clearly
  talk about resolution. It only sees literal paths.
- **A header-only CSV committed as a placeholder.** Tell: `cites '…' — file is empty`. The non-empty
  rule exists because an empty register makes a bundle look wired while resolving nothing.
- **A comment line above the header.** Tell: `check_lookups` prints `0 source_view value(s)` — or the
  additivity gate prints `no measure registry declares measure_type/additivity (nothing to project)` —
  on a register you know declares both, and then ticks. **A green carrying a zero count is the gate
  saying it parsed nothing, not that nothing is wrong.** Read the count before the tick; a register that
  really was read reports a positive number of rows.
- **Cutting the register from the raw table.** Tell: register row counts and the served view disagree,
  and codes the transform repaired reappear in their broken spelling.
- **A fact key with no register at all.** Tell: the rendered guarantee prints *"NO OFFLINE REGISTER —
  this concept cannot refuse an unknown name."* Refusing an unknown name is the point; without a
  register the engine can only return an empty result and let the reader draw the wrong conclusion.
- **Treating a normalized search key as identity.** A search key deliberately folds spellings together,
  and folding is lossy — distinct entities collapse into a sibling's key, a filter on it over-selects,
  and the answer looks clean while being wrong. Resolve to the code, then display the resolved name
  back so the reader can see what was swept in.
- **Double-homing a closed domain** in `values.items` *and* a register. Tell: they differ by one member
  and nobody knows which is current.

## What stays your judgment

- **Which dimensions deserve a register.** The gate checks the ones you cite; it cannot tell you about
  the one you never wrote. A column a user will name and you did not register stays invisible until
  someone gets a confident empty answer.
- **Whether a register is complete.** These gates are offline: nothing counts your rows against the
  warehouse. "797 rows" is checked to be non-empty, never checked to be all of them.
- **What the search key should fold and what it must keep apart** — the difference between a helpful
  synonym and a silent over-select is domain knowledge, not structure.
- **Whether an unresolved row is a data defect** (register it in P10) **or a genuine open question for
  an SME** (`confidence: Q`, and say who must answer).
- **Whether the labels are right.** A defensible mapping and a correct mapping look identical to every
  gate here. If you inferred a name rather than reading it from the source, mark it `I` and say so —
  that stamp is the only thing standing between an inference and a fact.
