---
type: Dataset
title: dim_country
description: dataset dim_country
relation: dim_country
tags:
- Contoso 5
- dataset
- value set
---

- **Served as** — `"contoso_served"."dim_country"`
- **Key** — `country_code`
- **Made by** — [dim_country](../transforms/dim_country.md)
- **Members** — its rows are the members of a value set: —
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `country_code` | dimension | PK | — | — | — | — | the country's code. The value `--` is a placeholder and not a country: it is where the source put the online store's country, and counting it would add a country Contoso does not sell in (rule Country.rows). |
| `country_name` | name | — | — | — | names `country_code` (long) | — | the country's name as a reader would see it. 'Online' is the name the sentinel carries and is not a place. |
| `is_placeholder` | identifier | — | — | — | — | — | true on the placeholder row whose code is `--` (no real country, such as the online store's), false on every real country, never empty. Made by the transform so that rule Country.rows reads its `real` and `sentinel` rows from a true/false column instead of a stored value; it selects exactly the rows the code test selected. Offered to no question on its own: a question reaches it through the rule. |

## Checks

_This dataset declares no checks._

## Value sets

- ← [`dim_customer`](dim_customer.md).`country_code` links to `country_code` via edge `customer__based_in__country`
- ← [`dim_location`](dim_location.md).`country_code` links to `country_code` via edge `location__in__country`
- ← [`dim_store`](dim_store.md).`country_code` links to `country_code` via edge `store__trades_in__country`
- ← [`v_contoso5_sales_line`](v_contoso5_sales_line.md).`sale_country_code` links to `country_code` via edge `order__attributed_to__country`

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `country_code` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `country_name` | `name` | via `names` | via `names` | — | — | — | values; pattern for common / long / short | display (L13) |
| `is_placeholder` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |

## Bound by

*1 concept(s) take rows from this dataset — a change to a column's declaration reaches every one of them.*

- [Country](../../ontology/concepts/Country.md) — serves `country_code`, `country_name`, `is_placeholder`

## Findings

_No finding is filed under this dataset._
