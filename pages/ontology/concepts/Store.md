---
type: Concept
title: Store
description: THE PREMISES Contoso sells from — a shop that stood on one place for one trading period, with its own name, floor area, opening date and closing date.
tags:
- Contoso 5
- concept
resource: table://dim_store
rule_pages:
- ../rules/Country.whose.md
- ../rules/Currency.whose.md
- ../rules/Customer.age.md
- ../rules/Store.channel.md
- ../rules/Store.premises_not_place.md
- ../rules/Store.record_questions.md
- ../rules/Store.trading.md
---

THE PREMISES Contoso sells from — a shop that stood on one place for one trading period, with its own name, floor area, opening date and closing date. It is what every sale is recorded against. A PLACE MAY HOLD A SUCCESSION OF PREMISES, so a store is NOT its place: see the Location concept for the place, and `dim_store.store_key#rulings.finer_than` for the declaration that one rolls up into the other. The account is ontology/concepts/Store.md. THIS DEFINITION CARRIES NO COUNTS, by the operator's ruling of 2026-10-24: "you are disclosing values that variy through the time as constnts?!?!?! this is no go ... you can decribe things without constants too". Counts belong where they can be re-measured: data/profiles/dim_store.yaml.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`dim_store`](../../data/datasets/dim_store.md)
- **Counts** — `store_key`
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*7 rule(s) are about this concept, 7 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Country.whose](../rules/Country.whose.md) — **ruled** · names it · choice over `territory`, `store`, `customer`, `location` — default `territory` — When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.
- [Currency.whose](../rules/Currency.whose.md) — **proposed** · names it · choice over `paid_in`, `rate_source`, `rate_target` — default `paid_in` — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- [Customer.age](../rules/Customer.age.md) — **proposed** · names it · prose — not enforced (owner operator) — An age is computed, never stored: a customer's age from the birth date and a store's age from its opening date, both measured at the sampling date rather than at today's date. Which age arithmetic is meant — completed years counting the birthday, or calendar year boundaries crossed — has not been ruled.
- [Store.channel](../rules/Store.channel.md) — **ruled** · names it · choice over `physical`, `online` — default `physical` — A store is a shop you can walk into. The online channel is recorded as a store, but a question about stores — how many there are, which ones — covers physical shops only unless it names the online channel. That default holds only when the question is about stores: revenue and every other figure of the sale includes both channels, even when the question's route passes through stores.
- [Store.premises_not_place](../rules/Store.premises_not_place.md) — **proposed** · names it · choice over `premises`, `site` — default `premises` — A store is the premises Contoso sells from: a shop standing on one place for one trading period, with its own name, floor area, opening date and closing date. It is part of a location, not the location itself — one place may hold a succession of premises over time, each of them a store. So one store is counted and listed by its premises, and a count, list or sum over stores is a different question from the same figure over places; an answer that could be read at either level says which level it used. The site reading (one row per place, whatever premises it held) is the other option.
- [Store.record_questions](../rules/Store.record_questions.md) — **proposed** · parent · prose — not enforced (owner operator) — A question about what the store table records — how many store versions or rows there are, or a list of every restructured store — covers every recorded row, the online channel included, with no channel or trading-state restriction. "How many stores do we have" is a different question and keeps the physical and active defaults.
- [Store.trading](../rules/Store.trading.md) — **ruled** · parent · choice over `closed`, `active`, `shut`, `restructured` — default `active` — A store is active while it has no closing date. A store with a closing date is closed, and a closed store is either shut — closed for good — or restructured — closed and replaced. A question about stores covers active stores unless it names another state.

**Words**

*56 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| closed | `dataset:dim_store.close_date` | binds | — | — | — |
| closing date | `dataset:dim_store.close_date` | binds | — | — | — |
| when it closed | `dataset:dim_store.close_date` | binds | — | — | — |
| store country code | `dataset:dim_store.country_code` | binds | — | — | — |
| opened | `dataset:dim_store.open_date` | binds | — | — | — |
| opening date | `dataset:dim_store.open_date` | binds | — | — | — |
| when it opened | `dataset:dim_store.open_date` | binds | — | — | — |
| area | `dataset:dim_store.square_metres` | binds | — | — | — |
| floor space | `dataset:dim_store.square_metres` | binds | — | — | — |
| how big | `dataset:dim_store.square_metres` | binds | — | — | — |
| size | `dataset:dim_store.square_metres` | binds | — | — | — |
| square meters | `dataset:dim_store.square_metres` | binds | — | — | — |
| county | `dataset:dim_store.state` | binds | — | — | — |
| province | `dataset:dim_store.state` | binds | — | — | — |
| region | `dataset:dim_store.state` | binds | — | — | — |
| status | `dataset:dim_store.status_annotation` | binds | — | — | — |
| store status | `dataset:dim_store.status_annotation` | binds | — | — | — |
| why it closed | `dataset:dim_store.status_annotation` | binds | — | — | — |
| channel | `dataset:dim_store.store_code` | binds | — | — | — |
| location | `dataset:dim_store.store_code` | binds | — | — | — |
| physical or online | `dataset:dim_store.store_code` | binds | — | — | — |
| site | `dataset:dim_store.store_code` | binds | — | — | — |
| premises | `dataset:dim_store.store_key` | binds | — | — | — |
| store id | `dataset:dim_store.store_key` | binds | — | — | — |
| name of the store | `dataset:dim_store.store_name` | binds | — | — | — |
| shop name | `dataset:dim_store.store_name` | binds | — | — | — |
| all stores | `rule:Store.record_questions` | finds | — | — | — |
| records | `rule:Store.record_questions` | finds | — | — | — |
| rows | `rule:Store.record_questions` | finds | — | — | — |
| store | `rule:Store.record_questions` | finds | — | — | — |
| store history | `rule:Store.record_questions` | finds | — | — | — |
| versions | `rule:Store.record_questions` | finds | — | — | — |
| active | `rule:Store.trading` | finds | — | — | — |
| close date | `rule:Store.trading` | finds | — | — | — |
| closed | `rule:Store.trading` | finds | — | — | — |
| open | `rule:Store.trading` | finds | — | — | — |
| restructured | `rule:Store.trading` | finds | — | — | — |
| shut | `rule:Store.trading` | finds | — | — | — |
| store | `rule:Store.trading` | finds | — | — | — |
| trading | `rule:Store.trading` | finds | — | — | — |
| not closed | `rule:Store.trading.active` | binds | — | — | — |
| open | `rule:Store.trading.active` | binds | — | — | — |
| operating | `rule:Store.trading.active` | binds | — | — | — |
| still open | `rule:Store.trading.active` | binds | — | — | — |
| trading | `rule:Store.trading.active` | binds | — | — | — |
| ceased | `rule:Store.trading.closed` | binds | — | — | — |
| inactive | `rule:Store.trading.closed` | binds | — | — | — |
| no longer trading | `rule:Store.trading.closed` | binds | — | — | — |
| not active | `rule:Store.trading.closed` | binds | — | — | — |
| closed and reopened | `rule:Store.trading.restructured` | binds | — | — | — |
| rebuilt | `rule:Store.trading.restructured` | binds | — | — | — |
| replaced | `rule:Store.trading.restructured` | binds | — | — | — |
| closed and not replaced | `rule:Store.trading.shut` | binds | — | — | — |
| closed permanently | `rule:Store.trading.shut` | binds | — | — | — |
| shut down | `rule:Store.trading.shut` | binds | — | — | — |
| shut for good | `rule:Store.trading.shut` | binds | — | — | — |

## Grounded in

- [`dim_store`](../../data/datasets/dim_store.md) — served as `"contoso_served"."dim_store"`

## Grain

- One row of `dim_store` is identified by `store_key` (the dataset key).
- One Store is one distinct `store_key` (`counts`, the instance).

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `store_key` | dimension | — | — | — | — | THE PREMISES — one row per shop per trading period, and the grain every sale is recorded against: `v_contoso5_sales_line.store_key` points here, never at the site. A shop has its own name, floor area, opening date and closing date, because those are properties of premises and not of a place. `999999` is the online outlet. A PLACE MAY HOLD A SUCCESSION OF PREMISES, which is why this is finer than `location_code` and why the two must never be used interchangeably: summing floor area over premises counts a re-let site once per tenancy, and counting premises answers a different question from counting sites. The `finer_than` ruling below is what says so to a reader. | ← [Order](Order.md) via `order__placed_at__store` |
| `store_code` | identifier | — | — | — | — | THE SITE code: several store rows can share it over time. The value -1 is the ONLINE PLACEHOLDER and not a place. The transform turns it into `is_online`, which is what rule Store.channel reads (`physical` is false, `online` is true). | [Location](Location.md) via `store__sited_in__location` |
| `store_name` | name | — | — | names `store_code` (common) | — | the store's name as a reader would see it. 'Online store' is the single non-physical outlet. A reading that finds the online channel by MATCHING THIS NAME is right by luck; the channel is `is_online` (rule Store.channel). | — |
| `country_code` | dimension | — | — | — | [`dim_country`](../../data/datasets/dim_country.md).`country_code` via `store__trades_in__country` | the country the store trades in. The online store carries '--', the sentinel dim_country names 'Online' and Country.rows excludes — so this column cannot attribute an internet sale to a real country. | [Country](Country.md) via `store__trades_in__country` |
| `state` | dimension | — | — | — | — | the state, province or region the store sits in, within its country. | — |
| `open_date` | date | — | — | — | — | the day the store opened for trade. | — |
| `close_date` | date | — | — | — | — | the day the store closed, or null if it is still trading. THE TRADING-STATE COLUMN: `active` is this being null (Store.trading). | — |
| `status_annotation` | dimension | — | — | — | — | why a store stopped trading, where the source said: blank for a trading store, 'Closed' or 'Restructured' for an ended one, null on the online placeholder. Prose from the source, not a closed vocabulary of this bundle's own (rule Store.trading). | — |
| `square_metres` | measure | — | stock · m2 | — | — | the store's floor area in square metres. | — |
| `is_online` | identifier | — | — | — | — | true on the online outlet (its site code is -1), false on every physical shop, never empty. Rule Store.channel reads `physical` as false and `online` as true. | — |
| `is_shut` | identifier | — | — | — | — | true where the store closed for good (`status_annotation` is Closed), false otherwise, never empty. Rule Store.trading reads its `shut` option from it. | — |
| `is_restructured` | identifier | — | — | — | — | true where the store closed and was replaced (`status_annotation` is Restructured), false otherwise, never empty. Rule Store.trading reads its `restructured` option from it. | — |

_Declared per column, over 12 served columns: is 12 of 12 · label 0 of 12 · measure 1 of 12 · names 1 of 12 · value set 1 of 12 · means 12 of 12 · joins → 3 of 12. An em dash is a column for which nothing is declared._

## Axes

Measure `square_metres`: quantity `stock` · average: across members ÷ instances; over time: mean of period levels.

| axis | axis kind | fold `square_metres` |
|---|---|---|
| `store_key` | dimension | sum |
| `country_code` | dimension | sum |
| `state` | dimension | sum |
| `open_date` | date | `over_time` (end) per entity first |
| `close_date` | date | `over_time` (end) per entity first |
| `status_annotation` | dimension | sum |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

*2 edge(s) out · 1 in — the only joins (L7), walked in both directions.*

**Joins to** — edges from this concept:

- [Country](Country.md) — `store__trades_in__country` on `country_code` = `country_code`
- [Location](Location.md) — `store__sited_in__location` on `store_code` = `location_code`

**Joined from** — edges into this concept:

- [Order](Order.md) — `order__placed_at__store` on `store_key` = `store_key`

## Source of record

- Declaration: `ontology/concepts/Store.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/Store.md`](../../../ontology/concepts/Store.md) — the authored account (X-3); this page cites it and never writes it.
