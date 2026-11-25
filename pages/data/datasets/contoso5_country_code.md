---
type: Dataset
title: contoso5_country_code
description: dataset contoso5_country_code
relation: contoso5_country_code
tags:
- Contoso 5
- dataset
---

- **Stored as** — a file: `data/lookups/contoso5_country_code.csv` (9 row(s))
- **Key** — `code`
- **Made by** — [contoso5_country_code](../transforms/contoso5_country_code.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `code` | identifier | PK | — | — | — | — | THE MEMBER: a country code, '--' included, which is the online sentinel and not a country. This relation IS the declared value set for that column, so a value absent here is a value the warehouse does not hold. |
| `label` | name | — | — | — | names `code` (long) | — | the reader-facing name of the country code beside it. Its word ('country name') lives on the owning column, dim_country.country_name, which this column copies. |

## Checks

_This dataset declares no checks._

## Value sets

_No column of this dataset is linked to a value set, and none links to it._

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `code` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `label` | `name` | via `names` | via `names` | — | — | — | values; pattern for common / long / short | display (L13) |

## Bound by

_No concept takes rows from this dataset (no concept's `table:` names it), so no question reads these columns through the ontology._

## Findings

- [DQ-CASE-G-contoso5_country_code-COLUMNS](../quality/DQ-CASE-G-contoso5_country_code-COLUMNS.md) — high · open — nobody has ruled — data-sanity case G-contoso5_country_code-COLUMNS did not pass
- [DQ-CASE-G-contoso5_country_code-KEY](../quality/DQ-CASE-G-contoso5_country_code-KEY.md) — high · open — nobody has ruled — data-sanity case G-contoso5_country_code-KEY did not pass
- [DQ-CASE-G-contoso5_country_code-NULLS](../quality/DQ-CASE-G-contoso5_country_code-NULLS.md) — medium · open — nobody has ruled — data-sanity case G-contoso5_country_code-NULLS did not pass
- [DQ-UNCLAIMED-CONTOSO5_COUNTRY_CODE](../quality/DQ-UNCLAIMED-CONTOSO5_COUNTRY_CODE.md) — medium · accepted · said by ontology-developer — served relation `contoso5_country_code` is claimed by no concept
