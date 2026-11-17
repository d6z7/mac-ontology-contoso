---
type: Concept
title: Customer
description: A person on Contoso's customer register, each with a name, a birth date and a place — continent, country, state, city.
tags:
- Contoso 5
- concept
resource: table://dim_customer
rule_pages:
- ../rules/Country.where_we_have_customers.md
- ../rules/Country.whose.md
- ../rules/Customer.active_on_the_reference_date.md
- ../rules/Customer.age.md
- ../rules/Customer.as_of_now_or_sale.md
- ../rules/Customer.per_customer.md
- ../rules/Customer.register_not_buyers.md
---

A person on Contoso's customer register, each with a name, a birth date and a place — continent, country, state, city. The register is not the buyer list: many registered customers have never ordered (rule Customer.register_not_buyers). The account is pages/knowledge/customer.md.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`dim_customer`](../../data/datasets/dim_customer.md)
- **Counts** — `customer_key` (no `counts`: the dataset key)
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*7 rule(s) are about this concept, 7 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Country.where_we_have_customers](../rules/Country.where_we_have_customers.md) — **ruled** · names it · prose — not enforced (owner operator) — A question asking for the countries where we have customers asks for countries: the countries at least one customer lives in, one answer row per country, never one row per customer. Country is the subject and Customer the restriction. The same reading holds for other existence phrasings — countries that have a customer, with any customer — and the question must be answered, not refused.
- [Country.whose](../rules/Country.whose.md) — **ruled** · names it · choice over `territory`, `store`, `customer`, `location` — default `territory` — When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.
- [Customer.active_on_the_reference_date](../rules/Customer.active_on_the_reference_date.md) — **proposed** · parent · choice over `active`, `registered` — default `active` — A customer is active on a reference date when that date falls inside the customer's validity window — on or after the day the record became valid and on or before the day it stopped being valid. The reference date is the date the question states, else the data's own "now", and the answer says which. "Customers" with no other word means the active customers; "registered" customers are every customer on the register, whether valid on that date or not. Active customers are not the same set as customers who have bought something — each can hold people the other does not.
- [Customer.age](../rules/Customer.age.md) — **proposed** · parent · prose — not enforced (owner operator) — An age is computed, never stored: a customer's age from the birth date and a store's age from its opening date, both measured at the sampling date rather than at today's date. Which age arithmetic is meant — completed years counting the birthday, or calendar year boundaries crossed — has not been ruled.
- [Customer.as_of_now_or_sale](../rules/Customer.as_of_now_or_sale.md) — **proposed** · parent · prose — not enforced (owner operator) — The customer register keeps history: a row is a version of a person, valid over a window. The customer as they are now and the customer a past sale was made to can be different rows, and reading one as the other moves old sales to new addresses. A question joining customers to sales over a period says which it means; neither reading is declared the default.
- [Customer.per_customer](../rules/Customer.per_customer.md) — **proposed** · parent · choice over `buyers`, `active`, `registered` — default `buyers` — A figure "per customer" divides by a count of customers, and which customers it counts is a choice. By default it counts the buyers: the distinct customers on the sales lines the figure is summed over, so revenue per customer by country divides each country's revenue by the customers who bought in that country. The other options count the customers active on the reference date, or every customer on the register. The answer says which customers it divided by.
- [Customer.register_not_buyers](../rules/Customer.register_not_buyers.md) — **proposed** · parent · prose — not enforced (owner operator) — The customer register is wider than the buyers: a customer is a person on the register, and many registered customers have never bought anything. This is by design of the source, not a defect. "Customers" and "buyers" are two populations, and an answer counting customers says which one it counted.

**Words**

*52 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| birthday | `dataset:dim_customer.birth_date` | binds | — | — | — |
| born | `dataset:dim_customer.birth_date` | binds | — | — | — |
| date of birth | `dataset:dim_customer.birth_date` | binds | — | — | — |
| town | `dataset:dim_customer.city` | binds | — | — | — |
| where the buyer is | `dataset:dim_customer.country_code` | binds | — | — | — |
| customer id | `dataset:dim_customer.customer_key` | binds | — | — | — |
| name | `dataset:dim_customer.customer_name` | binds | — | — | — |
| who | `dataset:dim_customer.customer_name` | binds | — | — | — |
| sex | `dataset:dim_customer.gender` | binds | — | — | — |
| province | `dataset:dim_customer.state` | binds | — | — | — |
| region | `dataset:dim_customer.state` | binds | — | — | — |
| record from | `dataset:dim_customer.valid_from` | binds | — | — | — |
| valid from | `dataset:dim_customer.valid_from` | binds | — | — | — |
| record until | `dataset:dim_customer.valid_to` | binds | — | — | — |
| active | `rule:Customer.active_on_the_reference_date` | finds | — | — | — |
| as of | `rule:Customer.active_on_the_reference_date` | finds | — | — | — |
| customer | `rule:Customer.active_on_the_reference_date` | finds | — | — | — |
| how many customers | `rule:Customer.active_on_the_reference_date` | finds | — | — | — |
| reference date | `rule:Customer.active_on_the_reference_date` | finds | — | — | — |
| registered | `rule:Customer.active_on_the_reference_date` | finds | — | — | — |
| stichtag | `rule:Customer.active_on_the_reference_date` | finds | — | — | — |
| valid | `rule:Customer.active_on_the_reference_date` | finds | — | — | — |
| active | `rule:Customer.active_on_the_reference_date.active` | binds | — | — | — |
| active customers | `rule:Customer.active_on_the_reference_date.active` | binds | — | — | — |
| current | `rule:Customer.active_on_the_reference_date.active` | binds | — | — | — |
| current customers | `rule:Customer.active_on_the_reference_date.active` | binds | — | — | — |
| valid | `rule:Customer.active_on_the_reference_date.active` | binds | — | — | — |
| all customers | `rule:Customer.active_on_the_reference_date.registered` | binds | — | — | — |
| ever registered | `rule:Customer.active_on_the_reference_date.registered` | binds | — | — | — |
| on the register | `rule:Customer.active_on_the_reference_date.registered` | binds | — | — | — |
| registered | `rule:Customer.active_on_the_reference_date.registered` | binds | — | — | — |
| registered customers | `rule:Customer.active_on_the_reference_date.registered` | binds | — | — | — |
| age | `rule:Customer.age` | finds | — | — | — |
| average age | `rule:Customer.age` | finds | — | — | — |
| birth date | `rule:Customer.age` | finds | — | — | — |
| customer age | `rule:Customer.age` | finds | — | — | — |
| opening date | `rule:Customer.age` | finds | — | — | — |
| store age | `rule:Customer.age` | finds | — | — | — |
| as of | `rule:Customer.as_of_now_or_sale` | finds | — | — | — |
| customer | `rule:Customer.as_of_now_or_sale` | finds | — | — | — |
| history | `rule:Customer.as_of_now_or_sale` | finds | — | — | — |
| moved | `rule:Customer.as_of_now_or_sale` | finds | — | — | — |
| valid from | `rule:Customer.as_of_now_or_sale` | finds | — | — | — |
| valid to | `rule:Customer.as_of_now_or_sale` | finds | — | — | — |
| version | `rule:Customer.as_of_now_or_sale` | finds | — | — | — |
| per customer | `rule:Customer.per_customer` | finds | — | — | — |
| buyer | `rule:Customer.register_not_buyers` | finds | — | — | — |
| count customers | `rule:Customer.register_not_buyers` | finds | — | — | — |
| customer | `rule:Customer.register_not_buyers` | finds | — | — | — |
| never bought | `rule:Customer.register_not_buyers` | finds | — | — | — |
| population | `rule:Customer.register_not_buyers` | finds | — | — | — |
| register | `rule:Customer.register_not_buyers` | finds | — | — | — |

## Grounded in

- [`dim_customer`](../../data/datasets/dim_customer.md) — served as `"contoso_served"."dim_customer"`

## Grain

- One row of `dim_customer` is identified by `customer_key` (the dataset key).
- One Customer is one row — no `counts`, so the instance is the dataset key.
- `valid` start=`valid_from`, end=`valid_end` — versions of one instance in real-world time (L6).

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `customer_key` | identifier | — | — | — | — | the row key: one row per customer. The register is not the buyer list — many customers have never ordered (rule Customer.register_not_buyers). | ← [Order](Order.md) via `order__placed_by__customer` |
| `customer_name` | name | — | — | names `customer_key` (common) | — | the customer's name as registered. | — |
| `continent` | dimension | — | — | — | — | the continent the customer lives on. | — |
| `country_code` | dimension | — | — | — | [`dim_country`](../../data/datasets/dim_country.md).`country_code` via `customer__based_in__country` | the country the CUSTOMER lives in. No customer carries the `--` online placeholder. This is the only column that can place an internet sale in a real country. | [Country](Country.md) via `customer__based_in__country` |
| `state` | dimension | — | — | — | — | the state, province or region the customer lives in. | — |
| `city` | dimension | — | — | — | — | the city the customer lives in. | — |
| `gender` | dimension | — | — | — | — | the customer's recorded gender. | — |
| `birth_date` | date | — | — | — | — | the customer's date of birth. | — |
| `valid_from` | identifier | — | — | — | — | the day this customer record became valid — the start of the validity window that says whether a customer is active on a reference date. The register is kept as a history, so a sale could in principle be attributed to where the customer lived ON THE ORDER DATE — nothing in this bundle declares that it should be. | — |
| `valid_to` | identifier | — | — | — | — | the day this customer record stopped being valid — the last day of the validity window, as the source states it. Paired with `valid_from`. | — |
| `valid_end` | identifier | — | — | — | — | the day after `valid_to`: the half-open end of the validity window, made by the transform. A record is valid on a day when `valid_from` is on or before it and `valid_end` is after it, which selects exactly the records `valid_to` on or after that day selects. It is what rule Customer.active_on_the_reference_date reads; offered to no question on its own. | — |

_Declared per column, over 11 served columns: is 11 of 11 · label 0 of 11 · measure 0 of 11 · names 1 of 11 · value set 1 of 11 · means 11 of 11 · joins → 2 of 11. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind |
|---|---|
| `continent` | dimension |
| `country_code` | dimension |
| `state` | dimension |
| `city` | dimension |
| `gender` | dimension |
| `birth_date` | date |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

*1 edge(s) out · 1 in — the only joins (L7), walked in both directions.*

**Joins to** — edges from this concept:

- [Country](Country.md) — `customer__based_in__country` on `country_code` = `country_code`

**Joined from** — edges into this concept:

- [Order](Order.md) — `order__placed_by__customer` on `customer_key` = `customer_key`

## Source of record

- Declaration: `ontology/concepts/Customer.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/Customer.md`](../../../ontology/concepts/Customer.md) — the authored account (X-3); this page cites it and never writes it.
