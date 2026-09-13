---
name: source-profiling
description: Measure a data source before modeling it — row counts, distinct counts, null rates, value sets and anomalies — as a durable artifact. Use as step P1, before any concept exists.
---

# P1 · PROFILE — measure the source before you model it

Profiling is the act of writing down what the data **actually contains** — row counts, exact distinct counts, null counts, value ranges, value sets, and the things that look wrong — as a durable artifact, before a single concept exists. Skipped or done casually, every later step inherits an assumption instead of a fact: a grain is typed by hand from a column name that *looks* unique, a concept exposes a column that is 98 % null, an engine invents an identifier because nobody recorded which values the column can hold. Those defects are not caught at compile time; they are caught at answer time, by a user, as a wrong number. The profile is also not a throwaway — the data-sanity suite, the grain evidence and the generated tests are all *projected from it*, so a profile that was never persisted is a measurement you will pay for twice.

## When

Immediately after you can read the source, and **before P2 (grain), P3 (source descriptors as documents of record) and everything downstream**. What must already exist:

- A **skeleton descriptor** per relation at `data/sources/<stem>.yaml` (raw landings) or `data/datasets/<stem>.yaml` (served relations), carrying `table.schema`, `table.name` and `columns[]` with `name` and `type`. `mac_profile.py` refuses a descriptor without `table.name` and `columns[]`. Build the skeleton from the warehouse catalog, never from documentation — documentation is a claim about the schema, and the schema is itself only a claim about the data.
- A read path the bundle owns: `tools/run_properties.py` exposing a connection helper with `query(sql) -> (rows, meta)`, plus the `engine:` block in `acceptance/properties.yaml`. The framework owns the algorithm; your bundle owns the connection.
- Nothing under `ontology/`. If concepts already exist, you are not in P1.

`data/profiles/` is the default measurement plane and needs no manifest entry.

## Do

1. **Enumerate the relations in scope** — every relation you might serve, plus every dimension a question could name in words. Profiling a relation you later drop costs one scan; modeling one you never measured costs a wrong answer.
2. **Mark `role: audit` on load/write timestamp columns before you profile.** The source watermark — the fact that dates your evidence — is *derived* from a time-typed column carrying `role: audit`. Unmarked, you get `newest_write: null`, and the load stamp is treated as an ordinary category whose values get captured as if a user would ever filter by one.
3. **Run the census: `tools/mac_profile.py <root> <stem>`.** One scan over the relation produces, per column, exact `count(DISTINCT)`, exact nulls (`count(*) - count(col)`), and `min`/`max` where ordering means something (date/time/numeric — a min/max over free text is noise). `--dry-run` prints the SQL, which is the escape hatch if your engine is driven some other way: run it yourself and fold the numbers into the same file shape by hand.
4. **Exact counts, never sketches, never samples.** An approximate-distinct sketch was measured returning *more* distinct values than the relation had rows, and reporting one more distinct code than there were ids where the exact check found no violation at all. A sketch can *rank* candidate keys; it can never *decide* uniqueness — and uniqueness is the question the next step asks. Sampling fails for the same reason from the other side: taking a sample destroys duplicates, so uniqueness is not sample-testable.
5. **Capture value sets for bounded columns, in one further pass.** A column at or under 600 distinct values is bounded and its full domain is written to the *descriptor* as `values:`. Do it in a single query that aggregates every bounded column at once; one query per column once meant a dozen extra full scans of a table whose census alone cost ~10 GB.
6. **Bounded is not enumerable — this is a judgment, and the tool only approximates it.** A domain is worth keeping when someone would **filter by naming one of its members**. Delivery statuses: keep. Dates, load stamps and concatenated surrogate keys: bounded only by accident. On one real sweep those accidental domains were 56 % of all captured domain bytes and told the engine nothing it could act on. Drop an id column's domain when a label twin (`customer_id` beside `customer`) already carries the meaning.
7. **Read the numbers and write down the anomalies.** The ones that always matter: `distinct == rows` (candidate identifier); `distinct == 1` (a constant — it can never be part of a key); `distinct == 0` (the column is entirely null and is a fiction of the schema); nulls on a column the schema calls required; sentinel dates far outside the plausible range in `min`/`max`; and two columns whose null counts are nearly equal, which usually means one upstream gap and not two.
8. **Check declared type against measured reality.** The profiler decides `min`/`max` from the *declared* type. A ship date stored as a string is declared `string`, gets no `min`/`max`, and the earliest-value assertion the sanity suite would have generated silently never exists. **The tell:** a column whose name says date or amount but whose profile row has only `distinct` and `nulls`. Fix the declared type (or record the mismatch as a data-quality issue for P10) and re-measure.
9. **Re-run once against unchanged data.** The output must be byte-identical except `measured_at`. That idempotence is the exit test: once it holds, any future diff in the numbers means **the source moved**, which is the only reason to look at it.
10. **If a descriptor already carries measured blocks inline**, split them out: `tools/mac_profile_split.py <root> --apply` (add `--prune-domains` to drop domains from bounded-but-not-enumerable columns without paying for a rescan). Descriptor and profile have different lifecycles — the descriptor is read on every request and its mtime keys prompt caches, while `measured_at` moves on every measurement.
11. **Run `tools/check_profile_plane.py <root>` and stop.** Do not author a concept in this pass.

## Produces

- `data/profiles/<stem>.yaml` — one per profiled relation, machine-written:
  `of: <stem>` (must equal the file stem), `relation: <schema>.<name>`,
  `profile: {measured_at, rows, newest_write, method, engine, scanned_bytes}`,
  `columns: [{name, distinct, nulls, min?, max?}]`.
  P2 later adds an `identity_evidence:` block to this same file; a re-census must carry it forward, never clear it.
- Edits to the descriptor (`data/sources/…` or `data/datasets/…`): a `values:` domain on bounded **and** enumerable columns only. The domain lives with the meaning; everything counted lives in the profile.

## Accepted by

- **`check_profile_plane`** — the measurement must still describe the thing it measured, checked as a join between profile and descriptor in four mechanical ways. **ORPHAN**: a profile whose descriptor is gone — a measurement of nothing. **MISNAMED**: `of:` disagrees with the filename, so every join to it silently misses. **STALE COLUMN**: a census row for a column the descriptor no longer declares — counts for something that was dropped. **STALE DOMAIN**: a descriptor column carrying `values:` that the profile never measured — a domain nobody re-measures and everybody believes. The gate exists because a stale profile is *worse than no profile*: it still reads as evidence.
- **Volume is deliberately not gated.** A row count moving is the source doing its job. Asserting row counts would fire on every load and be switched off within a week, taking the real checks with it. Structure is what is watched: value-set membership, never-null staying never-null, the *earliest* date (the max moving forward is a load; the min moving forward means history was dropped silently).
- **Read later by**, so a sloppy profile gets expensive rather than caught here: `mac_generate_sanity.py` (projects the data-sanity properties from your census — nobody authors those), `mac_admit_identity.py` and `check_grain_declaration` (P2 reads `identity_evidence.key` out of this file), `mac_inherit_grain.py`, and the generated ontology tests.

## Getting it right first time

- **Modeling while measuring.** The commonest failure, and the reason this is its own step. You notice `order_id` and write "identity: order_id" without ever having measured `distinct == rows`. **The tell:** a sentence in your notes containing *should*, *presumably*, or *obviously*. Measurement produces numbers; if what you just wrote is not a number, it belongs in a later step.
- **Profiling before marking `role: audit`.** **The tell:** `newest_write: null` on a relation that clearly has a load column, plus a captured domain of a few hundred timestamps.
- **Believing the schema's declared types.** **The tell:** a `_date`/`_amount` column with no `min`/`max` (see step 8).
- **Only profiling the served relations.** Raw sources are descriptors too, and a first cut of the split tool that walked only the datasets directory halved a generated suite — 267 properties over 25 relations became 150 over 13 — because twelve profiled relations were raw sources. **The tell:** a suite whose property count fell after a change that was supposed to add coverage. Always print and read the counts.
- **Deleting a column from a descriptor and leaving its census row.** **The tell:** `check_profile_plane` says STALE COLUMN. Re-measure rather than hand-editing the profile; hand-edits break idempotence, and idempotence is the only thing that makes a future diff mean anything.
- **Hand-editing `measured_at` or numbers to make a diff quiet.** That converts the one gate you have into decoration.
- **Capturing every bounded domain because it is cheap.** It is not: those bytes are inlined into every request the engine makes. See step 6.

## What stays your judgment

- **Which relations to profile at all**, and how deep. No gate knows what you might later want to serve.
- **Whether a bounded column's value set is a category a question would name.** The 600-value threshold is a cost heuristic, not a semantic one; the enumerability rule (audit columns, ids with a label twin, continuous types) is a good default that will be wrong for some column of yours.
- **Whether a null means missing data or "not applicable".** A shipment with no delivery date because it has not shipped is not the same defect as one with no delivery date because the feed dropped it, and both look like `nulls: 41`.
- **Whether an anomaly is a data-quality issue (P10), a type declaration to fix, or normal.** The gates check that a number is *recorded and current*; nothing checks that it is *correct*.
- **Whether a column that discriminates is identity or delivery metadata** — that question is measured in P2, and even there the tool reduces it to a small set of closed questions and refuses to answer them itself.
- **When to re-measure.** Nothing forces it. The honest rule: re-measure before you rely on the profile for a new decision, and treat any diff other than `measured_at` as news about the source.
