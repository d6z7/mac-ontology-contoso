---
type: Dataset
title: dim_location
description: dataset dim_location
relation: dim_location
tags:
- Contoso 5
- dataset
---

- **Served as** — `"contoso_served"."dim_location"`
- **Key** — `location_code`
- **Made by** — [dim_location](../transforms/dim_location.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `location_code` | identifier | PK | — | — | — | — | THE SITE ITSELF — one row per site, which is what makes this relation the place a question about sites should be answered from. The value -1 is the online placeholder and not a place (rule Location.channel). SURFACES WIDENED 2026-10-24 BY THE OPERATOR, verbatim: "dont call it site code ... just site, location, city" (rule Location.site). `city` WAS ASKED FOR AND WITHDRAWN THE SAME DAY: this bundle has NO STORE CITY — the source store table carries a state or region and no city or town, and `GeoAreaKey` is another site identifier rather than a link to a geography. City exists only on the CUSTOMER (`dim_customer.city`), where it is declared personally identifying (`offers.suppressed: DQ-IDENTIFYING-DIM_CUSTOMER-CITY`) and says where a customer lives, not where a shop stands. Surfacing `city` here would bind "which cities" to an INTEGER site code and present codes as city names; unbound, the question fails to bind and the walk says so, which is the correct outcome for a fact this bundle does not hold. |
| `country_code` | dimension | — | — | — | — | — | the country the site sits in. |
| `country_name` | name | — | — | — | names `country_code` (long) | — | the name of the country the site sits in, carried here as well as on dim_country. |
| `state` | dimension | — | — | — | — | parent=`country_code` | the state, province or region the site sits in. |
| `units_ever_here` | measure | — | — | precomputed · units | — | — | how many store rows have ever stood at this site. A site re-tenanted has several store rows over time; each is one premises (rule Store.premises_not_place). |
| `is_online` | identifier | — | — | — | — | — | true on the online placeholder (site code -1, which is not a place), false on every physical site, never empty. Made by the transform so that rule Location.channel reads `physical` as false and `online` as true instead of a stored value; it selects exactly the rows the code test selected. Offered to no question on its own: a question reaches it through the rule. |
| `has_closed_store` | identifier | — | — | — | — | — | true where a store at this site has closed (at least one of its store rows carries a closing date), false otherwise, never empty. Rule Location.closed reads its `ever` option from it. |
| `is_closed_now` | identifier | — | — | — | — | — | true where no store at this site trades (every one of its store rows carries a closing date), false otherwise, never empty. Rule Location.closed reads its `now` option from it. |

## Checks

_This dataset declares no checks._

## Value sets

- `country_code` → value set [`dim_country`](dim_country.md).`country_code` via edge `location__in__country`

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `location_code` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `country_code` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `country_name` | `name` | via `names` | via `names` | — | — | — | values; pattern for common / long / short | display (L13) |
| `state` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `units_ever_here` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `is_online` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `has_closed_store` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `is_closed_now` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |

## Bound by

*1 concept(s) take rows from this dataset — a change to a column's declaration reaches every one of them.*

- [Location](../../ontology/concepts/Location.md) — serves `location_code`, `country_code`, `country_name`, `state`, `units_ever_here`, `is_online`, `has_closed_store`, `is_closed_now`

## Findings

_No finding is filed under this dataset._
