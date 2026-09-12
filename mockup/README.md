# Contoso · Ask — static demo (`mockup/`)

A **zero-setup** replay of the Contoso `/ask` experience. Open [`index.html`](index.html)
by double-clicking it — no Python, no DuckDB, no `claude`, no server, no API key.

## What it is (and isn't)

It is the **real** ask UI (`../ask_server.py`'s page) with exactly one thing changed:
the `POST /ask` network call is swapped for a lookup into a set of **real runs recorded
ahead of time**. Every value, generated SQL string, ontology walk and disclosed
assumption you see came straight out of the actual pipeline — the offline rule parser
executing against `contoso.duckdb`. It is a *recording of the real thing*, not a mock-up
that fakes answers.

Typing a question outside the recorded set shows a "static demo" notice instead of
inventing an answer — the honest boundary of a canned demo.

The recorded set spans every route the system can take:

| Question | Route |
|---|---|
| what was the best selling product? | COMMIT · ranked top-1 |
| sales by category in 2024 | COMMIT · table + chart |
| top 5 brands by units | COMMIT · table + chart |
| which country sold the most? | COMMIT · ranked top-1 |
| what were our total sales? | COMMIT · scalar grand total |
| what were our total sales in a single currency? | ASK · reporting currency ambiguous |
| who is the best salesperson? | REFUSE · dimension not in the model |
| what was our profit margin? | REFUSE · derived measure |

## To ask *anything* live

Download the repo and run the real interpreter — it turns free-text questions into
SQL against the ontology and executes them live:

```bash
python3 ask_server.py        # http://localhost:8000
```

See [`../docs/ask-setup.md`](../docs/ask-setup.md) for the full guide (the LLM path
uses the `claude` CLI; an offline rule-parser fallback needs no key).

## Regenerate this demo

Re-capture the runs and rebuild `index.html` (needs the `duckdb` module + a built
`../contoso.duckdb`):

```bash
python3 mockup/build_mockup.py
```

`build_mockup.py` imports the real `ask_server`, records `answer_rules(...)` for each
question above (offline parser — no LLM, no cost), and injects those runs into a copy
of the real page. Because it reuses the live UI verbatim, the demo can never visually
drift from the real thing.
