---
type: Dataset
title: contoso5_sub_category_name
description: dataset contoso5_sub_category_name
relation: contoso5_sub_category_name
tags:
- Contoso 5
- dataset
---

- **Stored as** — a file: `data/lookups/contoso5_sub_category_name.csv` (32 row(s))
- **Key** — `code`
- **Made by** — [contoso5_sub_category_name](../transforms/contoso5_sub_category_name.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `code` | identifier | PK | — | — | — | — | THE MEMBER: a product sub-category, one level below the category. This relation IS the declared value set for that column, so a value absent here is a value the warehouse does not hold. |

## Checks

_This dataset declares no checks._

## Value sets

_No column of this dataset is linked to a value set, and none links to it._

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `code` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |

## Bound by

_No concept takes rows from this dataset (no concept's `table:` names it), so no question reads these columns through the ontology._

## Findings

- [DQ-CASE-G-contoso5_sub_category_name-COLUMNS](../quality/DQ-CASE-G-contoso5_sub_category_name-COLUMNS.md) — high · open — nobody has ruled — data-sanity case G-contoso5_sub_category_name-COLUMNS did not pass
- [DQ-CASE-G-contoso5_sub_category_name-KEY](../quality/DQ-CASE-G-contoso5_sub_category_name-KEY.md) — high · open — nobody has ruled — data-sanity case G-contoso5_sub_category_name-KEY did not pass
- [DQ-CASE-G-contoso5_sub_category_name-NULLS](../quality/DQ-CASE-G-contoso5_sub_category_name-NULLS.md) — medium · open — nobody has ruled — data-sanity case G-contoso5_sub_category_name-NULLS did not pass
- [DQ-UNCLAIMED-CONTOSO5_SUB_CATEGORY_NAME](../quality/DQ-UNCLAIMED-CONTOSO5_SUB_CATEGORY_NAME.md) — medium · accepted · said by ontology-developer — served relation `contoso5_sub_category_name` is claimed by no concept
