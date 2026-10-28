---
type: Relation
title: contoso5_country_code
description: semantic plane · 2 described column(s) · 0 binding concept(s)
tags:
- CONTOSO5
- relation
- semantic-plane
---

What a question may DO with each column of `contoso5_country_code` — the SEMANTIC plane of this relation. Its physical facts (types, measured distincts, where its rows live) are on the data-plane page; this says what the columns MEAN.

## Details

- **Schema version** — 0.3.0-develop
- **Confidence** — C
- **Provenance** — authored
- **Source** — CONTOSO5

## Key

- One row is identified by `code`.

## Columns

| column | key | offers | references | rulings |
|---|---|---|---|---|
| `code` | **key** | — | — | — |
| `label` | — | axis `categorical` | — | label_of `code` (long) |

_Declared per column, over 2 columns: offers 1 of 2 · references 0 of 2 · rulings 1 of 2. An em dash is a column for which nothing is declared._

## Bound by

_No concept binds this relation through `grounding.bindings[]`, so nothing in the ontology reads these column facts._

## Served as

- Kind — `file` · its rows live in a FILE, so a value is resolved from that file and NOT by querying the warehouse.
- The same relation's PHYSICAL page: [`contoso5_country_code`](../../data/datasets/contoso5_country_code.md)
