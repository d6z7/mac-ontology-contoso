---
name: transformation-authoring
description: Author the transform YAML and SQL that turn a hostile raw relation into a served dataset, with defect to rule to guarantee recorded. Use as step P4.
---

# P4 · TRANSFORM — raw to served, declared in its own schema

A transform is the seam where raw data stops being someone else's shape and becomes a relation your
ontology is willing to mean something about. It is TWO artifacts that must agree: an executable `.sql`
that builds the served view, and a `.yaml` descriptor that says — in prose a human can argue with —
which defect each part of that SQL dissolves and which upstream column each served column descends
from. Without the descriptor you still get a working view, but nobody can tell a schema change from a
mistake, nobody can see which cleanup is load-bearing, and the lineage the whole estate renders from
says nothing. Without the split, the SQL is trapped in a YAML string where it cannot be read, linted,
diffed or executed.

## When

After P3 (every raw input has a `data/sources/<name>.yaml` descriptor recording its measured columns)
and after P2 (you know the grain of the relation you are about to produce). Before P5, which names the
served dataset, and before P7, which binds meaning to it. You need one more thing in place: your
bundle must declare its own `view_schema` in `connection.yaml` (or one of the deployment variants) —
without it the isolation gate cannot judge anything and silently skips.

## Do

1. **Decide the served relation and write its name once.** `<own_schema>.<served_name>`, e.g.
   `sales_ops.v_orders_current`. That exact string becomes `produces.relation`, the `CREATE OR REPLACE
   VIEW` target in the SQL, and the file stem of both files. P5 will hold you to it across five places.
2. **Write `data/transforms/<served_name>.sql`.** Full executable statement, one served relation per
   file. Open it with a comment block naming the raw inputs and what the view bakes out — that header
   is the first thing a stranger reads when the view surprises them.
3. **Write the sibling `data/transforms/<served_name>.yaml`** with `metadata` (pipeline, source,
   `layer: data-transformation`, owner), and `produces: {relation, sql_file: data/transforms/<served_name>.sql,
   grain: "one row per (…)"}`. The `sql_file` pointer is what proves extraction happened; the descriptor
   may still quote short illustrative fragments beside it, and that is documentation, not the body.
4. **Declare every input, with the right `kind`.** `raw_source` for a landing table; `dataset` for an
   upstream *served* view (a view-of-view is normal and its parent is still a lineage parent);
   `authored_seed` / `external` for a hand-authored register or an out-of-plane input. Give each a
   `role` (a short phrase saying what the branch is for: `order_branch`, `customer_identity`,
   `region_map`) and a `descriptor:` pointing at the YAML that records that input's columns.
5. **Write the `consumes` map on each lineage parent**: `<upstream_column>: <rule_id>` — or a list of
   rule ids where several rules read the same column. This map is the lineage. Every column name in it
   must be a column the upstream descriptor actually declares, or it resolves to nothing.
6. **Write one entry in `transforms[]` per rule id**, each carrying: `id`, `impurity_class` (the shape
   of the defect: `eav_shape`, `identifier_sprawl`, `label_vs_identity`, `master_coverage_gap` — pick a
   term and reuse it across the bundle), `raw_defect` (what is measurably wrong upstream, with numbers
   from P1), `rule` (the fix in prose), `sql` (a SHORT fragment quoting the relevant clause, including
   its output alias), `establishes_guarantee` (what a consumer may now rely on), and `status`
   (`applied` = live in the deployed view; `authored` = written but not yet deployed — do not blur them).
7. **Make each rule's `sql` fragment name its output alias.** The projector resolves a served column by
   finding `… AS <alias>` inside the fragment that mentions the consumed column. A fragment with no
   alias falls back to assuming the name is unchanged, and if it changed, that served column ends up
   explained by nothing.
8. **Register the defects you dissolve.** A rule with an `impurity_class` should carry `resolves: [DQ-…]`
   naming the issue in the quality register (P10), and the resolution map should point back.
9. **Declare the ones you did NOT fix as `open_transforms[]`** — same shape, `proposed_rule` instead of
   `rule`, no SQL. A known defect you left alone is knowledge; a known defect you left silent is a trap.
10. **Run the gates** (each takes the bundle root): `check_transform_sql_extracted.py`,
    `check_schema_isolation.py`, `check_lineage_coverage.py`. Read the coverage table it prints, not
    just the exit code.

## Produces

    data/transforms/<served_name>.sql     — the executable CREATE OR REPLACE VIEW, one per served relation
    data/transforms/<served_name>.yaml    — the descriptor: produces / inputs[].consumes / transforms[] rules
    (optional) data/transforms/<served_name>.md — narrative for readers, never the source of truth

## Accepted by

- **`check_transform_sql_extracted.py`** — a descriptor may not carry the body. It goes red if a
  descriptor has a substantial inline `sql:` scalar (multi-line, or over 120 characters) and no
  `sql_file:` pointer, and red again if a pointer names a `.sql` that is not there. The second half
  matters more than it looks: renaming the `.sql` and forgetting the pointer leaves a descriptor that
  documents a transform nobody can run.
- **`check_schema_isolation.py`** — every schema-qualified relation this bundle binds to (concept
  groundings and `data/datasets/*.yaml` `table.schema`) must carry this bundle's *own* `view_schema`.
  Bare, unqualified names carry no collision risk and pass. The rule exists because one source's views
  were once created inside another source's schema and overwrote that source's dimension tables — a
  silent, total data loss that no compiler error announced.
- **`check_lineage_coverage.py`** — every served dataset must *explain something*: at least one output
  column must descend from a real upstream column via your `consumes` map. Zero coverage on a view that
  declares a lineage parent is a hard error, because that is exactly what a mis-declared `inputs[]`
  looks like: wrong `kind`, wrong `descriptor`, a `consumes` naming columns the upstream does not have,
  or no `consumes` at all. All those collapse to "every column is derived/const", and a naive count of
  explained columns would read 100% while the lineage said nothing. Thin coverage (under 50%) warns.
  A column that is neither edge-covered nor a declared derivation is an error — an unaccounted output.
  Coverage below 100% is legitimate and deliberately not failed: aggregates, pivots and per-branch
  literals genuinely descend from no single column.
- **`check_vacuous_assertions.py`** (P4-adjacent, bites here) — it statically parses acceptance SQL and
  flags any asserted value that traces back only to rows the SQL typed itself. This is the honesty test
  for a transform that embeds a curated mapping as a `VALUES` CTE: the CTE is fine as *data* transcribed
  from a governed register, but the moment your evidence for the mapping is a query over the same typed
  block, you have counted your own list. That is not hypothetical — one such test counted 38 rows it had
  just written, passed forever, and hid a spelling divergence between the register and the model.
- Downstream, `check_relation_identity` and `check_ontology_grounds_on_datasets` will hold
  `produces.relation` to the dataset name and to the concept's grounding, so get the string right now.

## Getting it right first time

- **Pasting SQL into the YAML because it is "only a few lines".** Tell: a `sql:` value with a newline in
  it and no `sql_file:` sibling. Short quoted fragments beside a real pointer are fine and encouraged.
- **Calling an upstream served view `raw_source`, or an upstream register `dataset`.** Tell: the
  coverage table prints `parents` > 0 and coverage 0%. Also note the deliberate asymmetry — for a raw
  parent, an unconsumed column that survives by name is inferred as a passthrough edge; for a dataset
  parent it is not, because two governed views sharing a column name is not evidence of descent. So a
  view-of-view must declare its `consumes` explicitly or it will explain nothing.
- **`consumes` written against the SQL instead of against the descriptor.** Tell: the gate reports the
  column as unclassifiable or the coverage is mysteriously short. The map's keys must be upstream
  columns as *recorded in P3*, and if P3 is out of date, fix P3 rather than typing what you wish.
- **A rule fragment without its alias.** Tell: a served column shows up in the `unaccounted` list
  although you clearly wrote the transform for it.
- **One giant view over incompatible physical shapes.** When branches genuinely differ in skeleton,
  several thin conformance views beat one heroic union — and the union kind is only assigned when
  sibling raw branches share the same `consumes` shape anyway.
- **Marking `status: applied` for SQL that was authored but never deployed.** Tell: nobody can reproduce
  your guarantee against the live warehouse. Use `authored` and say so in the change log.
- **Skipping the transform entirely because it is a 1:1 passthrough.** Declare it. A rename-only
  transform is still the seam that makes the next upstream schema change visible instead of fatal.

## What stays your judgment

No gate decides **which impurities are worth dissolving** and which should be left visible as
open_transforms — cleaning too much hides upstream rot from the people who could fix it. No gate decides
whether the values in a curated backfill are **correct**; it can only check that they are declared,
attributed and not self-certifying. No gate decides **where one transform ends and the next begins**, or
whether your `grain` sentence is true — it will happily accept an honest-looking grain that duplicates
rows. And no gate can tell you whether the guarantee you wrote is the one a consumer actually needs;
that sentence is a promise to a stranger, and it is the part of this step a machine cannot write for you.
