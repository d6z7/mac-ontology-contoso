---
name: ontology-authoring
description: Author and evolve the semantic model against meaning-as-code — concepts, vocabulary, relationships, projections. Use when building or changing an ontology.
---

# Ontology authoring

Build the semantic model against the `meaning-as-code` framework. Pin the framework version; keep
the ontology **source-aware** but the framework **source-agnostic** (the ontology names the source;
`meaning-as-code` never does).

## Before authoring

- Read `specs/<initiative>/spec.md` + AC. No AC → stop (Stop-the-Line).
- `ls decisions/` and existing ontologies — do not relitigate settled shapes; reuse patterns.
- Confirm the schema tooling resolves (`run_checks.sh` honors `MEANING_AS_CODE`).

## Shape

- **Concepts** — the entities/measures users ask about; one canonical definition each.
- **Vocabulary** — terms and synonyms that map language to concepts (drives the interpreter).
- **Relationships** — how concepts connect (joins the runtime traverses).
- **Projections / mappings** — how each concept binds to the physical dataset (coordinate with the
  Data Engineer's `physical_mapping.yaml`).

## Rules

- Every concept must be **executable**: it resolves to real data via a projection, or it does not ship.
- Keep vocabulary unambiguous — ambiguity surfaces at runtime as a clarification, not a guess.
- Version the ontology; the runtime consumes a compiled, immutable artifact, not this working tree.
- **No-probe by construction (MANDATORY, do it every time — never wait to be asked).** Pre-resolve every
  lookup at BUILD time so the runtime answers in ~1–2 composed queries and NEVER explores the warehouse.
  For every source: profile the dims (distinct values), FLATTEN any EAV into a **materialized** flat serving
  view, ship `data/lookups/*.csv` name→code registers, fill enumeration `values`, and author a
  **`no_probe_guarantee`** on every concept (the explicit "resolve name→code + one join, no EAV pivot, no
  probing" promise — mirror `<a bundle repo> source`). A concept whose answer would need runtime probing is not
  done. Track queries-per-answer as the governance metric (a good answer ≈ 1–2 queries; a dozen = a gap).

## Validate

`./run_checks.sh <source>` — shapes, references, separation, resolver, suite-completeness must pass.
Hand off to QA / Tester (G3).
