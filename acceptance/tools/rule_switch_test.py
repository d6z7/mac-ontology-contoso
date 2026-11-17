"""rule_switch_test.py — an answer follows its rule, and switching the rule switches the answer.

Operator, 2026-11-17: "the answer depends on the rule you set. you can set i one way or another way. the ruling must be
transparent and must be changeable. it can be ruled and then is the discussion finished. you should test only if by
switching the rule you get different resutls." — and — "the answer must follow ruling ... you only need to prove that".

A reference that depends on a choice rule says so in `follows`: the rule, the option its top-level answer assumes, and
under `otherwise.<option>` the answer (statement and figure) under every other option. `<option>` is an option of the
rule's choice, or a default keyword the grammar allows (`all` = no filter, `ask` = asked back; GRAMMAR_v3 §2.4, L3).

Per reference and rule, this checks, against the warehouse:
  FOLLOWS     the rule exists, acts (proposed | ruled) and its CURRENT default is the option the answer assumes.
  REPRODUCES  the top-level statement returns the top-level figure (sdk.acceptance.selfcheck.verify).
  per option  its statement returns its figure, and that figure DIFFERS from the default's or is the SAME
              (sdk.acceptance.selfcheck.compare — the one comparator for "same answer").
  BINDING     the mutation twin: set the rule's default to each other option (in memory) and FOLLOWS must fail,
              naming the answer the reference then has to carry. A reference that still "follows" a switched rule
              is not bound to it.
  ENGINE      (--engine) for a reference with a pinned interpreter intent, the rule's default is flipped in a copy of
              the bundle and the intent re-planned by the runtime (no model, no warehouse) through
              mac_keys_change_an_answer's own copy and replay: CHANGED, SAME, or both refused.

Per rule: an option no reference distinguishes from the default is UNDISTINGUISHED — the corpus does not test it
(the rule is dead there or untested). A rule with no distinguished option fails.

    python acceptance/tools/rule_switch_test.py [--warehouse <bundle root>] [--engine --variants <dir>] [--json <path>]

--warehouse: a bundle root whose connection and warehouse file to read (default: this bundle); read-only.
Needs meaning-as-code ($MAC_ROOT) for the comparator and, with --engine, the runtime ($MAC_RUNTIME_SRC or beside it).
Exit 0 = every answer follows its rule and every rule switches at least one answer; 1 = a failure; 2 = cannot run.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(os.environ.get("MAC_BUNDLE_ROOT") or Path(__file__).resolve().parents[2])
KEYWORDS = {"all", "ask"}            # default values the grammar allows besides an option (GRAMMAR_v3 §2.4)
ACTS = {"proposed", "ruled"}         # only these states act (L3)


def mac_root() -> Path | None:
    for cand in (os.environ.get("MAC_ROOT"), os.environ.get("MAC_REPO")):
        if cand and (Path(cand) / "sdk" / "acceptance" / "selfcheck.py").is_file():
            return Path(cand)
    return None


def load_rules(root: Path) -> dict:
    out = {}
    for p in sorted((root / "ontology" / "rules").glob("*.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        out[d.get("rule", p.stem)] = d
    return out


def references(root: Path) -> list:
    out = []
    for p in sorted((root / "acceptance" / "reference").glob("*.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        if d.get("follows"):
            out.append(d)
    return out


def follows_check(rules: dict, entry: dict, override: dict | None = None) -> str | None:
    """None when the reference follows the rule's current default, else why not."""
    rid, opt = entry.get("rule"), entry.get("option")
    r = rules.get(rid)
    if r is None:
        return f"rule {rid} does not exist"
    if r.get("state") not in ACTS:
        return f"rule {rid} is {r.get('state')!r}: only proposed and ruled rules act"
    ch = r.get("choice") or {}
    if not ch:
        return f"rule {rid} is not a choice"
    default = (override or {}).get(rid, ch.get("default"))
    if default != opt:
        return f"rule {rid} defaults to {default!r}; the answer assumes {opt!r}"
    names = set((ch.get("options") or {}).keys()) | KEYWORDS
    bad = [o for o in [opt, *(entry.get("otherwise") or {})] if o not in names]
    if bad:
        return f"rule {rid} has no option {bad}"
    return None


def outcome_of(doc: dict, selfcheck) -> str | None:
    return selfcheck.withheld(doc)


def compare_answers(selfcheck, want, got_res) -> bool:
    v, _ = selfcheck.compare(want, got_res["columns"], got_res["rows"], got_res["row_count"],
                             capped=got_res.get("capped", False))
    return v in selfcheck.SOUND


def engine_switch(root: Path, variants: Path, rules: dict, refs: list) -> dict:
    """{(id, rule, option): CHANGED | SAME | BOTH REFUSED | RUNTIME REFUSES THE SETTING | NO INTENT | DID NOT LOAD}
    by flipping the default in a
    copy of the bundle and re-planning the pinned intent — mac_keys_change_an_answer's write_variant and replay."""
    sys.path.insert(0, str(mac_root() / "tools"))
    import _neighbours  # noqa: E402
    _neighbours.ensure_runtime_on_path()
    import mac_keys_change_an_answer as K  # noqa: E402
    import mac_model as M  # noqa: E402

    intents, _ = K.corpus(root)
    out: dict = {}
    wanted = {}
    for d in refs:
        for e in d["follows"]:
            for opt in e.get("otherwise") or {}:
                if d["id"] in intents:
                    wanted.setdefault((e["rule"], opt), []).append(d["id"])
                else:
                    out[(d["id"], e["rule"], opt)] = "NO INTENT"
    if not wanted:
        return out
    ids = sorted({i for v in wanted.values() for i in v})
    base_dir = variants / "baseline"
    K.write_variant(root, base_dir, None)
    base = K.replay(base_dir, {i: intents[i] for i in ids})
    if isinstance(base, str):
        return {(i, r, o): f"DID NOT LOAD: {base}" for (r, o), v in wanted.items() for i in v}
    for (rid, opt), qids in sorted(wanted.items()):
        vdir = variants / f"{rid}={opt}"
        K.write_variant(root, vdir, None)
        rp = vdir / "ontology" / "rules" / f"{rid}.yaml"
        doc = yaml.safe_load(rp.read_text(encoding="utf-8"))
        doc["choice"]["default"] = opt
        rp.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
        M.clear_cache()
        after = K.replay(vdir, {i: intents[i] for i in qids})
        for i in qids:
            if isinstance(after, str):
                out[(i, rid, opt)] = f"DID NOT LOAD: {after[:120]}"
                continue
            b, a = base.get(i, ""), after.get(i, "")
            if a.startswith("raised") and not b.startswith("raised"):
                out[(i, rid, opt)] = "RUNTIME REFUSES THE SETTING: " + a[7:140]
            elif a != b:
                out[(i, rid, opt)] = "CHANGED"
            elif '"type": "Refusal"' in b or b.startswith("raised"):
                out[(i, rid, opt)] = "BOTH REFUSED"
            else:
                out[(i, rid, opt)] = "SAME"
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--warehouse", help="a bundle root whose connection and warehouse to read (default: this bundle)")
    ap.add_argument("--engine", action="store_true", help="also flip each default in a bundle copy and re-plan")
    ap.add_argument("--variants", help="with --engine: where the bundle copies are written (never inside the bundle)")
    ap.add_argument("--json", help="write the run record here")
    a = ap.parse_args(argv)
    mac = mac_root()
    if mac is None:
        print("COULD NOT RUN: rule_switch_test — set $MAC_ROOT to a meaning-as-code checkout (sdk/acceptance/selfcheck.py)")
        return 2
    sys.path.insert(0, str(mac))
    from sdk.acceptance import selfcheck  # noqa: E402

    wh = Path(a.warehouse).resolve() if a.warehouse else ROOT
    rules, refs = load_rules(ROOT), references(ROOT)
    if not refs:
        print("COULD NOT RUN: rule_switch_test — no reference declares `follows`: an empty run proves nothing")
        return 2
    if a.engine and not a.variants:
        print("COULD NOT RUN: rule_switch_test — --engine needs --variants <dir> outside the bundle")
        return 2

    failures, rows = [], []
    per_option: dict = {}            # (rule, option) -> {"differs": [ids], "same": [ids]}
    for d in refs:
        rid_ = d["id"]
        top_withheld = outcome_of(d, selfcheck)
        ver = selfcheck.verify(wh, d)
        if ver["verdict"] not in selfcheck.SOUND and not (top_withheld and ver["verdict"] == "REFUSAL-EXPECTING"):
            failures.append(f"{rid_}: REPRODUCES failed — {ver['verdict']}: {ver.get('detail', '')[:160]}")
        top_res = None if top_withheld else selfcheck.run(wh, str(d.get("sql") or ""))
        for e in d["follows"]:
            why = follows_check(rules, e)
            if why:
                failures.append(f"{rid_}: FOLLOWS failed — {why}")
            for opt, alt in (e.get("otherwise") or {}).items():
                key = (e["rule"], opt)
                slot = per_option.setdefault(key, {"differs": [], "same": []})
                alt_withheld = outcome_of(alt, selfcheck)
                if alt_withheld or top_withheld:
                    differs = bool(alt_withheld) != bool(top_withheld)
                    shown = alt.get("expected_outcome") if alt_withheld else alt.get("expected")
                else:
                    av = selfcheck.verify(wh, {"id": rid_, **alt})
                    if av["verdict"] not in selfcheck.SOUND:
                        failures.append(f"{rid_}: {e['rule']}={opt} does not reproduce its own figure — "
                                        f"{av['verdict']}: {av.get('detail', '')[:160]}")
                        continue
                    alt_res = selfcheck.run(wh, alt["sql"])
                    differs = not compare_answers(selfcheck, d.get("expected"), alt_res) or \
                        not (top_res and top_res.get("ok") and compare_answers(selfcheck, alt.get("expected"), top_res))
                    shown = alt.get("expected")
                slot["differs" if differs else "same"].append(rid_)
                # BINDING: the mutation twin — with the default set to `opt`, the reference must stop following
                bound = follows_check(rules, e, override={e["rule"]: opt}) is not None
                if not bound:
                    failures.append(f"{rid_}: BINDING failed — setting {e['rule']} to {opt!r} leaves it 'following'")
                rows.append({"id": rid_, "rule": e["rule"], "default": e["option"], "option": opt,
                             "verdict": "DIFFERS" if differs else "SAME", "bound": bound,
                             "default_answer": d.get("expected", d.get("expected_outcome")), "option_answer": shown})

    engine = engine_switch(ROOT, Path(a.variants).resolve(), rules, refs) if a.engine else {}

    def brief(v):
        if isinstance(v, dict):
            return f"{v.get('rows')} rows" + (f", first {v['values'][0]}" if v.get("values") else "")
        return str(v)

    print(f"  {len(refs)} reference(s) follow a rule; {len(rows)} (reference, other option) switch(es) run "
          f"against {wh.name}")
    for r in rows:
        eng = engine.get((r["id"], r["rule"], r["option"]))
        print(f"  {r['verdict']:<8} {r['id']:<9} {r['rule']}: {r['default']} -> {r['option']:<10} "
              f"{brief(r['default_answer'])}  |  {brief(r['option_answer'])}" + (f"   [engine: {eng}]" if eng else ""))
    print("\n  PER RULE (an option no reference distinguishes is not tested by this corpus)")
    by_rule: dict = {}
    for (rule, opt), s in sorted(per_option.items()):
        by_rule.setdefault(rule, []).append((opt, s))
        tag = "SWITCHES" if s["differs"] else "UNDISTINGUISHED"
        print(f"    {tag:<15} {rule} -> {opt}: differs on {len(s['differs'])} of {len(s['differs']) + len(s['same'])}"
              + (f" ({', '.join(s['differs'])})" if s["differs"] else ""))
    for rule, opts in by_rule.items():
        if not any(s["differs"] for _, s in opts):
            failures.append(f"rule {rule}: no option changes any answer — dead or untested in this corpus")
    if engine:
        tally: dict = {}
        for v in engine.values():
            tally[v.split(":")[0]] = tally.get(v.split(":")[0], 0) + 1
        print("\n  ENGINE (default flipped in a bundle copy, pinned intent re-planned): "
              + ", ".join(f"{n} {k}" for k, n in sorted(tally.items())))
    if a.json:
        Path(a.json).write_text(json.dumps({"rows": rows, "failures": failures,
                                            "engine": {"|".join(k): v for k, v in engine.items()}},
                                           indent=1, default=str), encoding="utf-8")
    undist = sum(1 for s in per_option.values() if not s["differs"])
    if failures:
        for f in failures:
            print(f"  FAIL {f}")
        print(f"FAIL: rule_switch_test — {len(failures)} failure(s) over {len(refs)} reference(s)")
        return 1
    print(f"PASS: rule_switch_test — {len(refs)} reference(s) follow their rule's current default and reproduce; "
          f"{len(by_rule)} rule(s), each switches at least one answer; {undist} option(s) undistinguished by this corpus")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
