#!/usr/bin/env bash
# build.sh — build THIS BUNDLE'S OWN warehouse. It shares nothing with any other bundle.
#
# WHAT contoso5 IS FOR, and it is not what contoso4 is for. contoso4 measures the cost of one person's
# CURATION by holding the data constant against contoso2. contoso5 holds the data constant against
# contoso4 and varies something else: it is ingested as TWO SEPARATE DELIVERIES, the landing plane first
# and on its own, under the checklist and the enforcement the operator ruled on 2026-09-28 ("split data
# plane delivery in two parts ... have checklist for each one of them ... have linter and enforcement for
# every syntax thing we implement").
#
# IT EXISTS BECAUSE THE FIRST SPLIT RUN FOUND FOUR COUPLED DEFECTS, each hiding the next, and every one
# of them was invisible on a bundle that had been incrementally re-run: a stage resuming on its sibling's
# output, a value domain stripped and preserved nowhere, a producer deleting the banner that tells a
# reader not to hand-edit, and a measured foreign key that never reached a declaration because the
# descriptor could not be regenerated after the measurement. Only a bundle ingested ONCE, from nothing,
# can show that. That is this bundle's whole job.
#
# THE SERVED SCHEMA IS CREATED EMPTY AND STAYS EMPTY until a datasets delivery is asked for. A bundle
# carrying only a landing plane is a legitimate delivered state, not a half-finished one.
#
# NO FRAMEWORK PATH APPEARS IN THIS FILE, so the bundle carries no dependency on where the framework is
# checked out and `check_bundle_isolation` has nothing to find.
#
#     ./build.sh        # landings -> main.*, create contoso_served (empty)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DATA="$HERE/data"
DB="$HERE/contoso5.duckdb"
# THE 100K EDITION, AND IT SAID `1m` UNTIL 2026-10-09. The size label in this release counts
# ORDERS -- the upstream's own words are "10K: about 10,000 orders" -- and `main.orders` in the
# warehouse this script is supposed to rebuild holds 93 470 of them. That is the 100K edition.
#
# SO THIS SCRIPT DID NOT REBUILD THIS BUNDLE. `parquet-1m.7z` is ~1 000 000 orders: re-running it
# would have produced roughly ten times the data (223 974 sales lines becoming ~2.4M), and every
# profile, every acceptance answer and every row count measured in this bundle would have stopped
# matching the warehouse they were measured against -- silently, because nothing compares them.
# The parquet files are gitignored, so this line IS the provenance, and it recorded the wrong one.
#
# THREE INDEPENDENT CHECKS AGREE ON 100K, which is why this is an edit and not a guess:
#   * `main.orders` = 93 470, counted live from contoso5.duckdb ("about 100,000 orders")
#   * the asset sizes: parquet-100k.7z is 9 MB and parquet-1m.7z is 62 MB compressed
#   * this script's OWN next line says the extracted data is 17 MB, which fits 9 MB compressed
#     and cannot fit 62 MB. The comment was right and the URL was wrong.
RELEASE_SIZE="100k"   # orders, per the upstream's naming; see above before changing it
RELEASE="https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/download/ready-to-use-data/parquet-${RELEASE_SIZE}.7z"

command -v duckdb >/dev/null || { echo "!! duckdb not found -> brew install duckdb"; exit 1; }

if ! ls "$DATA"/*.parquet >/dev/null 2>&1; then
  echo "!! no parquet in $DATA (gitignored, 17 MB, regenerable). Fetch and extract:"
  echo "     curl -fL -o \"$DATA/parquet-${RELEASE_SIZE}.7z\" \"$RELEASE\""
  echo "     bsdtar -xf \"$DATA/parquet-${RELEASE_SIZE}.7z\" -C \"$DATA\"     # or: 7z x"
  exit 1
fi

echo "==> loading this bundle's landings into main.*"
rm -f "$DB"
SQL=""
for f in "$DATA"/*.parquet; do
  t="$(basename "$f" .parquet | tr '[:upper:]' '[:lower:]' | tr ' -' '__')"
  SQL+="CREATE OR REPLACE TABLE \"$t\" AS SELECT * FROM read_parquet('$f');"$'\n'
done
duckdb "$DB" -c "$SQL"

# THE SERVED SCHEMA IS CREATED EMPTY, ALWAYS. A declared serving layer with nothing in it is an honest
# state that downstream tools can read correctly; pointing view_schema at `main` instead would make the
# landings masquerade as served datasets.
echo "==> creating the served schema (empty until a transform fills it)"
duckdb "$DB" -c "CREATE SCHEMA IF NOT EXISTS contoso_served;"

shopt -s nullglob
sqls=("$DATA"/transforms/*.sql)
if [ ${#sqls[@]} -eq 0 ]; then
  echo "==> no transform declared yet, so contoso_served stays EMPTY."
  echo "    A 1:1 passthrough needs no judgement and is always derivable — generate it, then re-run:"
  echo "      python3 <framework>/tools/mac_passthrough.py \"$HERE\""
  echo "      ./build.sh"
else
  echo "==> applying this bundle's transforms -> contoso_served.*"
  for sql in "${sqls[@]}"; do
    echo "    $(basename "$sql")"
    grep -v '^[[:space:]]*--' "$sql" | duckdb "$DB" || { echo "!! failed: $sql"; exit 1; }
  done
fi

echo "==> landings and served relations:"
duckdb "$DB" -c "SELECT table_schema, table_type, count(*) AS n FROM information_schema.tables
                 WHERE table_schema IN ('main','contoso_served') GROUP BY 1,2 ORDER BY 1,2;"
echo "==> done: $DB"
