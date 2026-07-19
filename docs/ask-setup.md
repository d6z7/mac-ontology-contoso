# Contoso · Ask — running the live LLM ask

> **Status: backlog draft.** Enough to clone and run; fuller docs (screenshots, deploy, bring-your-own-LLM) are a backlog item, not finished here.

`ask_server.py` is a live `/ask` over the Contoso ontology. It works like this:
the **LLM interprets** the question against the ontology and returns a routing decision + SQL; **this
server executes** that SQL against the local DuckDB warehouse and renders the answer. The meaning lives
in the ontology, not in code — the model reads `ontology/*.yaml` as its context on every question.

## What a cloner needs

1. **The Claude Code CLI** — `claude`, installed and signed in.
   - Check: `claude --version` (this project was built against 2.1.x).
   - The CLI carries the auth. **There is no `pip install anthropic` and no `ANTHROPIC_API_KEY`** — the
     server shells out to `claude`.
2. **Python 3.9+ with the `duckdb` module** — `python3 -c "import duckdb"` must succeed
   (`pip install duckdb` if not).
3. **The warehouse** — `contoso.duckdb` in the repo root (built by `setup.sh`).

## Run

```bash
python3 ask_server.py            # serves http://localhost:8000
python3 ask_server.py 8010       # or any port (use this if :8000 is taken)
```

Open the URL, ask a question (e.g. *"what was the best selling product?"*, *"which category is most
profitable?"*, *"top 5 brands by units in 2024"*). The left pane shows the report (value · assumptions ·
ontology walk · executed SQL); the right pane is the conversation.

## Cost & latency — know this before you demo

- Each question is **one `claude` call**: roughly **$0.03–0.10 and ~15–30 seconds**.
- Model is configurable: `CONTOSO_ASK_MODEL=claude-sonnet-5 python3 ask_server.py` for stronger SQL,
  or the default `claude-haiku-4-5` for speed/cost. (Opus with extended thinking is too slow — >120s —
  for interactive use.)

## Offline fallback (no LLM)

```bash
CONTOSO_ASK_NO_LLM=1 python3 ask_server.py 8010
```

Runs a **deterministic keyword parser** instead of the LLM: instant and free, but it only understands the
Contoso question space by pattern, not by language. Useful for CI or a machine without the `claude` CLI —
and honest about what it is (the UI labels the engine per answer: `claude` vs `offline rule parser`).

## How it works (one screen)

```
question ──▶ claude -p  (prompt = ontology/*.yaml + schema + rules)
                 │  returns STRICT JSON: {route, sql, assumptions, trace, ...}
                 ▼
        route COMMIT ─▶ server runs the SQL on contoso.duckdb ─▶ render value/table/chart
             ASK     ─▶ ask which currency (chips)
             REFUSE  ─▶ decline (dimension not in the model)
```

- The SQL runs on a **read-only** DuckDB connection. Still, for any non-local deployment, review the
  generated SQL path and add allow-listing — the model writes the query.
- The full raw ontology is the prompt; nothing about the meaning is hard-coded in `ask_server.py`.

## Open-source note

This live path **depends on the `claude` CLI**. A repo cloner without Claude Code can
still run the offline fallback. A pluggable "bring-your-own-LLM" interpreter (OpenAI-compatible, local
models) is a **backlog** item.
