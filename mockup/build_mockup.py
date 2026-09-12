#!/usr/bin/env python3
"""
build_mockup.py — assemble the ZERO-SETUP static /ask demo (mockup/index.html).

The mockup is NOT a re-implementation and NOT a hand-faked screen. It is the REAL
ask UI (ask_server.PAGE) with exactly one thing swapped: the `fetch('/ask')` call
becomes a lookup into a set of REAL runs captured here, ahead of time, straight
from the real offline pipeline (ask_server.answer_rules — the rule parser +
DuckDB execution, no LLM, no spend). So every value, SQL string, ontology walk and
assumption you see in the demo actually came out of the system.

Anyone can open the resulting index.html by double-clicking it — no Python, no
DuckDB, no `claude`, no server. To ask ANYTHING live (free text), they download the
repo and run `python3 ask_server.py` (see ../docs/ask-setup.md).

Regenerate:  python3 mockup/build_mockup.py       # from the repo root (needs the `duckdb` module + contoso.duckdb)
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # mockup/
REPO = HERE.parent                              # repo root (carries ask_server.py + contoso.duckdb)
REPO_URL = "https://github.com/d6z7/mac-ontology-contoso"

os.environ["CONTOSO_ASK_NO_LLM"] = "1"          # force the offline rule parser — no claude, no cost
sys.path.insert(0, str(REPO))
import ask_server as a                           # module load opens contoso.duckdb read-only

# The recorded question set — spans every route (COMMIT / ASK / REFUSE) and every
# render shape (scalar value, ranked top-1, table+chart). These are the same
# examples the article and the live UI's "Try:" chips use.
QUESTIONS = [
    "what was the best selling product?",               # COMMIT · rank(1)
    "sales by category in 2024",                        # COMMIT · table + chart (year filter)
    "top 5 brands by units",                            # COMMIT · table + chart (units measure)
    "which country sold the most?",                     # COMMIT · rank(1) (store join)
    "what were our total sales?",                       # COMMIT · scalar grand total (USD base)
    "what were our total sales in a single currency?",  # ASK  · reporting currency ambiguous
    "who is the best salesperson?",                     # REFUSE · dimension not in the model
    "what was our profit margin?",                      # REFUSE · derived measure — offline defers to the ontology
]


def normkey(s):
    """Loose match so typed variants ('Best selling product') hit the recorded run."""
    return re.sub(r"\s+", " ", str(s).strip().lower()).rstrip("?.! ")


def capture():
    runs = {}
    for q in QUESTIONS:
        runs[normkey(q)] = a.answer_rules(q)     # REAL offline pipeline → the exact JSON the browser renders
    return runs


def js_json(obj):
    """JSON safe to embed inside a <script> (neutralise any '</' and unicode line seps)."""
    return (json.dumps(obj, ensure_ascii=False)
            .replace("<", "\\u003c").replace(" ", "\\u2028").replace(" ", "\\u2029"))


def build():
    runs = capture()
    page = a.PAGE

    # 1) title + the top-bar provenance label (honest about what this is)
    page = page.replace("<title>Contoso · Ask — meaning as code</title>",
                        "<title>Contoso · Ask (demo) — meaning as code</title>")
    page = page.replace(
        '<span class="src">/ CONTOSO · claude interprets the ontology → DuckDB executes</span>',
        '<span class="src">/ CONTOSO · static replay of real recorded runs · '
        '<a href="%s" style="color:var(--accent);text-decoration:none">get the code →</a></span>' % REPO_URL)

    # 2) the ONE substantive swap: no backend — resolve from the embedded real runs
    fetch_block = (
        "  try{const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},"
        "body:JSON.stringify({q})});e.a=await r.json();}\n"
        "  catch(err){e.a={q:q,route:'REFUSE',kind:'refuse',head:'Server not reachable.',"
        "why:esc(String(err)),trace:[],assume:[]};}")
    replacement = (
        "  await new Promise(r=>setTimeout(r,240));   // brief pause so the replay reads as a live run\n"
        "  e.a=resolveCanned(q);")
    assert fetch_block in page, "ask_server.PAGE fetch block not found — did the server change? Update build_mockup.py."
    page = page.replace(fetch_block, replacement)

    # 3) the "live interpreter" foot line → honest static-demo line
    page = page.replace(
        '<div class="foot">Enter to send · Shift+Enter for a new line · live interpreter over the ontology, executed on contoso.duckdb</div>',
        '<div class="foot">Static demo · replays real recorded runs (offline parser · executed on contoso.duckdb) · '
        '<a href="%s" style="color:var(--faint)">download the code</a> to ask anything live</div>' % REPO_URL)

    # 4) inject the embedded runs + the resolver + a badge style for the demo notice,
    #    just before the page's own </script> so it can override ask()'s call site.
    inject = (
        "\n// ---- static demo: embedded REAL runs (captured by mockup/build_mockup.py) ----\n"
        "const __RUNS__=%s;\n"
        "const __QLIST__=%s;\n"
        "function _nk(s){return String(s).trim().toLowerCase().replace(/\\s+/g,' ').replace(/[?.! ]+$/,'');}\n"
        "function resolveCanned(q){const r=__RUNS__[_nk(q)];if(r)return r;\n"
        "  return {q:q,route:'DEMO',kind:'ask',prompt:'This is a static demo.',\n"
        "    hint:'It replays a fixed set of real, recorded runs — offline rule parser, executed on contoso.duckdb. "
        "To ask anything in free text, download the repo and run ask_server.py (see the README). Meanwhile, try one of these:',\n"
        "    chips:__QLIST__};}\n"
        % (js_json(runs), js_json(QUESTIONS)))
    page = page.replace("\nrender();\n</script>", inject + "\nrender();\n</script>")

    # small style so the DEMO notice badge reads cleanly (reuses the ask palette)
    page = page.replace("</style>",
        "  .badge.demo{background:var(--accent-soft);color:var(--accent)}"
        ".report.demo .rep-ask{color:var(--accent)}\n</style>")

    out = HERE / "index.html"
    out.write_text(page, encoding="utf-8")
    n_commit = sum(1 for r in runs.values() if r.get("route") == "COMMIT")
    n_ask = sum(1 for r in runs.values() if r.get("route") == "ASK")
    n_refuse = sum(1 for r in runs.values() if r.get("route") == "REFUSE")
    print("built %s — %d recorded runs (%d COMMIT · %d ASK · %d REFUSE), %d bytes"
          % (out.relative_to(REPO), len(runs), n_commit, n_ask, n_refuse, out.stat().st_size))


if __name__ == "__main__":
    build()
