---
type: Dataset
title: contoso5_channel
description: dataset contoso5_channel
relation: contoso5_channel
tags:
- Contoso 5
- dataset
---

- **Stored as** — a file: `data/lookups/contoso5_channel.csv` (2 row(s))
- **Key** — `code`
- **Made by** — [contoso5_channel](../transforms/contoso5_channel.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `code` | identifier | PK | — | — | — | — | THE MEMBER: which channel a sale was made through — `physical` for a shop a customer can walk into, `online` for the web shop. This relation IS the declared value set for `v_contoso5_sales_line.channel`, so a value absent here is a value the warehouse does not hold. The names are the ones `Store.channel` already declares for its two populations, so the axis has one vocabulary across the fact, the dimension and this domain. |

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

- [DQ-CASE-G-contoso5_channel-COLUMNS](../quality/DQ-CASE-G-contoso5_channel-COLUMNS.md) — high · open — nobody has ruled — data-sanity case G-contoso5_channel-COLUMNS did not pass
- [DQ-CASE-G-contoso5_channel-KEY](../quality/DQ-CASE-G-contoso5_channel-KEY.md) — high · open — nobody has ruled — data-sanity case G-contoso5_channel-KEY did not pass
- [DQ-CASE-G-contoso5_channel-NULLS](../quality/DQ-CASE-G-contoso5_channel-NULLS.md) — medium · open — nobody has ruled — data-sanity case G-contoso5_channel-NULLS did not pass
- [DQ-UNCLAIMED-CONTOSO5_CHANNEL](../quality/DQ-UNCLAIMED-CONTOSO5_CHANNEL.md) — medium · accepted · said by ontology-developer — served relation `contoso5_channel` is claimed by no concept
