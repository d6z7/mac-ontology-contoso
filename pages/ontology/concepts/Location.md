---
type: Concept
title: Location
description: THE PLACE a store stands on — a country and a state, and nothing that belongs to the shop itself.
tags:
- Contoso 5
- concept
resource: table://dim_location
rule_pages:
- ../rules/Currency.whose.md
- ../rules/Location.channel.md
- ../rules/Location.closed.md
- ../rules/Location.site.md
- ../rules/Store.premises_not_place.md
---

THE PLACE a store stands on — a country and a state, and nothing that belongs to the shop itself. Floor area, opening and closing dates are properties of PREMISES and live on Store; what a place owns is where it is. ONE PLACE MAY HOLD A SUCCESSION OF PREMISES over time, which is the fact this concept exists to keep separate from Store: `dim_store.store_key` declares `finer_than: location_code`, so premises roll UP into a place and a place never divides down into one. Summing a per-premises measure over a place that has been re-let counts it once per tenancy. A PLACE IS NOT A CITY IN THIS BUNDLE. Its finest geography is `state`, which in France means regions and overseas territories; `main.store` carries no city or town column. City exists only on the customer, as where a customer lives, and is declared personally identifying. No counts here, by the ruling of 2026-10-24 — they belong in data/profiles/dim_location.yaml where they can be re-measured. The account is ontology/concepts/Location.md.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`dim_location`](../../data/datasets/dim_location.md)
- **Counts** — `location_code` (no `counts`: the dataset key)
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*5 rule(s) are about this concept, 5 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Currency.whose](../rules/Currency.whose.md) — **proposed** · names it · choice over `paid_in`, `rate_source`, `rate_target` — default `paid_in` — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- [Location.channel](../rules/Location.channel.md) — **proposed** · parent · choice over `physical`, `online` — default `physical` — The online store is recorded as a location, but it is not a place. Questions about locations and places cover physical locations only, unless they name the online channel.
- [Location.closed](../rules/Location.closed.md) — **proposed** · parent · choice over `ever`, `now` — default `ever` — A site counts as closed when a store at it has closed, whether or not another store trades there now. A question may ask instead for the sites where no store trades now. The answer says which it counted.
- [Location.site](../rules/Location.site.md) — **proposed** · parent · prose — not enforced (owner operator) — Site and location name the same notion: the place a store stands on, described by its country and its state or region. A store's place has no city in this business's data — its finest geography is the state or region — and a city is only where a customer lives, so a question about the cities stores are in has no answer here and must say so rather than offer site codes.
- [Store.premises_not_place](../rules/Store.premises_not_place.md) — **proposed** · names it · choice over `premises`, `site` — default `premises` — A store is the premises Contoso sells from: a shop standing on one place for one trading period, with its own name, floor area, opening date and closing date. It is part of a location, not the location itself — one place may hold a succession of premises over time, each of them a store. So one store is counted and listed by its premises, and a count, list or sum over stores is a different question from the same figure over places; an answer that could be read at either level says which level it used. The site reading (one row per place, whatever premises it held) is the other option.

**Words**

*22 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| site country code | `dataset:dim_location.country_code` | binds | — | — | — |
| site country name | `dataset:dim_location.country_name` | binds | — | — | — |
| location | `dataset:dim_location.location_code` | binds | — | — | — |
| site | `dataset:dim_location.location_code` | binds | — | — | — |
| province | `dataset:dim_location.state` | binds | — | — | — |
| region | `dataset:dim_location.state` | binds | — | — | — |
| how many stores here | `dataset:dim_location.units_ever_here` | binds | — | — | — |
| stores ever here | `dataset:dim_location.units_ever_here` | binds | — | — | — |
| tenancies | `dataset:dim_location.units_ever_here` | binds | — | — | — |
| channel | `rule:Location.channel` | finds | — | — | — |
| location | `rule:Location.channel` | finds | — | — | — |
| online | `rule:Location.channel` | finds | — | — | — |
| physical | `rule:Location.channel` | finds | — | — | — |
| place | `rule:Location.channel` | finds | — | — | — |
| site | `rule:Location.channel` | finds | — | — | — |
| city | `rule:Location.site` | finds | — | — | — |
| geography | `rule:Location.site` | finds | — | — | — |
| location | `rule:Location.site` | finds | — | — | — |
| place | `rule:Location.site` | finds | — | — | — |
| region | `rule:Location.site` | finds | — | — | — |
| site | `rule:Location.site` | finds | — | — | — |
| state | `rule:Location.site` | finds | — | — | — |

## Grounded in

- [`dim_location`](../../data/datasets/dim_location.md) — served as `"contoso_served"."dim_location"`

## Grain

- One row of `dim_location` is identified by `location_code` (the dataset key).
- One Location is one row — no `counts`, so the instance is the dataset key.

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `location_code` | identifier | — | — | — | — | THE SITE ITSELF — one row per site, which is what makes this relation the place a question about sites should be answered from. The value -1 is the online placeholder and not a place (rule Location.channel). SURFACES WIDENED 2026-10-24 BY THE OPERATOR, verbatim: "dont call it site code ... just site, location, city" (rule Location.site). `city` WAS ASKED FOR AND WITHDRAWN THE SAME DAY: this bundle has NO STORE CITY — the source store table carries a state or region and no city or town, and `GeoAreaKey` is another site identifier rather than a link to a geography. City exists only on the CUSTOMER (`dim_customer.city`), where it is declared personally identifying (`offers.suppressed: DQ-IDENTIFYING-DIM_CUSTOMER-CITY`) and says where a customer lives, not where a shop stands. Surfacing `city` here would bind "which cities" to an INTEGER site code and present codes as city names; unbound, the question fails to bind and the walk says so, which is the correct outcome for a fact this bundle does not hold. | ← [Store](Store.md) via `store__sited_in__location` |
| `country_code` | dimension | — | — | — | [`dim_country`](../../data/datasets/dim_country.md).`country_code` via `location__in__country` | the country the site sits in. | [Country](Country.md) via `location__in__country` |
| `country_name` | name | — | — | names `country_code` (long) | — | the name of the country the site sits in, carried here as well as on dim_country. | — |
| `state` | dimension | — | — | — | — | the state, province or region the site sits in. | — |
| `units_ever_here` | measure | — | precomputed · units | — | — | how many store rows have ever stood at this site. A site re-tenanted has several store rows over time; each is one premises (rule Store.premises_not_place). | — |
| `is_online` | identifier | — | — | — | — | true on the online placeholder (site code -1, which is not a place), false on every physical site, never empty. Made by the transform so that rule Location.channel reads `physical` as false and `online` as true instead of a stored value; it selects exactly the rows the code test selected. Offered to no question on its own: a question reaches it through the rule. | — |
| `has_closed_store` | identifier | — | — | — | — | true where a store at this site has closed (at least one of its store rows carries a closing date), false otherwise, never empty. Rule Location.closed reads its `ever` option from it. | — |
| `is_closed_now` | identifier | — | — | — | — | true where no store at this site trades (every one of its store rows carries a closing date), false otherwise, never empty. Rule Location.closed reads its `now` option from it. | — |

_Declared per column, over 8 served columns: is 8 of 8 · label 0 of 8 · measure 1 of 8 · names 1 of 8 · value set 1 of 8 · means 8 of 8 · joins → 2 of 8. An em dash is a column for which nothing is declared._

## Axes

Measure `units_ever_here`: quantity `precomputed`.

| axis | axis kind | fold `units_ever_here` |
|---|---|---|
| `country_code` | dimension | read only |
| `state` | dimension | read only |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

*1 edge(s) out · 1 in — the only joins (L7), walked in both directions.*

**Joins to** — edges from this concept:

- [Country](Country.md) — `location__in__country` on `country_code` = `country_code`

**Joined from** — edges into this concept:

- [Store](Store.md) — `store__sited_in__location` on `location_code` = `store_code`

## Source of record

- Declaration: `ontology/concepts/Location.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/Location.md`](../../../ontology/concepts/Location.md) — the authored account (X-3); this page cites it and never writes it.
