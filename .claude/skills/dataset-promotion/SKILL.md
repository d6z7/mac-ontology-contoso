---
name: dataset-promotion
description: Decide whether and at what grain a relation is served, and register the ones deliberately NOT promoted. Use as steps P3 through P5.
---

# P3–P5 · Promotion — which raw relations become served datasets

Promotion is the decision that a measured raw relation will be *served*: given a transform, a dataset descriptor, a canonical name, and a declared grain — so that meaning can bind to it. Everything downstream inherits this decision, and it is the one step no gate can make for you. Skipped, it does not fail loudly: it produces a bundle that compiles while quietly serving forty near-duplicate views, or one view at a grain nobody can aggregate, or a landing table bound directly by a concept. The baseline test's three agents each invented a different answer here, which is why this skill exists: two operators must reach the same promotion set, the same names, and the same recorded reasons for what they left behind.

## When

After P1 (profile) and P2 (grain declaration), before P6 (lookups) and P7 (concepts). You must already have: a measured inventory of every raw relation (columns, row counts, distinct values, anomalies), a declared cell key for each fact relation, and this bundle's own `view_schema` declared in `connection.yaml` / `deployment.yaml`. You should also have the question scope — the kinds of questions this ingestion must answer. Promotion without that scope is guessing; you will serve everything, which is the same as serving nothing.

## Do

1. **Lay out the disposition table before writing any file.** One row per raw relation, and exactly one of four dispositions per row. It is the only artifact of this step that a reviewer can argue with, so make it explicitly:
   - `PASSTHROUGH` — already at the grain and vocabulary you would serve; nothing to dissolve.
   - `CLEANSE` — impurities to dissolve first (attribute/value shape, mixed-case vocabulary, integer-scaled amounts, parallel identifier columns).
   - `COMBINE` — several raw relations that are one business fact at one grain (`shipments_eu`, `shipments_us`, …) → **one** dataset with a discriminator column, not N near-identical views.
   - `NOT SERVED` — with a written reason (step 7).
2. **Do not promote the same fact twice.** Two served relations carrying the same measure at two grains under two names give one question two defensible answers, and the engine will pick by accident. If a measure genuinely needs its own view at its own grain, that is an exception to be written down, not a default.
3. **Decide the served grain deliberately — it is not inherited.** Default to the finest grain the questions need, and let the ontology aggregate. Collapse below the raw grain only when the raw grain carries something meaning must never see (republication vintage, bitemporal duplicates, superseded corrections), and then the collapse belongs in the transform as a named rule, never as a convention consumers are expected to remember. Write the chosen grain into `produces.grain` as a sentence: `"one row per order_id"`, `"one row per (shipment_id, checkpoint_code)"`.
4. **Name it — and route the naming question to the gate that owns it, not to this skill.** Choose the business noun first: the word the business actually says, `lower_snake_case`. That part is irreducibly yours — no gate can make it (see *What stays your judgment*). **The SHAPE that noun gets wrapped in is not yours, and it is not this skill's either.** Two gates own it, they are the authority, and this skill deliberately does not restate what they say — a naming rule stated in two places drifts, and the operator who follows the copy is the one who ends up naming things alone.

   - **`check_served_name_distinct` owns what the name SPELLS.** It publishes the convention *in its own failure message*, derived from this bundle: each refusal names the accepted shape **and** a conforming rename for the exact relation it refused. **Run it and take the name it gives you:**

     ```
     python3 <framework>/tools/check_served_name_distinct.py <bundle-root>
     ```

     **Run it EARLY — with your first dataset descriptor on disk, before you write the other forty.** That first refusal *is* how you learn this bundle's convention; it costs a minute and it settles the naming decision for the whole bundle. The awkward case — the raw relation is *already* a clean business noun, so there is no infix to strip — is answered there too. It is the case that gate was rewritten to answer, so read its answer instead of reasoning one out.

   - **`check_relation_identity` owns WHERE that one string appears** — the file stem must equal `table.name`, and that same string must then appear in the physical view `<own_schema>.<name>`, every concept's `grounding.sources[].relation` tail, and every lookup CSV's `source_view`. Rename the stem and `table.name` **together**; renaming one only moves the red.

   Then fix that shape for the whole bundle — every served relation takes the same one. A bundle with two naming shapes in it is worse than either shape applied consistently. Both gates are offline, take the bundle root, and run in seconds, so there is never a reason to guess now and check later.

5. **Write the three files, in this order, one relation at a time.** `data/sources/<raw_name>.yaml` (the observed landing, its columns as measured) → `data/transforms/<name>.yaml` + `data/transforms/<name>.sql` → `data/datasets/<name>.yaml`. Give the transform file the *dataset's* stem, not the raw's; the chain gate resolves `data/transforms/<stem>.yaml` first and everything after is easier to read.
6. **The 1:1 passthrough still gets all three files.** This is the commonest case for a ready-made warehouse and the one every example omits, so here it is in full:

   ```yaml
   # data/transforms/orders.yaml
   produces:
     relation: my_source.orders            # own view_schema, never another source's
     sql_file: data/transforms/orders.sql  # a real sibling file, even for a bare SELECT
     grain: "one row per order_id"
   inputs:
     - relation: raw_landing.orders_landing   # tail MUST equal the raw descriptor's table.name
       kind: raw_source
       descriptor: data/sources/orders_landing.yaml
       consumes:                              # ONLY columns that change name or shape
         order_placed_ts: rename-placed-at
   transforms:
     - id: rename-placed-at
       rule: "carry the raw timestamp under its business name"
       sql: "order_placed_ts AS placed_at"
       status: applied
   ```
   Columns whose name survives unchanged need no `consumes` entry — the lineage projector draws a `passthrough` edge for any raw column that reappears in the dataset descriptor under the same name. Columns you **rename** are exactly the ones that need a rule, because a renamed column has no name collision to be found by.
7. **Record every non-promotion as a first-class entry, in one place.** A relation you measured and chose not to serve is knowledge; in a comment or a chat message it is lost, and the next operator re-profiles it from scratch or promotes it by accident. Add one entry per non-promoted relation to `data/quality/data_quality_register.yaml`:

   ```yaml
   issues:
     - id: NS-ORDERS-STAGING
       title: "orders_staging measured, deliberately not served"
       confidence: C
       finding: >
         Measured 2026-05-04: 14.2M rows, no stable key (order_id repeats up to 9x with no
         version column). Superseded by orders_landing, which carries the same columns keyed.
       current_handling: "Not promoted. No transform, no dataset, no concept binds it."
       residual_risk: "If upstream retires orders_landing this becomes the only source and must be re-decided."
       sme_owner: "<the person who can rule on the duplicate key>"
   ```
   Say four things every time: the measured evidence, why not, what would reverse the decision, and who owns that ruling. If a decision record plane exists in the bundle, cross-reference it from there; do not restate the reason in two files — one fact, one home.

8. **Profile the served relation you just created**, under its new stem (`data/profiles/<served-name>.yaml`, `of: <served-name>`), and put the measured key in `identity_evidence.key`. The rename in step 4 does not carry the raw's profile forward.

## Produces

- `data/sources/<raw_name>.yaml` — one per raw landing you consume (P3)
- `data/transforms/<served_name>.yaml` + `data/transforms/<served_name>.sql` — one pair per served dataset, passthroughs included (P4)
- `data/datasets/<served_name>.yaml` — the schema-of-record the ontology will bind (P5)
- `data/profiles/<served_name>.yaml` — the measurement of the served relation
- entries in `data/quality/data_quality_register.yaml` — one per deliberate non-promotion

## Accepted by

- **`check_ontology_grounds_on_datasets`** — the chain `raw → transform → dataset → concept` must be whole in both directions. Errors: a concept grounding on a raw name; a grounding relation that is *both* a served and a raw name (ambiguous — nothing on disk proves the concept reads the curated one); a dataset no transform produces; a transform producing a relation no dataset declares. Warns on an orphan landing — a raw source consumed by no transform. **That warning list is your non-promotion audit**: every line on it should have a register entry from step 7. Nothing today pairs the two automatically — that pairing is a reviewer's job, and a KNOWN-GAP.
- **`check_served_name_distinct`** — a served `table.name` may not equal any raw source's stem or `table.name`. When they collide, the lineage's source node and dataset node merge and the transform renders as a self-loop: the picture says the view is built from itself. **It is also where the naming convention lives** — its refusal prints the accepted shape and a conforming rename for this bundle. Read the remedy there, not here (step 4).
- **`check_relation_identity`** — the file stem must equal `table.name`, and any grounding tail or lookup `source_view` naming a known physical view instead of the canonical stem is a divergence. Half-renaming is the classic break: `table.name: clean_orders` over a file still stemmed `orders`. **Known docstring/code divergence, worth raising upstream:** this gate's *prose* states a naming rule ("the raw table's base name, no `_clean`/`clean_`"), while its *code* (check A) only compares stem to `table.name`. Two gates' prose disagreeing about served names is a framework defect, not a choice for you to make privately: the gate that judges what a served name spells is `check_served_name_distinct`, this one judges only that the string is the same everywhere. Report the collision (00-SHARED, *When the kit and a gate disagree*).
- **`check_lineage_coverage`** — a served dataset whose columns descend from *nothing*, while its transform declares a lineage parent, is an error. Zero coverage means the `inputs[]` are mis-declared and the lineage silently collapsed: it still renders, it just says nothing. Below 100% is fine and expected (aggregates, literals, pivots).
- **`check_schema_isolation`** — `produces.relation` and the dataset's `table.schema` must carry *this* bundle's own view schema. It exists because one source's views were once created into another's schema and overwrote its dimensions.
- **`check_transform_sql_extracted`** — `sql_file:` must point at a real sibling `.sql`; a multi-line SQL body inline is refused, because inline SQL cannot be linted, diffed, or run.
- **`check_grain_declaration`** / **`check_profile_plane`** — the served relation's key must exist, name columns it actually has, and its profile must still describe it.

## Getting it right first time

- **The passthrough with renamed columns reads as 0% lineage.** You wrote the trivial transform, left `transforms: []` and no `consumes`, and every served column got a new business name. No name collides, so no edge is drawn. *Tell:* `check_lineage_coverage` prints `0%  ← ERROR (explains nothing)` for a view you know is a straight copy.
- **`inputs[].relation` tail spelled as the source's file stem.** The projector indexes raw descriptors by `table.name`. Get the tail wrong and it finds no columns — same 0% symptom, different cause. *Tell:* coverage 0% with `parents: 1`.
- **Setting `impurity_class` on a plain rename.** That word means "this dissolves a registered defect", and `check_dq_resolution_sync` will then warn that you declared no `resolves:`. A rename dissolves nothing. Leave it off; classification works from the `sql` alone.
- **Naming the served view after the raw table.** Both gates fire at once — the chain gate calls the binding ambiguous, the distinctness gate calls it a self-loop. *Tell:* your dataset stem is character-for-character a raw stem — which happens for the obvious reason (you kept the system prefix or the `_landing`/`_export` suffix) **and** for the easy-to-miss one (the raw relation was already a clean business noun, so "use the business noun" handed you back the raw name). The gate distinguishes the two cases and prescribes a different remedy for each; run it rather than guessing which you are in.
- **Renaming `table.name` and leaving the file stem (or the reverse).** *Tell:* one naming gate goes green the moment the other reds — distinctness passes and identity fails, or vice versa. Neither gate is wrong: whatever the name becomes, it has to become that in the stem *and* in `table.name`, together.
- **Serving one dataset per raw relation, reflexively.** Ninety landings do not mean ninety datasets. If two relations answer the same question at the same grain, they are one dataset with a discriminator; if a relation answers no question in scope, it is a step-7 entry.
- **Recording a non-promotion as silence.** The absence of a file is indistinguishable from an oversight. Six months later nobody can tell whether that landing was rejected or missed.
- **Serving at the raw grain when the raw grain contains republication vintage.** Every correction becomes its own row, sums double, and the defect surfaces as a number that is quietly too big. Collapse in the transform and say so in `produces.grain`.

## What stays your judgment

No gate decides **which** relations deserve to be served, or **at what grain** — the gates only check that whatever you promoted is wired consistently. No gate decides whether two raw relations are one business fact or two. No gate decides whether your served name is the word the business actually uses; it only checks that the same string appears in all five places, and it will happily certify a bundle where every name is wrong in the same way. And no gate can tell a deliberate non-promotion from a lazy one — an empty disposition table passes every check in this step. The honest output of P3–P5 is not a green run: it is a disposition table where every raw relation has a disposition, every non-promotion has a reason someone can dispute, and every open question about grain is written down under a named owner rather than settled by whoever was typing.
