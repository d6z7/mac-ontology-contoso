---
type: Dataset
title: dim_customer
description: dataset dim_customer
relation: dim_customer
tags:
- Contoso 5
- dataset
---

- **Served as** — `"contoso_served"."dim_customer"`
- **Key** — `customer_key`
- **Made by** — [dim_customer](../transforms/dim_customer.md)
- **valid** — start=`valid_from`, end=`valid_end`
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `customer_key` | identifier | PK | — | — | — | — | the row key: one row per customer. The register is not the buyer list — many customers have never ordered (rule Customer.register_not_buyers). |
| `customer_name` | name | — | — | — | names `customer_key` (common) | match=`pattern` | the customer's name as registered. |
| `continent` | dimension | — | — | — | — | — | the continent the customer lives on. |
| `country_code` | dimension | — | — | — | — | parent=`continent` | the country the CUSTOMER lives in. No customer carries the `--` online placeholder. This is the only column that can place an internet sale in a real country. |
| `state` | dimension | — | — | — | — | within=`country_code` | the state, province or region the customer lives in. |
| `city` | dimension | — | — | — | — | match=`pattern` | the city the customer lives in. |
| `gender` | dimension | — | — | — | — | — | the customer's recorded gender. |
| `birth_date` | date | — | — | — | — | — | the customer's date of birth. |
| `valid_from` | identifier | — | — | — | — | — | the day this customer record became valid — the start of the validity window that says whether a customer is active on a reference date. The register is kept as a history, so a sale could in principle be attributed to where the customer lived ON THE ORDER DATE — nothing in this bundle declares that it should be. |
| `valid_to` | identifier | — | — | — | — | — | the day this customer record stopped being valid — the last day of the validity window, as the source states it. Paired with `valid_from`. |
| `valid_end` | identifier | — | — | — | — | — | the day after `valid_to`: the half-open end of the validity window, made by the transform. A record is valid on a day when `valid_from` is on or before it and `valid_end` is after it, which selects exactly the records `valid_to` on or after that day selects. It is what rule Customer.active_on_the_reference_date reads; offered to no question on its own. |

## Checks

_This dataset declares no checks._

## Value sets

- `country_code` → value set [`dim_country`](dim_country.md).`country_code` via edge `customer__based_in__country`

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `customer_key` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `customer_name` | `name` | via `names` | via `names` | — | — | — | values; pattern for common / long / short | display (L13) |
| `continent` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `country_code` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `state` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `city` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `gender` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `birth_date` | `date` | grains | period | — | yes | yes | calendar words | yes |
| `valid_from` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `valid_to` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `valid_end` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |

## Bound by

*1 concept(s) take rows from this dataset — a change to a column's declaration reaches every one of them.*

- [Customer](../../ontology/concepts/Customer.md) — serves `customer_key`, `customer_name`, `continent`, `country_code`, `state`, `city`, `gender`, `birth_date`, `valid_from`, `valid_to`, `valid_end`

## Findings

- [DQ-IDENTIFYING-DIM_CUSTOMER-CITY](../quality/DQ-IDENTIFYING-DIM_CUSTOMER-CITY.md) — medium · open — nobody has ruled — `dim_customer.city` names individuals — 21,317 of 34,581 values are held by exactly one row
- [DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME](../quality/DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME.md) — medium · open — nobody has ruled — `dim_customer.customer_name` names individuals — 94,488 of 99,200 values are held by exactly one row
- [DQ-DANGLINGKEY-GEOAREAKEY](../quality/DQ-DANGLINGKEY-GEOAREAKEY.md) — medium · open — nobody has ruled — `GeoAreaKey` is key-shaped and no relation in scope carries it as a key
