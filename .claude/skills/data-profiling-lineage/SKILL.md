---
name: data-profiling-lineage
description: Profile source-data quality and steer transformations into the AI-friendly dataset the ontology binds to; own physical mappings + lineage. Use for data-engineering work.
---

# Data profiling & lineage

Data shaping is **development**, not runtime. Produce the AI-friendly dataset the ontology binds to,
and keep its lineage sound.

## Profile first

- Sample the source (the warehouse / the query engine over S3 — not Prisma/RLS). Assess completeness, distinct values,
  nulls, types, cardinality, obvious anomalies.
- Record findings in `specs/<initiative>/` so the Ontology Developer designs against reality.

## Shape

- Steer transformations toward an **AI-friendly** shape: stable keys, resolved enums, consistent
  grain, documented units — the shape the interpreter/executor can query without guessing.
- Bind `physical_mapping.yaml` to **real** source columns; a mapping to a non-existent column fails checks.

## Lineage (enforced)

Honor the standing decisions:

- the bundle's decision record establishing the lineage-enforced data plane
- the bundle's decision record on capturing the raw input schema

Every field the ontology exposes must trace back to a known source column through a recorded transform.

## Validate

`./run_checks.sh <source>`; coordinate with the Ontology Developer; hand off to QA / Tester (G3).
