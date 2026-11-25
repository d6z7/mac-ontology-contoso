---
type: Dataset
title: contoso5_gender
description: dataset contoso5_gender
relation: contoso5_gender
tags:
- Contoso 5
- dataset
---

- **Stored as** — a file: `data/lookups/contoso5_gender.csv` (2 row(s))
- **Key** — `code`
- **Made by** — [contoso5_gender](../transforms/contoso5_gender.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `code` | identifier | PK | — | — | — | — | THE MEMBER: a recorded customer gender. This relation IS the declared value set for that column, so a value absent here is a value the warehouse does not hold. |

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

- [DQ-CASE-G-contoso5_gender-COLUMNS](../quality/DQ-CASE-G-contoso5_gender-COLUMNS.md) — high · open — nobody has ruled — data-sanity case G-contoso5_gender-COLUMNS did not pass
- [DQ-CASE-G-contoso5_gender-KEY](../quality/DQ-CASE-G-contoso5_gender-KEY.md) — high · open — nobody has ruled — data-sanity case G-contoso5_gender-KEY did not pass
- [DQ-CASE-G-contoso5_gender-NULLS](../quality/DQ-CASE-G-contoso5_gender-NULLS.md) — medium · open — nobody has ruled — data-sanity case G-contoso5_gender-NULLS did not pass
- [DQ-UNCLAIMED-CONTOSO5_GENDER](../quality/DQ-UNCLAIMED-CONTOSO5_GENDER.md) — medium · accepted · said by ontology-developer — served relation `contoso5_gender` is claimed by no concept
