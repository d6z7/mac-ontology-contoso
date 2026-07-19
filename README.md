# mac-ontology-contoso

Public, neutral **demo warehouse** for the ontology / semantic-layer article series.
Everything here is safe to screenshot and publish — no internal data, MIT-licensed source.

## Why this exists

The meaning-as-code approach is easiest to show on a warehouse with a genuinely
*contested* metric. This is a neutral, openly-licensed dataset chosen for exactly that
shape: **multi-brand × multi-market × product hierarchy × a contested "total" metric** —
so the demo is safe to publish while still exercising the hard cases.

## Engine

**DuckDB** — embedded, no server, reads Parquet directly, and its SQL dialect is close
to other analytical/columnar SQL engines, so the ontology's generated SQL ports over to
another warehouse with minimal change.

## Data

**SQLBI Contoso Data Generator V2** — MIT licensed.

- Source: <https://github.com/sql-bi/Contoso-Data-Generator-V2-Data> (release `ready-to-use-data`)
- License: **MIT** (© 2024 SQLBI) — free to publish screenshots and redistribute derived snapshots.
- Note: the classic Microsoft Contoso Azure blob is **dead** (anonymous access disabled), so we use SQLBI V2.

V2 is **not** the classic `FactSales`/`FactOnlineSales` star. Its tables are:

    customers · stores · dates · currencyexchanges · sales · orders · orderrows · products
    (+ product category / subcategory)

`sales` is the denormalized form of `orders` × `orderrows` (header/detail). Multi-brand
lives on `products` (Brand column); geography (country → continent) lives on `stores`/`customers`.
Run `setup.sh` then `DESCRIBE <table>` in DuckDB to see exact columns.

## Setup

    brew install duckdb            # engine (macOS 'bsdtar' extracts the .7z — no p7zip needed)
    bash setup.sh 1m               # scale: 100k | 1m | 10m   (default 1m)
    duckdb contoso.duckdb          # open a SQL shell
    duckdb contoso.duckdb < queries/contested_total.sql   # the demo

## The demo: one question, several defensible answers

**"What were our total sales?"** is deliberately under-specified here — exactly the
contested metric the ontology is built to resolve:

- **header/detail double-count** — sum `sales` *and* `orders`×`orderrows` → 2× revenue.
- **currency** — amounts are store-local; without picking a currency (via `currencyexchanges`)
  a global sum is meaningless — never sum a raw cross-currency total.
- **gross vs net** — with or without discount.
- **by brand** — `products.Brand` (multi-brand).
- **by region** — store / customer geography rolls up country → continent.

The ontology fixes one definition, **discloses the assumption**, and drills to the
physical binding — the "prove it isn't guessing" moment that converts skeptics.

## Ontology

A meaning-as-code semantic layer sits on top of the warehouse and resolves the contested question
above into one disclosed answer. It lives in `ontology/` and binds to the tables via `data/datasets/`.

    ./validate.sh                                              # 3 framework gates (structural/referential/constraint)
    python3 ../meaning-as-code/tools/mac_to_explorer.py .      # (re)build the explorer
    open projections/contoso.explorer.html                     # browse concepts, rules, graph, data, manual

Six concepts (Sales · Product · Brand · Currency · Store · Order) and the contested-total rules, which
sort into decision lanes: **COMMIT** (net, convert-then-sum), **ASK** (which currency?), **REFUSE**
(no cross-currency sum; no header/detail double-count; 'Online' is not a market).

## Layout

- `setup.sh` — one-command local warehouse build
- `validate.sh` — run the three MAC framework gates
- `ontology/` — concepts, edges, derived-measure rules
- `data/datasets/` — the seam: physical table descriptors the ontology binds to
- `data/` (rest) — downloaded + extracted data (gitignored)
- `contoso.duckdb` — the built warehouse (gitignored)
- `projections/contoso.explorer.html` — the rendered explorer (the shareable artifact)
- `docs/manual.md` — the `ask(1)` man page (Manual tab)
- `queries/contested_total.sql` — the demo, in raw SQL
