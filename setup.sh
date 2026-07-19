#!/usr/bin/env bash
#
# setup.sh — stand up the Contoso demo warehouse locally in DuckDB.
#
#   Data:   SQLBI Contoso Data Generator V2 (MIT) — safe to publish.
#   Engine: DuckDB (embedded; no server).
#
# Usage:  bash setup.sh [100k|1m|10m]     (default: 1m)
#
set -euo pipefail

SCALE="${1:-1m}"
case "$SCALE" in 100k|1m|10m) ;; *) echo "scale must be 100k, 1m or 10m"; exit 2 ;; esac

ASSET="parquet-${SCALE}.7z"
BASE="https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/download/ready-to-use-data"
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA="$HERE/data"
DB="$HERE/contoso.duckdb"

echo "==> Contoso demo warehouse  (scale=$SCALE)"

# --- deps -------------------------------------------------------------------
command -v duckdb >/dev/null || { echo "!! duckdb not found -> brew install duckdb"; exit 1; }
SEVENZ="$(command -v 7z || command -v 7zz || command -v 7za || true)"
if [ -z "$SEVENZ" ] && ! command -v bsdtar >/dev/null; then
  echo "!! no .7z extractor found. macOS ships 'bsdtar' (used automatically);"
  echo "   otherwise: brew install p7zip   (or: brew install sevenzip)"
  exit 1
fi

mkdir -p "$DATA"

# --- download ---------------------------------------------------------------
if [ ! -f "$DATA/$ASSET" ]; then
  echo "==> downloading $ASSET"
  curl -fL --retry 3 -o "$DATA/$ASSET" "$BASE/$ASSET"
else
  echo "==> $ASSET already present, skipping download"
fi

# --- extract ----------------------------------------------------------------
echo "==> extracting parquet"
if [ -n "$SEVENZ" ]; then
  "$SEVENZ" x -y -o"$DATA" "$DATA/$ASSET" >/dev/null
else
  bsdtar -xf "$DATA/$ASSET" -C "$DATA"          # libarchive reads 7z; ships with macOS
fi

# --- load: one table per parquet file (table name = lowercased file stem) ---
echo "==> building $DB"
rm -f "$DB"
SQL=""
while IFS= read -r f; do
  base="$(basename "$f" .parquet)"
  t="$(tr '[:upper:]' '[:lower:]' <<<"$base" | tr ' -' '__')"
  SQL+="CREATE OR REPLACE TABLE \"$t\" AS SELECT * FROM read_parquet('$f');"$'\n'
done < <(find "$DATA" -name '*.parquet' | sort)
[ -n "$SQL" ] || { echo "!! no parquet files found after extract"; exit 1; }
duckdb "$DB" -c "$SQL"

# --- report -----------------------------------------------------------------
echo "==> tables loaded:"
duckdb "$DB" -c "SELECT table_name AS tbl, estimated_size AS approx_rows FROM duckdb_tables() ORDER BY 1;" \
  || duckdb "$DB" -c "SHOW TABLES;"
echo "==> done.  open with:  duckdb \"$DB\""
