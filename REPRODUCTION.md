# contoso5 — a MAC example bundle, and how to reproduce it

A complete **meaning-as-code (MAC)** bundle over the SQLBI **Contoso Data Generator V2** dataset
(MIT licence), 100K edition: 93,470 orders over 223,974 sales lines, 2016-05-18 to 2025-12-31.

It is the worked example the MAC framework is developed and tested against: the declarations a
reader (a person, a planner or a language model) needs to turn a business question about this data
into correct SQL, and the evidence that those declarations hold against the rows.

Project id: `example/contoso5` · grammar v3 (MAC `0.4.1-develop`, GRAMMAR_v3.md v3.2)

## What is in it

The layout is fixed by the standard (GRAMMAR_v3 §1); every reference points toward the data.

| path | what |
|---|---|
| `mac.project.yaml`, `connection.yaml` | identity, connector, serving schema, the reference date (`as_of`) |
| `data/sources/` | the landing tables as delivered (SQLBI parquet), each with its `.md` account |
| `data/transforms/` | the SQL that builds the served views (`contoso_served.*`), each with its `.yaml` |
| `data/datasets/` | one file per served dataset: columns, kinds, keys, measure facts, checks |
| `data/lookups/` | value sets kept as CSV |
| `data/lexicon/` | every word, one row per (word, address), one CSV per dataset |
| `data/quality/` | the findings about each dataset |
| `data/profiles/`, `data/lineage/` | tool outputs: measured types, counts, references, column lineage |
| `ontology/concepts/` | 11 concepts, each on ONE dataset, with its `.md` account |
| `ontology/edges.yaml` | how two concepts join |
| `ontology/rules/` | one decision per file: what it says, who said it, its state, its behaviour |
| `acceptance/` | questions, approved reference answers (SQL + expected value), oracles, and the acceptance tools (`acceptance/tools/`, incl. `trace_extract.py`) |
| `evidence/` | the bundle's records: `MODELLING-LOG.md` (why the model is shaped as it is), measurements, and what the bundle still needs (`evidence/TODO.md`) |
| `pages/` | generated pages and projections (never authored) |
| `REPRODUCTION.md`, `reproduction.yaml` | this account, and the stages that rebuild the warehouse |

## Build the warehouse

The DuckDB warehouse is not committed; it is rebuilt from the public release by the stages in
`reproduction.yaml` (they were `./build.sh` until the v3 migration — the v3 layout has no root home for a
script). Each stage's `command` runs from the bundle root and needs `duckdb` on PATH:

```
run() { python3 -c 'import sys,yaml; print({s["id"]: s for s in yaml.safe_load(open("reproduction.yaml"))["stages"]}[sys.argv[1]]["command"])' "$1" | bash; }
run fetch        # the 100K parquet release -> data/*.parquet (gitignored)
run warehouse    # landings -> main.*, contoso_served created EMPTY
run served       # every data/transforms/*.sql -> contoso_served.* (re-runnable on its own: a changed transform)
```

### Why the warehouse is built this way (carried from build.sh)

- **This bundle's own warehouse; it shares nothing with any other bundle.** contoso5 holds the data
  constant against contoso4 and varies something else: it is ingested as TWO SEPARATE DELIVERIES, the
  landing plane first and on its own, under the checklist and the enforcement the operator ruled on
  2026-09-28 ("split data plane delivery in two parts ... have checklist for each one of them ... have
  linter and enforcement for every syntax thing we implement"). It exists because the first split run
  found four coupled defects, each hiding the next, all invisible on a bundle that had been incrementally
  re-run: a stage resuming on its sibling's output, a value domain stripped and preserved nowhere, a
  producer deleting the banner that tells a reader not to hand-edit, and a measured foreign key that never
  reached a declaration. Only a bundle ingested ONCE, from nothing, can show that.
- **The served schema is created empty and stays empty until a datasets delivery is asked for.** A
  bundle carrying only a landing plane is a legitimate delivered state. Pointing the serving schema at
  `main` instead would make the landings masquerade as served datasets.
- **The 100K edition, and it said `1m` until 2026-10-09.** The release's size label counts ORDERS
  (upstream: "10K: about 10,000 orders"), and `main.orders` holds 93,470 of them. `parquet-1m.7z` would
  produce roughly ten times the data and silently invalidate every profile, acceptance answer and row
  count measured here. Three independent checks agree on 100K: the live order count, the asset sizes
  (9 MB vs 62 MB compressed) and the 17 MB extracted size. The parquet files are gitignored, so the
  `fetch` stage's URL IS the provenance.
- **Transforms apply in passes, not alphabetically.** A view binds when it is created, and a value set
  cut from a served view (contoso5_brand <- dim_product) sorts before the view it reads. Each pass applies
  what it can; a pass that applies nothing while some remain is a real failure and stops the build.
- **No framework path appears in the stages**, so the bundle carries no dependency on where the
  framework is checked out.

## Check it

With the MAC framework checked out beside it, `tools/mac_compile.py .` builds this layout: the
v3 validator checks every file against the grammar, law L0 builds the bundle, and the L15 verdict
says what it can answer. It exits 1 on any error; `--write` persists `pages/compile.json`.

## Upstream semantics

The meaning of the source fields is published by SQLBI:
https://docs.sqlbi.com/contoso-data-generator/ — amounts are USD, the exchange rate is USD to
local, and about half the customers never ordered, by design.
