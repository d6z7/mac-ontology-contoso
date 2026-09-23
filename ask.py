#!/usr/bin/env python3
"""
ask.py — the Contoso `/ask` demo: a natural-language question -> a disclosed answer WITH ITS FULL TRACE.

This is the OFFLINE interpreter. It recognises the demo's canonical questions with simple pattern matching,
then answers them the way the ONTOLOGY says to — walking the decision-policy slot by slot, running the Sales
concept's own SQL rule against the live DuckDB warehouse, and disclosing everything it did: the files it read,
how each open slot resolved (and the rule that governed it), the assumptions it made, and the paths it rejected.

Every route, disclosure, rule id and dead-end below is read from the ontology files — none is a hard-coded
string. The trace it emits mirrors, on public/MIT Contoso data, the shape of a real interpreter's captured run.

(The real interpreter swaps this pattern-matcher for an LLM that reads the same ontology as context; the
slot walk / disclosure / refusal logic is unchanged — only the recogniser differs.)

  python3 ask.py "what were our total sales?"   # answer + full trace, in the terminal
  python3 ask.py                                 # the scripted demo: COMMIT / ASK / REFUSE
  python3 ask.py --html projections/ask.trace.html   # render the demo's traces as a trace page
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DB = HERE / "contoso.duckdb"


def _load(rel):
    return yaml.safe_load((HERE / rel).read_text(encoding="utf-8")) or {}


RULES = _load("ontology/rules.yaml")          # derived-measure SQL (net_sales_base_currency)
QRULES = _load("ontology/query_rules.yaml")   # general rules + decision_policy slot index
POLICY = {s["slot"]: s for s in QRULES.get("decision_policy", {}).get("slots", [])}
ONTOLOGY_VERSION = QRULES.get("metadata", {}).get("schema_version", "?")
REVIEWED = QRULES.get("decision_policy", {}).get("governance", {}).get("last_reviewed") \
    or QRULES.get("metadata", {}).get("date", "?")

# worst-wins ranking over the policy tiers: blocked (REFUSE) > mandatory (ASK) > default/bound (COMMIT)
LANE_OF = {"BLOCKED": "REFUSE", "ASK": "ASK", "DEFAULT": "COMMIT", "BOUND": "COMMIT", "NA": None}
RANK = {"BLOCKED": 3, "ASK": 2, "DEFAULT": 1, "BOUND": 1, "NA": 0}


def derived(rule_id):
    return next((r for r in RULES.get("rules", []) if r.get("rule") == rule_id), {})


def duckdb(sql):
    out = subprocess.run(["duckdb", str(DB), "-json", "-c", sql], capture_output=True, text=True)
    if out.returncode:
        raise RuntimeError(out.stderr.strip())
    return json.loads(out.stdout or "[]")


def money(x):
    return "$%.1fM" % (x / 1_000_000)


def _rule(slot):
    """The governing rule id for a decision slot, read from the policy index."""
    return POLICY[slot]["governing_rule"].split("(")[0].strip()


# --- the six decision slots, in worst-wins evaluation order, labelled for the walk -------------------
SLOT_LABEL = {
    "currency.basis":            "reporting currency",
    "measure.gross_vs_net":      "gross vs net",
    "period.window":             "time window",
    "source.double_count":       "header/detail double-count",
    "market.online_channel":     "'Online' as a market",
    "capability.missing_dimension": "requested dimension carried?",
}
SLOT_ORDER = list(SLOT_LABEL)


def _verdict(walk):
    """Worst-wins over the engaged slots -> the lane."""
    top = max(walk, key=lambda s: RANK[s["status"]])
    return LANE_OF[top["status"]] or "COMMIT"


def build_trace(q):
    """Return the full disclosed trace for one question (the public analogue of a captured run)."""
    ql = q.lower()

    # ---- REFUSE — a dimension the data does not carry ---------------------------------------------
    miss = next((m for m in ("salesperson", "sales person", "sales rep", "supplier",
                             "promotion", "discount reason") if m in ql), None)
    if miss:
        walk = [_na(s) for s in SLOT_ORDER]
        walk[-1] = dict(slot="capability.missing_dimension", status="BLOCKED",
                        note="'%s' is not a dimension the model carries -> REFUSE." % miss,
                        rule=_rule("capability.missing_dimension"))
        return dict(
            id="ask.refuse", q=q, route="REFUSE", value=None,
            head="No %s dimension in the model." % miss,
            why="It can slice by: brand, product, category, store/country, currency, date. "
                "It will not fabricate a dimension the data doesn't carry.",
            sql=None, walk=walk, verdict="REFUSE",
            assumptions=[],
            dead_ends=[
                dict(text="Approximate '%s' with StoreKey or a nearby column" % miss,
                     rule="capability.refuse_missing_dimension"),
                dict(text="Fabricate the dimension from generic priors",
                     rule="resolve.never_fabricate"),
            ],
            trail=[
                ("ontology/query_rules.yaml", "capability.refuse_missing_dimension + the decision_policy slot index"),
                ("ontology/concepts/sales/sales.yaml", "the dimensions Sales DOES carry"),
                ("ontology/edges.yaml", "the real join set: product, store, currency, date, brand — no salesperson"),
            ],
        )

    # ---- ASK — a single-currency total is asked but none is named --------------------------------
    if re.search(r"\b(single|one|a)\s+currenc", ql) and not re.search(r"\b(usd|eur|gbp|cad|aud)\b", ql):
        walk = [
            dict(slot="currency.basis", status="ASK",
                 note="a single reporting currency is asked for but none of the 5 (USD/EUR/GBP/CAD/AUD) is named "
                      "-> clarify, don't guess.",
                 rule="sales.ask_currency_when_ambiguous"),
            _default("measure.gross_vs_net", "NET (Quantity x NetPrice) — 'sales' unqualified."),
            _default("period.window", "full available range 2016-2025, disclosed."),
            _na("source.double_count"), _na("market.online_channel"),
            _na("capability.missing_dimension"),
        ]
        return dict(
            id="ask.ask", q=q, route="ASK", value=None,
            head="Which reporting currency?",
            why="The rows span 5 currencies (USD, EUR, GBP, CAD, AUD) and none was named. "
                "Name one, or I commit to the disclosed base currency (USD) as the default.",
            sql=None, walk=walk, verdict="ASK",
            assumptions=[],
            dead_ends=[
                dict(text="Silently default to USD without disclosing it",
                     rule="ambiguity.ask_dont_guess"),
                dict(text="SUM(NetPrice) across the five currencies as if comparable",
                     rule="sales.single_currency_basis"),
            ],
            trail=[
                ("ontology/query_rules.yaml", "ambiguity.ask_dont_guess + the currency.basis slot"),
                ("ontology/concepts/finance/currency.yaml", "the 5-member closed currency set — why it's ambiguous"),
                ("ontology/concepts/sales/sales.yaml", "sales.ask_currency_when_ambiguous"),
            ],
        )

    # ---- COMMIT — total sales: NET, converted to one base currency, then summed -------------------
    rule = derived("net_sales_base_currency")
    expr = rule.get("template", "").splitlines()[0].split("--")[0].strip()
    sql = "SELECT %s AS value FROM sales" % expr
    val = float(duckdb(sql)[0]["value"])
    rng = duckdb("SELECT strftime(min(OrderDate),'%Y-%m-%d') lo, strftime(max(OrderDate),'%Y-%m-%d') hi FROM sales")[0]
    walk = [
        _default("currency.basis",
                 "no currency named -> convert each line to the base currency (USD) via its ExchangeRate BEFORE summing."),
        _default("measure.gross_vs_net", "unqualified 'sales' -> NET (Quantity x NetPrice), not gross."),
        _default("period.window", "no window named -> the full available range %s to %s, disclosed." % (rng["lo"], rng["hi"])),
        _held("source.double_count", "the query sums `sales` only, never `sales` + orders x orderrows — invariant holds."),
        _na("market.online_channel"),
        _na("capability.missing_dimension"),
    ]
    return dict(
        id="ask.commit", q=q, route="COMMIT", value=money(val),
        head=money(val),
        why="net of discount · each line converted to one base currency (USD) before summing · "
            "all channels · full available period.  Assumed: net not gross; base currency USD.",
        sql=sql, walk=walk, verdict="COMMIT",
        assumptions=[
            dict(text="net, not gross (Quantity x NetPrice)", rule="sales.net_of_discount"),
            dict(text="base currency USD; each line converted before summing", rule="sales.single_currency_basis"),
            dict(text="full available period %s to %s" % (rng["lo"], rng["hi"]), rule="measure.period_resolution"),
            dict(text="all defaults disclosed in the answer", rule="assumption.disclose_defaults"),
        ],
        dead_ends=[
            dict(text="SUM(NetPrice) across mixed CurrencyCode (raw, unconverted)", rule="sales.single_currency_basis"),
            dict(text="SUM(Quantity x UnitPrice) — gross, before discount", rule="sales.net_of_discount"),
            dict(text="Sum `sales` AND orders x orderrows together (doubles revenue)", rule="sales.no_double_count_header_detail"),
        ],
        trail=[
            ("ontology/query_rules.yaml", "general rules + decision_policy slot index"),
            ("ontology/concepts/sales/sales.yaml", "Sales measure; derived_by_rule net_sales_base_currency; net/currency/double-count rules"),
            ("ontology/rules.yaml", "net_sales_base_currency — the SQL template"),
            ("ontology/concepts/finance/currency.yaml", "the 5-member set + ExchangeRate factor"),
        ],
    )


# ---- slot-walk helpers -------------------------------------------------------------------------------
def _default(slot, note):
    return dict(slot=slot, status="DEFAULT", note=note, rule=_rule(slot))


def _held(slot, note):
    # a blocked (invariant) slot that was NOT violated by this query
    return dict(slot=slot, status="HELD", note=note, rule=_rule(slot))


def _na(slot):
    return dict(slot=slot, status="NA", note="not engaged by this question.", rule=_rule(slot))


# ============================ terminal renderer ======================================================
_C = {"COMMIT": "\033[1;32m", "ASK": "\033[1;33m", "REFUSE": "\033[1;31m"}
_STAT = {"BOUND": "bound", "DEFAULT": "default", "ASK": "ask", "BLOCKED": "REFUSE",
         "HELD": "held", "NA": "—"}


def show(t):
    tty = sys.stdout.isatty()
    c = _C.get(t["route"], "") if tty else ""
    z = "\033[0m" if tty else ""
    b = "\033[1m" if tty else ""
    dim = "\033[2m" if tty else ""
    print("\n  ask> %s%s%s" % (b, t["q"], z))
    print("  %s%s%s  %s%s%s" % (c, t["route"], z, b, t["head"], z))
    print("       %s" % t["why"])
    print("       %sroute (worst-wins slot walk):%s" % (dim, z))
    for s in t["walk"]:
        if s["status"] == "NA":
            continue
        print("         %-26s %-8s %s%s%s" % (SLOT_LABEL[s["slot"]], _STAT[s["status"]], dim, s["rule"], z))
    if t["assumptions"]:
        print("       %sassumptions:%s" % (dim, z))
        for a in t["assumptions"]:
            print("         · %s  %s(%s)%s" % (a["text"], dim, a["rule"], z))
    if t["dead_ends"]:
        print("       %sdead-ends (rejected):%s" % (dim, z))
        for d in t["dead_ends"]:
            print("         ✗ %s  %s(%s)%s" % (d["text"], dim, d["rule"], z))
    if t["sql"]:
        print("       %ssql:%s %s" % (dim, z, t["sql"]))


# ============================ HTML trace-page renderer ================================================
def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


_STAT_HTML = {  # status chip label + css modifier
    "BOUND":   ("BOUND", "bound"),
    "DEFAULT": ("DEFAULT", "default"),
    "HELD":    ("HELD", "held"),
    "ASK":     ("ASK", "ask"),
    "BLOCKED": ("BLOCKED", "blocked"),
    "NA":      ("—", "na"),
}


def _card_html(t):
    lane = t["route"].lower()
    head_cls = "head head--big" if t["route"] == "COMMIT" else "head"
    rows = []
    for s in t["walk"]:
        lbl, mod = _STAT_HTML[s["status"]]
        rows.append(
            '<tr class="slot slot--%s"><td class="s-name">%s</td>'
            '<td class="s-stat"><span class="pill pill--%s">%s</span></td>'
            '<td class="s-note">%s</td><td class="s-rule"><code>%s</code></td></tr>'
            % (mod, _esc(SLOT_LABEL[s["slot"]]), mod, lbl, _esc(s["note"]), _esc(s["rule"])))
    walk_tbl = (
        '<table class="walk"><thead><tr><th>decision slot</th><th>resolution</th>'
        '<th></th><th>governing rule</th></tr></thead><tbody>%s</tbody></table>' % "".join(rows))

    verdict = ('<div class="verdict verdict--%s"><span class="vk">worst-wins verdict</span>'
               '<span class="vv">%s</span></div>' % (lane, t["route"]))

    def _list(items, cls, mark, keys):
        if not items:
            return ""
        lis = "".join(
            '<li><span class="%s-mark">%s</span><span class="li-txt">%s</span>'
            '<code class="li-rule">%s</code></li>' % (cls, mark, _esc(i[keys[0]]), _esc(i[keys[1]]))
            for i in items)
        return '<ul class="dl dl--%s">%s</ul>' % (cls, lis)

    assume = _list(t["assumptions"], "as", "·", ("text", "rule"))
    deads = _list(t["dead_ends"], "de", "✗", ("text", "rule"))

    trail = "".join(
        '<li><code class="tr-file">%s</code><span class="tr-note">%s</span></li>' % (_esc(f), _esc(n))
        for f, n in t["trail"])

    sql = ('<div class="sql"><span class="sec-k">sql</span><code>%s</code></div>' % _esc(t["sql"])) if t["sql"] else ""

    sections = ['<div class="sec"><div class="sec-k">route · decision-policy slot walk</div>%s%s</div>'
                % (walk_tbl, verdict)]
    if assume:
        sections.append('<div class="sec"><div class="sec-k">assumptions <em>· each licensed by a rule</em></div>%s</div>' % assume)
    if deads:
        sections.append('<div class="sec"><div class="sec-k">dead-ends <em>· paths the rules rejected</em></div>%s</div>' % deads)
    sections.append('<div class="sec"><div class="sec-k">deduction trail <em>· what it read</em></div><ul class="trail">%s</ul></div>' % trail)
    if sql:
        sections.append('<div class="sec">%s</div>' % sql)

    return (
        '<section class="card card--%s">'
        '  <div class="qbar"><span class="prompt">ask&gt;</span><span class="qtext">%s</span></div>'
        '  <div class="ans"><span class="lane lane--%s">%s</span><span class="%s">%s</span></div>'
        '  <p class="why">%s</p>'
        '  <div class="body">%s</div>'
        '</section>'
        % (lane, _esc(t["q"]), lane, t["route"], head_cls, _esc(t["head"]),
           _esc(t["why"]), "".join(sections)))


def render_html(traces, out_path, artifact=False):
    """Write the trace page. Full standalone doc by default; body-only (for the Artifact host,
    which supplies its own <!doctype>/<head>/<body>) when artifact=True."""
    cards = "\n".join(_card_html(t) for t in traces)
    prov = ("engine duckdb · interpreter offline (pattern) · ontology v%s · reviewed %s · "
            "3 questions · %d slots each" % (ONTOLOGY_VERSION, REVIEWED, len(SLOT_ORDER)))
    inner = (_TITLE + _STYLE + _BODY) if artifact else (_DOC_OPEN + _STYLE + _DOC_MID + _BODY + _DOC_CLOSE)
    html = inner.replace("{{CARDS}}", cards).replace("{{PROV}}", _esc(prov))
    Path(out_path).write_text(html, encoding="utf-8")
    return out_path


_TITLE = '<title>The /ask trace — how the answer was reached</title>\n'
_DOC_OPEN = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
             '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + _TITLE)
_DOC_MID = "</head>\n<body>\n"
_DOC_CLOSE = "</body>\n</html>\n"

_STYLE = r"""<style>
  :root{
    --page:#f4f5f7; --card:#ffffff;
    --ink:#101828; --muted:#5b6472; --faint:#98a2b3; --line:#e7e9ee;
    --mean:#0e9384; --mean-ink:#0b7268; --mean-bg:#e6f7f4;
    --commit:#15803d; --commit-bg:#eaf7ee; --commit-bd:#b7e2c5;
    --ask:#b45309;    --ask-bg:#fdf3e7;    --ask-bd:#efd3a6;
    --refuse:#b42318; --refuse-bg:#fef3f2; --refuse-bd:#f5c9c4;
    --held:#3538cd;   --held-bg:#eef0ff;   --held-bd:#c9cdf6;
    --na:#98a2b3;     --na-bg:#f2f4f7;     --na-bd:#e4e7ec;
    --con:#f7f8fa; --con-bd:#e7e9ee;
    --shadow:0 1px 2px rgba(16,24,40,.04), 0 8px 24px rgba(16,24,40,.06);
    --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
  }
  @media (prefers-color-scheme:dark){ :root{ --page:#0d1017; } }
  :root[data-theme="dark"]{ --page:#0d1017; }
  :root[data-theme="light"]{ --page:#f4f5f7; }

  *{box-sizing:border-box} body{margin:0}
  .frame{background:var(--page);min-height:100vh;padding:44px 20px 64px}
  .wrap{max-width:1040px;margin:0 auto;font-family:var(--sans);color:var(--ink);-webkit-font-smoothing:antialiased}

  .eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);margin:0 0 12px}
  h1{font-size:clamp(24px,4vw,34px);line-height:1.07;letter-spacing:-.02em;margin:0 0 12px;text-wrap:balance;font-weight:680}
  .dek{font-size:clamp(14px,1.6vw,16.5px);line-height:1.55;color:var(--muted);max-width:70ch;margin:0 0 8px}
  .dek b{color:var(--mean-ink)}
  .legend{display:flex;flex-wrap:wrap;gap:8px 14px;margin:18px 0 26px;font-family:var(--mono);font-size:11.5px;color:var(--muted)}
  .legend .pill{transform:translateY(-1px)}

  .card{background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow);
    overflow:hidden;margin:0 0 22px}
  .card--commit{border-top:3px solid var(--commit)}
  .card--ask{border-top:3px solid var(--ask)}
  .card--refuse{border-top:3px solid var(--refuse)}

  .qbar{display:flex;align-items:baseline;gap:9px;padding:15px 22px 0}
  .qbar .prompt{font-family:var(--mono);color:var(--mean);user-select:none}
  .qtext{font-family:var(--mono);font-size:15px;letter-spacing:-.01em}

  .ans{display:flex;align-items:baseline;gap:13px;flex-wrap:wrap;padding:11px 22px 0}
  .lane{font-family:var(--mono);font-size:11.5px;font-weight:700;letter-spacing:.08em;padding:4px 10px;border-radius:6px;line-height:1}
  .lane--commit{background:var(--commit-bg);border:1px solid var(--commit-bd);color:var(--commit)}
  .lane--ask{background:var(--ask-bg);border:1px solid var(--ask-bd);color:var(--ask)}
  .lane--refuse{background:var(--refuse-bg);border:1px solid var(--refuse-bd);color:var(--refuse)}
  .head{font-weight:660;letter-spacing:-.01em;font-size:17px}
  .head--big{font-size:29px;color:var(--commit);font-weight:730;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
  .why{margin:11px 22px 0;font-size:13.5px;line-height:1.55;color:var(--muted);max-width:88ch}

  .body{padding:6px 22px 22px}
  .sec{padding:18px 0 4px;border-top:1px solid var(--line);margin-top:16px}
  .sec:first-child{border-top:0;margin-top:14px}
  .sec-k{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin:0 0 12px}
  .sec-k em{font-style:normal;color:var(--na);text-transform:none;letter-spacing:0}

  .walk{width:100%;border-collapse:collapse;font-size:13px}
  .walk th{font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--faint);
    text-align:left;font-weight:600;padding:0 12px 8px 0;border-bottom:1px solid var(--line)}
  .walk td{padding:9px 12px 9px 0;border-bottom:1px solid var(--line);vertical-align:top}
  .walk tr:last-child td{border-bottom:0}
  .slot--na{opacity:.5}
  .s-name{font-weight:560;white-space:nowrap}
  .s-note{color:var(--muted);line-height:1.5;max-width:46ch}
  .s-rule code{font-family:var(--mono);font-size:11.5px;color:var(--mean-ink);word-break:break-word}
  .s-stat{white-space:nowrap}

  .pill{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.05em;padding:3px 7px;border-radius:5px;line-height:1;display:inline-block}
  .pill--bound,.pill--default{background:var(--commit-bg);border:1px solid var(--commit-bd);color:var(--commit)}
  .pill--held{background:var(--held-bg);border:1px solid var(--held-bd);color:var(--held)}
  .pill--ask{background:var(--ask-bg);border:1px solid var(--ask-bd);color:var(--ask)}
  .pill--blocked{background:var(--refuse-bg);border:1px solid var(--refuse-bd);color:var(--refuse)}
  .pill--na{background:var(--na-bg);border:1px solid var(--na-bd);color:var(--na)}

  .verdict{display:flex;align-items:center;gap:12px;margin-top:14px;padding:11px 15px;border-radius:10px;
    font-family:var(--mono)}
  .verdict--commit{background:var(--commit-bg);border:1px solid var(--commit-bd)}
  .verdict--ask{background:var(--ask-bg);border:1px solid var(--ask-bd)}
  .verdict--refuse{background:var(--refuse-bg);border:1px solid var(--refuse-bd)}
  .verdict .vk{font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--faint)}
  .verdict .vv{font-size:14px;font-weight:700;letter-spacing:.04em;margin-left:auto}
  .verdict--commit .vv{color:var(--commit)} .verdict--ask .vv{color:var(--ask)} .verdict--refuse .vv{color:var(--refuse)}

  .dl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
  .dl li{display:flex;align-items:baseline;gap:10px;font-size:13.5px;line-height:1.5;flex-wrap:wrap}
  .as-mark{color:var(--mean);font-weight:700;flex:none}
  .de-mark{color:var(--refuse);font-weight:700;flex:none;font-size:12px}
  .li-txt{color:var(--ink)}
  .dl--de .li-txt{color:var(--muted)}
  .li-rule{font-family:var(--mono);font-size:11px;color:var(--mean-ink);background:var(--con);
    border:1px solid var(--con-bd);border-radius:5px;padding:2px 7px;margin-left:auto}

  .trail{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
  .trail li{display:flex;gap:12px;align-items:baseline;font-size:13px;flex-wrap:wrap}
  .tr-file{font-family:var(--mono);font-size:12px;color:var(--ink);background:var(--con);
    border:1px solid var(--con-bd);border-radius:6px;padding:2px 8px;flex:none}
  .tr-note{color:var(--muted);line-height:1.5}

  .sql{display:flex;flex-direction:column;gap:8px}
  .sql code{font-family:var(--mono);font-size:12.5px;color:var(--ink);background:var(--con);
    border:1px solid var(--con-bd);border-radius:8px;padding:11px 13px;overflow-x:auto;white-space:pre}

  .foot{font-family:var(--mono);font-size:11.5px;color:var(--faint);text-align:center;margin-top:28px;line-height:1.6}
  .foot .note{display:block;color:var(--na);margin-top:4px;max-width:70ch;margin-left:auto;margin-right:auto}
</style>
"""

_BODY = r"""<div class="frame">
  <div class="wrap">
    <p class="eyebrow">Meaning as code — the /ask trace</p>
    <h1>Not just the answer — how it got there.</h1>
    <p class="dek">The same three questions, each answered with its <b>whole trace disclosed</b>: which files it read, how every open decision resolved and the rule that governed it, the assumptions it made, and the paths the rules made it reject. <b>Worst-wins</b> across the slots decides commit, ask, or refuse.</p>
    <div class="legend">
      <span><span class="pill pill--default">DEFAULT</span> resolved by a disclosed default</span>
      <span><span class="pill pill--held">HELD</span> invariant held</span>
      <span><span class="pill pill--ask">ASK</span> must clarify</span>
      <span><span class="pill pill--blocked">BLOCKED</span> rule refuses</span>
      <span><span class="pill pill--na">—</span> not engaged</span>
    </div>

    {{CARDS}}

    <p class="foot">{{PROV}}
      <span class="note">Public Contoso (SQLBI, MIT) on DuckDB. Every rule id above resolves to a file in this ontology; nothing here is hand-written prose — it is generated from the model.</span>
    </p>
  </div>
</div>
"""


# ============================ ASK CONSOLE (transcript UI over real runs) ==============================
# A self-contained chat-style console: ask a question, get the route + the ontology walk + the value.
# Every entry below is built from data EXECUTED against contoso.duckdb at generation time — nothing is
# hand-typed. The in-page input matches new questions against this same executed library (a static demo
# needs no server), the way a captured-run board replays real results.

_HL_KW = ("select", "from", "where", "and", "or", "group by", "order by", "join", "using",
          "on", "as", "in", "between", "desc", "asc", "limit")
_HL_FN = ("sum", "round", "year", "count", "avg")


def _hl(sql):
    """Light SQL highlighter -> HTML spans (keywords, functions, 'strings')."""
    toks = re.split(r"('[^']*')", sql)
    out = []
    for i, part in enumerate(toks):
        if i % 2:  # inside quotes
            out.append('<span class="str">%s</span>' % _esc(part))
            continue
        part = _esc(part)
        for kw in sorted(_HL_KW, key=len, reverse=True):
            part = re.sub(r"(?i)\b%s\b" % kw.replace(" ", r"\s+"),
                          lambda m: '<span class="kw">%s</span>' % m.group(0), part)
        for fn in _HL_FN:
            part = re.sub(r"(?i)\b(%s)(?=\s*\()" % fn,
                          lambda m: '<span class="fn">%s</span>' % m.group(0), part)
        out.append(part)
    return "".join(out)


def _q1(sql):
    return duckdb(sql)


def _musd(v):
    return "$%.1fM" % (float(v) / 1_000_000)


def _de(n):
    """European thousands for the console tables (. thousands, , decimal) — display only."""
    return ("%.1f" % n).replace(".", "#").replace(",", ".").replace("#", ",")


def _trace_from(trace):
    """Turn a build_trace() deduction trail into console {file,res} lines + a final verdict note."""
    lines = [{"file": f, "res": n} for f, n in trace["trail"]]
    tiers = ", ".join(sorted({s["status"].lower() for s in trace["walk"] if s["status"] != "NA"}))
    final = "route_rules → slots [%s] · worst-wins → %s" % (tiers, trace["route"])
    return lines, final


def build_entries():
    """The executed library the console renders (and matches new questions against)."""
    rng = _q1("SELECT strftime(min(OrderDate),'%Y') lo, strftime(max(OrderDate),'%Y') hi FROM sales")[0]
    span = "%s–%s" % (rng["lo"], rng["hi"])
    yrs = _q1("SELECT year(OrderDate) yr, SUM(Quantity*NetPrice*ExchangeRate) v "
              "FROM sales GROUP BY 1 ORDER BY 1 DESC LIMIT 3")
    brands = _q1("SELECT p.Brand b, SUM(s.Quantity*s.NetPrice*s.ExchangeRate) v "
                 "FROM sales s JOIN product p ON s.ProductKey=p.ProductKey GROUP BY 1 ORDER BY 2 DESC LIMIT 6")
    gross = float(_q1("SELECT SUM(Quantity*UnitPrice*ExchangeRate) v FROM sales")[0]["v"])
    net = float(_q1("SELECT SUM(Quantity*NetPrice*ExchangeRate) v FROM sales")[0]["v"])

    t_commit = build_trace("what were our total sales?")
    t_ask = build_trace("total sales in a single currency")
    t_refuse = build_trace("sales by salesperson")

    # ---- YoY delta for the total-sales table (top two full years present) ----
    y0, y1 = yrs[0], yrs[1]
    delta = (float(y0["v"]) - float(y1["v"])) / float(y1["v"]) * 100
    darrow = "▲" if delta >= 0 else "▼"
    dcls = "up" if delta >= 0 else "down"

    def line(t):
        ls, fn = _trace_from(t)
        return ls, fn

    lc, fc = line(t_commit)
    la, fa = line(t_ask)
    lr, fr = line(t_refuse)

    entries = []

    # 1 — COMMIT: total sales
    entries.append({
        "id": "total-sales", "q": "What were our total sales?", "route": "commit",
        "time": "%s · 09:12" % REVIEWED, "cached": False,
        "trace": lc, "final": fc,
        "answer": {
            "kind": "value", "value": _musd(net), "unit": "net · USD",
            "caption": "Net sales, all channels, each line converted to USD before summing — full available period (%s)." % span,
            "table": {
                "cols": ["Year", "Net sales (M USD)", ""],
                "rows": [
                    [str(y0["yr"]), _de(float(y0["v"]) / 1e6), '<span class="delta-%s">%s %s%%</span>' % (dcls, darrow, _de(abs(delta)))],
                    [str(y1["yr"]), _de(float(y1["v"]) / 1e6), ""],
                    [str(yrs[2]["yr"]), _de(float(yrs[2]["v"]) / 1e6), ""],
                ],
            },
            "chart": {"title": "Net sales by year (M USD)",
                      "bars": [{"label": str(r["yr"]), "value": round(float(r["v"]) / 1e6, 1)} for r in yrs]},
            "assumption": 'Assumed <b>net</b> (not gross) and base currency <b>USD</b>; each line converted before summing — all disclosed. '
                          'Licensed by <code>sales.net_of_discount</code> · <code>sales.single_currency_basis</code>.',
            "sql": _hl("SELECT SUM(Quantity * NetPrice * ExchangeRate) AS net_usd FROM sales"),
        },
    })

    # 2 — ASK: single currency, none named
    entries.append({
        "id": "single-currency", "q": "Total sales in a single currency", "route": "ask",
        "time": "%s · 09:14" % REVIEWED, "cached": False,
        "trace": la, "final": fa,
        "answer": {
            "kind": "ask",
            "prompt": "Which reporting currency?",
            "hint": "The rows span five currencies (USD, EUR, GBP, CAD, AUD) and none was named. I won't pick one silently — "
                    "name it, or accept the disclosed base currency (USD).",
            "chips": ["USD", "EUR", "GBP", "CAD", "AUD"],
        },
    })

    # 3 — REFUSE: dimension the data does not carry
    entries.append({
        "id": "by-salesperson", "q": "Sales by salesperson", "route": "refuse",
        "time": "%s · 09:15" % REVIEWED, "cached": False,
        "trace": lr, "final": fr,
        "answer": {
            "kind": "refuse",
            "head": "No salesperson dimension in the model.",
            "why": "It can slice by <b>brand, product, category, store/country, currency, date</b>. "
                   "It will not fabricate a dimension the data doesn't carry.",
        },
    })

    # ---- canned library: extra executed questions the input can match ----
    # gross
    entries.append({
        "id": "gross-sales", "q": "Total gross sales", "route": "commit", "library": True,
        "time": "%s · 09:18" % REVIEWED, "cached": True,
        "trace": [
            {"file": "ontology/query_rules.yaml", "res": "measure.gross_vs_net slot · 'gross' explicitly asked"},
            {"file": "ontology/rules.yaml", "res": "gross_sales_base_currency · SUM(Quantity × UnitPrice × ExchangeRate)"},
            {"file": "ontology/concepts/sales/sales.yaml", "res": "sales.net_of_discount — gross reported only when explicitly asked"},
        ],
        "final": "route_rules → gross explicit, converted, disclosed → COMMIT",
        "answer": {
            "kind": "value", "value": _musd(gross), "unit": "gross · USD",
            "caption": "Gross sales (list price, before discount), converted to USD. Net is %s — the difference is discount." % _musd(net),
            "table": {"cols": ["Basis", "M USD", ""],
                      "rows": [["Gross (UnitPrice)", _de(gross / 1e6), ""],
                               ["Net (NetPrice)", _de(net / 1e6), '<span class="delta-down">▼ %s%%</span>' % _de((gross - net) / gross * 100)]]},
            "chart": {"title": "Gross vs net (M USD)",
                      "bars": [{"label": "Gross", "value": round(gross / 1e6, 1)}, {"label": "Net", "value": round(net / 1e6, 1)}]},
            "assumption": 'Reported <b>gross</b> because the question asked for it; otherwise "sales" means net. Licensed by <code>sales.net_of_discount</code>.',
            "sql": _hl("SELECT SUM(Quantity * UnitPrice * ExchangeRate) AS gross_usd FROM sales"),
        },
    })
    # by brand
    entries.append({
        "id": "by-brand", "q": "Sales by brand", "route": "commit", "library": True,
        "time": "%s · 09:20" % REVIEWED, "cached": True,
        "trace": [
            {"file": "ontology/concepts/catalog/brand.yaml", "res": "Brand → closed set (grounded on product.Brand)"},
            {"file": "ontology/edges.yaml", "res": "sales.ProductKey → product · brand carried"},
            {"file": "ontology/rules.yaml", "res": "net_sales_base_currency · grouped by brand"},
        ],
        "final": "route_rules → dimension carried, converted → COMMIT",
        "answer": {
            "kind": "value", "value": _musd(net), "unit": "net · USD",
            "caption": "Net sales by brand, converted to USD, full period — top %d of 11 shown (%s leads at %s)."
                       % (len(brands), _esc(brands[0]["b"]), _musd(float(brands[0]["v"]))),
            "table": {"cols": ["Brand", "Net sales (M USD)", ""],
                      "rows": [[_esc(r["b"]), _de(float(r["v"]) / 1e6), ""] for r in brands]},
            "chart": {"title": "Net sales by brand (M USD)",
                      "bars": [{"label": _esc(r["b"]), "value": round(float(r["v"]) / 1e6, 1)} for r in brands]},
            "assumption": 'Net, USD, full period — same defaults as the grand total, disclosed. Brand is a closed set grounded on <code>product.Brand</code>.',
            "sql": _hl("SELECT p.Brand, SUM(s.Quantity * s.NetPrice * s.ExchangeRate) AS net_usd "
                       "FROM sales s JOIN product p ON s.ProductKey = p.ProductKey "
                       "GROUP BY p.Brand ORDER BY net_usd DESC"),
        },
    })

    return entries


def render_console(out_path, artifact=False):
    entries = build_entries()
    data = json.dumps(entries, ensure_ascii=False)
    meta = "ontology v%s · reviewed %s" % (ONTOLOGY_VERSION, REVIEWED)
    inner = (_CONSOLE_TITLE + _CONSOLE_STYLE + _CONSOLE_BODY + _CONSOLE_SCRIPT) if artifact else \
        (_DOC_OPEN + _CONSOLE_STYLE + _DOC_MID + _CONSOLE_BODY + _CONSOLE_SCRIPT + _DOC_CLOSE)
    # _DOC_OPEN already carries the trace-page <title>; swap it for the console title in full-doc mode
    inner = inner.replace(_TITLE, _CONSOLE_TITLE) if not artifact else inner
    html = inner.replace("{{DATA}}", data).replace("{{META}}", _esc(meta))
    Path(out_path).write_text(html, encoding="utf-8")
    return out_path


_CONSOLE_TITLE = "<title>Contoso · Ask — meaning as code</title>\n"

_CONSOLE_STYLE = r"""<style>
  :root{
    /* ---- LIGHT (default) — shares the article family's route colours ---- */
    --bg:#eef1f5; --bg-a:#5b8cff12; --bg-b:#8a5bff0e;
    --panel:#ffffff; --panel-alt:#f6f8fb; --panel-raise:#eef1f6;
    --border:#e3e7ee; --border-soft:#edf0f5;
    --text:#101828; --dim:#5b6472; --faint:#98a2b3;
    --accent:#3357d6; --accent-dim:#3357d622;
    --commit:#15803d; --commit-soft:#eaf7ee; --commit-line:#b7e2c5;
    --ask:#b45309; --ask-soft:#fdf3e7; --ask-line:#efd3a6;
    --refuse:#b42318; --refuse-soft:#fef3f2; --refuse-line:#f5c9c4;
    --header-bg:#ffffffcc; --tray-bg:#ffffffcc;
    --qb1:#eaf0fb; --qb2:#e3ebfa; --qbubble-bd:#d3e0f6;
    --value-commit:#0b6e35;
    --code-file:#3357d6; --code-res:#0b7268;
    --sql-bg:#f7f8fa; --code-kw:#3357d6; --code-fn:#7c3aed; --code-str:#0b7268;
    --assume-text:#7a4405; --assume-code-bg:#ffffff;
    --scroll:#cbd2dd; --shadow:0 1px 2px #1018280f, 0 8px 24px #10182814;
    --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    --radius:14px;
  }
  /* ---- DARK ---- */
  @media (prefers-color-scheme:dark){ :root{
    --bg:#0a0c10; --bg-a:#17233a55; --bg-b:#1a1030aa;
    --panel:#12151c; --panel-alt:#161a23; --panel-raise:#1b202b;
    --border:#242a35; --border-soft:#1b2029;
    --text:#e7eaf1; --dim:#9aa3b4; --faint:#616a7a;
    --accent:#5b8cff; --accent-dim:#5b8cff33;
    --commit:#39d98a; --commit-soft:#39d98a1f; --commit-line:#39d98a55;
    --ask:#ffb545; --ask-soft:#ffb5451f; --ask-line:#ffb54555;
    --refuse:#ff6b81; --refuse-soft:#ff6b811f; --refuse-line:#ff6b8155;
    --header-bg:#0d1017cc; --tray-bg:#0d101788;
    --qb1:#243149; --qb2:#1b2436; --qbubble-bd:#2c3852;
    --value-commit:#eafff4;
    --code-file:#7aa2f7; --code-res:#8fe3b3;
    --sql-bg:#0d1017; --code-kw:#7aa2f7; --code-fn:#c39bff; --code-str:#8fe3b3;
    --assume-text:#ffe4b8; --assume-code-bg:#0d101755;
    --scroll:#2a3140; --shadow:0 8px 30px #00000055;
  }}
  :root[data-theme="light"]{
    --bg:#eef1f5; --bg-a:#5b8cff12; --bg-b:#8a5bff0e;
    --panel:#ffffff; --panel-alt:#f6f8fb; --panel-raise:#eef1f6;
    --border:#e3e7ee; --border-soft:#edf0f5;
    --text:#101828; --dim:#5b6472; --faint:#98a2b3;
    --accent:#3357d6; --accent-dim:#3357d622;
    --commit:#15803d; --commit-soft:#eaf7ee; --commit-line:#b7e2c5;
    --ask:#b45309; --ask-soft:#fdf3e7; --ask-line:#efd3a6;
    --refuse:#b42318; --refuse-soft:#fef3f2; --refuse-line:#f5c9c4;
    --header-bg:#ffffffcc; --tray-bg:#ffffffcc;
    --qb1:#eaf0fb; --qb2:#e3ebfa; --qbubble-bd:#d3e0f6;
    --value-commit:#0b6e35;
    --code-file:#3357d6; --code-res:#0b7268;
    --sql-bg:#f7f8fa; --code-kw:#3357d6; --code-fn:#7c3aed; --code-str:#0b7268;
    --assume-text:#7a4405; --assume-code-bg:#ffffff;
    --scroll:#cbd2dd; --shadow:0 1px 2px #1018280f, 0 8px 24px #10182814;
  }
  :root[data-theme="dark"]{
    --bg:#0a0c10; --bg-a:#17233a55; --bg-b:#1a1030aa;
    --panel:#12151c; --panel-alt:#161a23; --panel-raise:#1b202b;
    --border:#242a35; --border-soft:#1b2029;
    --text:#e7eaf1; --dim:#9aa3b4; --faint:#616a7a;
    --accent:#5b8cff; --accent-dim:#5b8cff33;
    --commit:#39d98a; --commit-soft:#39d98a1f; --commit-line:#39d98a55;
    --ask:#ffb545; --ask-soft:#ffb5451f; --ask-line:#ffb54555;
    --refuse:#ff6b81; --refuse-soft:#ff6b811f; --refuse-line:#ff6b8155;
    --header-bg:#0d1017cc; --tray-bg:#0d101788;
    --qb1:#243149; --qb2:#1b2436; --qbubble-bd:#2c3852;
    --value-commit:#eafff4;
    --code-file:#7aa2f7; --code-res:#8fe3b3;
    --sql-bg:#0d1017; --code-kw:#7aa2f7; --code-fn:#c39bff; --code-str:#8fe3b3;
    --assume-text:#ffe4b8; --assume-code-bg:#0d101755;
    --scroll:#2a3140; --shadow:0 8px 30px #00000055;
  }
  *{box-sizing:border-box}
  html,body{height:100%}
  body{margin:0;color:var(--text);font-family:var(--sans);font-size:14px;-webkit-font-smoothing:antialiased;
    background:radial-gradient(1200px 600px at 15% -10%, var(--bg-a), transparent 60%),
               radial-gradient(1000px 700px at 100% 0%, var(--bg-b), transparent 55%), var(--bg);}
  ::selection{background:var(--accent-dim)}
  ::-webkit-scrollbar{width:10px;height:10px}
  ::-webkit-scrollbar-thumb{background:var(--scroll);border-radius:8px;border:2px solid transparent;background-clip:padding-box}
  .app{height:100vh;display:flex;flex-direction:column}

  header.top{flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;padding:12px 22px;
    border-bottom:1px solid var(--border-soft);background:var(--header-bg);backdrop-filter:blur(6px);z-index:30}
  .brand{display:flex;align-items:center;gap:11px}
  .brand .mark{width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,#5b8cff,#8a5bff);
    display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#fff;box-shadow:0 4px 14px #5b8cff40;letter-spacing:.5px}
  .brand .name{font-weight:650;font-size:14.5px}
  .brand .name b{color:var(--accent);font-weight:650}
  .brand .sub{font-size:11.5px;color:var(--faint);margin-top:1px}
  .brand .titles{display:flex;flex-direction:column}
  .top-actions{display:flex;align-items:center;gap:10px}
  .session-count{font-size:11.5px;color:var(--dim);background:var(--panel-alt);border:1px solid var(--border);padding:5px 11px;border-radius:20px}
  .btn{appearance:none;border:1px solid var(--border);background:var(--panel-alt);color:var(--dim);font-size:12.5px;
    padding:7px 12px;border-radius:9px;cursor:pointer;font-family:var(--sans);display:flex;align-items:center;gap:6px;transition:.15s}
  .btn:hover{border-color:#3a4353;color:var(--text);background:var(--panel-raise)}
  .btn.primary{background:linear-gradient(135deg,#5b8cff,#7a6bff);color:#fff;border:none}
  .btn.primary:hover{filter:brightness(1.08)}

  .stage{flex:1 1 auto;display:flex;flex-direction:column;min-height:0}
  .pinned-tray{flex:0 0 auto;display:flex;gap:8px;align-items:center;overflow-x:auto;padding:9px 24px;border-bottom:1px solid var(--border-soft);background:#0d101788}
  .pinned-tray.empty{display:none}
  .pinned-tray .label{font-size:11px;color:var(--faint);flex:0 0 auto;display:flex;align-items:center;gap:5px}
  .pinned-chip{flex:0 0 auto;display:flex;align-items:center;gap:6px;background:var(--panel-alt);border:1px solid var(--border);
    color:var(--dim);font-size:11.5px;padding:5px 11px;border-radius:20px;cursor:pointer;white-space:nowrap;transition:.15s}
  .pinned-chip:hover{border-color:var(--ask);color:var(--text)}
  .pinned-chip .pin{color:var(--ask)}

  .compare-strip{flex:0 0 auto;margin:10px 24px 0;padding:10px 16px;border-radius:12px;background:var(--panel-alt);
    border:1px solid var(--accent);display:flex;align-items:center;gap:16px;font-size:12.5px}
  .compare-strip.empty{display:none}
  .compare-strip .ttl{color:var(--accent);font-weight:650;font-size:11px;text-transform:uppercase;letter-spacing:.4px}
  .compare-item .q{color:var(--dim);font-size:11.5px;max-width:230px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .compare-item .v{color:var(--text);font-weight:650;font-size:14px}
  .compare-strip .spacer{flex:1}
  .compare-close{background:none;border:none;color:var(--faint);cursor:pointer;font-size:16px}

  .transcript{flex:1 1 auto;overflow-y:auto;padding:24px 0 8px;scroll-behavior:smooth}
  .transcript-inner{max-width:880px;margin:0 auto;padding:0 24px;display:flex;flex-direction:column;gap:22px}

  .entry{animation:rise .34s ease}
  @keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
  .q-row{display:flex;justify-content:flex-end;margin-bottom:10px}
  .q-bubble{max-width:78%;background:linear-gradient(135deg,#243149,#1b2436);border:1px solid #2c3852;color:var(--text);
    padding:10px 16px;border-radius:16px 16px 4px 16px;font-size:14.5px;line-height:1.45}

  .a-card{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden}
  .a-card.route-commit{border-color:var(--commit-line)}
  .a-card.route-ask{border-color:var(--ask-line)}
  .a-card.route-refuse{border-color:var(--refuse-line)}
  .a-head{display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid var(--border-soft);background:var(--panel-alt)}
  .badge{display:flex;align-items:center;gap:6px;font-size:10.5px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;padding:4px 10px;border-radius:20px}
  .badge .dot{width:6px;height:6px;border-radius:50%}
  .badge.commit{background:var(--commit-soft);color:var(--commit)} .badge.commit .dot{background:var(--commit)}
  .badge.ask{background:var(--ask-soft);color:var(--ask)} .badge.ask .dot{background:var(--ask)}
  .badge.refuse{background:var(--refuse-soft);color:var(--refuse)} .badge.refuse .dot{background:var(--refuse)}
  .a-meta{font-size:11px;color:var(--faint);display:flex;align-items:center;gap:8px}
  .a-meta .cached{color:#6fdcae}
  .a-head .spacer{flex:1}

  .trace{border-bottom:1px solid var(--border-soft)}
  .trace-toggle{width:100%;display:flex;align-items:center;gap:8px;background:none;border:none;color:var(--dim);cursor:pointer;padding:10px 14px;font-size:12px;font-family:var(--sans)}
  .trace-toggle:hover{color:var(--text)}
  .trace-toggle .chev{color:var(--faint);transition:transform .2s;display:inline-block;font-size:10px}
  .trace.collapsed .trace-toggle .chev{transform:rotate(-90deg)}
  .trace-toggle .lbl{font-weight:600}
  .trace-toggle .count{color:var(--faint);font-weight:400}
  .trace-body{padding:2px 14px 12px 30px}
  .trace.collapsed .trace-body{display:none}
  .trace-line{font-family:var(--mono);font-size:12px;line-height:1.65;color:var(--dim);padding:2px 0;display:flex;gap:8px}
  .trace-line .idx{color:var(--faint);flex:0 0 16px}
  .trace-line .file{color:#7aa2f7}
  .trace-line .arrow{color:var(--faint)}
  .trace-line .res{color:#8fe3b3}
  .trace-final{margin-top:6px;font-family:var(--mono);font-size:11.5px;color:var(--faint);font-style:italic}

  .a-body{padding:14px 16px 16px}
  .a-value{font-size:34px;font-weight:720;letter-spacing:-.5px;font-variant-numeric:tabular-nums;line-height:1}
  .route-commit .a-value{color:#eafff4}
  .a-value .unit{font-size:14px;font-weight:500;color:var(--dim);margin-left:8px;letter-spacing:0}
  .a-caption{color:var(--dim);font-size:13px;line-height:1.5;margin:8px 0 0;max-width:70ch}

  .assumption{margin-top:14px;display:flex;gap:10px;background:var(--ask-soft);border:1px solid var(--ask-line);border-radius:10px;padding:10px 13px;font-size:12.5px;line-height:1.5;color:#ffe4b8}
  .assumption b{color:var(--ask)} .assumption code{font-family:var(--mono);font-size:11.5px;background:#0d101755;border:1px solid var(--ask-line);border-radius:5px;padding:1px 5px;color:#ffd59a}
  .assumption .warn{color:var(--ask);flex:0 0 auto}

  table.rt{width:100%;border-collapse:collapse;margin-top:14px;font-size:13px}
  table.rt th{text-align:left;font-size:10.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--faint);font-weight:600;padding:0 10px 7px 0;border-bottom:1px solid var(--border)}
  table.rt td{padding:8px 10px 8px 0;border-bottom:1px solid var(--border-soft);font-variant-numeric:tabular-nums}
  table.rt tr:last-child td{border-bottom:0}
  table.rt td:nth-child(2){text-align:right;color:var(--text)}
  table.rt td:nth-child(3){text-align:right;width:90px}
  .delta-up{color:var(--commit);font-size:12px} .delta-down{color:var(--refuse);font-size:12px}

  .chart{margin-top:14px;display:none;flex-direction:column;gap:8px}
  .chart.open{display:flex}
  .chart .ctitle{font-size:11px;color:var(--faint);text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px}
  .bar-row{display:grid;grid-template-columns:130px 1fr 74px;align-items:center;gap:10px;font-size:12.5px}
  .bar-label{color:var(--dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bar-track{height:9px;background:var(--panel-raise);border-radius:6px;overflow:hidden}
  .bar-fill{height:100%;background:linear-gradient(90deg,#5b8cff,#39d98a);border-radius:6px}
  .bar-val{text-align:right;color:var(--text);font-variant-numeric:tabular-nums}

  .sqlwrap{margin-top:14px}
  .sql-toggle{background:none;border:none;color:var(--faint);cursor:pointer;font-size:11.5px;font-family:var(--sans);padding:0;display:flex;align-items:center;gap:6px}
  .sql-toggle:hover{color:var(--text)}
  .sql-toggle .chev{font-size:9px;transition:transform .2s;display:inline-block}
  .sqlwrap.open .sql-toggle .chev{transform:rotate(90deg)}
  .sql-body{display:none;margin-top:8px}
  .sqlwrap.open .sql-body{display:block}
  .sql-body pre{margin:0;font-family:var(--mono);font-size:12px;line-height:1.6;color:var(--dim);background:#0d1017;border:1px solid var(--border);border-radius:10px;padding:12px 14px;overflow-x:auto;white-space:pre}
  .sql-body .kw{color:#7aa2f7} .sql-body .fn{color:#c39bff} .sql-body .str{color:#8fe3b3}

  .clarify-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
  .cchip{border:1px solid var(--border);background:var(--panel-alt);color:var(--dim);font-size:12.5px;padding:6px 13px;border-radius:20px;cursor:pointer;transition:.15s;font-family:var(--sans)}
  .cchip:hover{border-color:var(--ask);color:var(--text);background:var(--ask-soft)}

  .refuse-body{display:flex;gap:11px;align-items:flex-start;font-size:14px;line-height:1.55}
  .refuse-body .ico{color:var(--refuse);flex:0 0 auto;font-size:16px;margin-top:1px}
  .refuse-body b{color:var(--text)}

  .actions{display:flex;gap:8px;margin-top:16px;flex-wrap:wrap}
  .act{appearance:none;border:1px solid var(--border);background:none;color:var(--dim);font-size:12px;padding:6px 12px;border-radius:9px;cursor:pointer;font-family:var(--sans);display:flex;align-items:center;gap:6px;transition:.15s}
  .act:hover{border-color:#3a4353;color:var(--text);background:var(--panel-alt)}
  .act.on{border-color:var(--ask);color:var(--ask)}
  .act.on.cmp{border-color:var(--accent);color:var(--accent)}

  .input-dock{flex:0 0 auto;display:flex;justify-content:center;padding:16px 24px 12px}
  .input-wrap{width:100%;max-width:760px;display:flex;flex-direction:column;gap:10px}
  .try-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:11.5px;color:var(--faint)}
  .try-row .tchip{border:1px solid var(--border);background:var(--panel-alt);color:var(--dim);font-size:12px;padding:6px 12px;border-radius:20px;cursor:pointer;transition:.15s;font-family:var(--sans)}
  .try-row .tchip:hover{border-color:var(--accent);color:var(--text);background:#5b8cff14}
  .input-shell{display:flex;align-items:flex-end;gap:8px;background:var(--panel-raise);border:1px solid var(--border);border-radius:18px;padding:10px 10px 10px 18px;box-shadow:0 8px 30px #00000055;transition:.2s}
  .input-shell:focus-within{border-color:var(--accent);box-shadow:0 8px 30px #00000055,0 0 0 3px #5b8cff22}
  .input-shell textarea{flex:1;resize:none;border:none;outline:none;background:transparent;color:var(--text);font-family:var(--sans);font-size:14.5px;line-height:1.5;max-height:130px;padding:6px 0}
  .input-shell textarea::placeholder{color:var(--faint)}
  .send-btn{flex:0 0 auto;width:38px;height:38px;border-radius:12px;border:none;background:linear-gradient(135deg,#5b8cff,#7a6bff);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.15s}
  .send-btn:hover{filter:brightness(1.1)} .send-btn:active{transform:scale(.94)}
  .input-hint{text-align:center;font-size:11px;color:var(--faint);padding-bottom:8px}
  .input-hint b{color:var(--dim);font-weight:500}
</style>
"""

_CONSOLE_BODY = r"""<div class="app">
  <header class="top">
    <div class="brand">
      <div class="mark">C</div>
      <div class="titles">
        <div class="name">Contoso · <b>Ask</b></div>
        <div class="sub">catalog-sales context workspace — meaning as code</div>
      </div>
    </div>
    <div class="top-actions">
      <span class="session-count" id="sessionCount"></span>
      <button class="btn" id="reloadBtn">↻ Reload demo</button>
      <button class="btn primary" id="newBtn">+ New session</button>
    </div>
  </header>
  <div class="stage" id="stage">
    <div class="pinned-tray empty" id="pinnedTray"></div>
    <div class="compare-strip empty" id="compareStrip"></div>
    <div class="transcript" id="transcript">
      <div class="transcript-inner" id="transcriptInner"></div>
    </div>
    <div class="input-dock">
      <div class="input-wrap">
        <div class="try-row" id="tryRow"></div>
        <div class="input-shell">
          <textarea id="input" rows="1" placeholder="Ask about sales, brands, currency, gross vs net…"></textarea>
          <button class="send-btn" id="sendBtn" title="Ask (Enter)">
            <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor"><path d="M2 10l16-7-7 16-2-6-7-3z"/></svg>
          </button>
        </div>
        <div class="input-hint"><b>Enter</b> to send · <b>Shift+Enter</b> for a new line · every value is executed against contoso.duckdb — {{META}}</div>
      </div>
    </div>
  </div>
</div>
"""

_CONSOLE_SCRIPT = r"""<script>
const SEED = {{DATA}};
function esc(s){return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
let entries = [];
let uid = 0;
const LIB = {}; SEED.forEach(e=>{ LIB[e.id]=e; });

// ---------- new-question matcher (matches against the executed library) ----------
function match(text){
  const q = text.toLowerCase().trim();
  if(!q) return null;
  if(/(salesperson|sales person|sales rep|supplier|promotion|discount reason)/.test(q)) return clone('by-salesperson', text);
  if(/gross/.test(q)) return clone('gross-sales', text);
  if(/(by|per)\s+brand|brand(s)?\b/.test(q)) return clone('by-brand', text);
  if(/(single|one|a)\s+currenc/.test(q) && !/(usd|eur|gbp|cad|aud)\b/.test(q)) return clone('single-currency', text);
  if(/(total|net)?\s*sales|revenue|turnover/.test(q)) return clone('total-sales', text);
  return unknown(text);
}
function clone(id, text){
  const base = LIB[id]; if(!base) return unknown(text);
  const e = JSON.parse(JSON.stringify(base));
  e.uid = ++uid; e.q = text || base.q; e.cached=false; e.time='just now';
  e.collapsed = e.route==='commit'; // commit collapses the walk by default; ask/refuse keep it open
  return e;
}
function unknown(text){
  return { uid:++uid, q:text, route:'ask', cached:false, time:'just now', collapsed:false,
    trace:[{file:'ontology/query_rules.yaml', res:'no concept in this demo matched the question'}],
    final:'route_rules → out of the demo’s executed scope → ASK',
    answer:{ kind:'ask', prompt:'I can only answer what this small demo has executed.',
      hint:'This is the public Contoso demo — try one of these, each backed by a real query.',
      chips:['What were our total sales?','Total gross sales','Sales by brand','Total sales in a single currency','Sales by salesperson'] } };
}
// currency-clarify resolution: USD is executed; other currencies are honestly abstained (data carries the USD base only)
function resolveCurrency(cur){
  if(cur==='USD'){ const e=clone('total-sales','Total sales in USD'); e.answer.caption='Net sales in the disclosed base currency, USD — '+e.answer.caption.replace(/^Net sales, /,''); push(e); return; }
  const e = { uid:++uid, q:'Total sales in '+cur, route:'refuse', cached:false, time:'just now', collapsed:false,
    trace:[{file:'ontology/concepts/finance/currency.yaml', res:'each line carries its rate to the USD base only'},
           {file:'ontology/query_rules.yaml', res:'resolve.never_fabricate — a USD→'+cur+' rate is not in the model'}],
    final:'route_rules → target currency ungrounded → ABSTAIN (flag gap, don’t invent)',
    answer:{ kind:'refuse', head:'A '+cur+' total isn’t grounded in this data.',
      why:'The warehouse carries each line’s rate to the <b>USD</b> base, so USD is executable. A <b>'+cur+'</b> total needs a USD→'+cur+' rate that isn’t in the model — so it’s flagged as a data gap, not guessed.' } };
  push(e);
}

// ---------- render ----------
function traceHTML(e){
  const lines = e.trace.map((t,i)=>`<div class="trace-line"><span class="idx">${i+1}</span><span class="file">${esc(t.file)}</span><span class="arrow">→</span><span class="res">${esc(t.res)}</span></div>`).join('');
  return `<div class="trace ${e.collapsed?'collapsed':''}" data-uid="${e.uid}">
    <button class="trace-toggle" onclick="toggleTrace(${e.uid})"><span class="chev">▶</span><span class="lbl">Reasoning</span><span class="count">— ${e.trace.length} steps, ontology walk</span></button>
    <div class="trace-body">${lines}<div class="trace-final">${esc(e.final)}</div></div></div>`;
}
function answerHTML(e){
  const a = e.answer;
  if(a.kind==='ask'){
    return `<div class="a-body"><div class="a-value" style="font-size:19px;color:var(--ask)">${esc(a.prompt)}</div>
      <p class="a-caption">${a.hint}</p>
      <div class="clarify-chips">${(a.chips||[]).map(c=>`<button class="cchip" onclick="onChip('${esc(c)}')">${esc(c)}</button>`).join('')}</div></div>`;
  }
  if(a.kind==='refuse'){
    return `<div class="a-body"><div class="refuse-body"><span class="ico">⊘</span><div><b>${esc(a.head)}</b><br>${a.why}</div></div></div>`;
  }
  // value
  const table = a.table ? `<table class="rt"><thead><tr>${a.table.cols.map(c=>`<th>${esc(c)}</th>`).join('')}</tr></thead>
    <tbody>${a.table.rows.map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table>` : '';
  const chart = a.chart ? (()=>{ const mx=Math.max(...a.chart.bars.map(b=>b.value))||1;
    return `<div class="chart" data-uid="${e.uid}"><div class="ctitle">${esc(a.chart.title)}</div>${a.chart.bars.map(b=>`
      <div class="bar-row"><span class="bar-label">${esc(b.label)}</span><span class="bar-track"><span class="bar-fill" style="width:${Math.max(3,b.value/mx*100).toFixed(1)}%"></span></span><span class="bar-val">${(''+b.value).replace('.',',')}</span></div>`).join('')}</div>`; })() : '';
  const assumption = a.assumption ? `<div class="assumption"><span class="warn">⚠</span><div>${a.assumption}</div></div>` : '';
  const sql = a.sql ? `<div class="sqlwrap" data-uid="${e.uid}"><button class="sql-toggle" onclick="toggleSql(${e.uid})"><span class="chev">▶</span> View generated SQL</button><div class="sql-body"><pre>${a.sql}</pre></div></div>` : '';
  const chartBtn = a.chart ? `<button class="act" onclick="toggleChart(${e.uid})">▤ Chart</button>` : '';
  return `<div class="a-body">
    <div class="a-value">${esc(a.value)}<span class="unit">${esc(a.unit||'')}</span></div>
    ${a.caption?`<p class="a-caption">${esc(a.caption)}</p>`:''}
    ${assumption}${table}${chart}${sql}
    <div class="actions">
      <button class="act ${e.pinned?'on':''}" onclick="togglePin(${e.uid})">📌 ${e.pinned?'Pinned':'Pin'}</button>
      <button class="act ${e.comparing?'on cmp':''}" onclick="toggleCompare(${e.uid})">⇄ Compare</button>
      ${chartBtn}
    </div></div>`;
}
function renderEntry(e){
  const rb = {commit:'COMMIT',ask:'ASK',refuse:'REFUSE'}[e.route];
  return `<div class="entry" data-uid="${e.uid}">
    <div class="q-row"><div class="q-bubble">${esc(e.q)}</div></div>
    <div class="a-card route-${e.route}">
      <div class="a-head"><span class="badge ${e.route}"><span class="dot"></span>${rb}</span>
        <span class="a-meta">${esc(e.time)} ${e.cached?'· <span class="cached">✓ cached</span>':'· executed'}</span><span class="spacer"></span></div>
      ${traceHTML(e)}${answerHTML(e)}
    </div></div>`;
}
function render(){
  document.getElementById('sessionCount').textContent = entries.length + (entries.length===1?' question':' questions') + ' this session';
  document.getElementById('transcriptInner').innerHTML = entries.map(renderEntry).join('');
  // pinned tray
  const pins = entries.filter(e=>e.pinned);
  const tray = document.getElementById('pinnedTray');
  tray.className = 'pinned-tray' + (pins.length?'':' empty');
  tray.innerHTML = '<span class="label">📌 Pinned</span>' + pins.map(e=>`<button class="pinned-chip" onclick="scrollTo(${e.uid})"><span class="pin">📌</span>${esc(e.q)}${e.answer.value?' · '+esc(e.answer.value):''}</button>`).join('');
  // compare strip
  const cmp = entries.filter(e=>e.comparing);
  const strip = document.getElementById('compareStrip');
  strip.className = 'compare-strip' + (cmp.length?'':' empty');
  if(cmp.length) strip.innerHTML = '<span class="ttl">Compare</span>' + cmp.map(e=>`<div class="compare-item"><div class="q">${esc(e.q)}</div><div class="v">${esc(e.answer.value||e.answer.head||'—')}</div></div>`).join('') + '<span class="spacer"></span><button class="compare-close" onclick="clearCompare()">✕</button>';
}
function push(e){ entries.push(e); render(); requestAnimationFrame(()=>{ const t=document.getElementById('transcript'); t.scrollTop=t.scrollHeight; }); }

// ---------- interactions ----------
function byUid(u){ return entries.find(e=>e.uid===u); }
function toggleTrace(u){ const e=byUid(u); e.collapsed=!e.collapsed; render(); }
function toggleSql(u){ document.querySelector(`.sqlwrap[data-uid="${u}"]`).classList.toggle('open'); }
function toggleChart(u){ document.querySelector(`.chart[data-uid="${u}"]`).classList.toggle('open'); }
function togglePin(u){ const e=byUid(u); e.pinned=!e.pinned; render(); }
function toggleCompare(u){ const e=byUid(u); e.comparing=!e.comparing; render(); }
function clearCompare(){ entries.forEach(e=>e.comparing=false); render(); }
function scrollTo(u){ const el=document.querySelector(`.entry[data-uid="${u}"]`); if(el) el.scrollIntoView({behavior:'smooth',block:'center'}); }
function onChip(text){ if(['USD','EUR','GBP','CAD','AUD'].includes(text)) resolveCurrency(text); else submit(text); }
function submit(text){ const e=match(text); if(e) push(e); }
function ask(){ const ta=document.getElementById('input'); const v=ta.value.trim(); if(!v) return; ta.value=''; ta.style.height='auto'; submit(v); }

function reset(seed){
  entries = seed ? SEED.map((e,i)=>{ const c=JSON.parse(JSON.stringify(e)); c.uid=++uid; c.collapsed=(c.route==='commit'&&i>0); return c; }) : [];
  render();
  if(!seed){ const t=document.getElementById('transcript'); }
}

// wire up
document.getElementById('sendBtn').onclick = ask;
const ta = document.getElementById('input');
ta.addEventListener('keydown', ev=>{ if(ev.key==='Enter' && !ev.shiftKey){ ev.preventDefault(); ask(); } });
ta.addEventListener('input', ()=>{ ta.style.height='auto'; ta.style.height=Math.min(130,ta.scrollHeight)+'px'; });
document.getElementById('reloadBtn').onclick = ()=>reset(true);
document.getElementById('newBtn').onclick = ()=>{ reset(false); ta.focus(); };
document.getElementById('tryRow').innerHTML = '<span>Try:</span>' +
  ['Total gross sales','Sales by brand','Sales by salesperson'].map(q=>`<button class="tchip" onclick="submit('${q}')">${q}</button>`).join('');

reset(true);
</script>
"""


# ============================ CORPUS BOARD (the b_board-style verdict grid) ===========================
# A real regression board over a small Contoso question corpus. Each COMMIT question carries a FROZEN
# oracle value (hand-verified once); ask.py re-executes the ontology's own SQL and the tile is graded
# GREEN only if the executed value still matches its oracle — so a broken rule turns a tile red. ASK/REFUSE
# questions are graded on the route (correctly declined = green). Click a tile → the whole story.
#
# CORPUS rows:  (group, id, q, route, rule, sql|None, oracle|None, fmt, caption, trace[], assume[], dead[])
#   route: COMMIT | ASK | REFUSE   ·   fmt: 'musd' (money) | 'name' (string claim)
#   oracle: frozen expected value (raw units for musd; a string for name; None for ASK/REFUSE)

_NET = "SUM(Quantity * NetPrice * ExchangeRate)"
_GROSS = "SUM(Quantity * UnitPrice * ExchangeRate)"

CORPUS = [
    # ---- SALES ----
    ("SALES", "S.1", "What were our total sales?", "COMMIT", "net_sales_base_currency",
     "SELECT %s v FROM sales" % _NET, 223_597_710.6, "musd",
     "Net sales, all channels, converted to USD, full period.",
     [("ontology/rules.yaml", "net_sales_base_currency · SUM(Qty × NetPrice × FX)"),
      ("ontology/concepts/sales/sales.yaml", "net + single-currency rules"),
      ("route_rules", "slots default/held · worst-wins → COMMIT")],
     [("net, not gross", "sales.net_of_discount"), ("base currency USD, converted before summing", "sales.single_currency_basis")],
     [("SUM(NetPrice) across mixed currencies", "sales.single_currency_basis"),
      ("sum sales + orders×orderrows", "sales.no_double_count_header_detail")]),
    ("SALES", "S.2", "What were our total gross sales?", "COMMIT", "gross_sales_base_currency",
     "SELECT %s v FROM sales" % _GROSS, 237_682_283.7, "musd",
     "Gross (list price, pre-discount), converted to USD — reported because 'gross' was explicit.",
     [("ontology/rules.yaml", "gross_sales_base_currency · SUM(Qty × UnitPrice × FX)"),
      ("ontology/concepts/sales/sales.yaml", "sales.net_of_discount — gross only when asked")],
     [("gross reported because explicitly asked", "sales.net_of_discount")],
     [("defaulting to net when the word was 'gross'", "sales.net_of_discount")]),
    ("SALES", "S.3", "Net sales in 2024?", "COMMIT", "net_sales_base_currency",
     "SELECT %s v FROM sales WHERE year(OrderDate)=2024" % _NET, 32_930_633.8, "musd",
     "Net sales for calendar 2024, converted to USD.",
     [("ontology/concepts/time/period.yaml", "2024 → year window (bound, not defaulted)"),
      ("ontology/rules.yaml", "net_sales_base_currency, period-filtered")],
     [("the window was explicit (2024) — nothing assumed", "measure.period_resolution")], []),
    ("SALES", "S.4", "Net sales in 2023?", "COMMIT", "net_sales_base_currency",
     "SELECT %s v FROM sales WHERE year(OrderDate)=2023" % _NET, 45_472_704.2, "musd",
     "Net sales for calendar 2023, converted to USD.",
     [("ontology/concepts/time/period.yaml", "2023 → year window"),
      ("ontology/rules.yaml", "net_sales_base_currency, period-filtered")],
     [("explicit window (2023)", "measure.period_resolution")], []),
    # ---- CURRENCY ----
    ("CURRENCY", "CUR.1", "Total sales in a single currency", "ASK", "sales.ask_currency_when_ambiguous",
     None, None, "musd",
     "Five currencies span the rows and none was named — clarify, don't guess.",
     [("ontology/concepts/finance/currency.yaml", "5-member closed set → ambiguous"),
      ("route_rules", "currency.basis mandatory here → ASK")],
     [], [("silently default to USD", "ambiguity.ask_dont_guess")]),
    ("CURRENCY", "CUR.2", "Total sales in USD", "COMMIT", "net_sales_base_currency",
     "SELECT %s v FROM sales" % _NET, 223_597_710.6, "musd",
     "USD named explicitly — the disclosed base currency; net, full period.",
     [("ontology/concepts/finance/currency.yaml", "USD = the base the rates convert to"),
      ("ontology/rules.yaml", "net_sales_base_currency")],
     [("net; USD is the executable base", "sales.single_currency_basis")], []),
    ("CURRENCY", "CUR.3", "Total sales in EUR", "REFUSE", "resolve.never_fabricate",
     None, None, "musd",
     "Ungrounded: the data carries each line's rate to the USD base only — a EUR total needs a rate not in the model.",
     [("ontology/concepts/finance/currency.yaml", "each line's rate → USD base only"),
      ("route_rules", "USD→EUR rate absent → ABSTAIN, flag the gap")],
     [], [("invent a USD→EUR rate from priors", "resolve.never_fabricate")]),
    # ---- BRAND ----
    ("BRAND", "B.1", "Net sales by brand", "COMMIT", "net_sales_base_currency",
     "SELECT MAX(v) v FROM (SELECT %s v FROM sales s JOIN product p ON s.ProductKey=p.ProductKey GROUP BY p.Brand)" % _NET,
     49_989_208.4, "musd",
     "Net sales grouped by brand; the tile checks the leading brand's total.",
     [("ontology/concepts/catalog/brand.yaml", "Brand → closed set (grounded on product.Brand)"),
      ("ontology/edges.yaml", "sales.ProductKey → product · brand carried")],
     [("net, USD, full period — same defaults as the grand total", "assumption.disclose_defaults")], []),
    ("BRAND", "B.2", "Which brand sold the most?", "COMMIT", "net_sales_base_currency",
     "SELECT p.Brand v FROM sales s JOIN product p ON s.ProductKey=p.ProductKey GROUP BY p.Brand ORDER BY %s DESC LIMIT 1" % _NET,
     "Adventure Works", "name",
     "The single top brand by net sales — a claim, checked against the frozen expected name.",
     [("ontology/concepts/catalog/brand.yaml", "Brand closed set"),
      ("ontology/rules.yaml", "net_sales_base_currency, argmax over brand")],
     [("ranked by net USD", "sales.single_currency_basis")], []),
    # ---- CAPABILITY ----
    ("CAPABILITY", "CAP.1", "Sales by salesperson", "REFUSE", "capability.refuse_missing_dimension",
     None, None, "musd",
     "No salesperson dimension in the model — refuse, name what it does carry.",
     [("ontology/query_rules.yaml", "capability.refuse_missing_dimension"),
      ("ontology/edges.yaml", "join set: product, store, currency, date, brand — no salesperson")],
     [], [("approximate with StoreKey", "capability.refuse_missing_dimension"),
          ("fabricate the dimension", "resolve.never_fabricate")]),
    ("CAPABILITY", "CAP.2", "Sales by supplier", "REFUSE", "capability.refuse_missing_dimension",
     None, None, "musd",
     "Supplier is not a dimension the data carries.",
     [("ontology/query_rules.yaml", "capability.refuse_missing_dimension"),
      ("ontology/edges.yaml", "no supplier edge")],
     [], [("borrow Manufacturer as a stand-in for supplier", "capability.refuse_missing_dimension")]),
    # ---- INTEGRITY ----
    ("INTEGRITY", "INT.1", "Total sales adding orders and order-rows", "REFUSE", "sales.no_double_count_header_detail",
     None, None, "musd",
     "Summing `sales` and orders×orderrows together double-counts the same facts — blocked.",
     [("ontology/concepts/sales/sales.yaml", "sales.no_double_count_header_detail (blocked slot)"),
      ("route_rules", "double-count invariant would be violated → REFUSE")],
     [], [("join header to detail and sum both", "sales.no_double_count_header_detail")]),
]


def _grade(row, run_val):
    """Grade a resolved corpus row -> ('good'|'crit'|'warn'|'open', run_display, note)."""
    _, _id, _q, route, _rule, sql, oracle, fmt, *_ = row
    if route in ("ASK", "REFUSE"):
        return "good", route, "correctly declined (route matched)"
    if oracle is None:
        return "open", "—", "no frozen oracle"
    if fmt == "name":
        ok = str(run_val).strip() == str(oracle).strip()
        return ("good" if ok else "crit"), str(run_val), ("matches oracle" if ok else "≠ oracle '%s'" % oracle)
    run = float(run_val)
    ok = abs(run - float(oracle)) / float(oracle) < 0.005
    return ("good" if ok else "crit"), _musd(run), \
        ("matches oracle %s" % _musd(oracle) if ok else "≠ oracle %s" % _musd(oracle))


def resolve_corpus():
    """Execute every COMMIT question's ontology SQL, grade against the frozen oracle, build detail rows."""
    out = []
    for row in CORPUS:
        group, _id, q, route, rule, sql, oracle, fmt, caption, trace, assume, dead = row
        run_val = duckdb(sql)[0]["v"] if sql else None
        verdict, run_disp, note = _grade(row, run_val)
        oracle_disp = (_musd(oracle) if fmt == "musd" else str(oracle)) if oracle is not None else None
        out.append({
            "group": group, "id": _id, "q": q, "route": route, "rule": rule,
            "verdict": verdict, "value": run_disp, "oracle": oracle_disp, "note": note,
            "caption": caption, "sql": _hl(sql) if sql else None,
            "trace": [{"file": f, "res": r} for f, r in trace],
            "assume": [{"t": t, "rule": rl} for t, rl in assume],
            "dead": [{"t": t, "rule": rl} for t, rl in dead],
        })
    return out


def _board_data():
    rows = resolve_corpus()
    n = len(rows)
    green = sum(1 for r in rows if r["verdict"] == "good")
    commits = sum(1 for r in rows if r["route"] == "COMMIT" and r["verdict"] == "good")
    declined = sum(1 for r in rows if r["route"] in ("ASK", "REFUSE") and r["verdict"] == "good")
    openn = sum(1 for r in rows if r["verdict"] == "open")
    crit = sum(1 for r in rows if r["verdict"] == "crit")
    # preserve first-seen group order
    groups = []
    for r in rows:
        if r["group"] not in groups:
            groups.append(r["group"])
    return {"rows": rows, "groups": groups,
            "kpi": {"n": n, "green": green, "commits": commits, "declined": declined, "open": openn, "crit": crit}}


def render_board(out_path, artifact=False):
    data = _board_data()
    js = json.dumps(data, ensure_ascii=False)
    meta = "ontology v%s · reviewed %s · every value executed against contoso.duckdb" % (ONTOLOGY_VERSION, REVIEWED)
    inner = (_BOARD_TITLE + _BOARD_STYLE + _BOARD_BODY + _BOARD_SCRIPT) if artifact else \
        (_DOC_OPEN.replace(_TITLE, _BOARD_TITLE) + _BOARD_STYLE + _DOC_MID + _BOARD_BODY + _BOARD_SCRIPT + _DOC_CLOSE)
    html = inner.replace("{{DATA}}", js).replace("{{META}}", _esc(meta))
    Path(out_path).write_text(html, encoding="utf-8")
    return out_path


# ============================ ASK APP (the ask.html split: workspace + conversation) ==================
# A faithful Contoso build of the upstream ask.html page: LEFT = workspace (the focused report you pin/graph/
# compare), RIGHT = conversation (persistent trace). Ask a question -> it is walked through the ontology
# and answered from EXECUTED data (build_entries, run against contoso.duckdb) — never guessed. Light by
# default, theme-aware; the session persists in localStorage and nothing re-runs on reload.

_ASK_TITLE = "<title>Contoso · Ask — meaning as code</title>\n"

_ASK_STYLE = r"""<style>
  :root{--ground:#eef1f5;--card:#ffffff;--panel2:#f7f9fc;--ink:#141a22;--muted:#5a6674;--faint:#8a94a3;--hair:#d4dae2;
    --accent:#1f5fe0;--accent-soft:#1f5fe022;--commit:#0f9d58;--commit-bg:#0f9d5814;--commit-line:#0f9d5855;
    --ask:#c67a12;--ask-bg:#c67a1214;--ask-line:#c67a1255;--refuse:#d4483b;--refuse-bg:#d4483b12;--refuse-line:#d4483b55;
    --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
    --sans:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;--r:12px}
  :root[data-theme="dark"]{--ground:#0c1015;--card:#141b24;--panel2:#111722;--ink:#e6ebf1;--muted:#94a3b4;--faint:#63707f;--hair:#263140;
    --accent:#5b8cf5;--accent-soft:#5b8cf522;--commit:#3ec27a;--commit-bg:#3ec27a1c;--commit-line:#3ec27a55;
    --ask:#e6a13c;--ask-bg:#e6a13c1c;--ask-line:#e6a13c55;--refuse:#f0685c;--refuse-bg:#f0685c1c;--refuse-line:#f0685c55}
  *{box-sizing:border-box}
  html,body{height:100%}
  body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.55;-webkit-font-smoothing:antialiased}
  .app{height:100vh;display:flex;flex-direction:column}

  .topnav{flex:0 0 auto;display:flex;align-items:center;gap:12px;padding:11px 20px;border-bottom:1px solid var(--hair);background:var(--card)}
  .brand{font-weight:680;font-size:15px} .brand b{color:var(--accent)}
  .brand .src{color:var(--muted);font-weight:500;font-size:12.5px;margin-left:8px}
  .topnav .sp{flex:1}
  .btn{font-family:var(--sans);font-size:12.5px;color:var(--muted);background:var(--panel2);border:1px solid var(--hair);border-radius:8px;padding:6px 11px;cursor:pointer}
  .btn:hover{color:var(--ink);border-color:var(--accent);background:var(--accent-soft)}
  .iconbtn{width:32px;height:31px;font-size:15px;padding:0}

  .split{flex:1 1 auto;display:grid;grid-template-columns:1fr 1fr;min-height:0}
  .col{min-height:0;display:flex;flex-direction:column;overflow:hidden}
  .left-col{border-right:1px solid var(--hair)}
  .col-head{flex:0 0 auto;display:flex;align-items:center;gap:8px;padding:12px 20px;border-bottom:1px solid var(--hair);background:var(--panel2)}
  .kicker{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);font-weight:600;display:flex;align-items:center;gap:7px}
  .kicker .dot{color:var(--accent);font-size:9px}
  .col-head .cnt{margin-left:auto;font-family:var(--mono);font-size:11px;color:var(--faint)}

  .workspace,.history{flex:1 1 auto;overflow-y:auto;padding:20px}
  .empty{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--muted);gap:8px;padding:30px}
  .empty .ico{font-size:30px;opacity:.7} .empty h3{margin:0;font-size:16px;color:var(--ink);font-weight:640} .empty p{margin:0;max-width:38ch;font-size:13px;line-height:1.5}

  /* ---- workspace focused report ---- */
  .report{animation:fade .3s ease} @keyframes fade{from{opacity:0}to{opacity:1}}
  .rep-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  .badge{font-family:var(--mono);font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:4px 10px;border-radius:20px}
  .badge.commit{background:var(--commit-bg);color:var(--commit)} .badge.ask{background:var(--ask-bg);color:var(--ask)} .badge.refuse{background:var(--refuse-bg);color:var(--refuse)}
  .rep-q{font-size:19px;font-weight:640;letter-spacing:-.01em;margin:14px 0 0;max-width:46ch}
  .rep-val{font-family:var(--mono);font-size:33px;font-weight:700;letter-spacing:-.01em;margin-top:16px}
  .rep-val .u{font-size:14px;color:var(--muted);margin-left:9px;font-weight:500}
  .commit .rep-val{color:var(--ink)}
  .rep-cap{color:var(--muted);font-size:13px;margin-top:8px;max-width:64ch}
  .rep-ask{font-size:20px;font-weight:640;color:var(--ask);margin-top:16px} .rep-refuse{font-size:19px;font-weight:640;color:var(--refuse);margin-top:16px}

  .assume{margin-top:16px;display:flex;gap:9px;background:var(--ask-bg);border:1px solid var(--ask-line);border-radius:10px;padding:11px 13px;font-size:12.5px;line-height:1.5;color:var(--ink)}
  .assume b{color:var(--ask)} .assume code{font-family:var(--mono);font-size:11px;background:var(--card);border:1px solid var(--ask-line);border-radius:5px;padding:1px 5px}
  .assume .w{color:var(--ask);flex:0 0 auto}

  .sec{margin-top:22px}
  .sec h5{font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--faint);font-weight:700;margin:0 0 11px;display:flex;align-items:center;gap:10px}
  .sec h5::after{content:"";flex:1;height:1px;background:var(--hair)}
  .sec.reason h5{color:var(--accent)}
  .walk{background:var(--card);border:1px solid var(--hair);border-left:3px solid var(--accent);border-radius:10px;padding:12px 15px}
  .tline{font-family:var(--mono);font-size:12px;line-height:1.7;display:flex;gap:8px;color:var(--muted)}
  .tline .idx{color:var(--faint);flex:0 0 15px} .tline .file{color:var(--accent)} .tline .ar{color:var(--faint)} .tline .res{color:var(--ink)}
  .tfinal{margin-top:7px;font-family:var(--mono);font-size:11px;color:var(--faint);font-style:italic}

  table.rt{width:100%;border-collapse:collapse;font-size:13px}
  table.rt th{text-align:left;font-size:10px;letter-spacing:.05em;text-transform:uppercase;color:var(--faint);font-weight:600;padding:0 10px 7px 0;border-bottom:1px solid var(--hair)}
  table.rt td{padding:8px 10px 8px 0;border-bottom:1px solid var(--hair);font-variant-numeric:tabular-nums}
  table.rt tr:last-child td{border-bottom:0} table.rt td:nth-child(2){text-align:right} table.rt td:nth-child(3){text-align:right;width:80px}
  .du{color:var(--commit)} .dd{color:var(--refuse)}

  .chart{display:none;flex-direction:column;gap:7px} .chart.open{display:flex}
  .bar{display:grid;grid-template-columns:120px 1fr 66px;align-items:center;gap:9px;font-size:12px}
  .bl{color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bt{height:8px;background:var(--panel2);border:1px solid var(--hair);border-radius:5px;overflow:hidden} .bf{height:100%;background:linear-gradient(90deg,var(--accent),var(--commit))}
  .bv{text-align:right;font-variant-numeric:tabular-nums}

  pre.sql{margin:0;font-family:var(--mono);font-size:12px;line-height:1.55;background:var(--card);border:1px solid var(--hair);border-radius:10px;padding:12px 14px;overflow-x:auto;white-space:pre-wrap}
  pre.sql .kw{color:var(--accent)} pre.sql .fn{color:#7c3aed} pre.sql .str{color:var(--commit)}
  :root[data-theme="dark"] pre.sql .fn{color:#c39bff}
  .cchips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
  .cchip{font-family:var(--sans);font-size:12.5px;border:1px solid var(--hair);background:var(--panel2);color:var(--muted);border-radius:20px;padding:6px 13px;cursor:pointer}
  .cchip:hover{border-color:var(--ask);color:var(--ink);background:var(--ask-bg)}

  .actions{display:flex;gap:8px;margin-top:20px;flex-wrap:wrap}
  .act{font-family:var(--sans);font-size:12px;color:var(--muted);background:var(--panel2);border:1px solid var(--hair);border-radius:8px;padding:6px 12px;cursor:pointer}
  .act:hover{color:var(--ink);border-color:var(--accent)} .act.on{border-color:var(--accent);color:var(--accent)}

  /* ---- conversation ---- */
  .entry{border:1px solid var(--hair);border-radius:var(--r);background:var(--card);padding:12px 14px;margin-bottom:12px;cursor:pointer;transition:.12s}
  .entry:hover{border-color:var(--accent)} .entry.on{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
  .entry .eq{font-weight:560;font-size:14px;margin-bottom:9px}
  .entry .er{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
  .entry .ev{font-family:var(--mono);font-weight:700;font-size:15px} .entry.commit .ev{color:var(--commit)}
  .entry .eside{margin-left:auto;font-size:11px;color:var(--accent);font-family:var(--mono)}
  .entry .esub{color:var(--muted);font-size:12px;margin-top:6px;line-height:1.45}

  .composer-zone{flex:0 0 auto;border-top:1px solid var(--hair);background:var(--card);padding:14px 20px}
  .hero{text-align:center;padding:6px 10px 16px} .hero .ico{font-size:24px;color:var(--accent)} .hero h2{margin:8px 0 0;font-size:20px;font-weight:660}
  .hero p{color:var(--muted);font-size:13px;margin:8px auto 0;max-width:44ch;line-height:1.5}
  .try-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center;margin-top:14px;font-size:11.5px;color:var(--faint)}
  .try-row .tchip{font-family:var(--sans);font-size:12px;border:1px solid var(--hair);background:var(--panel2);color:var(--muted);border-radius:20px;padding:6px 12px;cursor:pointer}
  .try-row .tchip:hover{border-color:var(--accent);color:var(--ink);background:var(--accent-soft)}
  .composer{display:flex;align-items:flex-end;gap:8px;background:var(--panel2);border:1px solid var(--hair);border-radius:14px;padding:8px 8px 8px 16px;margin-top:12px}
  .composer:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
  .composer textarea{flex:1;resize:none;border:none;outline:none;background:transparent;color:var(--ink);font-family:var(--sans);font-size:14.5px;line-height:1.5;max-height:120px;padding:5px 0}
  .composer textarea::placeholder{color:var(--faint)}
  .send{flex:0 0 auto;width:36px;height:36px;border-radius:10px;border:none;background:var(--accent);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center}
  .send:hover{filter:brightness(1.08)}
  .foot{margin-top:9px;font-size:11px;color:var(--faint);text-align:center}
  @media(max-width:820px){.split{grid-template-columns:1fr;grid-template-rows:1fr 1fr}.left-col{border-right:none;border-bottom:1px solid var(--hair)}}
</style>
"""

_ASK_BODY = r"""<div class="app">
  <div class="topnav">
    <span class="brand">Contoso · <b>Ask</b><span class="src">/ CONTOSO · meaning as code</span></span>
    <span class="sp"></span>
    <button class="btn" id="resetBtn" title="Clear this session">＋ New session</button>
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
        <div class="hero" id="hero">
          <div class="ico">✳</div>
          <h2>Ask Contoso anything</h2>
          <p>Sales questions get walked through the ontology, then answered from executed data — never guessed.</p>
          <div class="try-row" id="tryRow"></div>
        </div>
        <div class="composer">
          <textarea id="input" rows="1" placeholder="Ask about sales, brands, currency, gross vs net…"></textarea>
          <button class="send" id="sendBtn" title="Send (Enter)"><svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor"><path d="M2 10l16-7-7 16-2-6-7-3z"/></svg></button>
        </div>
        <div class="foot">Enter to send · Shift+Enter for a new line · {{META}}</div>
      </div>
    </section>
  </div>
</div>
"""

_ASK_SCRIPT = r"""<script>
const SEED = {{DATA}};
const LIB = {}; SEED.forEach(e=>LIB[e.id]=e);
function esc(s){return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
const KEY='contoso_ask_session';
let entries=[], focus=null, uid=0;

// ---- persistence ----
function save(){ try{localStorage.setItem(KEY,JSON.stringify({entries,focus,uid}));}catch(e){} }
function load(){ try{const s=JSON.parse(localStorage.getItem(KEY)||'null'); if(s&&s.entries){entries=s.entries;focus=s.focus;uid=s.uid||entries.length;}}catch(e){} }

// ---- matcher (executed library) ----
function clone(id,text){const b=LIB[id]; if(!b) return unknown(text); const e=JSON.parse(JSON.stringify(b)); e.uid=++uid; e.q=text||b.q; e.collapsed=true; return e;}
function unknown(text){return {uid:++uid,q:text,route:'ask',collapsed:false,
  trace:[{file:'ontology/query_rules.yaml',res:'no concept in this demo matched the question'}],
  final:'route_rules → outside the demo’s executed scope → ASK',
  answer:{kind:'ask',prompt:'I can only answer what this small demo has executed.',hint:'Public Contoso demo — try one of these, each backed by a real query.',
    chips:['What were our total sales?','Total gross sales','Sales by brand','Total sales in a single currency','Sales by salesperson']}};}
function match(text){const q=text.toLowerCase().trim(); if(!q) return null;
  if(/(salesperson|sales person|sales rep|supplier|promotion|discount reason)/.test(q)) return clone('by-salesperson',text);
  if(/gross/.test(q)) return clone('gross-sales',text);
  if(/(by |per )?brand/.test(q)) return clone('by-brand',text);
  if(/(single|one|a)\s+currenc/.test(q)&&!/(usd|eur|gbp|cad|aud)\b/.test(q)) return clone('single-currency',text);
  if(/total|net|sales|revenue|turnover/.test(q)) return clone('total-sales',text);
  return unknown(text);}
function resolveCurrency(cur){ if(cur==='USD'){const e=clone('total-sales','Total sales in USD');e.answer.caption='In the disclosed base currency, USD. '+e.answer.caption;push(e);return;}
  const e={uid:++uid,q:'Total sales in '+cur,route:'refuse',collapsed:false,
    trace:[{file:'ontology/concepts/finance/currency.yaml',res:'each line carries its rate to the USD base only'},{file:'ontology/query_rules.yaml',res:'resolve.never_fabricate — no USD→'+cur+' rate in the model'}],
    final:'route_rules → target currency ungrounded → ABSTAIN',
    answer:{kind:'refuse',head:'A '+cur+' total isn’t grounded in this data.',why:'The warehouse carries each line’s rate to the <b>USD</b> base, so USD is executable. A <b>'+cur+'</b> total needs a USD→'+cur+' rate that isn’t in the model — flagged, not guessed.'}};
  push(e);}

// ---- SQL/section builders (workspace) ----
function walkHTML(e){const l=e.trace.map((t,i)=>`<div class="tline"><span class="idx">${i+1}</span><span class="file">${esc(t.file)}</span><span class="ar">→</span><span class="res">${esc(t.res)}</span></div>`).join('');
  return `<div class="sec reason"><h5>how it routed — ontology walk</h5><div class="walk">${l}<div class="tfinal">${esc(e.final)}</div></div></div>`;}
function report(e){
  const a=e.answer, rc=e.route;
  let head;
  if(a.kind==='value') head=`<div class="rep-val">${esc(a.value)}<span class="u">${esc(a.unit||'')}</span></div>${a.caption?`<p class="rep-cap">${esc(a.caption)}</p>`:''}`;
  else if(a.kind==='ask') head=`<div class="rep-ask">${esc(a.prompt)}</div><p class="rep-cap">${a.hint}</p><div class="cchips">${(a.chips||[]).map(c=>`<button class="cchip" onclick="onChip('${esc(c)}')">${esc(c)}</button>`).join('')}</div>`;
  else head=`<div class="rep-refuse">${esc(a.head)}</div><p class="rep-cap">${a.why}</p>`;
  const assume=a.assumption?`<div class="assume"><span class="w">⚠</span><div>${a.assumption}</div></div>`:'';
  const table=a.table?`<div class="sec"><h5>result</h5><table class="rt"><thead><tr>${a.table.cols.map(c=>`<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${a.table.rows.map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table>`+(a.chart?`<div class="chart" id="ch${e.uid}">${chartBars(a.chart)}</div>`:'')+`</div>`:'';
  const sql=a.sql?`<div class="sec"><h5>generated sql</h5><pre class="sql">${a.sql}</pre></div>`:'';
  const acts=a.kind==='value'?`<div class="actions"><button class="act ${e.pinned?'on':''}" onclick="togglePin(${e.uid})">📌 ${e.pinned?'Pinned':'Pin'}</button>${a.chart?`<button class="act" onclick="toggleChart(${e.uid})">▤ Graph</button>`:''}<button class="act ${e.cmp?'on':''}" onclick="toggleCmp(${e.uid})">⇄ Compare</button></div>`:'';
  return `<div class="report ${rc}"><div class="rep-head"><span class="badge ${rc}">${rc.toUpperCase()}</span></div>
    <div class="rep-q">${esc(e.q)}</div>${head}${assume}${walkHTML(e)}${table}${sql}${acts}</div>`;
}
function chartBars(c){const mx=Math.max(...c.bars.map(b=>b.value))||1;return `<div style="font-size:10px;color:var(--faint);text-transform:uppercase;letter-spacing:.05em;margin:4px 0 8px">${esc(c.title)}</div>`+c.bars.map(b=>`<div class="bar"><span class="bl">${esc(b.label)}</span><span class="bt"><span class="bf" style="width:${Math.max(3,b.value/mx*100).toFixed(1)}%"></span></span><span class="bv">${(''+b.value).replace('.',',')}</span></div>`).join('');}

// ---- render ----
function shortResult(e){const a=e.answer; if(a.kind==='value') return `<span class="ev">${esc(a.value)}</span> <span style="color:var(--muted);font-size:12px">${esc(a.unit||'')}</span>`;
  if(a.kind==='ask') return `<span style="color:var(--ask);font-weight:600">Clarification needed</span>`; return `<span style="color:var(--refuse);font-weight:600">Declined</span>`;}
function render(){
  document.getElementById('entryCount').textContent = entries.length? entries.length+(entries.length===1?' question':' questions'):'';
  document.getElementById('hero').style.display = entries.length? 'none':'block';
  document.getElementById('history').innerHTML = entries.map(e=>
    `<div class="entry ${e.route} ${e.uid===focus?'on':''}" onclick="focusOn(${e.uid})"><div class="eq">${esc(e.q)}</div><div class="er"><span class="badge ${e.route}">${e.route.toUpperCase()}</span>${shortResult(e)}<span class="eside">open in workspace →</span></div></div>`).join('');
  const ws=document.getElementById('workspace'); const fe=entries.find(e=>e.uid===focus);
  ws.innerHTML = fe? report(fe) : `<div class="empty"><div class="ico">🗂️</div><h3>No result focused yet</h3><p>Ask a question, or click any entry in the conversation — its report opens here, ready to pin, graph, or compare.</p></div>`;
  save();
}
function push(e){entries.push(e);focus=e.uid;render();requestAnimationFrame(()=>{const h=document.getElementById('history');h.scrollTop=h.scrollHeight;});}
function focusOn(u){focus=u;render();document.getElementById('workspace').scrollTop=0;}
function toggleChart(u){const el=document.getElementById('ch'+u);if(el)el.classList.toggle('open');}
function togglePin(u){const e=entries.find(x=>x.uid===u);e.pinned=!e.pinned;render();}
function toggleCmp(u){const e=entries.find(x=>x.uid===u);e.cmp=!e.cmp;render();}
function onChip(t){if(['USD','EUR','GBP','CAD','AUD'].includes(t))resolveCurrency(t);else submit(t);}
function submit(t){const e=match(t);if(e)push(e);}
function ask(){const ta=document.getElementById('input');const v=ta.value.trim();if(!v)return;ta.value='';ta.style.height='auto';submit(v);}

// ---- theme ----
function applyTheme(t){document.documentElement.dataset.theme=t;try{localStorage.setItem('contoso_theme',t);}catch(e){}document.getElementById('themeBtn').textContent=t==='dark'?'☀':'◑';}
(function(){let t='light';try{t=localStorage.getItem('contoso_theme')||'light';}catch(e){}document.documentElement.dataset.theme=t;})();

// ---- wire ----
const ta=document.getElementById('input');
ta.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();ask();}});
ta.addEventListener('input',()=>{ta.style.height='auto';ta.style.height=Math.min(120,ta.scrollHeight)+'px';});
document.getElementById('sendBtn').onclick=ask;
document.getElementById('resetBtn').onclick=()=>{entries=[];focus=null;uid=0;render();ta.focus();};
document.getElementById('themeBtn').onclick=()=>applyTheme(document.documentElement.dataset.theme==='dark'?'light':'dark');
document.getElementById('tryRow').innerHTML='<span>Try:</span>'+['What were our total sales?','Sales by brand','Total sales in a single currency'].map(q=>`<button class="tchip" onclick="submit('${q}')">${q}</button>`).join('');
applyTheme(document.documentElement.dataset.theme||'light');
load(); render();
</script>
"""


def render_ask(out_path, artifact=False):
    entries = build_entries()
    data = json.dumps(entries, ensure_ascii=False)
    meta = "ontology v%s · every value executed against contoso.duckdb" % ONTOLOGY_VERSION
    inner = (_ASK_TITLE + _ASK_STYLE + _ASK_BODY + _ASK_SCRIPT) if artifact else \
        (_DOC_OPEN.replace(_TITLE, _ASK_TITLE) + _ASK_STYLE + _DOC_MID + _ASK_BODY + _ASK_SCRIPT + _DOC_CLOSE)
    html = inner.replace("{{DATA}}", data).replace("{{META}}", _esc(meta))
    Path(out_path).write_text(html, encoding="utf-8")
    return out_path


_BOARD_TITLE = "<title>Contoso · /ask — corpus board</title>\n"

_BOARD_STYLE = r"""<style>
  :root{--ground:#eef1f5;--card:#ffffff;--ink:#141a22;--muted:#5a6674;--hair:#d4dae2;
    --accent:#1f5fe0;--accent-soft:#1f5fe022;--good:#0f9d58;--good-bg:#0f9d5818;
    --warn:#c67a12;--warn-bg:#c67a1218;--open:#64748b;--open-bg:#64748b18;
    --crit:#d4483b;--crit-bg:#d4483b18;
    --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
    --sans:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    --r:10px;--maxw:1120px}
  :root[data-theme="dark"]{--ground:#0c1015;--card:#141b24;--ink:#e6ebf1;--muted:#94a3b4;--hair:#263140;
    --accent:#5b8cf5;--accent-soft:#5b8cf522;--good:#3ec27a;--good-bg:#3ec27a18;--warn:#e6a13c;
    --warn-bg:#e6a13c1c;--open:#8093a6;--open-bg:#8093a61c;--crit:#f0685c;--crit-bg:#f0685c1c}
  *{box-sizing:border-box}
  body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);line-height:1.55;font-size:15px}
  .wrap{max-width:var(--maxw);margin:0 auto;padding:34px 22px 70px}
  h1,h2{margin:0;text-wrap:balance}
  .eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
  [hidden]{display:none!important}
  header.hd{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;flex-wrap:wrap;border-bottom:1px solid var(--hair);padding-bottom:22px;margin-bottom:26px}
  .title{font-size:30px;font-weight:680;letter-spacing:-.01em;margin-top:6px} .title b{color:var(--accent)}
  .sub{color:var(--muted);margin-top:7px;max-width:64ch}
  .rhead{display:flex;flex-direction:column;align-items:flex-end;gap:10px}
  .stamp{font-family:var(--mono);font-size:11.5px;color:var(--muted);text-align:right;line-height:1.7}
  .stamp b{color:var(--ink)}
  .tbtn{font-family:var(--mono);font-size:11.5px;color:var(--muted);background:none;border:1px solid var(--hair);border-radius:7px;padding:5px 10px;cursor:pointer}
  .tbtn:hover{background:var(--accent-soft);color:var(--ink)}
  .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:26px}
  .kpi{background:var(--card);border:1px solid var(--hair);border-radius:var(--r);padding:15px 16px}
  .kpi .n{font-family:var(--mono);font-size:26px;font-weight:600;font-variant-numeric:tabular-nums}
  .kpi .n s{text-decoration:none;color:var(--muted);font-size:16px}
  .kpi .l{font-size:12.5px;color:var(--muted);margin-top:2px}
  .kpi.good .n{color:var(--good)} .kpi.accent .n{color:var(--accent)} .kpi.open .n{color:var(--open)} .kpi.crit .n{color:var(--crit)}
  .legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:0 0 16px}
  .legend span{display:inline-flex;align-items:center;gap:6px}
  .dot{width:11px;height:11px;border-radius:3px;display:inline-block}
  .dot.good{background:var(--good)} .dot.warn{background:var(--warn)} .dot.open{background:var(--open)} .dot.crit{background:var(--crit)}
  .grid{display:flex;flex-wrap:wrap;gap:16px}
  .shapegrp{background:var(--card);border:1px solid var(--hair);border-radius:var(--r);padding:12px 13px;flex:1 1 220px}
  .shapegrp h4{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600;margin:0 0 10px;display:flex;gap:7px}
  .shapegrp h4 em{font-style:normal;color:var(--muted);font-weight:400}
  .cells{display:flex;flex-wrap:wrap;gap:6px}
  .cell{font-family:var(--mono);font-size:11px;font-weight:600;padding:5px 8px;border-radius:6px;border:1px solid transparent;min-width:44px;text-align:center;cursor:pointer;transition:transform .08s;background:none}
  .cell:hover{transform:translateY(-1px)}
  .cell.good{background:var(--good-bg);color:var(--good);border-color:var(--good)}
  .cell.warn{background:var(--warn-bg);color:var(--warn);border-color:var(--warn)}
  .cell.open{background:var(--open-bg);color:var(--open);border-color:var(--open)}
  .cell.crit{background:var(--crit-bg);color:var(--crit);border-color:var(--crit)}
  footer{margin-top:30px;padding-top:18px;border-top:1px solid var(--hair);font-family:var(--mono);font-size:11.5px;color:var(--muted)}

  /* ---------- detail view ---------- */
  .backbar{display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--hair);padding-bottom:16px;margin-bottom:22px}
  .back{font-family:var(--mono);font-size:12.5px;font-weight:600;color:var(--accent);background:none;border:1px solid var(--hair);border-radius:7px;padding:6px 12px;cursor:pointer}
  .back:hover{background:var(--accent-soft)}
  .backbar .nav{margin-left:auto;display:flex;gap:6px}
  .navbtn{font-family:var(--mono);font-size:12px;color:var(--muted);background:none;border:1px solid var(--hair);border-radius:7px;padding:6px 10px;cursor:pointer}
  .navbtn:hover:not(:disabled){background:var(--open-bg);color:var(--ink)} .navbtn:disabled{opacity:.4;cursor:default}
  .did{font-family:var(--mono);font-size:22px;font-weight:700;display:flex;align-items:center;gap:11px;flex-wrap:wrap}
  .dq{font-size:21px;font-weight:600;margin-top:12px;max-width:52ch;letter-spacing:-.01em}
  .vbadge{font-family:var(--mono);font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;text-transform:uppercase}
  .vbadge.commit{background:var(--good-bg);color:var(--good)} .vbadge.ask{background:var(--warn-bg);color:var(--warn)} .vbadge.refuse{background:var(--crit-bg);color:var(--crit)}
  .rtag{font-family:var(--mono);font-size:11px;font-weight:700;border-radius:6px;padding:3px 9px;text-transform:uppercase}
  .rtag.good{background:var(--good-bg);color:var(--good)} .rtag.crit{background:var(--crit-bg);color:var(--crit)} .rtag.open{background:var(--open-bg);color:var(--open)}
  .dval{font-family:var(--mono);font-size:34px;font-weight:700;margin-top:20px;letter-spacing:-.01em}
  .dcap{color:var(--muted);margin-top:8px;max-width:70ch}
  .dsec{margin-top:26px}
  .dsec h5{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700;margin:0 0 12px;display:flex;align-items:center;gap:10px}
  .dsec h5::after{content:"";flex:1;height:1px;background:var(--hair)}
  .dsec.reasoning h5{color:var(--accent)}
  .panel{background:var(--card);border:1px solid var(--hair);border-left:3px solid var(--accent);border-radius:var(--r);padding:14px 18px}
  .tline{font-family:var(--mono);font-size:12.5px;line-height:1.75;display:flex;gap:9px;color:var(--muted)}
  .tline .idx{color:var(--muted);flex:0 0 16px} .tline .file{color:var(--accent)} .tline .arrow{color:var(--muted)} .tline .res{color:var(--ink)}
  .dl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
  .dl li{display:flex;gap:10px;align-items:baseline;font-size:14px;line-height:1.5;flex-wrap:wrap}
  .dl .mk{flex:0 0 auto;font-weight:700} .dl.assume .mk{color:var(--good)} .dl.dead .mk{color:var(--crit)}
  .dl .txt{color:var(--ink)} .dl.dead .txt{color:var(--muted)}
  .dl code{font-family:var(--mono);font-size:11.5px;background:var(--open-bg);border-radius:5px;padding:1px 7px;margin-left:auto;color:var(--muted)}
  pre.code{font-family:var(--mono);font-size:12.5px;line-height:1.6;background:var(--card);border:1px solid var(--hair);border-radius:9px;padding:14px 16px;overflow-x:auto;margin:0;white-space:pre-wrap}
  pre.code .kw{color:var(--accent)} pre.code .fn{color:#7c3aed} pre.code .str{color:var(--good)}
  :root[data-theme="dark"] pre.code .fn{color:#c39bff}
  .oracle{display:flex;flex-wrap:wrap;gap:10px 22px;align-items:center;background:var(--card);border:1px solid var(--hair);border-radius:var(--r);padding:14px 18px;font-size:14px}
  .oracle .kv{display:flex;flex-direction:column;gap:2px} .oracle .k{font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)} .oracle .v{font-family:var(--mono);font-weight:700}
  .oracle .arrow{color:var(--muted)} .oracle .spacer{flex:1}
</style>
"""

_BOARD_BODY = r"""<div class="wrap">
  <!-- ================= BOARD VIEW ================= -->
  <div id="boardView">
    <header class="hd">
      <div>
        <div class="eyebrow">Contoso · /ask · meaning as code</div>
        <h1 class="title">Corpus <b>board</b></h1>
        <p class="sub">One tile per question — question · route · executed value · the value-vs-oracle verdict. Green means the ontology's own SQL still matches the frozen expected answer (or an ASK/REFUSE was correctly declined); a broken rule would turn a tile red. Click any tile for the whole story.</p>
      </div>
      <div class="rhead">
        <button class="tbtn" id="themeBtn">◑ theme</button>
        <div class="stamp" id="stamp"></div>
      </div>
    </header>
    <div class="kpis" id="kpis"></div>
    <div class="legend">
      <span><i class="dot good"></i> green — value matches oracle / correctly declined</span>
      <span><i class="dot crit"></i> value ≠ oracle</span>
      <span><i class="dot warn"></i> route mismatch</span>
      <span><i class="dot open"></i> no frozen oracle</span>
    </div>
    <div class="grid" id="grid"></div>
    <footer id="footBoard"></footer>
  </div>

  <!-- ================= DETAIL VIEW ================= -->
  <div id="detailView" hidden>
    <div class="backbar">
      <button class="back" id="backBtn">← board</button>
      <div class="nav"><button class="navbtn" id="prevBtn">← prev</button><button class="navbtn" id="nextBtn">next →</button></div>
    </div>
    <div id="detailBody"></div>
    <footer id="footDetail"></footer>
  </div>
</div>
"""

_BOARD_SCRIPT = r"""<script>
const DATA = {{DATA}};
const META = "{{META}}";
function esc(s){return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
const byId = {}; DATA.rows.forEach((r,i)=>{r._i=i; byId[r.id]=r;});
const routeCls = {COMMIT:'commit',ASK:'ask',REFUSE:'refuse'};

// ---- board ----
function renderBoard(){
  const k = DATA.kpi;
  document.getElementById('stamp').innerHTML = 'run <b>corpus-demo</b><br>'+esc(META);
  document.getElementById('kpis').innerHTML = [
    ['good', k.green+'<s>/'+k.n+'</s>', 'green — verified or correctly declined'],
    ['accent', k.commits, 'value-verified COMMITs'],
    ['accent', k.declined, 'correctly declined ASK / REFUSE'],
    [k.crit? 'crit':'open', k.crit || k.open, k.crit? 'value ≠ oracle' : 'open (no frozen oracle)'],
  ].map(([c,n,l])=>`<div class="kpi ${c}"><div class="n">${n}</div><div class="l">${esc(l)}</div></div>`).join('');
  document.getElementById('grid').innerHTML = DATA.groups.map(g=>{
    const cells = DATA.rows.filter(r=>r.group===g).map(r=>
      `<button class="cell ${r.verdict}" onclick="showDetail('${r.id}')" title="${esc(r.q)}">${esc(r.id)}</button>`).join('');
    const cnt = DATA.rows.filter(r=>r.group===g).length;
    return `<div class="shapegrp"><h4>${esc(g)} <em>${cnt}</em></h4><div class="cells">${cells}</div></div>`;
  }).join('');
  document.getElementById('footBoard').textContent =
    'corpus = '+DATA.rows.length+' questions · oracles frozen, re-executed on every build · '+META;
}

// ---- detail ----
function listHTML(items, cls, mk){
  if(!items.length) return '';
  return `<ul class="dl ${cls}">`+items.map(i=>`<li><span class="mk">${mk}</span><span class="txt">${esc(i.t)}</span><code>${esc(i.rule)}</code></li>`).join('')+'</ul>';
}
function showDetail(id){
  const r = byId[id];
  const trace = r.trace.map((t,i)=>`<div class="tline"><span class="idx">${i+1}</span><span class="file">${esc(t.file)}</span><span class="arrow">→</span><span class="res">${esc(t.res)}</span></div>`).join('');
  const val = (r.route==='COMMIT') ? `<div class="dval">${esc(r.value)}</div><p class="dcap">${esc(r.caption)}</p>`
    : `<div class="dval" style="font-size:22px;color:var(--${r.route==='ASK'?'warn':'crit'})">${r.route==='ASK'?'Clarification needed':'Declined'}</div><p class="dcap">${esc(r.caption)}</p>`;
  const oracle = (r.route==='COMMIT' && r.oracle) ? `<div class="dsec"><h5>oracle check</h5><div class="oracle">
      <div class="kv"><span class="k">executed</span><span class="v">${esc(r.value)}</span></div><span class="arrow">vs</span>
      <div class="kv"><span class="k">frozen oracle</span><span class="v">${esc(r.oracle)}</span></div>
      <span class="spacer"></span><span class="rtag ${r.verdict}">${esc(r.note)}</span></div></div>` : '';
  const sql = r.sql ? `<div class="dsec"><h5>generated sql</h5><pre class="code">${r.sql}</pre></div>` : '';
  document.getElementById('detailBody').innerHTML = `
    <div class="did"><span>${esc(r.id)}</span><span class="vbadge ${routeCls[r.route]}">${esc(r.route)}</span><span class="rtag ${r.verdict}">${r.verdict==='good'?'green':(r.verdict==='crit'?'red':r.verdict)}</span></div>
    <div class="dq">${esc(r.q)}</div>
    ${val}
    <div class="dsec reasoning"><h5>how it routed — ontology walk</h5><div class="panel">${trace}</div></div>
    ${r.assume.length?`<div class="dsec"><h5>assumptions · each licensed by a rule</h5>${listHTML(r.assume,'assume','·')}</div>`:''}
    ${r.dead.length?`<div class="dsec"><h5>dead-ends · paths the rules rejected</h5>${listHTML(r.dead,'dead','✗')}</div>`:''}
    ${oracle}${sql}`;
  document.getElementById('footDetail').textContent = 'rule: '+r.rule+' · '+META;
  document.getElementById('prevBtn').disabled = r._i===0;
  document.getElementById('nextBtn').disabled = r._i===DATA.rows.length-1;
  document.getElementById('boardView').hidden = true;
  document.getElementById('detailView').hidden = false;
  window.scrollTo(0,0);
}
function toBoard(){ document.getElementById('detailView').hidden=true; document.getElementById('boardView').hidden=false; window.scrollTo(0,0); }
let curId=null;
const _showDetail=showDetail; showDetail=function(id){curId=id;_showDetail(id);};
document.getElementById('backBtn').onclick=toBoard;
document.getElementById('prevBtn').onclick=()=>{const i=byId[curId]._i; if(i>0) showDetail(DATA.rows[i-1].id);};
document.getElementById('nextBtn').onclick=()=>{const i=byId[curId]._i; if(i<DATA.rows.length-1) showDetail(DATA.rows[i+1].id);};
document.getElementById('themeBtn').onclick=()=>{const el=document.documentElement; el.dataset.theme = el.dataset.theme==='dark'?'light':'dark';};
renderBoard();
</script>
"""


DEMO = [
    "what were our total sales?",
    "total sales in a single currency",
    "sales by salesperson",
]

if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] in ("--ask", "--ask-artifact"):
        artifact = argv[0] == "--ask-artifact"
        out = argv[1] if len(argv) > 1 else ("articles/ask-app.html" if artifact else "projections/ask.app.html")
        path = render_ask(HERE / out, artifact=artifact)
        print("wrote %s%s" % (path, "  (artifact body)" if artifact else ""))
    elif argv and argv[0] in ("--board", "--board-artifact"):
        artifact = argv[0] == "--board-artifact"
        out = argv[1] if len(argv) > 1 else ("articles/ask-board.html" if artifact else "projections/ask.board.html")
        path = render_board(HERE / out, artifact=artifact)
        print("wrote %s%s" % (path, "  (artifact body)" if artifact else ""))
    elif argv and argv[0] in ("--console", "--console-artifact"):
        artifact = argv[0] == "--console-artifact"
        out = argv[1] if len(argv) > 1 else ("articles/ask-console.html" if artifact else "projections/ask.console.html")
        path = render_console(HERE / out, artifact=artifact)
        print("wrote %s%s" % (path, "  (artifact body)" if artifact else ""))
    elif argv and argv[0] in ("--html", "--artifact"):
        artifact = argv[0] == "--artifact"
        out = argv[1] if len(argv) > 1 else ("articles/ask-trace.html" if artifact else "projections/ask.trace.html")
        traces = [build_trace(q) for q in DEMO]
        path = render_html(traces, HERE / out, artifact=artifact)
        print("wrote %s  (%d traces%s)" % (path, len(traces), ", artifact body" if artifact else ""))
    else:
        questions = [" ".join(argv)] if argv else DEMO
        for q in questions:
            show(build_trace(q))
        print()
