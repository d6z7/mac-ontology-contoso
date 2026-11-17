---
type: Doc
title: SME questions — ontology
description: 2 questions and 39 sign-off requests the model and its tests put to an SME
tags:
- Contoso 5
- sme-questions
---

What the model and its tests ask a subject-matter expert: **2 question(s)** and **39 sign-off request(s)**, 41 row(s) in all. Consolidated from the rules (state and wording), the concepts and their datasets, and test oracles flagged needs-SME; projected from pages/ontology/ontology_quality.json and acceptance/sme_needs.json, so it stays in sync.

Conversation status is not part of this projection; it lives in the bundle's SME question ledger.

Rows by origin: register 41

## Questions — 2

### `concept:Country#enumeration`

- origin: register · owner role: not declared · concept: [Country](../../ontology/concepts/Country.md)
- source: `data/datasets/dim_country.yaml` → `members.complete`

> Is “Country” a closed set of values — every kind in the world, every value in this data, or an open list? Its value set dim_country does not say (`members.complete`).

### `concept:Currency#enumeration`

- origin: register · owner role: not declared · concept: [Currency](../../ontology/concepts/Currency.md)
- source: `data/datasets/dim_currency.yaml` → `members.complete`

> Is “Currency” a closed set of values — every kind in the world, every value in this data, or an open list? Its value set dim_currency does not say (`members.complete`).

## Sign-offs — 39

### `rule:Brand.not_manufacturer#state`

- origin: register · owner role: not declared · concept: [Brand](../../ontology/concepts/Brand.md), [Product](../../ontology/concepts/Product.md)
- source: `ontology/rules/Brand.not_manufacturer.yaml` → `state`

> Is the rule “Brand.not_manufacturer” right? It is recorded as proposed, not ruled: A brand is the name a customer buys a product under; a manufacturer is who made it. The two sets overlap in names but are two notions, and a question asking who is behind a product says which it means rather than treating them as interchangeable.

### `rule:Color.one_spelling#state`

- origin: register · owner role: not declared · concept: [Color](../../ontology/concepts/Color.md)
- source: `ontology/rules/Color.one_spelling.yaml` → `state`

> Is the rule “Color.one_spelling” right? It is recorded as proposed, not ruled: A colour is one member however the source spells its case: colour names are capitalised, so Blue and blue are one colour. A breakdown or count by colour never lists two spellings of one colour.

### `rule:Country.rows#state`

- origin: register · owner role: not declared · concept: [Country](../../ontology/concepts/Country.md)
- source: `ontology/rules/Country.rows.yaml` → `state`

> Is the rule “Country.rows” right? It is recorded as proposed, not ruled: The placeholder country code `--` is not a country. It marks rows that carry no real country, such as the online store. Questions about countries count and list real countries only, unless they name the placeholder.

### `rule:Country.where_we_have_customers#wording`

- origin: register · owner role: not declared · concept: [Country](../../ontology/concepts/Country.md), [Customer](../../ontology/concepts/Customer.md)
- source: `ontology/rules/Country.where_we_have_customers.yaml` → `says`

> Is this how you would state the rule “Country.where_we_have_customers”? Its statement quotes none of the words it was ruled in, and awaits your acceptance: A question asking for the countries where we have customers asks for countries: the countries at least one customer lives in, one answer row per country, never one row per customer. Country is the subject and Customer the restriction. The same reading holds for other existence phrasings — countries that have a customer, with any customer — and the question must be answered, not refused.

### `rule:Country.whose#wording`

- origin: register · owner role: not declared · concept: [Country](../../ontology/concepts/Country.md), [Customer](../../ontology/concepts/Customer.md), [Order](../../ontology/concepts/Order.md), [Store](../../ontology/concepts/Store.md)
- source: `ontology/rules/Country.whose.yaml` → `says`

> Is this how you would state the rule “Country.whose”? Its statement quotes none of the words it was ruled in, and awaits your acceptance: When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.

### `rule:Currency.code_is_not_the_unit#state`

- origin: register · owner role: not declared · concept: [Currency](../../ontology/concepts/Currency.md), [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Currency.code_is_not_the_unit.yaml` → `state`

> Is the rule “Currency.code_is_not_the_unit” right? It is recorded as proposed, not ruled: Every amount on a sale is in US dollars. A sale's currency is the currency the customer transacted in, not the unit of its amounts: filtering by that currency does not turn the amounts into it. Sales asked for in a named currency are converted through the exchange rate.

### `rule:Currency.whose#state`

- origin: register · owner role: not declared · concept: [Currency](../../ontology/concepts/Currency.md), [Order](../../ontology/concepts/Order.md), [Store](../../ontology/concepts/Store.md), [Location](../../ontology/concepts/Location.md), [ExchangeRate](../../ontology/concepts/ExchangeRate.md)
- source: `ontology/rules/Currency.whose.yaml` → `state`

> Is the rule “Currency.whose” right? It is recorded as proposed, not ruled: A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.

### `rule:Customer.active_on_the_reference_date#state`

- origin: register · owner role: not declared · concept: [Customer](../../ontology/concepts/Customer.md)
- source: `ontology/rules/Customer.active_on_the_reference_date.yaml` → `state`

> Is the rule “Customer.active_on_the_reference_date” right? It is recorded as proposed, not ruled: A customer is active on a reference date when that date falls inside the customer's validity window — on or after the day the record became valid and on or before the day it stopped being valid. The reference date is the date the question states, else the data's own "now", and the answer says which. "Customers" with no other word means the active customers; "registered" customers are every customer on the register, whether valid on that date or not. Active customers are not the same set as customers who have bought something — each can hold people the other does not.

### `rule:Customer.age#state`

- origin: register · owner role: not declared · concept: [Customer](../../ontology/concepts/Customer.md), [Store](../../ontology/concepts/Store.md)
- source: `ontology/rules/Customer.age.yaml` → `state`

> Is the rule “Customer.age” right? It is recorded as proposed, not ruled: An age is computed, never stored: a customer's age from the birth date and a store's age from its opening date, both measured at the sampling date rather than at today's date. Which age arithmetic is meant — completed years counting the birthday, or calendar year boundaries crossed — has not been ruled.

### `rule:Customer.as_of_now_or_sale#state`

- origin: register · owner role: not declared · concept: [Customer](../../ontology/concepts/Customer.md), [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Customer.as_of_now_or_sale.yaml` → `state`

> Is the rule “Customer.as_of_now_or_sale” right? It is recorded as proposed, not ruled: The customer register keeps history: a row is a version of a person, valid over a window. The customer as they are now and the customer a past sale was made to can be different rows, and reading one as the other moves old sales to new addresses. A question joining customers to sales over a period says which it means; neither reading is declared the default.

### `rule:Customer.per_customer#state`

- origin: register · owner role: not declared · concept: [Customer](../../ontology/concepts/Customer.md), [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Customer.per_customer.yaml` → `state`

> Is the rule “Customer.per_customer” right? It is recorded as proposed, not ruled: A figure "per customer" divides by a count of customers, and which customers it counts is a choice. By default it counts the buyers: the distinct customers on the sales lines the figure is summed over, so revenue per customer by country divides each country's revenue by the customers who bought in that country. The other options count the customers active on the reference date, or every customer on the register. The answer says which customers it divided by.

### `rule:Customer.register_not_buyers#state`

- origin: register · owner role: not declared · concept: [Customer](../../ontology/concepts/Customer.md)
- source: `ontology/rules/Customer.register_not_buyers.yaml` → `state`

> Is the rule “Customer.register_not_buyers” right? It is recorded as proposed, not ruled: The customer register is wider than the buyers: a customer is a person on the register, and many registered customers have never bought anything. This is by design of the source, not a defect. "Customers" and "buyers" are two populations, and an answer counting customers says which one it counted.

### `rule:ExchangeRate.convert_per_day#state`

- origin: register · owner role: not declared · concept: [ExchangeRate](../../ontology/concepts/ExchangeRate.md)
- source: `ontology/rules/ExchangeRate.convert_per_day.yaml` → `state`

> Is the rule “ExchangeRate.convert_per_day” right? It is recorded as proposed, not ruled: An amount is converted at its own day's rate, never at a rate averaged over a period. A rate is not a quantity to add up: over time it can at most be averaged, and across currency pairs it is not combined at all.

### `rule:ExchangeRate.direction_is_part_of_the_key#state`

- origin: register · owner role: not declared · concept: [ExchangeRate](../../ontology/concepts/ExchangeRate.md), [Currency](../../ontology/concepts/Currency.md)
- source: `ontology/rules/ExchangeRate.direction_is_part_of_the_key.yaml` → `state`

> Is the rule “ExchangeRate.direction_is_part_of_the_key” right? It is recorded as proposed, not ruled: An exchange rate's target currency means something only together with its source currency: the direction is part of the rate's identity, so a rate is never picked or grouped by its target currency alone.

### `rule:Location.channel#state`

- origin: register · owner role: not declared · concept: [Location](../../ontology/concepts/Location.md)
- source: `ontology/rules/Location.channel.yaml` → `state`

> Is the rule “Location.channel” right? It is recorded as proposed, not ruled: The online store is recorded as a location, but it is not a place. Questions about locations and places cover physical locations only, unless they name the online channel.

### `rule:Location.closed#state`

- origin: register · owner role: not declared · concept: [Location](../../ontology/concepts/Location.md)
- source: `ontology/rules/Location.closed.yaml` → `state`

> Is the rule “Location.closed” right? It is recorded as proposed, not ruled: A site counts as closed when a store at it has closed, whether or not another store trades there now. A question may ask instead for the sites where no store trades now. The answer says which it counted.

### `rule:Location.site#state`

- origin: register · owner role: not declared · concept: [Location](../../ontology/concepts/Location.md)
- source: `ontology/rules/Location.site.yaml` → `state`

> Is the rule “Location.site” right? It is recorded as proposed, not ruled: Site and location name the same notion: the place a store stands on, described by its country and its state or region. A store's place has no city in this business's data — its finest geography is the state or region — and a city is only where a customer lives, so a question about the cities stores are in has no answer here and must say so rather than offer site codes.

### `rule:Order.channel#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.channel.yaml` → `state`

> Is the rule “Order.channel” right? It is recorded as proposed, not ruled: A sale is made in one of two channels: a shop you can walk into or the web shop. A figure of the sale that names no channel covers both channels, even when the question reaches the sale through stores; a question that names the shops or the web shop gets that channel. The answer says which channels it covered.

### `rule:Order.cost_is_procurement#wording`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.cost_is_procurement.yaml` → `says`

> Is this how you would state the rule “Order.cost_is_procurement”? Its statement quotes none of the words it was ruled in, and awaits your acceptance: Cost means only what the goods cost Contoso to buy — the procurement cost. Every other money figure on a sale, gross, net, discount and margin, is revenue or income, never a cost.

### `rule:Order.date#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.date.yaml` → `state`

> Is the rule “Order.date” right? It is recorded as proposed, not ruled: An order's date is the day it was placed, not the day it was delivered. A question that says when, or names a period, without saying delivery is answered on the order date; a question that says delivered or shipped is answered on the delivery date.

### `rule:Order.default_measure#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.default_measure.yaml` → `state`

> Is the rule “Order.default_measure” right? It is recorded as proposed, not ruled: A question about Order that names no figure reads `net_amount`; the other figures are read when named.

### `rule:Order.discount_percent_is_over_gross#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.discount_percent_is_over_gross.yaml` → `state`

> Is the rule “Order.discount_percent_is_over_gross” right? It is recorded as proposed, not ruled: A discount percentage is the money given away divided by the gross amount before discount — not by the net amount.

### `rule:Order.discount_total_is_money#wording`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.discount_total_is_money.yaml` → `says`

> Is this how you would state the rule “Order.discount_total_is_money”? Its statement quotes none of the words it was ruled in, and awaits your acceptance: A total discount is money: the sum of what was given away below the regular price on every discounted sale in scope. It is never a sum or an average of discount rates. The rate is meant only when the question names it — discount percentage, discount rate, average discount.

### `rule:Order.how_many#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.how_many.yaml` → `state`

> Is the rule “Order.how_many” right? It is recorded as proposed, not ruled: How many is three questions. Purchases are counted as orders; items sold are the quantity summed; order lines are how the data is stored and are not a business quantity. "How many did we sell" asks for items, "how many times did we sell" or "how many orders" asks for purchases.

### `rule:Order.is_the_purchase#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.is_the_purchase.yaml` → `state`

> Is the rule “Order.is_the_purchase” right? It is recorded as proposed, not ruled: An order is the purchase: one customer buying at one store on one day in one currency. Its lines are not orders and not events of their own — a line borrows the when, the who and the where from its order and adds only which product and how many. Counting orders counts purchases, never lines.

### `rule:Order.margin_ratio_is_named#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.margin_ratio_is_named.yaml` → `state`

> Is the rule “Order.margin_ratio_is_named” right? It is recorded as proposed, not ruled: A margin ratio can be stated two ways over the same profit, and the question must say which: margin percent is profit over net revenue, markup is profit over cost. A question naming neither is asked.

### `rule:Order.no_lifecycle_state#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.no_lifecycle_state.yaml` → `state`

> Is the rule “Order.no_lifecycle_state” right? It is recorded as proposed, not ruled: An order has no state beyond its two dates: it was placed on one day and delivered on another. Nothing records a cancellation or a return, so a question about either has no answer in this business's data and says so; an absent state is never read as zero.

### `rule:Order.now_is_the_newest_order#wording`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.now_is_the_newest_order.yaml` → `says`

> Is this how you would state the rule “Order.now_is_the_newest_order”? Its statement quotes none of the words it was ruled in, and awaits your acceptance: "Now", for this data, is the date of the newest order — measured from the data, not taken from the clock. Relative periods such as "last month" are read against it, and it moves forward by itself when new orders arrive.

### `rule:Order.period#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.period.yaml` → `state`

> Is the rule “Order.period” right? It is recorded as proposed, not ruled: A question that names no period covers all time. There is no implied "this year" and no implied latest month, and the answer states the window it covered.

### `rule:Order.price_is_per_article#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.price_is_per_article.yaml` → `state`

> Is the rule “Order.price_is_per_article” right? It is recorded as proposed, not ruled: An unqualified price means what the customer paid per article: the net amount divided by the number of units, both summed over the lines asked about — never an average of line prices.

### `rule:Order.price_terms#wording`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.price_terms.yaml` → `says`

> Is this how you would state the rule “Order.price_terms”? Its statement quotes none of the words it was ruled in, and awaits your acceptance: Four facts on a sale carry every price and cost. The unit price is the regular, list price of one unit before discount; the net price is the actual selling price of one unit after discount; the unit cost is what one unit cost Contoso; the quantity is how many units. Every amount derives from them: gross is quantity times unit price, net is quantity times net price, cost is quantity times unit cost, discount is gross less net, and margin is net less cost — so margin is profit on the discounted price, not on list. "Unit price" names the regular price, not what was paid.

### `rule:Order.rate_on_order_date#state`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md), [ExchangeRate](../../ontology/concepts/ExchangeRate.md)
- source: `ontology/rules/Order.rate_on_order_date.yaml` → `state`

> Is the rule “Order.rate_on_order_date” right? It is recorded as proposed, not ruled: An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a target currency alone does not pick a rate.

### `rule:Order.revenue_means_net#wording`

- origin: register · owner role: not declared · concept: [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Order.revenue_means_net.yaml` → `says`

> Is this how you would state the rule “Order.revenue_means_net”? Its statement quotes none of the words it was ruled in, and awaits your acceptance: "Revenue" or "sales" without "net" or "gross" means the net amount — what the customer was charged after discount — and the answer says so. "Gross revenue" means the amount before discount.

### `rule:Product.price_is_dated#state`

- origin: register · owner role: not declared · concept: [Product](../../ontology/concepts/Product.md), [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Product.price_is_dated.yaml` → `state`

> Is the rule “Product.price_is_dated” right? It is recorded as proposed, not ruled: A product carries no standing price and no standing cost. A price changes over time, so every price and cost is the one on the sale, dated by the sale, and a product's price is reached through its sales. A product's current price is the regular unit price on its latest sale, stated with that sale's date where it matters. A question qualifying products by price — high-value products — selects products by that price and then counts all their sales, never qualifies individual sale lines.

### `rule:ProductCategory.level#state`

- origin: register · owner role: not declared · concept: [ProductCategory](../../ontology/concepts/ProductCategory.md)
- source: `ontology/rules/ProductCategory.level.yaml` → `state`

> Is the rule “ProductCategory.level” right? It is recorded as proposed, not ruled: A product category is the top level of the product hierarchy. A question saying category is answered on the category; one saying sub-category is answered on the sub-category.

### `rule:Store.channel#wording`

- origin: register · owner role: not declared · concept: [Store](../../ontology/concepts/Store.md), [Order](../../ontology/concepts/Order.md)
- source: `ontology/rules/Store.channel.yaml` → `says`

> Is this how you would state the rule “Store.channel”? Its statement quotes none of the words it was ruled in, and awaits your acceptance: A store is a shop you can walk into. The online channel is recorded as a store, but a question about stores — how many there are, which ones — covers physical shops only unless it names the online channel. That default holds only when the question is about stores: revenue and every other figure of the sale includes both channels, even when the question's route passes through stores.

### `rule:Store.premises_not_place#state`

- origin: register · owner role: not declared · concept: [Store](../../ontology/concepts/Store.md), [Location](../../ontology/concepts/Location.md)
- source: `ontology/rules/Store.premises_not_place.yaml` → `state`

> Is the rule “Store.premises_not_place” right? It is recorded as proposed, not ruled: A store is the premises Contoso sells from: a shop standing on one place for one trading period, with its own name, floor area, opening date and closing date. It is part of a location, not the location itself — one place may hold a succession of premises over time, each of them a store. So one store is counted and listed by its premises, and a count, list or sum over stores is a different question from the same figure over places; an answer that could be read at either level says which level it used. The site reading (one row per place, whatever premises it held) is the other option.

### `rule:Store.record_questions#state`

- origin: register · owner role: not declared · concept: [Store](../../ontology/concepts/Store.md)
- source: `ontology/rules/Store.record_questions.yaml` → `state`

> Is the rule “Store.record_questions” right? It is recorded as proposed, not ruled: A question about what the store table records — how many store versions or rows there are, or a list of every restructured store — covers every recorded row, the online channel included, with no channel or trading-state restriction. "How many stores do we have" is a different question and keeps the physical and active defaults.

### `rule:Store.trading#wording`

- origin: register · owner role: not declared · concept: [Store](../../ontology/concepts/Store.md)
- source: `ontology/rules/Store.trading.yaml` → `says`

> Is this how you would state the rule “Store.trading”? Its statement quotes none of the words it was ruled in, and awaits your acceptance: A store is active while it has no closing date. A store with a closing date is closed, and a closed store is either shut — closed for good — or restructured — closed and replaced. A question about stores covers active stores unless it names another state.

## Findings — 0 (not questions)

None.

## Operator items — 0 (not SME questions)

None.
