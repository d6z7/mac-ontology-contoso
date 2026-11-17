---
type: Concept
title: Country
description: A country Contoso sells in.
tags:
- Contoso 5
- concept
resource: table://dim_country
rule_pages:
- ../rules/Country.rows.md
- ../rules/Country.where_we_have_customers.md
- ../rules/Country.whose.md
---

A country Contoso sells in. The placeholder code `--` is not a country: it marks rows with no real country, such as the online store (rule Country.rows). The account is pages/knowledge/country.md.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`dim_country`](../../data/datasets/dim_country.md)
- **Counts** — `country_code` (no `counts`: the dataset key)
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*3 rule(s) are about this concept, 3 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Country.rows](../rules/Country.rows.md) — **proposed** · parent · choice over `real`, `sentinel` — default `real` — The placeholder country code `--` is not a country. It marks rows that carry no real country, such as the online store. Questions about countries count and list real countries only, unless they name the placeholder.
- [Country.where_we_have_customers](../rules/Country.where_we_have_customers.md) — **ruled** · parent · prose — not enforced (owner operator) — A question asking for the countries where we have customers asks for countries: the countries at least one customer lives in, one answer row per country, never one row per customer. Country is the subject and Customer the restriction. The same reading holds for other existence phrasings — countries that have a customer, with any customer — and the question must be answered, not refused.
- [Country.whose](../rules/Country.whose.md) — **ruled** · parent · choice over `territory`, `store`, `customer`, `location` — default `territory` — When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.

**Words**

*38 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| iso code | `dataset:dim_country.country_code` | binds | — | — | — |
| country | `dataset:dim_country.country_name` | binds | — | — | — |
| country name | `dataset:dim_country.country_name` | binds | — | — | — |
| nation | `dataset:dim_country.country_name` | binds | — | — | — |
| which country | `dataset:dim_country.country_name` | binds | — | — | — |
| countries | `rule:Country.rows` | finds | — | — | — |
| country | `rule:Country.rows` | finds | — | — | — |
| no country | `rule:Country.rows` | finds | — | — | — |
| online | `rule:Country.rows` | finds | — | — | — |
| placeholder | `rule:Country.rows` | finds | — | — | — |
| sentinel | `rule:Country.rows` | finds | — | — | — |
| unknown country | `rule:Country.rows` | finds | — | — | — |
| countries | `rule:Country.where_we_have_customers` | finds | — | — | — |
| customer country | `rule:Country.where_we_have_customers` | finds | — | — | — |
| existence | `rule:Country.where_we_have_customers` | finds | — | — | — |
| list countries | `rule:Country.where_we_have_customers` | finds | — | — | — |
| where we have customers | `rule:Country.where_we_have_customers` | finds | — | — | — |
| attribution | `rule:Country.whose` | finds | — | — | — |
| by country | `rule:Country.whose` | finds | — | — | — |
| country | `rule:Country.whose` | finds | — | — | — |
| customer country | `rule:Country.whose` | finds | — | — | — |
| market | `rule:Country.whose` | finds | — | — | — |
| store country | `rule:Country.whose` | finds | — | — | — |
| territory | `rule:Country.whose` | finds | — | — | — |
| whose country | `rule:Country.whose` | finds | — | — | — |
| customer countries | `rule:Country.whose.customer` | binds | — | — | — |
| customer country | `rule:Country.whose.customer` | binds | — | — | — |
| where our customers are | `rule:Country.whose.customer` | binds | — | — | — |
| location country | `rule:Country.whose.location` | binds | — | — | — |
| site country | `rule:Country.whose.location` | binds | — | — | — |
| store country | `rule:Country.whose.store` | binds | — | — | — |
| trading country | `rule:Country.whose.store` | binds | — | — | — |
| where we trade | `rule:Country.whose.store` | binds | — | — | — |
| business in | `rule:Country.whose.territory` | binds | — | — | — |
| country of the sale | `rule:Country.whose.territory` | binds | — | — | — |
| market | `rule:Country.whose.territory` | binds | — | — | — |
| trade in | `rule:Country.whose.territory` | binds | — | — | — |
| where the sale was made | `rule:Country.whose.territory` | binds | — | — | — |

## Grounded in

- [`dim_country`](../../data/datasets/dim_country.md) — served as `"contoso_served"."dim_country"`
- Its rows are the members of a value set: —.

## Grain

- One row of `dim_country` is identified by `country_code` (the dataset key).
- One Country is one row — no `counts`, so the instance is the dataset key.

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `country_code` | dimension | — | — | — | — | the country's code. The value `--` is a placeholder and not a country: it is where the source put the online store's country, and counting it would add a country Contoso does not sell in (rule Country.rows). | ← [Customer](Customer.md) via `customer__based_in__country`, ← [Location](Location.md) via `location__in__country`, ← [Order](Order.md) via `order__attributed_to__country`, ← [Store](Store.md) via `store__trades_in__country` |
| `country_name` | name | — | — | names `country_code` (long) | — | the country's name as a reader would see it. 'Online' is the name the sentinel carries and is not a place. | — |
| `is_placeholder` | identifier | — | — | — | — | true on the placeholder row whose code is `--` (no real country, such as the online store's), false on every real country, never empty. Made by the transform so that rule Country.rows reads its `real` and `sentinel` rows from a true/false column instead of a stored value; it selects exactly the rows the code test selected. Offered to no question on its own: a question reaches it through the rule. | — |

_Declared per column, over 3 served columns: is 3 of 3 · label 0 of 3 · measure 0 of 3 · names 1 of 3 · value set 0 of 3 · means 3 of 3 · joins → 1 of 3. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind |
|---|---|
| `country_code` | dimension |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

*0 edge(s) out · 4 in — the only joins (L7), walked in both directions.*

**Joined from** — edges into this concept:

- [Customer](Customer.md) — `customer__based_in__country` on `country_code` = `country_code`
- [Location](Location.md) — `location__in__country` on `country_code` = `country_code`
- [Order](Order.md) — `order__attributed_to__country` on `country_code` = `sale_country_code`
- [Store](Store.md) — `store__trades_in__country` on `country_code` = `country_code`

## Source of record

- Declaration: `ontology/concepts/Country.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/Country.md`](../../../ontology/concepts/Country.md) — the authored account (X-3); this page cites it and never writes it.
