---
type: Reference
title: Usage guardrails — how to answer Contoso 5 safely
tags: [reference, guardrail]
---

# Usage guardrails (read first)

This page is projected from the ontology — every routing decision, default and rule below is declared in the bundle, not invented here. **Only interpretation is probabilistic; generate SQL from the question + this ontology ALONE, never from a live probe.** A fact the ontology does not state is a GAP to flag, not a value to guess.

## Routing — which dataset answers what

| concept | table | served as | answer with |
|---|---|---|---|
| [Brand](../ontology/concepts/Brand.md) | `dim_product` | `"contoso_served"."dim_product"` | 1 rule(s) — see below |
| [Colour](../ontology/concepts/Color.md) | `dim_product` | `"contoso_served"."dim_product"` | 1 rule(s) — see below |
| [Country](../ontology/concepts/Country.md) | `dim_country` | `"contoso_served"."dim_country"` | Country.rows: default `real`; Country.whose: default `territory` |
| [Currency](../ontology/concepts/Currency.md) | `dim_currency` | `"contoso_served"."dim_currency"` | Currency.whose: default `paid_in` |
| [Customer](../ontology/concepts/Customer.md) | `dim_customer` | `"contoso_served"."dim_customer"` | Customer.active_on_the_reference_date: default `active`; Customer.per_customer: default `buyers` |
| [ExchangeRate](../ontology/concepts/ExchangeRate.md) | `v_contoso5_fx_rate` | `"contoso_served"."v_contoso5_fx_rate"` | 4 rule(s) — see below |
| [Location](../ontology/concepts/Location.md) | `dim_location` | `"contoso_served"."dim_location"` | Location.channel: default `physical`; Location.closed: default `ever` |
| [Order](../ontology/concepts/Order.md) | `v_contoso5_sales_line` | `"contoso_served"."v_contoso5_sales_line"` | Order.channel: default `both`; Order.date: default `ordered`; Order.default_measure: default `net_amount`; Order.discoun |
| [Product](../ontology/concepts/Product.md) | `dim_product` | `"contoso_served"."dim_product"` | 2 rule(s) — see below |
| [ProductCategory](../ontology/concepts/ProductCategory.md) | `dim_product` | `"contoso_served"."dim_product"` | ProductCategory.level: default `category` |
| [Store](../ontology/concepts/Store.md) | `dim_store` | `"contoso_served"."dim_store"` | Store.trading: default `active` |

## How to answer — per-concept playbooks (the rules whose `about` names the concept)

### Brand — `dim_product`

- `Brand.not_manufacturer` — **proposed** — A brand is the name a customer buys a product under; a manufacturer is who made it. The two sets overlap in names but are two notions, and a question asking who is behind a product says which it means rather than treating them as interchangeable.

### Colour — `dim_product`

- `Color.one_spelling` — **proposed** — A colour is one member however the source spells its case: colour names are capitalised, so Blue and blue are one colour. A breakdown or count by colour never lists two spellings of one colour.

### Country — `dim_country`

- `Country.rows` — **proposed** — The placeholder country code `--` is not a country. It marks rows that carry no real country, such as the online store. Questions about countries count and list real countries only, unless they name the placeholder.
- `Country.where_we_have_customers` — **ruled** — A question asking for the countries where we have customers asks for countries: the countries at least one customer lives in, one answer row per country, never one row per customer. Country is the subject and Customer the restriction. The same reading holds for other existence phrasings — countries that have a customer, with any customer — and the question must be answered, not refused.
- `Country.whose` — **ruled** — When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.

### Currency — `dim_currency`

- `Currency.code_is_not_the_unit` — **proposed** — Every amount on a sale is in US dollars. A sale's currency is the currency the customer transacted in, not the unit of its amounts: filtering by that currency does not turn the amounts into it. Sales asked for in a named currency are converted through the exchange rate.
- `Currency.whose` — **proposed** — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- `ExchangeRate.direction_is_part_of_the_key` — **proposed** — An exchange rate's target currency means something only together with its source currency: the direction is part of the rate's identity, so a rate is never picked or grouped by its target currency alone.

### Customer — `dim_customer`

- `Customer.active_on_the_reference_date` — **proposed** — A customer is active on a reference date when that date falls inside the customer's validity window — on or after the day the record became valid and on or before the day it stopped being valid. The reference date is the date the question states, else the data's own "now", and the answer says which. "Customers" with no other word means the active customers; "registered" customers are every customer on the register, whether valid on that date or not. Active customers are not the same set as customers who have bought something — each can hold people the other does not.
- `Customer.age` — **proposed** — An age is computed, never stored: a customer's age from the birth date and a store's age from its opening date, both measured at the sampling date rather than at today's date. Which age arithmetic is meant — completed years counting the birthday, or calendar year boundaries crossed — has not been ruled.
- `Customer.as_of_now_or_sale` — **proposed** — The customer register keeps history: a row is a version of a person, valid over a window. The customer as they are now and the customer a past sale was made to can be different rows, and reading one as the other moves old sales to new addresses. A question joining customers to sales over a period says which it means; neither reading is declared the default.
- `Customer.per_customer` — **proposed** — A figure "per customer" divides by a count of customers, and which customers it counts is a choice. By default it counts the buyers: the distinct customers on the sales lines the figure is summed over, so revenue per customer by country divides each country's revenue by the customers who bought in that country. The other options count the customers active on the reference date, or every customer on the register. The answer says which customers it divided by.
- `Customer.register_not_buyers` — **proposed** — The customer register is wider than the buyers: a customer is a person on the register, and many registered customers have never bought anything. This is by design of the source, not a defect. "Customers" and "buyers" are two populations, and an answer counting customers says which one it counted.
- `Country.where_we_have_customers` — **ruled** — A question asking for the countries where we have customers asks for countries: the countries at least one customer lives in, one answer row per country, never one row per customer. Country is the subject and Customer the restriction. The same reading holds for other existence phrasings — countries that have a customer, with any customer — and the question must be answered, not refused.
- `Country.whose` — **ruled** — When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.

### ExchangeRate — `v_contoso5_fx_rate`

- `ExchangeRate.convert_per_day` — **proposed** — An amount is converted at its own day's rate, never at a rate averaged over a period. A rate is not a quantity to add up: over time it can at most be averaged, and across currency pairs it is not combined at all.
- `ExchangeRate.direction_is_part_of_the_key` — **proposed** — An exchange rate's target currency means something only together with its source currency: the direction is part of the rate's identity, so a rate is never picked or grouped by its target currency alone.
- `Currency.whose` — **proposed** — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- `Order.rate_on_order_date` — **proposed** — An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a target currency alone does not pick a rate.

### Location — `dim_location`

- `Location.channel` — **proposed** — The online store is recorded as a location, but it is not a place. Questions about locations and places cover physical locations only, unless they name the online channel.
- `Location.closed` — **proposed** — A site counts as closed when a store at it has closed, whether or not another store trades there now. A question may ask instead for the sites where no store trades now. The answer says which it counted.
- `Location.site` — **proposed** — Site and location name the same notion: the place a store stands on, described by its country and its state or region. A store's place has no city in this business's data — its finest geography is the state or region — and a city is only where a customer lives, so a question about the cities stores are in has no answer here and must say so rather than offer site codes.
- `Currency.whose` — **proposed** — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- `Store.premises_not_place` — **proposed** — A store is the premises Contoso sells from: a shop standing on one place for one trading period, with its own name, floor area, opening date and closing date. It is part of a location, not the location itself — one place may hold a succession of premises over time, each of them a store. So one store is counted and listed by its premises, and a count, list or sum over stores is a different question from the same figure over places; an answer that could be read at either level says which level it used. The site reading (one row per place, whatever premises it held) is the other option.

### Order — `v_contoso5_sales_line`

- `Order.channel` — **proposed** — A sale is made in one of two channels: a shop you can walk into or the web shop. A figure of the sale that names no channel covers both channels, even when the question reaches the sale through stores; a question that names the shops or the web shop gets that channel. The answer says which channels it covered.
- `Order.cost_is_procurement` — **ruled** — Cost means only what the goods cost Contoso to buy — the procurement cost. Every other money figure on a sale, gross, net, discount and margin, is revenue or income, never a cost.
- `Order.date` — **proposed** — An order's date is the day it was placed, not the day it was delivered. A question that says when, or names a period, without saying delivery is answered on the order date; a question that says delivered or shipped is answered on the delivery date.
- `Order.default_measure` — **proposed** — A question about Order that names no figure reads `net_amount`; the other figures are read when named.
- `Order.discount_percent_is_over_gross` — **proposed** — A discount percentage is the money given away divided by the gross amount before discount — not by the net amount.
- `Order.discount_total_is_money` — **ruled** — A total discount is money: the sum of what was given away below the regular price on every discounted sale in scope. It is never a sum or an average of discount rates. The rate is meant only when the question names it — discount percentage, discount rate, average discount.
- `Order.how_many` — **proposed** — How many is three questions. Purchases are counted as orders; items sold are the quantity summed; order lines are how the data is stored and are not a business quantity. "How many did we sell" asks for items, "how many times did we sell" or "how many orders" asks for purchases.
- `Order.is_the_purchase` — **proposed** — An order is the purchase: one customer buying at one store on one day in one currency. Its lines are not orders and not events of their own — a line borrows the when, the who and the where from its order and adds only which product and how many. Counting orders counts purchases, never lines.
- `Order.margin_ratio_is_named` — **proposed** — A margin ratio can be stated two ways over the same profit, and the question must say which: margin percent is profit over net revenue, markup is profit over cost. A question naming neither is asked.
- `Order.no_lifecycle_state` — **proposed** — An order has no state beyond its two dates: it was placed on one day and delivered on another. Nothing records a cancellation or a return, so a question about either has no answer in this business's data and says so; an absent state is never read as zero.
- `Order.now_is_the_newest_order` — **ruled** — "Now", for this data, is the date of the newest order — measured from the data, not taken from the clock. Relative periods such as "last month" are read against it, and it moves forward by itself when new orders arrive.
- `Order.period` — **proposed** — A question that names no period covers all time. There is no implied "this year" and no implied latest month, and the answer states the window it covered.
- `Order.price_is_per_article` — **proposed** — An unqualified price means what the customer paid per article: the net amount divided by the number of units, both summed over the lines asked about — never an average of line prices.
- `Order.price_terms` — **ruled** — Four facts on a sale carry every price and cost. The unit price is the regular, list price of one unit before discount; the net price is the actual selling price of one unit after discount; the unit cost is what one unit cost Contoso; the quantity is how many units. Every amount derives from them: gross is quantity times unit price, net is quantity times net price, cost is quantity times unit cost, discount is gross less net, and margin is net less cost — so margin is profit on the discounted price, not on list. "Unit price" names the regular price, not what was paid.
- `Order.rate_on_order_date` — **proposed** — An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a target currency alone does not pick a rate.
- `Order.revenue_means_net` — **ruled** — "Revenue" or "sales" without "net" or "gross" means the net amount — what the customer was charged after discount — and the answer says so. "Gross revenue" means the amount before discount.
- `Country.whose` — **ruled** — When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.
- `Currency.code_is_not_the_unit` — **proposed** — Every amount on a sale is in US dollars. A sale's currency is the currency the customer transacted in, not the unit of its amounts: filtering by that currency does not turn the amounts into it. Sales asked for in a named currency are converted through the exchange rate.
- `Currency.whose` — **proposed** — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- `Customer.as_of_now_or_sale` — **proposed** — The customer register keeps history: a row is a version of a person, valid over a window. The customer as they are now and the customer a past sale was made to can be different rows, and reading one as the other moves old sales to new addresses. A question joining customers to sales over a period says which it means; neither reading is declared the default.
- `Customer.per_customer` — **proposed** — A figure "per customer" divides by a count of customers, and which customers it counts is a choice. By default it counts the buyers: the distinct customers on the sales lines the figure is summed over, so revenue per customer by country divides each country's revenue by the customers who bought in that country. The other options count the customers active on the reference date, or every customer on the register. The answer says which customers it divided by.
- `Product.price_is_dated` — **proposed** — A product carries no standing price and no standing cost. A price changes over time, so every price and cost is the one on the sale, dated by the sale, and a product's price is reached through its sales. A product's current price is the regular unit price on its latest sale, stated with that sale's date where it matters. A question qualifying products by price — high-value products — selects products by that price and then counts all their sales, never qualifies individual sale lines.
- `Store.channel` — **ruled** — A store is a shop you can walk into. The online channel is recorded as a store, but a question about stores — how many there are, which ones — covers physical shops only unless it names the online channel. That default holds only when the question is about stores: revenue and every other figure of the sale includes both channels, even when the question's route passes through stores.

### Product — `dim_product`

- `Product.price_is_dated` — **proposed** — A product carries no standing price and no standing cost. A price changes over time, so every price and cost is the one on the sale, dated by the sale, and a product's price is reached through its sales. A product's current price is the regular unit price on its latest sale, stated with that sale's date where it matters. A question qualifying products by price — high-value products — selects products by that price and then counts all their sales, never qualifies individual sale lines.
- `Brand.not_manufacturer` — **proposed** — A brand is the name a customer buys a product under; a manufacturer is who made it. The two sets overlap in names but are two notions, and a question asking who is behind a product says which it means rather than treating them as interchangeable.

### ProductCategory — `dim_product`

- `ProductCategory.level` — **proposed** — A product category is the top level of the product hierarchy. A question saying category is answered on the category; one saying sub-category is answered on the sub-category.

### Store — `dim_store`

- `Store.record_questions` — **proposed** — A question about what the store table records — how many store versions or rows there are, or a list of every restructured store — covers every recorded row, the online channel included, with no channel or trading-state restriction. "How many stores do we have" is a different question and keeps the physical and active defaults.
- `Store.trading` — **ruled** — A store is active while it has no closing date. A store with a closing date is closed, and a closed store is either shut — closed for good — or restructured — closed and replaced. A question about stores covers active stores unless it names another state.
- `Country.whose` — **ruled** — When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.
- `Currency.whose` — **proposed** — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- `Customer.age` — **proposed** — An age is computed, never stored: a customer's age from the birth date and a store's age from its opening date, both measured at the sampling date rather than at today's date. Which age arithmetic is meant — completed years counting the birthday, or calendar year boundaries crossed — has not been ruled.
- `Store.channel` — **ruled** — A store is a shop you can walk into. The online channel is recorded as a store, but a question about stores — how many there are, which ones — covers physical shops only unless it names the online channel. That default holds only when the question is about stores: revenue and every other figure of the sale includes both channels, even when the question's route passes through stores.
- `Store.premises_not_place` — **proposed** — A store is the premises Contoso sells from: a shop standing on one place for one trading period, with its own name, floor area, opening date and closing date. It is part of a location, not the location itself — one place may hold a succession of premises over time, each of them a store. So one store is counted and listed by its premises, and a count, list or sum over stores is a different question from the same figure over places; an answer that could be read at either level says which level it used. The site reading (one row per place, whatever premises it held) is the other option.

## Filter traps & known issues

Recorded findings that change how you must query — an open finding that `blocks` an address makes a question reading it refuse (L14). Full detail in `known_issues/`.

- [DQ-AMBIGREF-CURRENCYCODE](known_issues/DQ-AMBIGREF-CURRENCYCODE.md) — _high_ · `CurrencyCode` includes perfectly into 2 different keys — which is THE reference? · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_brand-COLUMNS](known_issues/DQ-CASE-G-contoso5_brand-COLUMNS.md) — _high_ · data-sanity case G-contoso5_brand-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_brand-KEY](known_issues/DQ-CASE-G-contoso5_brand-KEY.md) — _high_ · data-sanity case G-contoso5_brand-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_brand-NULLS](known_issues/DQ-CASE-G-contoso5_brand-NULLS.md) — _medium_ · data-sanity case G-contoso5_brand-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_category_name-COLUMNS](known_issues/DQ-CASE-G-contoso5_category_name-COLUMNS.md) — _high_ · data-sanity case G-contoso5_category_name-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_category_name-KEY](known_issues/DQ-CASE-G-contoso5_category_name-KEY.md) — _high_ · data-sanity case G-contoso5_category_name-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_category_name-NULLS](known_issues/DQ-CASE-G-contoso5_category_name-NULLS.md) — _medium_ · data-sanity case G-contoso5_category_name-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_channel-COLUMNS](known_issues/DQ-CASE-G-contoso5_channel-COLUMNS.md) — _high_ · data-sanity case G-contoso5_channel-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_channel-KEY](known_issues/DQ-CASE-G-contoso5_channel-KEY.md) — _high_ · data-sanity case G-contoso5_channel-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_channel-NULLS](known_issues/DQ-CASE-G-contoso5_channel-NULLS.md) — _medium_ · data-sanity case G-contoso5_channel-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_color-COLUMNS](known_issues/DQ-CASE-G-contoso5_color-COLUMNS.md) — _high_ · data-sanity case G-contoso5_color-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_color-KEY](known_issues/DQ-CASE-G-contoso5_color-KEY.md) — _high_ · data-sanity case G-contoso5_color-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_color-NULLS](known_issues/DQ-CASE-G-contoso5_color-NULLS.md) — _medium_ · data-sanity case G-contoso5_color-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_continent-COLUMNS](known_issues/DQ-CASE-G-contoso5_continent-COLUMNS.md) — _high_ · data-sanity case G-contoso5_continent-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_continent-KEY](known_issues/DQ-CASE-G-contoso5_continent-KEY.md) — _high_ · data-sanity case G-contoso5_continent-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_continent-NULLS](known_issues/DQ-CASE-G-contoso5_continent-NULLS.md) — _medium_ · data-sanity case G-contoso5_continent-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_country_code-COLUMNS](known_issues/DQ-CASE-G-contoso5_country_code-COLUMNS.md) — _high_ · data-sanity case G-contoso5_country_code-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_country_code-KEY](known_issues/DQ-CASE-G-contoso5_country_code-KEY.md) — _high_ · data-sanity case G-contoso5_country_code-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_country_code-NULLS](known_issues/DQ-CASE-G-contoso5_country_code-NULLS.md) — _medium_ · data-sanity case G-contoso5_country_code-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_currency-COLUMNS](known_issues/DQ-CASE-G-contoso5_currency-COLUMNS.md) — _high_ · data-sanity case G-contoso5_currency-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_currency-KEY](known_issues/DQ-CASE-G-contoso5_currency-KEY.md) — _high_ · data-sanity case G-contoso5_currency-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_currency-NULLS](known_issues/DQ-CASE-G-contoso5_currency-NULLS.md) — _medium_ · data-sanity case G-contoso5_currency-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_gender-COLUMNS](known_issues/DQ-CASE-G-contoso5_gender-COLUMNS.md) — _high_ · data-sanity case G-contoso5_gender-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_gender-KEY](known_issues/DQ-CASE-G-contoso5_gender-KEY.md) — _high_ · data-sanity case G-contoso5_gender-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_gender-NULLS](known_issues/DQ-CASE-G-contoso5_gender-NULLS.md) — _medium_ · data-sanity case G-contoso5_gender-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_manufacturer-COLUMNS](known_issues/DQ-CASE-G-contoso5_manufacturer-COLUMNS.md) — _high_ · data-sanity case G-contoso5_manufacturer-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_manufacturer-KEY](known_issues/DQ-CASE-G-contoso5_manufacturer-KEY.md) — _high_ · data-sanity case G-contoso5_manufacturer-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_manufacturer-NULLS](known_issues/DQ-CASE-G-contoso5_manufacturer-NULLS.md) — _medium_ · data-sanity case G-contoso5_manufacturer-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_state-COLUMNS](known_issues/DQ-CASE-G-contoso5_state-COLUMNS.md) — _high_ · data-sanity case G-contoso5_state-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_state-KEY](known_issues/DQ-CASE-G-contoso5_state-KEY.md) — _high_ · data-sanity case G-contoso5_state-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_state-NULLS](known_issues/DQ-CASE-G-contoso5_state-NULLS.md) — _medium_ · data-sanity case G-contoso5_state-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_status-COLUMNS](known_issues/DQ-CASE-G-contoso5_status-COLUMNS.md) — _high_ · data-sanity case G-contoso5_status-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_status-KEY](known_issues/DQ-CASE-G-contoso5_status-KEY.md) — _high_ · data-sanity case G-contoso5_status-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_store_name-COLUMNS](known_issues/DQ-CASE-G-contoso5_store_name-COLUMNS.md) — _high_ · data-sanity case G-contoso5_store_name-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_store_name-KEY](known_issues/DQ-CASE-G-contoso5_store_name-KEY.md) — _high_ · data-sanity case G-contoso5_store_name-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_store_name-NULLS](known_issues/DQ-CASE-G-contoso5_store_name-NULLS.md) — _medium_ · data-sanity case G-contoso5_store_name-NULLS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_sub_category_name-COLUMNS](known_issues/DQ-CASE-G-contoso5_sub_category_name-COLUMNS.md) — _high_ · data-sanity case G-contoso5_sub_category_name-COLUMNS did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_sub_category_name-KEY](known_issues/DQ-CASE-G-contoso5_sub_category_name-KEY.md) — _high_ · data-sanity case G-contoso5_sub_category_name-KEY did not pass · **open — nobody has ruled**
- [DQ-CASE-G-contoso5_sub_category_name-NULLS](known_issues/DQ-CASE-G-contoso5_sub_category_name-NULLS.md) — _medium_ · data-sanity case G-contoso5_sub_category_name-NULLS did not pass · **open — nobody has ruled**
- [DQ-DANGLINGKEY-CATEGORYKEY](known_issues/DQ-DANGLINGKEY-CATEGORYKEY.md) — _medium_ · `CategoryKey` is key-shaped and no relation in scope carries it as a key · **open — nobody has ruled**
- [DQ-DANGLINGKEY-GEOAREAKEY](known_issues/DQ-DANGLINGKEY-GEOAREAKEY.md) — _medium_ · `GeoAreaKey` is key-shaped and no relation in scope carries it as a key · **open — nobody has ruled**
- [DQ-DANGLINGKEY-SUBCATEGORYKEY](known_issues/DQ-DANGLINGKEY-SUBCATEGORYKEY.md) — _medium_ · `SubCategoryKey` is key-shaped and no relation in scope carries it as a key · **open — nobody has ruled**
- [DQ-DUP-ORDERROWS-SALES](known_issues/DQ-DUP-ORDERROWS-SALES.md) — _medium_ · `sales` re-delivers every line of `orderrows` — one fact, twice · **open — nobody has ruled**
- [DQ-IDENTIFYING-DIM_CUSTOMER-CITY](known_issues/DQ-IDENTIFYING-DIM_CUSTOMER-CITY.md) — _medium_ · `dim_customer.city` names individuals — 21,317 of 34,581 values are held by exactly one row · **open — nobody has ruled**
- [DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME](known_issues/DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME.md) — _medium_ · `dim_customer.customer_name` names individuals — 94,488 of 99,200 values are held by exactly one row · **open — nobody has ruled**
- [DQ-ORPHAN-DATE](known_issues/DQ-ORPHAN-DATE.md) — _medium_ · raw landing `date` is consumed by no transformation · **open — nobody has ruled**
- [DQ-ORPHAN-ORDERROWS](known_issues/DQ-ORPHAN-ORDERROWS.md) — _medium_ · raw landing `orderrows` is consumed by no transformation · **open — nobody has ruled**
- [DQ-ORPHAN-ORDERS](known_issues/DQ-ORPHAN-ORDERS.md) — _medium_ · raw landing `orders` is consumed by no transformation · **open — nobody has ruled**
- [DQ-UNCLAIMED-CONTOSO5_BRAND](known_issues/DQ-UNCLAIMED-CONTOSO5_BRAND.md) — _medium_ · served relation `contoso5_brand` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_CATEGORY_NAME](known_issues/DQ-UNCLAIMED-CONTOSO5_CATEGORY_NAME.md) — _medium_ · served relation `contoso5_category_name` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_CHANNEL](known_issues/DQ-UNCLAIMED-CONTOSO5_CHANNEL.md) — _medium_ · served relation `contoso5_channel` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_COLOR](known_issues/DQ-UNCLAIMED-CONTOSO5_COLOR.md) — _medium_ · served relation `contoso5_color` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_CONTINENT](known_issues/DQ-UNCLAIMED-CONTOSO5_CONTINENT.md) — _medium_ · served relation `contoso5_continent` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_COUNTRY_CODE](known_issues/DQ-UNCLAIMED-CONTOSO5_COUNTRY_CODE.md) — _medium_ · served relation `contoso5_country_code` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_CURRENCY](known_issues/DQ-UNCLAIMED-CONTOSO5_CURRENCY.md) — _medium_ · served relation `contoso5_currency` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_GENDER](known_issues/DQ-UNCLAIMED-CONTOSO5_GENDER.md) — _medium_ · served relation `contoso5_gender` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_MANUFACTURER](known_issues/DQ-UNCLAIMED-CONTOSO5_MANUFACTURER.md) — _medium_ · served relation `contoso5_manufacturer` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_STATE](known_issues/DQ-UNCLAIMED-CONTOSO5_STATE.md) — _medium_ · served relation `contoso5_state` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_STATUS](known_issues/DQ-UNCLAIMED-CONTOSO5_STATUS.md) — _medium_ · served relation `contoso5_status` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_STORE_NAME](known_issues/DQ-UNCLAIMED-CONTOSO5_STORE_NAME.md) — _medium_ · served relation `contoso5_store_name` is claimed by no concept · **accepted · said by ontology-developer**
- [DQ-UNCLAIMED-CONTOSO5_SUB_CATEGORY_NAME](known_issues/DQ-UNCLAIMED-CONTOSO5_SUB_CATEGORY_NAME.md) — _medium_ · served relation `contoso5_sub_category_name` is claimed by no concept · **accepted · said by ontology-developer**
