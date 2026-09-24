"""replay_diff.py — what did a planner change actually MOVE, across the whole corpus?

WHY. `ne` stopped meaning `<>` and a declared collapse started reading its own `natural_key`.
Both change SQL SEMANTICS for every question in every bundle, not just the ones they were written
for. Shipping that on the strength of four hand-checked numbers is how a fix becomes a regression.

WHAT IT DOES. Replays every RECORDED intent (`acceptance/intents.yaml`) through the planner AS IT
IS NOW, executes it read-only, and diffs the value against the committed capture
(`acceptance/answers/<id>.yaml`). No model is called and no capture is rewritten — which is the
point: the interpreter is held fixed so every difference is attributable to the planner.

WHAT A DIFFERENCE MEANS. Nothing, on its own. The recorded captures are dated 2026-09-23 and
predate several fixes, so a moved number may be a repair or a regression and this tool cannot tell
them apart. It says WHICH questions moved and BY HOW MUCH; the anchors say which direction was
right, and only for the 17 questions that have one.

    python acceptance/tools/replay_diff.py [--db <duckdb>] [--only RC05,STORE-02]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path("/Users/e6db365/dev/mac-ontology-contoso")


def _numeric(row) -> float | None:
    """The first value in the row that is a number, Decimal included. None if there is none."""
    for cell in row:
        if isinstance(cell, bool):
            continue
        try:
            return float(cell)
        except (TypeError, ValueError):
            continue
    return None


def _digest(rows) -> float | None:
    """An order-independent summary of a result: the value for a scalar, the SUM for a series.

    Not a perfect comparator -- two different series can sum alike -- but it is stable, which is
    the property that matters for "did this change?". The row count is carried alongside it by
    the caller so a shape change is not hidden inside an equal sum.
    """
    if not rows:
        return None
    if len(rows) == 1:
        return _numeric(rows[0])
    total, seen = 0.0, False
    for r in rows:
        v = _numeric(r[::-1])  # the measure is the LAST column; slices come first
        if v is not None:
            total += v
            seen = True
    return round(total, 6) if seen else None  # float addition order varies; the report must not


def _recorded_value(doc: dict):
    for path in (("result", "value"), ("answer_parts", "value")):
        cur = doc
        for k in path:
            cur = (cur or {}).get(k) if isinstance(cur, dict) else None
        if isinstance(cur, (int, float)):
            return float(cur)
    return None


def _anchor_for(qid: str) -> float | None:
    """The independently derived value, when this question has one. Never the engine's."""
    for f in sorted((ROOT / "acceptance" / "anchors").glob("*.yaml")):
        doc = yaml.safe_load(f.read_text()) or {}
        if f"({qid})" in str(doc.get("question", "")):
            v = (doc.get("expected") or {}).get("value")
            return float(v) if isinstance(v, (int, float)) else None
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--db", default=str(ROOT / "contoso.duckdb"))
    ap.add_argument("--only", help="comma-separated question ids")
    a = ap.parse_args(argv)

    sys.path.insert(0, str(ROOT / "acceptance" / "tools"))
    import duckdb
    from intent_killtest import build, _fill
    from mac_runtime.models import Intent, Plan
    from mac_runtime.planner import plan as run_plan

    index, resolver = build()
    con = duckdb.connect(a.db, read_only=True)
    recorded = yaml.safe_load((ROOT / "acceptance" / "intents.yaml").read_text())["questions"]
    wanted = set(a.only.split(",")) if a.only else None

    moved, same, refused_now, planned_now, errors = [], [], [], [], []

    for entry in recorded:
        qid = entry["id"]
        if wanted and qid not in wanted:
            continue
        ans_path = ROOT / "acceptance" / "answers" / f"{qid}.yaml"
        doc = yaml.safe_load(ans_path.read_text()) if ans_path.exists() else {}
        before = _recorded_value(doc or {})
        was_refused = before is None

        try:
            intent = Intent.model_validate(_fill(dict(entry["intent"], confidence=1.0)))
        except Exception as exc:
            errors.append((qid, f"intent invalid: {type(exc).__name__}"))
            continue
        try:
            p = run_plan(intent, index, resolver)
        except Exception as exc:
            errors.append((qid, f"plan raised {type(exc).__name__}: {str(exc)[:60]}"))
            continue
        if not isinstance(p, Plan):
            if not was_refused:
                refused_now.append((qid, before, type(p).__name__))
            continue

        # BIND, DO NOT STRING-REPLACE. A naive `sql.replace(":brand", ...)` corrupts `:brand_1`
        # into `'X'_1`, and the first version of this tool reported 16 "execute failed" errors
        # that were entirely its own -- including a `syntax error at or near "ne"`, which read
        # exactly like a planner regression in the operator I had just changed. DuckDB takes
        # `$name` with a dict, so the substitution problem is handed to the driver.
        sql = re.sub(r":([A-Za-z_]\w*)", r"$\1", p.sql_preview)
        try:
            rows = con.execute(sql, dict(p.params or {})).fetchall()
        except Exception as exc:
            errors.append((qid, f"execute failed: {str(exc)[:60]}"))
            continue
        # A MULTI-ROW RESULT HAS NO FIRST ROW. The planner emits GROUP BY without ORDER BY, so
        # `rows[0]` is an arbitrary group and varies between runs of the SAME code: ADV-04 (12
        # monthly groups) returned three different values across six runs and read exactly like
        # planner non-determinism. It was this tool. Comparing a digest that does not depend on
        # row order is the fix; the planner is deterministic.
        after = _digest(rows)

        if was_refused:
            planned_now.append((qid, after))
        elif after is None:
            errors.append((qid, "planned and executed, but no numeric value in the first row"))
        elif abs(after - before) > 1e-6:
            moved.append((qid, before, after, _anchor_for(qid)))
        elif len(rows) != ((doc.get("result") or {}).get("rows") or len(rows)):
            moved.append((qid, before, after, _anchor_for(qid)))
        else:
            same.append(qid)

    print(f"\n{'=' * 84}\nREPLAY DIFF — recorded intents through the planner as it is now\n{'=' * 84}")
    print(f"  unchanged        {len(same):>4}")
    print(f"  MOVED            {len(moved):>4}")
    print(f"  refuses now      {len(refused_now):>4}   (planned when captured)")
    print(f"  plans now        {len(planned_now):>4}   (refused when captured)")
    print(f"  errors           {len(errors):>4}")

    if moved:
        print(f"\n  MOVED — anchor is the independently derived value, '·' means none exists:")
        print(f"    {"id":<12}{"captured":>20}{"now":>20}{"anchor":>20}   verdict")
        for qid, b, aft, anc in moved:
            v = "·"
            if anc is not None and aft is not None:
                v = "-> ANCHOR" if abs(aft - anc) < 1e-6 else (
                    "away from anchor" if abs(b - anc) < 1e-6 else "still off")
            bs = f"{b:,.2f}".rstrip("0").rstrip(".") if b is not None else "—"
            as_ = f"{aft:,.2f}".rstrip("0").rstrip(".") if aft is not None else "—"
            ans = f"{anc:,.2f}".rstrip("0").rstrip(".") if anc is not None else "·"
            print(f"    {qid:<12}{bs:>20}{as_:>20}{ans:>20}   {v}")
    for label, rows_ in (("REFUSES NOW", refused_now), ("PLANS NOW", planned_now),
                         ("ERRORS", errors)):
        if rows_:
            print(f"\n  {label}:")
            for r in rows_:
                print("    " + "  ".join(str(x) for x in r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
