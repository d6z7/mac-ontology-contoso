# contoso5 — a MAC example bundle

A complete **meaning-as-code (MAC)** bundle over the SQLBI **Contoso Data Generator V2** dataset
(MIT licence), 100K edition: 93,470 orders over 223,974 sales lines, 2016-05-18 to 2025-12-31.

It is the worked example the MAC framework is developed and tested against: the declarations a
reader (a person, a planner or a language model) needs to turn a business question about this data
into correct SQL, and the evidence that those declarations hold against the rows.

Project id: `example/contoso5` · MAC stamp `0.3.0-develop` · ontology version 1.1

## What is in it

| path | what |
|---|---|
| `mac.project.yaml` | the container: planes, runtime, connection |
| `data/sources/` | the landing tables as delivered (SQLBI parquet) |
| `data/transforms/` | the SQL that builds the served views (`contoso_served.*`) |
| `data/datasets/`, `data/profiles/`, `data/quality/` | what each served column IS, measured |
| `ontology/relations/` | what a question may do with each column: meaning, names (`surfaces`), additivity (`offers`) |
| `ontology/concepts/` | 11 concepts (Order is the fact node; Customer, Store, Product, Country, …) with their rules |
| `ontology/edges.yaml` | 15 typed relationships, one per join |
| `governance/tombstones.yaml` | every retired declaration and its successor |
| `acceptance/` | questions, approved reference answers (SQL + expected value), oracles |
| `knowledge/`, `references/` | prose accounts and known data issues |
| `ontology/MODELLING-LOG.md` | why the model is shaped the way it is, entry by entry |

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

With the MAC framework checked out beside it:

```
python3 ../meaning-as-code/tools/mac_compile.py .
```

It must print `COMPILES — 0 error(s)`.

## Upstream semantics

The meaning of the source fields is published by SQLBI:
https://docs.sqlbi.com/contoso-data-generator/ — amounts are USD, the exchange rate is USD to
local, and about half the customers never ordered, by design.
