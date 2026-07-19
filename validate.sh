#!/usr/bin/env bash
# validate.sh — run the three MAC framework gates against this ontology (structural · referential · constraint).
#   ./validate.sh
# Proves conformance, not correctness. Needs the meaning-as-code framework as a sibling dir
# (override with MEANING_AS_CODE=/path/to/meaning-as-code).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAC="${MEANING_AS_CODE:-$HERE/../meaning-as-code}"
cd "$MAC"

echo "── MAC validation · mac-ontology-contoso ──"
echo "[1/3] structural  — validate_schema.py"
python3 tools/validate_schema.py "$HERE"
echo "[2/3] referential — check_references.py"
python3 tools/check_references.py "$HERE"
echo "[3/3] constraint  — check_shapes.py"
python3 tools/check_shapes.py "$HERE"

# generated-artifact freshness: the operator manual (docs/manual.md) is generated from
# docs/manual.template.md + the ontology, so it must never drift. Regenerate to a temp and diff.
if [ -f "$HERE/docs/manual.template.md" ]; then
  echo "[4/4] freshness   — mac_to_manual.py (docs/manual.md must be in sync)"
  TMP="$(mktemp)"
  python3 tools/mac_to_manual.py "$HERE" -o "$TMP"
  if ! diff -q "$TMP" "$HERE/docs/manual.md" >/dev/null 2>&1; then
    echo "✗ docs/manual.md is STALE — regenerate:  python3 tools/mac_to_manual.py ." >&2
    rm -f "$TMP"; exit 1
  fi
  rm -f "$TMP"
fi
echo "✓ mac-ontology-contoso — all gates passed"
