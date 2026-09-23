#!/usr/bin/env python3
"""tools/run_properties.py — THE BUNDLE'S READ PATH. The framework owns the algorithm; this file
owns the connection.

Five framework tools (tools/_plugin.py) ask the bundle under analysis for a symbol and refuse to run
without it — `mac_profile.py` and `mac_admit_identity.py` need `Athena`, `mac_admit_identity.py`
also needs `source_watermark`, and three checkers ask for `resolve_declared`. All four symbols are
supplied here so that no framework gate becomes UNRUNNABLE against this bundle.

THREE THINGS WORTH KNOWING, because each one is a decision and not an accident:

1. THE SYMBOL IS CALLED `Athena`; WHAT IT OPENS IS DUCKDB. `_plugin.required(root, "Athena")` asks
   for that exact name, so the bundle answers under the name the framework asks for. The name is a
   source-shaped word in a source-agnostic framework — recorded as a kit/framework collision in the
   P1 run record rather than worked around here. Nothing about the class is Athena: it holds no
   credentials, bills nothing, and reaches a file.

2. WHICH DATABASE IS DECIDED BY connection.yaml, NOT BY THE CALLER. The framework passes four
   positional arguments read from `acceptance/properties.yaml#engine`
   (profile, region, workgroup, database). Here they are treated as LABELS only: they are recorded
   in the evidence (the profile's `engine:` field) and they never choose the file. The file comes
   from the connection the manifest declares (`mac.project.yaml#runtime.connection` ->
   `connection.yaml#config.database`), which is the one home for this bundle's connection and the
   one file an operator is allowed to override out of band. Two homes for a connection string is how
   a profile ends up measuring a different warehouse than the one it names.

3. `bytes_scanned` IS NOT REPORTED, BECAUSE THIS ENGINE DOES NOT KNOW IT. An embedded engine bills
   no scan. `query()` therefore returns a meta mapping that refuses to hold a `bytes_scanned` value,
   so the profile comes out with the field ABSENT rather than with a fabricated `0` that reads as
   "this scan was free" or as "nobody measured". Absent is a fact; 0 would be a claim.
"""
from __future__ import annotations

import pathlib

import duckdb
import yaml

# THE IMPORT IS AT MODULE LEVEL DELIBERATELY, and the alternative was tried and rejected. Deferring
# `import duckdb` into Athena keeps the three offline symbol-consumers runnable on an interpreter
# without the driver — but it moves the failure to connection time, where `mac_profile.py` does not
# guard the call: the driver's ModuleNotFoundError then escapes as a traceback (exit 1), and an
# exit-1 reads as a FINDING. Imported here, the whole plugin is simply unusable and every framework
# caller reports `could not run … exit 2`, which is over-refusal but never a false verdict — the
# distinction tools/_plugin.py exists to protect. Measured both ways on 2026-09-18.

#: bundle root — this file lives at <root>/tools/run_properties.py
ROOT = pathlib.Path(__file__).resolve().parent.parent


class _Meta(dict):
    """A query's engine metadata. Refuses `bytes_scanned`: see note 3 in the module docstring.

    The framework accumulates the field across passes (`meta["bytes_scanned"] = a + b`), which on an
    engine that reports nothing would turn two Nones into a 0. Dropping the write keeps the field
    absent, which is what "not measurable here" honestly looks like in the artifact.
    """

    _REFUSED = ("bytes_scanned",)

    def __setitem__(self, key, value):  # noqa: D105
        if key in self._REFUSED:
            return
        super().__setitem__(key, value)


def _connection() -> tuple[pathlib.Path, bool]:
    """Resolve (database file, read_only) from the connection this bundle's manifest declares."""
    manifest = yaml.safe_load((ROOT / "mac.project.yaml").read_text(encoding="utf-8")) or {}
    rel = ((manifest.get("runtime") or {}).get("connection")) or "connection.yaml"
    conn = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8")) or {}
    cfg = conn.get("config") or {}
    db = cfg.get("database")
    if not db:
        raise RuntimeError(f"{rel}#config.database is not set — nothing to connect to")
    # read_only DEFAULTS TO TRUE: a measurement path that can write is a measurement that can
    # change its own subject. connection.yaml may override it; nothing else may.
    return (ROOT / db) if not pathlib.Path(db).is_absolute() else pathlib.Path(db), \
        bool(cfg.get("read_only", True))


class Athena:  # noqa: N801 — the name the framework asks for; see note 1
    """A read handle over this bundle's warehouse, with the `query(sql) -> (rows, meta)` contract."""

    def __init__(self, profile: str | None = None, region: str | None = None,
                 workgroup: str | None = None, database: str | None = None) -> None:
        self.labels = {"profile": profile, "region": region,
                       "workgroup": workgroup, "database": database}
        self.path, self.read_only = _connection()
        if not self.path.exists():
            raise RuntimeError(f"{self.path} does not exist — run setup.sh to build the warehouse")
        self._con = duckdb.connect(str(self.path), read_only=self.read_only)

    def query(self, sql: str) -> tuple[list[dict], _Meta]:
        """Run one statement and return its rows as dicts, plus engine metadata.

        Every framework caller reads results positionally by generated alias (`d0`, `z0`, `v3`), so
        the mapping is keyed by the column names the engine returns, unaltered.
        """
        cur = self._con.execute(sql)
        names = [d[0] for d in cur.description]
        return [dict(zip(names, row)) for row in cur.fetchall()], _Meta()

    def close(self) -> None:
        self._con.close()


def source_watermark(ath: "Athena", relations: list[str]) -> dict[str, dict]:
    """The high-water mark of each relation, DERIVED from the descriptors — never from a name list.

    A write timestamp is something a descriptor already states: `role: audit` on a time-typed
    column. A relation whose descriptor marks none has no watermark, and this returns None for it
    rather than guessing at a column by its name. Contoso's raw landings carry no load stamp at all,
    so None here is the measured answer and not a gap in this function.
    """
    by_relation: dict[str, dict] = {}
    descriptors: dict[str, dict] = {}
    for plane in ("sources", "datasets"):
        for path in sorted((ROOT / "data" / plane).glob("*.yaml")):
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            tbl = doc.get("table") or {}
            key = ".".join(x for x in (tbl.get("schema"), tbl.get("name")) if x)
            if key:
                descriptors[key] = doc

    for rel in relations:
        doc = descriptors.get(rel) or {}
        audit = [c for c in (doc.get("columns") or [])
                 if c.get("role") == "audit"
                 and any(str(c.get("type", "")).lower().startswith(k)
                         for k in ("timestamp", "date", "time"))]
        newest = None
        if audit:
            col = str(audit[0]["name"]).replace('"', "")
            rows, _ = ath.query(f'SELECT CAST(max("{col}") AS varchar) AS w FROM {rel}')
            newest = rows[0]["w"] if rows else None
        by_relation[rel] = {"newest_write": newest,
                            "audit_column": (audit[0]["name"] if audit else None)}
    return by_relation


def resolve_declared(text: str) -> str:
    """Identity resolution — this bundle's declarations are not namespaced.

    Supplied EXPLICITLY, not left out: `_plugin.optional()` gives the documented identity fallback
    only to a bundle that declares NO plugin, and refuses (check unrunnable) for a bundle that
    declares one without the symbol. This bundle declares one, so it must say what resolution means
    here, and here it means: nothing to resolve.
    """
    return text


if __name__ == "__main__":
    # A smoke test for the read path itself, so "the connection works" is never an assumption.
    ath = Athena("local", "duckdb-local", "local", "contoso")
    rows, meta = ath.query("SELECT current_database() AS db, count(*) AS n FROM duckdb_tables()")
    print(f"  {ath.path.name} (read_only={ath.read_only}) -> {rows[0]}  meta={dict(meta)}")
