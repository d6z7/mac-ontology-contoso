---
type: Doc
title: Plane health — chain, lineage & protocol
description: Chain integrity, lineage coverage and change-protocol metrics
tags:
- CONTOSO5
- plane-health
---

The structural health of this source's data plane — the same numbers the gates check, surfaced here so they are visible without running a terminal command. **The gates remain authoritative**; this page is a read-view.

## Chain — `raw source → transformation → dataset → ontology concept`

| link | count |
|---|---|
| raw sources | 8 |
| transformations | 21 |
| served datasets | 21 |
| ontology concepts | 11 |

✅ every dataset is produced by a transformation.

## Lineage coverage

How many of each served view's columns descend from an upstream column. Computed columns (pivots, aggregates, literals) legitimately have no single parent, so <100% is normal — **0% is the alarm**: it means the transform's inputs are mis-declared and the lineage silently collapsed.

| dataset | covered | of | coverage | |
|---|---|---|---|---|
| `contoso5_brand` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_category_name` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_channel` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_color` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_continent` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_country_code` | 0 | 2 | 0% | 🔴 explains nothing |
| `contoso5_currency` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_gender` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_manufacturer` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_state` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_status` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_store_name` | 0 | 1 | 0% | 🔴 explains nothing |
| `contoso5_sub_category_name` | 0 | 1 | 0% | 🔴 explains nothing |
| `dim_country` | 2 | 2 | 100% | 🟢 |
| `dim_currency` | 1 | 1 | 100% | 🟢 |
| `dim_customer` | 9 | 10 | 90% | 🟢 |
| `dim_location` | 4 | 5 | 80% | 🟢 |
| `dim_product` | 10 | 10 | 100% | 🟢 |
| `dim_store` | 8 | 9 | 89% | 🟢 |
| `v_contoso5_fx_rate` | 4 | 4 | 100% | 🟢 |
| `v_contoso5_sales_line` | 13 | 19 | 68% | 🟢 |

**Overall — 51/74 columns (69%) trace to an upstream column.**

## Change protocol — autodiscovery vs manual

| | count |
|---|---|
| objects harvested (self-documenting) | 0 |
| objects authored / tuned (need a protocol entry) | 21 |
| objects with no provenance stamp | 29 |
| protocolled interventions | 0 |

⚠️ no `interventions/ledger.yaml` yet — manual changes are unrecorded.
