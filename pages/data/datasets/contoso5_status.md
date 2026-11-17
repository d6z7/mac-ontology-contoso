---
type: Dataset
title: contoso5_status
description: dataset contoso5_status
relation: contoso5_status
tags:
- Contoso 5
- dataset
---

- **Stored as** — a file: `data/lookups/contoso5_status.csv` (2 row(s))
- **Key** — `code`
- **Made by** — [contoso5_status](../transforms/contoso5_status.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `code` | identifier | PK | — | — | — | — | THE MEMBER: a reason a store stopped trading, as the source wrote it. This relation IS the declared value set for that column, so a value absent here is a value the warehouse does not hold. |

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

- [DQ-CASE-G-contoso5_status-COLUMNS](../quality/DQ-CASE-G-contoso5_status-COLUMNS.md) — high · open — nobody has ruled — data-sanity case G-contoso5_status-COLUMNS did not pass
- [DQ-CASE-G-contoso5_status-KEY](../quality/DQ-CASE-G-contoso5_status-KEY.md) — high · open — nobody has ruled — data-sanity case G-contoso5_status-KEY did not pass
- [DQ-UNCLAIMED-CONTOSO5_STATUS](../quality/DQ-UNCLAIMED-CONTOSO5_STATUS.md) — medium · accepted · said by ontology-developer — served relation `contoso5_status` is claimed by no concept
