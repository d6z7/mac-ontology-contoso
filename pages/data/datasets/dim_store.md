---
type: Dataset
title: dim_store
description: dataset dim_store
relation: dim_store
tags:
- Contoso 5
- dataset
---

- **Served as** — `"contoso_served"."dim_store"`
- **Key** — `store_key`
- **Made by** — [dim_store](../transforms/dim_store.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `store_key` | dimension | PK | — | — | — | parent=`store_code` | THE PREMISES — one row per shop per trading period, and the grain every sale is recorded against: `v_contoso5_sales_line.store_key` points here, never at the site. A shop has its own name, floor area, opening date and closing date, because those are properties of premises and not of a place. `999999` is the online outlet. A PLACE MAY HOLD A SUCCESSION OF PREMISES, which is why this is finer than `location_code` and why the two must never be used interchangeably: summing floor area over premises counts a re-let site once per tenancy, and counting premises answers a different question from counting sites. The `finer_than` ruling below is what says so to a reader. |
| `store_code` | identifier | — | — | — | — | — | THE SITE code: several store rows can share it over time. The value -1 is the ONLINE PLACEHOLDER and not a place. The transform turns it into `is_online`, which is what rule Store.channel reads (`physical` is false, `online` is true). |
| `store_name` | name | — | — | — | names `store_code` (common) | — | the store's name as a reader would see it. 'Online store' is the single non-physical outlet. A reading that finds the online channel by MATCHING THIS NAME is right by luck; the channel is `is_online` (rule Store.channel). |
| `country_code` | dimension | — | — | — | — | — | the country the store trades in. The online store carries '--', the sentinel dim_country names 'Online' and Country.rows excludes — so this column cannot attribute an internet sale to a real country. |
| `state` | dimension | — | — | — | — | — | the state, province or region the store sits in, within its country. |
| `open_date` | date | — | — | — | — | — | the day the store opened for trade. |
| `close_date` | date | — | — | — | — | — | the day the store closed, or null if it is still trading. THE TRADING-STATE COLUMN: `active` is this being null (Store.trading). |
| `status_annotation` | dimension | — | — | — | — | — | why a store stopped trading, where the source said: blank for a trading store, 'Closed' or 'Restructured' for an ended one, null on the online placeholder. Prose from the source, not a closed vocabulary of this bundle's own (rule Store.trading). |
| `square_metres` | measure | — | — | stock · m2 | — | — | the store's floor area in square metres. |
| `is_online` | identifier | — | — | — | — | — | true on the online outlet (its site code is -1), false on every physical shop, never empty. Rule Store.channel reads `physical` as false and `online` as true. |
| `is_shut` | identifier | — | — | — | — | — | true where the store closed for good (`status_annotation` is Closed), false otherwise, never empty. Rule Store.trading reads its `shut` option from it. |
| `is_restructured` | identifier | — | — | — | — | — | true where the store closed and was replaced (`status_annotation` is Restructured), false otherwise, never empty. Rule Store.trading reads its `restructured` option from it. |

## Checks

_This dataset declares no checks._

## Value sets

- `country_code` → value set [`dim_country`](dim_country.md).`country_code` via edge `store__trades_in__country`

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `store_key` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `store_code` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `store_name` | `name` | via `names` | via `names` | — | — | — | values; pattern for common / long / short | display (L13) |
| `country_code` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `state` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `open_date` | `date` | grains | period | — | yes | yes | calendar words | yes |
| `close_date` | `date` | grains | period | — | yes | yes | calendar words | yes |
| `status_annotation` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `square_metres` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `is_online` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `is_shut` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `is_restructured` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |

## Bound by

*1 concept(s) take rows from this dataset — a change to a column's declaration reaches every one of them.*

- [Store](../../ontology/concepts/Store.md) — serves `store_key`, `store_code`, `store_name`, `country_code`, `state`, `open_date`, `close_date`, `status_annotation`, `square_metres`, `is_online`, `is_shut`, `is_restructured`

## Findings

_No finding is filed under this dataset._
