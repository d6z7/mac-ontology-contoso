#!/usr/bin/env python3
"""contoso_measure.lookup.build.py — PROJECT the additivity law into this bundle's measure register.

    python3 data/lookups/contoso_measure.lookup.build.py [bundle-root] [--check]

WHAT IT WRITES  data/lookups/contoso_measure.lookup.csv — one row per concept with `class: measure`,
carrying the three columns the framework's registry gate recomputes
(`measure_type`, `additivity_time`, `additivity_categorical`) plus the identity and routing columns
this bundle's registers already use.

WHY IT IS A SCRIPT AND NOT A FILE SOMEBODY TYPES. How a measure folds along an axis is stated ONCE,
in the framework's closed value domain `mac_vocabulary.yaml#MeasureType`, where each member carries
an `additivity` map over the two axis kinds. A register that RESTATES those values is a second home
for the law and drifts from it silently — which is the documented history behind
`tools/check_measure_additivity_registry.py`: a register populated by hand disagreed with the law
the same day it was written, and claimed a planning target could be summed across regions.

So the two additivity columns here are never typed. They are read out of the vocabulary at build
time, for the member the concept itself declares. Change the law and re-run: the register follows.
Nothing about additivity is written in this file — grep it for `additive` and you will find this
sentence and no value.

WHAT IT REFUSES TO DO
  * invent a member: a `measure_type` that is not in the closed domain is an error, not a default;
  * invent a fold: a member whose `additivity` map lacks an axis kind is an error;
  * write an empty register: no measure concept found is exit 2 (COULD NOT RUN), never a clean file
    with a header and no rows — a zero-row register and "this bundle has no measures" must not look
    alike. The ontology plane may be locked or absent; that is a reason to refuse, not to guess.

`--check` rebuilds in memory and diffs against the file on disk: exit 0 identical, exit 1 stale.
"""
from __future__ import annotations

import argparse
import csv
import io
import os
import pathlib
import sys

try:
    import yaml
except ImportError:                                                # pragma: no cover
    sys.exit("PyYAML required: pip install pyyaml")

OUT_NAME = "contoso_measure.lookup.csv"

# The register's own shape. The first three are the LAW's columns, by the names the framework's gate
# looks for (tools/mac_model.py#MEASURE_REGISTER_COLUMNS); the rest are this bundle's identity and
# routing columns, in the order its other registers use (code first, provenance last).
#
# NO COLUMN HERE MAY BE NAMED AFTER A DECLARED AXIS, and that is load-bearing rather than tidy:
# mac_model.py#_axis_role treats every non-law column whose values vary as a MEASURE SELECTOR, and an
# axis whose name is a selector gets no statement from the law at all. A column named `time` or
# `store` would therefore switch the additivity law off for that axis, silently. Measured — see the
# run record, P8.
COLUMNS = ["code", "label", "search_key", "measure_type", "additivity_time",
           "additivity_categorical", "axes_time", "axes_categorical", "concept_file",
           "source_view", "confidence", "note"]


def die(msg: str, code: int = 2) -> "None":
    """Exit 2 = COULD NOT RUN (a population or the law is missing); exit 1 = the bundle says
    something the law cannot project, which is a defect in the bundle and not in the run."""
    print(f"{'could not run' if code == 2 else 'refusing to write'}: {msg}", file=sys.stderr)
    raise SystemExit(code)


def find_vocabulary(root: pathlib.Path, explicit: str | None) -> pathlib.Path:
    """The framework's own vocabulary file — the single home of the additivity law.

    Looked for in three places, in order, and never guessed: an explicit --vocabulary, the
    MAC_FRAMEWORK environment variable, then a `meaning-as-code/` checkout beside this bundle or any
    of its ancestors (the layout mac.project.yaml#reproduction already assumes when it writes
    `python3 meaning-as-code/tools/...`).
    """
    if explicit:
        p = pathlib.Path(explicit).expanduser()
        p = p / "mac_vocabulary.yaml" if p.is_dir() else p
        return p if p.is_file() else die(f"--vocabulary {p} is not a file")
    env = os.environ.get("MAC_FRAMEWORK")
    if env:
        p = pathlib.Path(env).expanduser() / "mac_vocabulary.yaml"
        if p.is_file():
            return p
        die(f"MAC_FRAMEWORK is set but {p} is not a file")
    for anc in [root, *root.parents]:
        p = anc / "meaning-as-code" / "mac_vocabulary.yaml"
        if p.is_file():
            return p
    die("the framework's mac_vocabulary.yaml was not found — pass --vocabulary <framework-root>, "
        "or set MAC_FRAMEWORK. The additivity law lives there and is not reproduced here")


def law(vocab: pathlib.Path) -> dict:
    doc = yaml.safe_load(vocab.read_text(encoding="utf-8")) or {}
    members = (doc.get("MeasureType") or {}).get("members") or {}
    if not members:
        die(f"{vocab}#MeasureType declares no members — the law is unreadable, so there is nothing "
            f"to project")
    return members


def concepts_dir(root: pathlib.Path, explicit: str | None) -> pathlib.Path:
    if explicit:
        return pathlib.Path(explicit).expanduser()
    proj = root / "mac.project.yaml"
    plane = "ontology"
    if proj.is_file():
        doc = yaml.safe_load(proj.read_text(encoding="utf-8")) or {}
        plane = ((doc.get("planes") or {}).get("ontology") or plane)
    return root / plane / "concepts"


def rows_for(root: pathlib.Path, cdir: pathlib.Path, members: dict) -> list[dict]:
    if not cdir.is_dir():
        die(f"{cdir} does not exist — no concept plane to project from")
    out: list[dict] = []
    for f in sorted(cdir.rglob("*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        c = doc.get("concept") or {}
        if str(c.get("class")) != "measure":
            continue
        sem = (c.get("semantics") or doc.get("semantics") or {})
        term = str(sem.get("measure_type") or "").strip()
        member = term.split(".")[-1]
        if member not in members:
            die(f"{f.name}: measure_type {term!r} is not a member of the closed domain "
                f"{sorted(members)} — a register row cannot be projected from a term the law does "
                f"not define", 1)
        additivity = (members[member].get("additivity") or {})
        cells = {}
        for kind in ("time", "categorical"):
            v = str(additivity.get(kind) or "").strip()
            if not v:
                die(f"{member}.{kind} is not stated in the law — the register would have to invent "
                    f"it", 1)
            cells[f"additivity_{kind}"] = v
        axes = sem.get("axis_kinds") or {}
        by_kind: dict[str, list[str]] = {"time": [], "categorical": []}
        for axis, kind in axes.items():
            k = str(kind).split(".")[-1].strip()
            if k not in by_kind:
                die(f"{f.name}: axis {axis!r} declares axis kind {kind!r}, which is not a member of "
                    f"mac.axis_kind — the register cannot say which law cell applies", 1)
            by_kind[k].append(str(axis))
        rel = ""
        srcs = ((doc.get("grounding") or {}).get("sources") or [])
        if srcs:
            rel = str(srcs[0].get("relation") or "").split(".")[-1]
        label = str(c.get("label") or c.get("name") or "")
        out.append({
            "code": str(c.get("name") or f.stem),
            "label": label,
            "search_key": label.lower(),
            "measure_type": term,
            **cells,
            "axes_time": ";".join(sorted(by_kind["time"])),
            "axes_categorical": ";".join(sorted(by_kind["categorical"])),
            "concept_file": f.relative_to(root).as_posix() if f.is_relative_to(root) else f.name,
            "source_view": rel,
            "confidence": str((doc.get("metadata") or {}).get("confidence") or ""),
            "note": (f"fold DERIVED from mac_vocabulary.yaml#MeasureType.{member}.additivity, aimed "
                     f"at this measure's own declared axis kinds; the type is declared at "
                     f"concept.semantics.measure_type and the arithmetic behind it is in "
                     f"queries/p8_measure_semantics.sql"),
        })
    if not out:
        die(f"{cdir} holds no concept with `class: measure` — nothing to project. A register with a "
            f"header and no rows would be indistinguishable from a bundle that has no measures")
    return sorted(out, key=lambda r: r["code"])


def render(rows: list[dict]) -> str:
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".", help="bundle root (default: cwd)")
    ap.add_argument("--vocabulary", help="framework root, or the mac_vocabulary.yaml path itself")
    ap.add_argument("--concepts", help="concept directory (default: the ontology plane's concepts/)")
    ap.add_argument("--check", action="store_true", help="diff against the file on disk; do not write")
    a = ap.parse_args()

    root = pathlib.Path(a.root).resolve()
    if not root.is_dir():
        die(f"{root} is not a directory")
    vocab = find_vocabulary(root, a.vocabulary)
    rows = rows_for(root, concepts_dir(root, a.concepts), law(vocab))
    text = render(rows)
    target = root / "data" / "lookups" / OUT_NAME

    if a.check:
        on_disk = target.read_text(encoding="utf-8") if target.is_file() else None
        if on_disk == text:
            print(f"OK — {OUT_NAME} is the projection of {vocab.name}#MeasureType over "
                  f"{len(rows)} measure concept(s)")
            return 0
        print(f"STALE — {OUT_NAME} is not what the law and the concepts project today "
              f"({len(rows)} row(s) expected)", file=sys.stderr)
        return 1

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print(f"wrote data/lookups/{OUT_NAME} — {len(rows)} measure(s) projected from "
          f"{vocab.name}#MeasureType: " + ", ".join(r["code"] for r in rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
