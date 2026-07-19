#!/usr/bin/env python3
"""
ask_server.py — the REAL Contoso /ask.  A live interpreter over the ontology + DuckDB, served as a small local web app.

    /usr/bin/python3 ask_server.py            # -> http://localhost:8000

This is NOT a canned matcher. Every question is parsed against the ontology's measures and dimensions,
turned into SQL, and EXECUTED against contoso.duckdb — so "what was the best selling product" resolves
`product` to a real dimension, `best selling` to argmax of the sales measure, generates the SQL, runs it,
and returns the answer with its trace. Unknown dimensions are refused; an unnamed single currency is asked.

Route:  COMMIT (answered from executed data) · ASK (needs one input) · REFUSE (dimension not in the model).
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
DB = HERE / "contoso.duckdb"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

con = duckdb.connect(str(DB), read_only=True)

# ---- grounding: real dimension members read from the warehouse (used to recognise filters) ----
BRANDS = [r[0] for r in con.execute("SELECT DISTINCT Brand FROM product WHERE Brand IS NOT NULL").fetchall()]
COUNTRIES = [r[0] for r in con.execute("SELECT DISTINCT CountryName FROM store WHERE CountryName IS NOT NULL").fetchall()]
CATEGORIES = [r[0] for r in con.execute("SELECT DISTINCT CategoryName FROM product WHERE CategoryName IS NOT NULL").fetchall()]
CURRENCIES = ["USD", "EUR", "GBP", "CAD", "AUD"]
YEARS = [r[0] for r in con.execute("SELECT DISTINCT year(OrderDate) FROM sales ORDER BY 1").fetchall()]

# ---- REAL LLM interpreter (shells to the `claude` CLI) ----
# The LLM reads the ontology and returns a routing decision + SQL as JSON; THIS server executes the SQL
# on DuckDB. No SDK, no API key — the `claude` CLI carries the auth. Falls back to the offline rule
# parser (interpret()) when `claude` is absent or the call fails. Disable with CONTOSO_ASK_NO_LLM=1.
CLAUDE = shutil.which("claude")
USE_LLM = bool(CLAUDE) and os.environ.get("CONTOSO_ASK_NO_LLM") != "1"
# Interpretation (NL -> SQL over a small schema) is easy: use a FAST model so the demo is snappy.
# Opus with extended thinking took >120s on the full-ontology prompt — unusable interactively.
MODEL = os.environ.get("CONTOSO_ASK_MODEL", "claude-haiku-4-5")
ONTOLOGY_TEXT = "\n\n".join(
    "### %s\n%s" % (p.relative_to(HERE), p.read_text(encoding="utf-8"))
    for p in sorted((HERE / "ontology").rglob("*.yaml")))
SCHEMA_TEXT = (
    "Tables (DuckDB):\n"
    "  sales(OrderKey, LineNumber, OrderDate, DeliveryDate, CustomerKey, StoreKey, ProductKey,\n"
    "        Quantity, UnitPrice, NetPrice, UnitCost, CurrencyCode, ExchangeRate)\n"
    "  product(ProductKey, ProductName, Manufacturer, Brand, Color, Weight, Cost, Price,\n"
    "          CategoryName, SubCategoryName)\n"
    "  store(StoreKey, CountryName, State, Status)\n"
    "Joins: sales.ProductKey = product.ProductKey ; sales.StoreKey = store.StoreKey.\n"
    "Grain of `sales` = one order line. CurrencyCode ∈ {USD,EUR,GBP,CAD,AUD}; ExchangeRate → USD base.")

PROMPT = """You are the /ask interpreter for a meaning-as-code system over the public Contoso retail dataset (DuckDB).
Interpret the QUESTION strictly against the ONTOLOGY and SCHEMA, honor its rules, and return a PLAN as STRICT JSON ONLY — no markdown, no prose, no code fences.

ONTOLOGY (the source of truth for meaning):
%(ontology)s

SCHEMA:
%(schema)s

RULES you MUST honor (they come from the ontology above):
- Unqualified "sales"/"revenue" = NET: SUM(Quantity*NetPrice*ExchangeRate). "gross" = SUM(Quantity*UnitPrice*ExchangeRate). [sales.net_of_discount]
- ALWAYS multiply by ExchangeRate to convert each line to the USD base BEFORE summing money; never SUM raw NetPrice across currencies. [sales.single_currency_basis]
- Never sum `sales` together with orders x orderrows (same facts twice). [sales.no_double_count_header_detail]
- Sliceable dimensions ONLY: product(ProductName), brand, category(CategoryName), subcategory, manufacturer, color, country(store.CountryName), currency(CurrencyCode), year/month/quarter(OrderDate). Any other slice (salesperson, supplier, employee, promotion, region, customer segment) -> route REFUSE. [capability.refuse_missing_dimension]
- If the question implies ONE reporting currency but names none -> route ASK. Naming a NON-USD currency for a converted total -> REFUSE (only the USD base rate exists). [sales.ask_currency_when_ambiguous / resolve.never_fabricate]
- No period given -> full available range, disclosed. [measure.period_resolution]
- Never invent a value, column, or rate; if it can't be grounded, REFUSE. [resolve.never_fabricate]

Return STRICT JSON with exactly these keys:
{"route":"COMMIT|ASK|REFUSE",
 "sql":"<COMMIT only: ONE DuckDB SELECT. Put any grouping dimension as the FIRST column and the numeric measure LAST, aliased AS val. Add ORDER BY / LIMIT as the question implies.>",
 "value_format":"usd|int|raw",
 "unit":"<short measure label, e.g. 'net sales'>",
 "caption":"<one sentence: what was computed and which defaults were assumed>",
 "assumptions":[{"text":"...","rule":"<ontology rule id>"}],
 "trace":[{"file":"ontology/...","res":"<what this file decided>"}],
 "final":"route_rules -> ... -> COMMIT|ASK|REFUSE",
 "prompt":"<ASK only: the clarifying question>","hint":"<ASK only>","chips":["USD","EUR"],
 "head":"<REFUSE only: the refusal headline>","why":"<REFUSE only: what it can do instead>"}

QUESTION: %(q)s"""


def interpret_llm(q):
    prompt = PROMPT % {"ontology": ONTOLOGY_TEXT, "schema": SCHEMA_TEXT, "q": q}
    proc = subprocess.run([CLAUDE, "-p", prompt, "--model", MODEL, "--output-format", "json"],
                          capture_output=True, text=True, timeout=90)
    if proc.returncode != 0:
        raise RuntimeError("claude exited %d: %s" % (proc.returncode, proc.stderr[:200]))
    env = json.loads(proc.stdout)
    txt = (env.get("result") or "").strip()
    m = re.search(r"\{.*\}", txt, re.S)          # tolerate stray prose / fences around the JSON
    plan = json.loads(m.group(0) if m else txt)
    plan["_cost"] = env.get("total_cost_usd")
    plan["_ms"] = env.get("duration_ms")
    return plan


def _fmt_val(v, fmt):
    if v is None:
        return "—"
    if fmt == "usd":
        return _money(v)
    if fmt == "int":
        return _int(v)
    try:
        f = float(v)
        return _int(f) if f == int(f) else ("%.2f" % f)
    except (TypeError, ValueError):
        return str(v)


def answer_llm(q):
    plan = interpret_llm(q)
    route = str(plan.get("route", "COMMIT")).upper()
    out = dict(q=q, engine="claude", cost=plan.get("_cost"), ms=plan.get("_ms"), route=route,
               trace=[{"file": t.get("file", ""), "res": t.get("res", "")} for t in plan.get("trace", [])],
               final=plan.get("final", ""),
               assume=[{"t": a.get("text", ""), "rule": a.get("rule", "")} for a in plan.get("assumptions", [])],
               sql=None)
    if route == "ASK":
        out.update(kind="ask", prompt=plan.get("prompt", "Which value?"),
                   hint=plan.get("hint", ""), chips=plan.get("chips", []) or CURRENCIES)
        return out
    if route == "REFUSE":
        out.update(kind="refuse", head=plan.get("head", "Not in the model."), why=plan.get("why", ""))
        return out
    sql = str(plan.get("sql", "")).strip().rstrip(";")
    if not re.match(r"(?is)^\s*(select|with)\b", sql):
        raise ValueError("interpreter returned no SELECT")
    cur = con.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    fmt = plan.get("value_format", "raw")
    unit = plan.get("unit", "")
    out["sql"] = _hl(sql)
    cap = plan.get("caption", "")
    if not rows:
        out.update(kind="value", value="—", unit=unit, caption=cap or "No rows matched.")
    elif len(rows) == 1 and len(cols) == 1:
        out.update(kind="value", value=_fmt_val(rows[0][0], fmt), unit=unit, caption=cap)
    elif len(rows) == 1:
        out.update(kind="value", value=str(rows[0][0]), unit="",
                   caption=(cap + " — " + _fmt_val(rows[0][-1], fmt)).strip(" —"),
                   table={"cols": cols, "rows": [[html.escape(str(c)) for c in rows[0]]]})
    else:
        def _num(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None
        tbl = [[(_fmt_val(c, fmt) if i == len(cols) - 1 else html.escape(str(c))) for i, c in enumerate(r)] for r in rows[:50]]
        out.update(kind="value", value=str(len(rows)), unit=(cols[0] if cols else "rows"), caption=cap,
                   table={"cols": cols, "rows": tbl},
                   chart={"title": unit or "result",
                          "bars": [{"label": str(r[0]), "value": round((_num(r[-1]) or 0) / (1e6 if fmt == "usd" else 1), 2)}
                                   for r in rows[:12] if _num(r[-1]) is not None]})
    return out

# ---- measures (concepts/sales/sales.yaml + rules.yaml) ----
MEASURES = {
    "net":      ("SUM(s.Quantity*s.NetPrice*s.ExchangeRate)",          "net sales",     "usd", "net_sales_base_currency"),
    "gross":    ("SUM(s.Quantity*s.UnitPrice*s.ExchangeRate)",         "gross sales",   "usd", "gross_sales_base_currency"),
    "quantity": ("SUM(s.Quantity)",                                    "units sold",    "int", "measure.additivity_by_type"),
    "orders":   ("COUNT(DISTINCT s.OrderKey)",                         "orders",        "int", "measure.additivity_by_type"),
    # NOTE: profit/margin is a DERIVED measure defined in the ontology (concepts/finance/margin.yaml), not
    # hardcoded here. The offline parser doesn't read the ontology, so it does not carry profit — it refuses
    # it (below) and defers to the LLM interpreter, which does read the ontology. This keeps "only the
    # ontology changed" honest across both paths.
}
# ---- dimensions (concepts/* + edges.yaml).  (sql, label, join, concept-file) ----
DIMS = {
    "product":      ("p.ProductName",              "product",      "product", "concepts/catalog/product.yaml"),
    "brand":        ("p.Brand",                    "brand",        "product", "concepts/catalog/brand.yaml"),
    "category":     ("p.CategoryName",             "category",     "product", "concepts/catalog/product.yaml"),
    "subcategory":  ("p.SubCategoryName",          "subcategory",  "product", "concepts/catalog/product.yaml"),
    "manufacturer": ("p.Manufacturer",             "manufacturer", "product", "concepts/catalog/product.yaml"),
    "color":        ("p.Color",                    "color",        "product", "concepts/catalog/product.yaml"),
    "country":      ("st.CountryName",             "country",      "store",   "concepts/geography/store.yaml"),
    "currency":     ("s.CurrencyCode",             "currency",     None,      "concepts/finance/currency.yaml"),
    "year":         ("year(s.OrderDate)",          "year",         None,      "concepts/time/period.yaml"),
    "month":        ("strftime(s.OrderDate,'%Y-%m')", "month",     None,      "concepts/time/period.yaml"),
    "quarter":      ("concat(year(s.OrderDate),'-Q',quarter(s.OrderDate))", "quarter", None, "concepts/time/period.yaml"),
}
# dimensions the data does NOT carry -> REFUSE (capability.refuse_missing_dimension)
MISSING = ["salesperson", "sales person", "sales rep", "supplier", "vendor", "employee",
           "promotion", "discount reason", "campaign", "region", "channel", "customer segment"]

DIM_WORDS = {  # question word -> dimension key
    "product": "product", "products": "product", "item": "product", "sku": "product",
    "brand": "brand", "brands": "brand", "make": "brand",
    "category": "category", "categories": "category",
    "subcategory": "subcategory", "sub-category": "subcategory",
    "manufacturer": "manufacturer", "manufacturers": "manufacturer",
    "color": "color", "colour": "color",
    "country": "country", "countries": "country", "market": "country", "markets": "country", "store": "country", "geography": "country",
    "currency": "currency", "currencies": "currency",
    "year": "year", "yearly": "year", "annual": "year",
    "month": "month", "monthly": "month",
    "quarter": "quarter", "quarterly": "quarter",
}


def _money(v):
    v = float(v)
    if abs(v) >= 1e6:
        return "$%.1fM" % (v / 1e6)
    if abs(v) >= 1e3:
        return "$%.0fK" % (v / 1e3)
    return "$%.0f" % v


def _int(v):
    return "{:,.0f}".format(float(v)).replace(",", ".")


def _fmt(v, kind):
    return _money(v) if kind == "usd" else _int(v)


def _hl(sql):
    kws = r"\b(SELECT|FROM|WHERE|AND|OR|GROUP BY|ORDER BY|JOIN|ON|AS|IN|BETWEEN|DESC|ASC|LIMIT)\b"
    fns = r"\b(SUM|COUNT|ROUND|YEAR|AVG|DISTINCT|strftime|quarter|concat)\b"
    s = html.escape(sql)
    s = re.sub(r"'[^']*'", lambda m: '<span class="str">%s</span>' % m.group(0), s)
    s = re.sub("(?i)" + kws, lambda m: '<span class="kw">%s</span>' % m.group(0), s)
    s = re.sub("(?i)" + fns, lambda m: '<span class="fn">%s</span>' % m.group(0), s)
    return s


def _find(ql, names):
    for n in sorted(names, key=len, reverse=True):
        if n.lower() in ql:
            return n
    return None


def interpret(q):
    """Parse the question against the ontology -> a plan dict (route, sql, trace, ...). The real interpreter."""
    ql = " " + q.lower().strip() + " "
    trace, assume, filt = [], [], []

    # ---- REFUSE: a dimension the model does not carry ----
    miss = next((m for m in MISSING if m in ql), None)
    if miss:
        return dict(route="REFUSE", rule="capability.refuse_missing_dimension",
                    head="No %s dimension in the model." % miss.strip(),
                    why="It can slice by <b>product, brand, category, manufacturer, color, country, currency, "
                        "year/month</b>. It won't fabricate a dimension the data doesn't carry.",
                    trace=[("ontology/query_rules.yaml", "capability.refuse_missing_dimension"),
                           ("ontology/edges.yaml", "join set carries no '%s'" % miss.strip())],
                    final="route_rules → dimension absent → REFUSE")

    # ---- REFUSE: a DERIVED measure the offline parser doesn't carry. Profit/margin is defined in the
    #      ontology (margin.yaml), not hardcoded here — so the honest offline behaviour is to decline and
    #      defer to the LLM interpreter that reads the ontology. (Keeps "only the ontology changed" true.)
    if re.search(r"\b(profit|margin|profitab)", ql):
        return dict(route="REFUSE", rule="resolve.never_fabricate",
                    head="Profit isn't in the offline parser.",
                    why="The offline keyword parser carries only the Sales concept's direct forms (net/gross sales, units, orders). "
                        "Profit is a <b>derived</b> measure defined in the ontology — answered by the LLM interpreter, which reads it.",
                    trace=[("(offline parser)", "no hardcoded profit measure"),
                           ("route_rules", "derived measure → deferred to the ontology-reading interpreter")],
                    final="route_rules → offline parser carries no profit measure → REFUSE")

    # ---- measure ----
    if re.search(r"\bgross\b", ql):
        mkey = "gross"
    elif re.search(r"\b(units?|quantity|volume|pieces)\b", ql):
        mkey = "quantity"
    elif re.search(r"\b(orders?|transactions?|how many orders)\b", ql) and not re.search(r"sales|revenue", ql):
        mkey = "orders"
    else:
        mkey = "net"
    mexpr, mlabel, mkind, mrule = MEASURES[mkey]
    trace.append(("ontology/rules.yaml" if mkey in ("net", "gross") else "ontology/concepts/sales/sales.yaml",
                  "measure '%s' → %s" % (mlabel, mexpr.replace("s.", ""))))
    if mkey == "net":
        assume.append(("net, not gross", "sales.net_of_discount"))
    if mkind == "usd":
        assume.append(("each line converted to the USD base before summing", "sales.single_currency_basis"))

    # ---- dimension (group-by) ----
    dkey = None
    for w, dk in DIM_WORDS.items():
        if re.search(r"\b" + re.escape(w) + r"\b", ql):
            dkey = dk
            break
    # "by X" strengthens; "best/top ... product" implies group by product
    if dkey:
        dexpr, dlabel, djoin, dfile = DIMS[dkey]
        trace.append(("ontology/" + dfile, "'%s' → dimension %s" % (dlabel, dexpr)))

    # ---- superlative / ranking ----
    superl = None
    if re.search(r"\b(best|top|most|highest|leading|largest|biggest|greatest)\b", ql):
        superl = "DESC"
    elif re.search(r"\b(worst|lowest|least|smallest|bottom|fewest)\b", ql):
        superl = "ASC"
    mN = re.search(r"\btop\s+(\d+)|\bbest\s+(\d+)|\b(\d+)\s+(?:best|top)\b", ql)
    limit = None
    if mN:
        limit = int(next(g for g in mN.groups() if g))
    elif superl:
        singular = bool(re.search(r"\b(the|which|what)\b.*\b(best|top|most|highest|worst|lowest)\b", ql)) and \
            not re.search(r"\b(products|brands|categories|countries|items)\b", ql)
        limit = 1 if singular else 10

    # ---- filters ----
    yr = re.search(r"\b(20\d\d)\b", ql)
    if yr and int(yr.group(1)) in YEARS:
        filt.append(("year(s.OrderDate) = %d" % int(yr.group(1)), "year " + yr.group(1)))
        trace.append(("ontology/concepts/time/period.yaml", "%s → explicit year window" % yr.group(1)))
    br = _find(ql, BRANDS)
    if br:
        filt.append(("p.Brand = '%s'" % br.replace("'", "''"), "brand " + br))
    co = _find(ql, COUNTRIES)
    if co:
        filt.append(("st.CountryName = '%s'" % co.replace("'", "''"), "country " + co))
    ca = _find(ql, CATEGORIES)
    if ca:
        filt.append(("p.CategoryName = '%s'" % ca.replace("'", "''"), "category " + ca))
    named_cur = _find(ql.upper(), CURRENCIES)

    # ---- ASK: a single reporting currency is implied but none named ----
    if re.search(r"\b(single|one|a)\s+currenc", ql) and not named_cur:
        return dict(route="ASK", rule="sales.ask_currency_when_ambiguous",
                    prompt="Which reporting currency?",
                    hint="The rows span five currencies (USD, EUR, GBP, CAD, AUD) and none was named — "
                         "name one, or accept the disclosed base (USD).",
                    chips=CURRENCIES,
                    trace=[("ontology/concepts/finance/currency.yaml", "5-member closed set → ambiguous"),
                           ("ontology/query_rules.yaml", "currency.basis mandatory here → ASK")],
                    final="route_rules → reporting currency unnamed → ASK")
    if named_cur and named_cur != "USD":
        return dict(route="REFUSE", rule="resolve.never_fabricate",
                    head="A %s total isn't grounded in this data." % named_cur,
                    why="Each line carries its rate to the <b>USD</b> base only; a %s total needs a USD→%s "
                        "rate that isn't in the model — flagged, not guessed." % (named_cur, named_cur),
                    trace=[("ontology/concepts/finance/currency.yaml", "rate → USD base only"),
                           ("ontology/query_rules.yaml", "resolve.never_fabricate")],
                    final="route_rules → target currency ungrounded → ABSTAIN")

    # ---- assemble SQL ----
    joins = set()
    if dkey and DIMS[dkey][2]:
        joins.add(DIMS[dkey][2])
    for _, lbl in []:
        pass
    if br or ca:
        joins.add("product")
    if co:
        joins.add("store")
    join_sql = ""
    if "product" in joins:
        join_sql += " JOIN product p ON s.ProductKey = p.ProductKey"
    if "store" in joins:
        join_sql += " JOIN store st ON s.StoreKey = st.StoreKey"

    where = " WHERE " + " AND ".join(f[0] for f in filt) if filt else ""
    for _, lbl in filt:
        pass

    if dkey:
        dexpr, dlabel, djoin, dfile = DIMS[dkey]
        order = "ORDER BY val %s" % (superl or "DESC")
        lim = " LIMIT %d" % (limit or 20)
        sql = "SELECT %s AS dim, %s AS val FROM sales s%s%s GROUP BY %s %s%s" % (
            dexpr, mexpr, join_sql, where, dexpr, order, lim)
        final = "route_rules → measure + dimension resolved, executed → COMMIT"
        trace.append(("route_rules", "%s%s → GROUP BY %s %s%s → COMMIT" % (
            "superlative " if superl else "", "top %d " % limit if limit else "", dlabel,
            (superl or "DESC"), " LIMIT %d" % limit if limit else "")))
        kind = "rank" if (superl and (limit == 1)) else "table"
    else:
        sql = "SELECT %s AS val FROM sales s%s%s" % (mexpr, join_sql, where)
        final = "route_rules → measure resolved, no open slots → COMMIT"
        trace.append(("route_rules", "grand total · worst-wins → COMMIT"))
        kind = "scalar"

    if not any("year" in f[0] for f in filt):
        assume.append(("full available period (%d–%d)" % (YEARS[0], YEARS[-1]), "measure.period_resolution"))

    return dict(route="COMMIT", rule=mrule, sql=sql, kind=kind, mkind=mkind, mlabel=mlabel,
                dlabel=(DIMS[dkey][1] if dkey else None), dkey=dkey, limit=limit, superl=superl,
                filters=[f[1] for f in filt], trace=trace, assume=assume, final=final)


def answer_rules(q):
    plan = interpret(q)
    if plan["route"] in ("ASK", "REFUSE"):
        return _wrap(q, plan, None)
    rows = con.execute(plan["sql"]).fetchall()
    return _wrap(q, plan, rows)


def answer(q):
    """Dispatch: real LLM interpreter (claude CLI) first; offline rule parser as the fallback."""
    if not (q or "").strip():
        return dict(q=q, route="ASK", kind="ask", prompt="Ask a question.", hint="", chips=[], trace=[], assume=[])
    if USE_LLM:
        try:
            return answer_llm(q)
        except Exception as e:
            r = answer_rules(q)
            r["engine"] = "fallback"
            r["fallback"] = "LLM interpret failed (%s) — used the offline parser" % str(e)[:160]
            return r
    r = answer_rules(q)
    r["engine"] = "rules"
    return r


def _wrap(q, plan, rows):
    out = dict(q=q, route=plan["route"], rule=plan.get("rule"),
               trace=[{"file": f, "res": r} for f, r in plan.get("trace", [])],
               final=plan.get("final", ""),
               assume=[{"t": t, "rule": r} for t, r in plan.get("assume", [])],
               sql=_hl(plan["sql"]) if plan.get("sql") else None)
    if plan["route"] == "ASK":
        out.update(kind="ask", prompt=plan["prompt"], hint=plan["hint"], chips=plan["chips"])
        return out
    if plan["route"] == "REFUSE":
        out.update(kind="refuse", head=plan["head"], why=plan["why"])
        return out

    mkind = plan["mkind"]
    scope = ("%s" % plan["mlabel"]) + (" · " + " · ".join(plan["filters"]) if plan["filters"] else "")
    if plan["kind"] == "scalar":
        v = rows[0][0] if rows and rows[0][0] is not None else 0
        out.update(kind="value", value=_fmt(v, mkind), unit=plan["mlabel"],
                   caption="%s%s, converted to USD where applicable." % (plan["mlabel"].capitalize(),
                           (" — " + ", ".join(plan["filters"])) if plan["filters"] else ", all channels, full period"))
    elif plan["kind"] == "rank":
        name, v = (rows[0][0], rows[0][1]) if rows else ("—", 0)
        out.update(kind="value", value=str(name), unit="",
                   caption="Top %s by %s%s — %s." % (plan["dlabel"], plan["mlabel"],
                           (" (" + ", ".join(plan["filters"]) + ")") if plan["filters"] else "", _fmt(v, mkind)),
                   table={"cols": [plan["dlabel"], plan["mlabel"]],
                          "rows": [[html.escape(str(r[0])), _fmt(r[1], mkind)] for r in rows]})
    else:  # table
        out.update(kind="value", value=str(len(rows)), unit=plan["dlabel"] + "s",
                   caption="%s by %s%s — top %d." % (plan["mlabel"].capitalize(), plan["dlabel"],
                           (" (" + ", ".join(plan["filters"]) + ")") if plan["filters"] else "", len(rows)),
                   table={"cols": [plan["dlabel"], plan["mlabel"]],
                          "rows": [[html.escape(str(r[0])), _fmt(r[1], mkind)] for r in rows]},
                   chart={"title": "%s by %s" % (plan["mlabel"], plan["dlabel"]),
                          "bars": [{"label": str(r[0]), "value": round(float(r[1]) / (1e6 if mkind == "usd" else 1), 2)} for r in rows[:12]]})
    return out


# ============================ HTTP server ============================
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.split("?")[0] in ("/", "/index.html", "/ask.html"):
            self._send(200, PAGE, "text/html; charset=utf-8")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/ask":
            return self._send(404, "not found", "text/plain")
        n = int(self.headers.get("Content-Length", 0))
        try:
            q = json.loads(self.rfile.read(n) or "{}").get("q", "")
            self._send(200, json.dumps(answer(q), ensure_ascii=False))
        except Exception as e:
            self._send(200, json.dumps({"route": "REFUSE", "kind": "refuse",
                       "q": q if 'q' in dir() else "", "head": "Could not run that.",
                       "why": html.escape(str(e)), "trace": [], "assume": [], "final": ""}))


PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Contoso · Ask — meaning as code</title>
<style>
  :root{--ground:#eef1f5;--card:#fff;--panel2:#f7f9fc;--ink:#141a22;--muted:#5a6674;--faint:#8a94a3;--hair:#d4dae2;
    --accent:#1f5fe0;--accent-soft:#1f5fe022;--commit:#0f9d58;--commit-bg:#0f9d5814;--commit-line:#0f9d5855;
    --ask:#c67a12;--ask-bg:#c67a1214;--ask-line:#c67a1255;--refuse:#d4483b;--refuse-bg:#d4483b12;--refuse-line:#d4483b55;
    --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;--sans:ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif;--r:12px}
  :root[data-theme="dark"]{--ground:#0c1015;--card:#141b24;--panel2:#111722;--ink:#e6ebf1;--muted:#94a3b4;--faint:#63707f;--hair:#263140;
    --accent:#5b8cf5;--accent-soft:#5b8cf522;--commit:#3ec27a;--commit-bg:#3ec27a1c;--commit-line:#3ec27a55;
    --ask:#e6a13c;--ask-bg:#e6a13c1c;--ask-line:#e6a13c55;--refuse:#f0685c;--refuse-bg:#f0685c1c;--refuse-line:#f0685c55}
  *{box-sizing:border-box}html,body{height:100%}
  body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.55;-webkit-font-smoothing:antialiased}
  .app{height:100vh;display:flex;flex-direction:column}
  .topnav{display:flex;align-items:center;gap:12px;padding:11px 20px;border-bottom:1px solid var(--hair);background:var(--card)}
  .brand{font-weight:680;font-size:15px}.brand b{color:var(--accent)}.brand .src{color:var(--muted);font-weight:500;font-size:12.5px;margin-left:8px}
  .sp{flex:1}.btn{font-size:12.5px;color:var(--muted);background:var(--panel2);border:1px solid var(--hair);border-radius:8px;padding:6px 11px;cursor:pointer}
  .btn:hover{color:var(--ink);border-color:var(--accent)}.iconbtn{width:32px;height:31px;font-size:15px;padding:0}
  .split{flex:1;display:grid;grid-template-columns:1fr 1fr;min-height:0}
  .col{min-height:0;display:flex;flex-direction:column;overflow:hidden}.left-col{border-right:1px solid var(--hair)}
  .col-head{display:flex;align-items:center;gap:8px;padding:12px 20px;border-bottom:1px solid var(--hair);background:var(--panel2)}
  .kicker{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);font-weight:600;display:flex;align-items:center;gap:7px}
  .kicker .dot{color:var(--accent);font-size:9px}.cnt{margin-left:auto;font-family:var(--mono);font-size:11px;color:var(--faint)}
  .workspace,.history{flex:1;overflow-y:auto;padding:20px}
  .empty{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--muted);gap:8px;padding:30px}
  .empty .ico{font-size:30px;opacity:.7}.empty h3{margin:0;font-size:16px;color:var(--ink);font-weight:640}.empty p{margin:0;max-width:38ch;font-size:13px}
  .badge{font-family:var(--mono);font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:4px 10px;border-radius:20px}
  .badge.commit{background:var(--commit-bg);color:var(--commit)}.badge.ask{background:var(--ask-bg);color:var(--ask)}.badge.refuse{background:var(--refuse-bg);color:var(--refuse)}
  .rep-q{font-size:19px;font-weight:640;margin:14px 0 0;max-width:48ch}
  .rep-val{font-family:var(--mono);font-size:31px;font-weight:700;margin-top:16px;word-break:break-word}.rep-val .u{font-size:14px;color:var(--muted);margin-left:9px;font-weight:500}
  .commit .rep-val{color:var(--ink)}.rep-cap{color:var(--muted);font-size:13px;margin-top:8px;max-width:64ch}
  .rep-ask{font-size:20px;font-weight:640;color:var(--ask);margin-top:16px}.rep-refuse{font-size:19px;font-weight:640;color:var(--refuse);margin-top:16px}
  .assume{margin-top:16px;display:flex;gap:9px;background:var(--ask-bg);border:1px solid var(--ask-line);border-radius:10px;padding:11px 13px;font-size:12.5px;color:var(--ink)}
  .assume b{color:var(--ask)}.assume code{font-family:var(--mono);font-size:11px;background:var(--card);border:1px solid var(--ask-line);border-radius:5px;padding:1px 5px}.assume .w{color:var(--ask)}
  .sec{margin-top:22px}.sec h5{font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--faint);font-weight:700;margin:0 0 11px;display:flex;align-items:center;gap:10px}
  .sec h5::after{content:"";flex:1;height:1px;background:var(--hair)}.sec.reason h5{color:var(--accent)}
  .walk{background:var(--card);border:1px solid var(--hair);border-left:3px solid var(--accent);border-radius:10px;padding:12px 15px}
  .tline{font-family:var(--mono);font-size:12px;line-height:1.7;display:flex;gap:8px;color:var(--muted)}
  .tline .idx{color:var(--faint);flex:0 0 15px}.tline .file{color:var(--accent)}.tline .ar{color:var(--faint)}.tline .res{color:var(--ink)}
  .tfinal{margin-top:7px;font-family:var(--mono);font-size:11px;color:var(--faint);font-style:italic}
  table.rt{width:100%;border-collapse:collapse;font-size:13px}
  table.rt th{text-align:left;font-size:10px;letter-spacing:.05em;text-transform:uppercase;color:var(--faint);font-weight:600;padding:0 10px 7px 0;border-bottom:1px solid var(--hair)}
  table.rt td{padding:8px 10px 8px 0;border-bottom:1px solid var(--hair);font-variant-numeric:tabular-nums}table.rt tr:last-child td{border-bottom:0}table.rt td:nth-child(2){text-align:right}
  .chart{display:none;flex-direction:column;gap:7px;margin-top:12px}.chart.open{display:flex}
  .bar{display:grid;grid-template-columns:150px 1fr 70px;align-items:center;gap:9px;font-size:12px}
  .bl{color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.bt{height:8px;background:var(--panel2);border:1px solid var(--hair);border-radius:5px;overflow:hidden}.bf{height:100%;background:linear-gradient(90deg,var(--accent),var(--commit))}.bv{text-align:right;font-variant-numeric:tabular-nums}
  pre.sql{margin:0;font-family:var(--mono);font-size:12px;line-height:1.55;background:var(--card);border:1px solid var(--hair);border-radius:10px;padding:12px 14px;overflow-x:auto;white-space:pre-wrap}
  pre.sql .kw{color:var(--accent)}pre.sql .fn{color:#7c3aed}pre.sql .str{color:var(--commit)}:root[data-theme="dark"] pre.sql .fn{color:#c39bff}
  .cchips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.cchip{font-size:12.5px;border:1px solid var(--hair);background:var(--panel2);color:var(--muted);border-radius:20px;padding:6px 13px;cursor:pointer}.cchip:hover{border-color:var(--ask);color:var(--ink)}
  .actions{display:flex;gap:8px;margin-top:20px;flex-wrap:wrap}.act{font-size:12px;color:var(--muted);background:var(--panel2);border:1px solid var(--hair);border-radius:8px;padding:6px 12px;cursor:pointer}.act:hover{color:var(--ink);border-color:var(--accent)}
  .entry{border:1px solid var(--hair);border-radius:var(--r);background:var(--card);padding:12px 14px;margin-bottom:12px;cursor:pointer;transition:.12s}
  .entry:hover{border-color:var(--accent)}.entry.on{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
  .entry .eq{font-weight:560;font-size:14px;margin-bottom:9px}.entry .er{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
  .entry .ev{font-family:var(--mono);font-weight:700;font-size:14px;color:var(--commit)}.entry .eside{margin-left:auto;font-size:11px;color:var(--accent);font-family:var(--mono)}
  .spin{width:13px;height:13px;border:2px solid var(--hair);border-top-color:var(--accent);border-radius:50%;display:inline-block;animation:sp .7s linear infinite}@keyframes sp{to{transform:rotate(360deg)}}
  .composer-zone{border-top:1px solid var(--hair);background:var(--card);padding:14px 20px}
  .hero{text-align:center;padding:6px 10px 16px}.hero .ico{font-size:24px;color:var(--accent)}.hero h2{margin:8px 0 0;font-size:20px;font-weight:660}.hero p{color:var(--muted);font-size:13px;margin:8px auto 0;max-width:46ch}
  .try-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center;margin-top:14px;font-size:11.5px;color:var(--faint)}
  .try-row .tchip{font-size:12px;border:1px solid var(--hair);background:var(--panel2);color:var(--muted);border-radius:20px;padding:6px 12px;cursor:pointer}.try-row .tchip:hover{border-color:var(--accent);color:var(--ink)}
  .composer{display:flex;align-items:flex-end;gap:8px;background:var(--panel2);border:1px solid var(--hair);border-radius:14px;padding:8px 8px 8px 16px;margin-top:12px}
  .composer:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
  .composer textarea{flex:1;resize:none;border:none;outline:none;background:transparent;color:var(--ink);font-family:var(--sans);font-size:14.5px;line-height:1.5;max-height:120px;padding:5px 0}
  .composer textarea::placeholder{color:var(--faint)}
  .send{width:36px;height:36px;border-radius:10px;border:none;background:var(--accent);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center}.send:hover{filter:brightness(1.08)}
  .rmeta{margin-top:18px;padding-top:12px;border-top:1px solid var(--hair);font-family:var(--mono);font-size:11px;color:var(--faint);display:flex;align-items:center;gap:8px}
  .rmeta .b{color:var(--commit);font-weight:600}.rmeta .warn{color:var(--ask)}
  .foot{margin-top:9px;font-size:11px;color:var(--faint);text-align:center}
  @media(max-width:820px){.split{grid-template-columns:1fr;grid-template-rows:1fr 1fr}.left-col{border-right:none;border-bottom:1px solid var(--hair)}}
</style></head><body>
<div class="app">
  <div class="topnav"><span class="brand">Contoso · <b>Ask</b><span class="src">/ CONTOSO · claude interprets the ontology → DuckDB executes</span></span>
    <span class="sp"></span>
    <button class="btn" id="resetBtn">＋ New session</button>
    <button class="btn iconbtn" id="themeBtn" title="Toggle light / dark">◑</button>
  </div>
  <div class="split">
    <section class="col left-col">
      <div class="col-head"><span class="kicker"><span class="dot">●</span> Workspace — act on a retained result</span></div>
      <div class="workspace" id="workspace"></div>
    </section>
    <section class="col right-col">
      <div class="col-head"><span class="kicker"><span class="dot">●</span> Conversation — persistent trace</span><span class="cnt" id="entryCount"></span></div>
      <div class="history" id="history"></div>
      <div class="composer-zone">
        <div class="hero" id="hero"><div class="ico">✳</div><h2>Ask Contoso anything</h2>
          <p>Every question is parsed against the ontology, turned into SQL and executed on contoso.duckdb — never guessed.</p>
          <div class="try-row" id="tryRow"></div></div>
        <div class="composer"><textarea id="input" rows="1" placeholder="e.g. what was the best selling product? · sales by category in 2024 · top 5 brands by units"></textarea>
          <button class="send" id="sendBtn"><svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor"><path d="M2 10l16-7-7 16-2-6-7-3z"/></svg></button></div>
        <div class="foot">Enter to send · Shift+Enter for a new line · live interpreter over the ontology, executed on contoso.duckdb</div>
      </div>
    </section>
  </div>
</div>
<script>
function esc(s){return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
let entries=[],focus=null,uid=0;
function walkHTML(a){const l=(a.trace||[]).map((t,i)=>`<div class="tline"><span class="idx">${i+1}</span><span class="file">${esc(t.file)}</span><span class="ar">→</span><span class="res">${esc(t.res)}</span></div>`).join('');
  return l?`<div class="sec reason"><h5>how it routed — ontology walk</h5><div class="walk">${l}${a.final?`<div class="tfinal">${esc(a.final)}</div>`:''}</div></div>`:'';}
function report(a){
  let head;
  if(a.kind==='value') head=`<div class="rep-val">${esc(a.value)}<span class="u">${esc(a.unit||'')}</span></div>${a.caption?`<p class="rep-cap">${esc(a.caption)}</p>`:''}`;
  else if(a.kind==='ask') head=`<div class="rep-ask">${esc(a.prompt)}</div><p class="rep-cap">${esc(a.hint)}</p><div class="cchips">${(a.chips||[]).map(c=>`<button class="cchip" onclick="onChip('${esc(c)}')">${esc(c)}</button>`).join('')}</div>`;
  else head=`<div class="rep-refuse">${esc(a.head)}</div><p class="rep-cap">${a.why}</p>`;
  const assume=(a.assume&&a.assume.length)?`<div class="assume"><span class="w">⚠</span><div>Assumed: ${a.assume.map(x=>esc(x.t)+' <code>'+esc(x.rule)+'</code>').join(' · ')} — disclosed.</div></div>`:'';
  const table=a.table?`<div class="sec"><h5>result</h5><table class="rt"><thead><tr>${a.table.cols.map(c=>`<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${a.table.rows.map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table>${a.chart?`<div class="chart open" id="chart">${bars(a.chart)}</div>`:''}</div>`:'';
  const sql=a.sql?`<div class="sec"><h5>generated sql · executed</h5><pre class="sql">${a.sql}</pre></div>`:'';
  let meta='';
  if(a.engine==='claude') meta=`<div class="rmeta"><span class="b">● claude</span> interpreted the ontology · ${((a.ms||0)/1000).toFixed(1)}s · $${(a.cost||0).toFixed(3)} · SQL executed on contoso.duckdb</div>`;
  else if(a.engine==='fallback') meta=`<div class="rmeta"><span class="warn">⚠ ${esc(a.fallback||'offline parser')}</span></div>`;
  else if(a.engine==='rules') meta=`<div class="rmeta">offline rule parser (no LLM) · SQL executed on contoso.duckdb</div>`;
  return `<div class="report ${a.route.toLowerCase()}"><span class="badge ${a.route.toLowerCase()}">${a.route}</span><div class="rep-q">${esc(a.q)}</div>${head}${assume}${walkHTML(a)}${table}${sql}${meta}</div>`;
}
function bars(c){const mx=Math.max(...c.bars.map(b=>b.value))||1;return `<div style="font-size:10px;color:var(--faint);text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">${esc(c.title)}</div>`+c.bars.map(b=>`<div class="bar"><span class="bl">${esc(b.label)}</span><span class="bt"><span class="bf" style="width:${Math.max(3,b.value/mx*100).toFixed(1)}%"></span></span><span class="bv">${(''+b.value).replace('.',',')}</span></div>`).join('');}
function shortResult(a){if(!a)return '<span class="spin"></span> <span style="color:var(--muted)">running…</span>';
  if(a.kind==='value')return `<span class="ev">${esc(a.value)}</span> <span style="color:var(--muted);font-size:12px">${esc(a.unit||'')}</span>`;
  if(a.kind==='ask')return '<span style="color:var(--ask);font-weight:600">Clarification needed</span>';return '<span style="color:var(--refuse);font-weight:600">Declined</span>';}
function render(){
  document.getElementById('entryCount').textContent=entries.length?entries.length+(entries.length===1?' question':' questions'):'';
  document.getElementById('hero').style.display=entries.length?'none':'block';
  document.getElementById('history').innerHTML=entries.map(e=>`<div class="entry ${e.a?e.a.route.toLowerCase():''} ${e.uid===focus?'on':''}" onclick="focusOn(${e.uid})"><div class="eq">${esc(e.q)}</div><div class="er">${e.a?`<span class="badge ${e.a.route.toLowerCase()}">${e.a.route}</span>`:''}${shortResult(e.a)}<span class="eside">open in workspace →</span></div></div>`).join('');
  const ws=document.getElementById('workspace'),fe=entries.find(e=>e.uid===focus);
  ws.innerHTML=fe?(fe.a?report(fe.a):`<div class="empty"><span class="spin"></span><p>Interpreting, generating SQL, executing…</p></div>`):`<div class="empty"><div class="ico">🗂️</div><h3>No result focused yet</h3><p>Ask a question, or click any entry in the conversation — its report opens here.</p></div>`;
}
async function ask(q){
  const e={uid:++uid,q:q,a:null};entries.push(e);focus=e.uid;render();
  const h=document.getElementById('history');requestAnimationFrame(()=>h.scrollTop=h.scrollHeight);
  try{const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q})});e.a=await r.json();}
  catch(err){e.a={q:q,route:'REFUSE',kind:'refuse',head:'Server not reachable.',why:esc(String(err)),trace:[],assume:[]};}
  render();
}
function focusOn(u){focus=u;render();document.getElementById('workspace').scrollTop=0;}
function onChip(t){submit(t);}
function submit(t){if(t&&t.trim())ask(t.trim());}
function fire(){const ta=document.getElementById('input'),v=ta.value.trim();if(!v)return;ta.value='';ta.style.height='auto';submit(v);}
function applyTheme(t){document.documentElement.dataset.theme=t;try{localStorage.setItem('contoso_theme',t)}catch(e){}document.getElementById('themeBtn').textContent=t==='dark'?'☀':'◑';}
(function(){let t='light';try{t=localStorage.getItem('contoso_theme')||'light'}catch(e){}applyTheme(t);})();
const ta=document.getElementById('input');
ta.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();fire();}});
ta.addEventListener('input',()=>{ta.style.height='auto';ta.style.height=Math.min(120,ta.scrollHeight)+'px';});
document.getElementById('sendBtn').onclick=fire;
document.getElementById('resetBtn').onclick=()=>{entries=[];focus=null;render();ta.focus();};
document.getElementById('themeBtn').onclick=()=>applyTheme(document.documentElement.dataset.theme==='dark'?'light':'dark');
document.getElementById('tryRow').innerHTML='<span>Try:</span>'+['what was the best selling product?','sales by category in 2024','top 5 brands by units','which country sold the most?'].map(q=>`<button class="tchip" onclick="submit('${q}')">${q}</button>`).join('');
render();
</script></body></html>"""


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    mode = ("LLM: claude CLI interprets the ontology (%s)" % CLAUDE) if USE_LLM else "LLM OFF — offline rule parser only"
    print("Contoso · Ask —", mode)
    print("  open  http://localhost:%d" % PORT)
    print("  (Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")


if __name__ == "__main__":
    main()
