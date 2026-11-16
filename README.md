# contoso5 — a MAC example bundle

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
| `acceptance/` | questions, approved reference answers (SQL + expected value), oracles |
| `evidence/` | the bundle's records: `MODELLING-LOG.md` (why the model is shaped as it is), `tombstones.yaml` (the 0.4.0 retirements), measurements, and the v3 migration's record (`evidence/v3-migration/`) |
| `pages/` | generated pages and projections (never authored) |

## Build the warehouse

The DuckDB warehouse is not committed; it is rebuilt from the public release:

```
cd data
curl -fL -o parquet-100k.7z \
  https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/download/ready-to-use-data/parquet-100k.7z
bsdtar -xf parquet-100k.7z          # or: 7z x parquet-100k.7z
cd .. && ./build.sh                 # needs duckdb on PATH
```

## Check it

With the MAC framework checked out beside it, the v3 tools read this layout:
`tools/mac_compile_v3.py` compiles it for the 0.4.0 engines and the v3 validator checks every
file against the grammar.

## Upstream semantics

The meaning of the source fields is published by SQLBI:
https://docs.sqlbi.com/contoso-data-generator/ — amounts are USD, the exchange rate is USD to
local, and about half the customers never ordered, by design.
