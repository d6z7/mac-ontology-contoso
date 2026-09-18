---
type: Doc
title: Plane health — chain, lineage & protocol
description: Chain integrity, lineage coverage and change-protocol metrics
tags:
- CONTOSO
- plane-health
---

The structural health of this source's data plane — the same numbers the gates check, surfaced here so they are visible without running a terminal command. **The gates remain authoritative**; this page is a read-view.

## Chain — `raw source → transformation → dataset → ontology concept`

| link | count |
|---|---|
| raw sources | 8 |
| transformations | 6 |
| served datasets | 6 |
| ontology concepts | 0 |

✅ every dataset is produced by a transformation.

## Lineage coverage

How many of each served view's columns descend from an upstream column. Computed columns (pivots, aggregates, literals) legitimately have no single parent, so <100% is normal — **0% is the alarm**: it means the transform's inputs are mis-declared and the lineage silently collapsed.

| dataset | covered | of | coverage | |
|---|---|---|---|---|
| `dim_contoso_calendar_day` | 17 | 17 | 100% | 🟢 |
| `dim_contoso_customer` | 13 | 13 | 100% | 🟢 |
| `dim_contoso_product` | 14 | 14 | 100% | 🟢 |
| `dim_contoso_store` | 11 | 11 | 100% | 🟢 |
| `v_contoso_fx_rate_day` | 4 | 4 | 100% | 🟢 |
| `v_contoso_order_line` | 12 | 12 | 100% | 🟢 |

**Overall — 71/71 columns (100%) trace to an upstream column.**

## Change protocol — autodiscovery vs manual

| | count |
|---|---|
| objects harvested (self-documenting) | 0 |
| objects authored / tuned (need a protocol entry) | 0 |
| objects with no provenance stamp | 20 |
| protocolled interventions | 0 |

⚠️ no `interventions/ledger.yaml` yet — manual changes are unrecorded.
