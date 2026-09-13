#!/usr/bin/env python3
"""
build_site.py — assemble the static article site (for Cloudflare Pages) from the article sources.

  python3 build_site.py            # -> site/  (index.html, articles/1..4.html, style.css, explorer.html, assets/)

Converts each articles/0N-*.md to a clean reading page, inlines every `> [visual — …]` figure from the
rendered PNGs, builds a landing index, and copies the live explorer. Pure static output — no backend.
"""
import html as _html
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = HERE / "articles"
OUT = HERE / "site"

# ---- byline / footer links ----
GITHUB = "https://github.com/d6z7/mac-ontology-contoso"
LINKEDIN = "https://www.linkedin.com/in/drazenzubovic/"
AUTHOR = "Drazen Zubovic"


def site_foot():
    links = '<a href="%s">code on GitHub</a>' % GITHUB
    if LINKEDIN:
        links += ' · <a href="%s">%s on LinkedIn</a>' % (LINKEDIN, _html.escape(AUTHOR))
    return "Meaning as Code — a public demo on the MIT-licensed Contoso dataset · " + links

# ---- the series ----
ARTICLES = [
    ("01-the-layer-you-deleted--v2-hardened.md", "The Layer You Deleted",
     "An LLM can replace most of your application layer — but not the part that made the numbers mean anything."),
    ("02-meaning-as-code.md", "Meaning as Code",
     "Inside the home for meaning: what's in it, why it's prose a human owns and a machine runs, and why we keep it like code."),
    ("03-from-data-to-meaning.md", "From Data to Meaning",
     "Where the ontology comes from: the model drafts the structure from your data; you author the meaning it can't."),
    ("04-meaning-that-grows.md", "Meaning That Grows",
     "The model tells you where it's thin. You teach it — in plain language — and it grows, provably and legibly."),
]

# ---- [visual — desc] → asset image(s). matched by first key found in the description ----
VMAP = [
    ("layer you deleted", ["01-layer-diagram.png"]),
    ("rdf/owl", ["01-rdf-vs-prose.png"]),
    ("opposite routes", ["ask-01-refuse-salesperson.png", "ask-02-commit-top-products.png"]),
    ("file is the bridge", ["02-human-machine-bridge.png"]),
    ("building blocks", ["02-building-blocks.png"]),
    ("semantic spectrum", ["02-semantic-spectrum.png"]),
    ("determinism dial", ["02-determinism-dial.png"]),
    ("many projections", ["02-project-anywhere.png"]),
    ("probes the data", ["03-probe-propose.png"]),
    ("structure vs meaning", ["03-structure-vs-meaning.png"]),
    ("test it", ["03-see-test-drift.png"]),
    ("the refusal", ["margin-01-refuse-before.png"]),
    ("the edit", ["04-margin-extension.png"]),
    ("the commit", ["margin-02-commit-after.png"]),
    ("the trace", ["04-trace-fired-deadends.png"]),
]


def resolve_visual(desc):
    d = desc.lower()
    for key, assets in VMAP:
        if key in d:
            cap = _html.escape(re.sub(r"\s+", " ", desc).strip())
            imgs = "".join('<img src="../assets/%s" alt="%s" loading="lazy">' % (a, cap) for a in assets)
            cls = " pair" if len(assets) > 1 else ""
            return '<figure class="fig%s">%s<figcaption>%s</figcaption></figure>' % (cls, imgs, cap)
    return "<!-- unresolved visual: %s -->" % _html.escape(desc)


def _inline(t):
    t = _html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"<em>\1</em>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', t)
    return t


def md_to_html(md):
    md = re.sub(r"^\s*<!--.*?-->\s*", "", md, flags=re.S)   # strip leading comment
    lines = md.split("\n")
    out, i, n = [], 0, len(md.split("\n"))
    lines = md.split("\n")
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, _inline(m.group(2)), lvl))
            i += 1
            continue
        if re.match(r"^-{3,}$", s):
            out.append("<hr>")
            i += 1
            continue
        if s.startswith(">"):
            blk = []
            while i < n and lines[i].strip().startswith(">"):
                blk.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            bt = "\n".join(blk).strip()
            vm = re.search(r"\[visual\s*[—\-]\s*(.*?)\]", bt)
            if vm:
                out.append(resolve_visual(vm.group(1)))
            else:
                out.append("<blockquote>%s</blockquote>" % _inline(" ".join(l.strip() for l in blk)))
            continue
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % _inline(it) for it in items))
            continue
        para = []
        while i < n and lines[i].strip() and not re.match(r"^(#{1,4}\s|>|[-*]\s|-{3,}$)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % _inline(" ".join(para)))
    return "\n".join(out)


# ---- templates ----
def art_page(num, title, body, prev, nxt):
    total = len(ARTICLES)
    nav = []
    nav.append('<a class="home" href="../index.html">← the series</a>')
    pn = ('<a href="%d.html">← %s</a>' % (prev[0], _html.escape(prev[1]))) if prev else "<span></span>"
    nn = ('<a href="%d.html">%s →</a>' % (nxt[0], _html.escape(nxt[1]))) if nxt else "<span></span>"
    return PAGE.format(
        title=_html.escape(title), css="../style.css",
        crumb='<a href="../index.html">Meaning as Code</a> · Part %d of %d' % (num, total),
        body='<article><p class="kicker">Part %d</p>%s</article>' % (num, body),
        foot='<nav class="pn">%s%s</nav>' % (pn, nn),
        home="../index.html", sitefoot=site_foot())


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<link rel="stylesheet" href="{css}"></head><body>
<header class="top"><div class="wrap"><span class="crumb">{crumb}</span></div></header>
<main class="wrap read">{body}{foot}</main>
<footer class="site"><div class="wrap">{sitefoot}</div></footer>
</body></html>"""


def landing():
    cards = ""
    for idx, (_, title, dek) in enumerate(ARTICLES, 1):
        cards += ('<a class="card" href="articles/%d.html"><span class="num">%02d</span>'
                  '<span class="ct"><b>%s</b><span class="cd">%s</span></span>'
                  '<span class="go">Read →</span></a>' % (idx, idx, _html.escape(title), _html.escape(dek)))
    return LANDING.format(cards=cards, sitefoot=site_foot())


LANDING = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Meaning as Code</title>
<link rel="stylesheet" href="style.css"></head><body>
<main class="wrap landing">
  <p class="eyebrow">Meaning as code</p>
  <h1 class="hero">Answers you can <span class="g">defend</span> — from your own data.</h1>
  <p class="lede">An AI that answers from what your data <b>means</b>, not just what it stores: it shows its
  reasoning, refuses what it can't ground, and gets sharper each time you teach it — in plain language, by
  the people who know the business. A four-part series, worked end-to-end on a public demo.</p>
  <div class="chips"><span class="chip">● early-stage concept</span><span class="chip">working proof-of-concept</span><span class="chip">MIT / public data</span></div>

  <h2 class="sh">The series</h2>
  <div class="cards">{cards}</div>

  <h2 class="sh">See it &amp; run it</h2>
  <div class="cards2">
    <a class="card2" href="explorer.html"><b>Browse the model →</b><span>The live explorer: 8 concepts, 13 rules, every binding — the ontology, clickable.</span></a>
    <a class="card2" href="https://github.com/d6z7/mac-ontology-contoso"><b>Run it yourself →</b><span>The code on GitHub: the warehouse, the ontology, and the live <code>/ask</code> app. MIT.</span></a>
  </div>
</main>
<footer class="site"><div class="wrap">{sitefoot}</div></footer>
</body></html>"""


CSS = """*{box-sizing:border-box}
:root{--ink:#141a22;--muted:#4c5663;--faint:#8a94a3;--hair:#e4e7ec;--bg:#fbfcfd;--card:#fff;--accent:#1f5fe0;--accent-soft:#1f5fe00c;
  --sans:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.65;font-size:18px}
.wrap{max-width:760px;margin:0 auto;padding:0 22px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.top{border-bottom:1px solid var(--hair);background:#fff;position:sticky;top:0;z-index:5}
.crumb{display:block;padding:13px 0;font-family:var(--mono);font-size:12.5px;color:var(--muted)}
.read{padding:20px 22px 60px}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);margin:8px 0 0}
article h1{font-size:clamp(30px,5vw,42px);line-height:1.08;letter-spacing:-.022em;margin:6px 0 6px;font-weight:720;text-wrap:balance}
article h2{font-size:24px;line-height:1.2;letter-spacing:-.015em;margin:44px 0 2px;font-weight:680}
article h3{font-size:19px;margin:32px 0 0;font-weight:660}
article p{margin:16px 0}
article > p:first-of-type,article h1 + p{font-size:20px;color:var(--muted)}
article em{font-style:italic}article strong{font-weight:680}
article code{font-family:var(--mono);font-size:.86em;background:#eef1f6;border:1px solid var(--hair);border-radius:5px;padding:1px 5px}
article ul{margin:16px 0;padding-left:24px}article li{margin:8px 0}
article blockquote{margin:22px 0;padding:14px 20px;border-left:3px solid var(--accent);background:var(--accent-soft);border-radius:0 10px 10px 0;font-size:18px}
article blockquote p{margin:6px 0}
article hr{border:0;border-top:1px solid var(--hair);margin:40px 0}
figure.fig{margin:30px 0;text-align:center}
figure.fig img{max-width:100%;width:min(920px,100%);border:1px solid var(--hair);border-radius:12px;box-shadow:0 1px 2px #1018280d,0 12px 34px #10182812}
figure.fig.pair{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}
figure.fig.pair img{width:calc(50% - 8px);min-width:280px}
figure.fig figcaption{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:10px;line-height:1.4}
.pn{display:flex;justify-content:space-between;gap:16px;margin-top:50px;padding-top:22px;border-top:1px solid var(--hair);font-weight:600}
.pn a{max-width:46%}
.home{font-family:var(--mono);font-size:13px}
.site{border-top:1px solid var(--hair);background:#fff;font-family:var(--mono);font-size:12.5px;color:var(--muted)}
.site .wrap{padding:20px 22px}

/* landing */
.landing{max-width:860px;padding:60px 22px 70px}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint)}
.hero{font-size:clamp(34px,6vw,56px);line-height:1.03;letter-spacing:-.028em;margin:14px 0 0;font-weight:740;text-wrap:balance}
.hero .g{color:var(--accent)}
.lede{font-size:clamp(17px,2vw,20px);line-height:1.55;color:var(--muted);max-width:62ch;margin:20px 0 0}
.lede b{color:var(--ink)}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}
.chip{font-family:var(--mono);font-size:11.5px;color:var(--muted);background:var(--card);border:1px solid var(--hair);border-radius:20px;padding:6px 12px}
.sh{font-size:14px;font-family:var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--faint);margin:52px 0 16px;font-weight:600}
.cards{display:flex;flex-direction:column;gap:12px}
.card{display:flex;align-items:center;gap:18px;background:var(--card);border:1px solid var(--hair);border-radius:14px;padding:18px 20px;box-shadow:0 1px 2px #1018280a;transition:.14s}
.card:hover{border-color:var(--accent);text-decoration:none;transform:translateY(-1px);box-shadow:0 8px 24px #10182814}
.card .num{font-family:var(--mono);font-size:22px;font-weight:700;color:var(--accent);flex:0 0 auto}
.card .ct{display:flex;flex-direction:column;gap:3px;min-width:0}
.card .ct b{font-size:18px;font-weight:680;color:var(--ink)}
.card .cd{font-size:14px;color:var(--muted);line-height:1.45}
.card .go{margin-left:auto;font-family:var(--mono);font-size:13px;color:var(--accent);flex:0 0 auto;align-self:center}
.cards2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:640px){.cards2{grid-template-columns:1fr}.card .go{display:none}}
.card2{display:flex;flex-direction:column;gap:6px;background:var(--card);border:1px solid var(--hair);border-radius:14px;padding:18px 20px;box-shadow:0 1px 2px #1018280a;transition:.14s}
.card2:hover{border-color:var(--accent);text-decoration:none}
.card2 b{font-size:17px;color:var(--ink)}.card2 span{font-size:14px;color:var(--muted);line-height:1.45}
.card2 code{font-family:var(--mono);font-size:.85em;background:#eef1f6;border-radius:4px;padding:1px 4px}
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "articles").mkdir(parents=True)
    (OUT / "assets").mkdir()
    (OUT / "style.css").write_text(CSS, encoding="utf-8")

    # article pages
    used = set()
    for idx, (fn, title, _dek) in enumerate(ARTICLES, 1):
        md = (ART / fn).read_text(encoding="utf-8")
        body = md_to_html(md)
        for a in re.findall(r'src="(?:\.\./)?assets/([^"]+)"', body):
            used.add(a)
        prev = (idx - 1, ARTICLES[idx - 2][1]) if idx > 1 else None
        nxt = (idx + 1, ARTICLES[idx][1]) if idx < len(ARTICLES) else None
        (OUT / "articles" / ("%d.html" % idx)).write_text(art_page(idx, title, body, prev, nxt), encoding="utf-8")

    # landing + explorer
    (OUT / "index.html").write_text(landing(), encoding="utf-8")
    shutil.copyfile(HERE / "projections" / "contoso.explorer.html", OUT / "explorer.html")

    # assets actually referenced
    for a in sorted(used):
        src = ART / a
        if src.exists():
            shutil.copyfile(src, OUT / "assets" / a)
        else:
            print("  ! missing asset:", a)

    print("built %s — %d articles, %d assets, index + explorer" % (OUT, len(ARTICLES), len(used)))
    print("  unresolved visuals:", sum(1 for i in range(1, 5)
          for _ in re.findall(r"unresolved visual", (OUT / "articles" / ("%d.html" % i)).read_text())))


if __name__ == "__main__":
    main()
