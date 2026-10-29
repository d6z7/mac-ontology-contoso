---
type: Doc
title: SME questions — ontology
description: 6 questions and 58 sign-off requests the model and its tests put to an SME
tags:
- CONTOSO5
- sme-questions
---

What the model and its tests ask a subject-matter expert: **6 question(s)** and **58 sign-off request(s)**, 64 row(s) in all. Consolidated from the register (model conditions and change-record `sme` blocks), concept open-question fields and test oracles flagged needs-SME; projected from ontology_quality.json and acceptance/sme_needs.json, so it stays in sync.

Conversation status is not part of this projection; it lives in the bundle's SME question ledger.

Rows by origin: register 64

## Questions — 6

### `concept:brand#enumeration`

- origin: register · owner role: not declared · concept: [brand](concepts/brand.md)
- source: `ontology/concepts/brand.yaml` → `values`

> Is “Brand” a closed set of values? If it is, what are all of its valid values?

### `concept:color#enumeration`

- origin: register · owner role: not declared · concept: [color](concepts/color.md)
- source: `ontology/concepts/color.yaml` → `values`

> Is “Colour” a closed set of values? If it is, what are all of its valid values?

### `concept:country#enumeration`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/concepts/country.yaml` → `values`

> Is “Country” a closed set of values? If it is, what are all of its valid values?

### `concept:currency#enumeration`

- origin: register · owner role: not declared · concept: [currency](concepts/currency.md)
- source: `ontology/concepts/currency.yaml` → `values`

> Is “Currency” a closed set of values? If it is, what are all of its valid values?

### `concept:exchange_rate#measure_type`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/concepts/exchange_rate.yaml` → `grounding.source.columns[].offers.aggregate.type`

> How does the measure “Exchange Rate” add up across its axes? No column of it declares `offers.aggregate.type` that mac.concept.column.measure_type resolves.

### `concept:product_category#enumeration`

- origin: register · owner role: not declared · concept: [product_category](concepts/product_category.md)
- source: `ontology/concepts/product_category.yaml` → `values`

> Is “Product Category” a closed set of values? If it is, what are all of its valid values?

## Sign-offs — 58

### `concept:brand#confidence`

- origin: register · owner role: not declared · concept: [brand](concepts/brand.md)
- source: `ontology/concepts/brand.yaml` → `metadata.confidence`

> Is the concept “Brand” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:color#confidence`

- origin: register · owner role: not declared · concept: [color](concepts/color.md)
- source: `ontology/concepts/color.yaml` → `metadata.confidence`

> Is the concept “Colour” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:country#confidence`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/concepts/country.yaml` → `metadata.confidence`

> Is the concept “Country” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:currency#confidence`

- origin: register · owner role: not declared · concept: [currency](concepts/currency.md)
- source: `ontology/concepts/currency.yaml` → `metadata.confidence`

> Is the concept “Currency” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:customer#confidence`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md)
- source: `ontology/concepts/customer.yaml` → `metadata.confidence`

> Is the concept “Customer” (entity) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:exchange_rate#confidence`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/concepts/exchange_rate.yaml` → `metadata.confidence`

> Is the concept “Exchange Rate” (measure) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:location#confidence`

- origin: register · owner role: not declared · concept: [location](concepts/location.md)
- source: `ontology/concepts/location.yaml` → `metadata.confidence`

> Is the concept “Location” (entity) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:product#confidence`

- origin: register · owner role: not declared · concept: [product](concepts/product.md)
- source: `ontology/concepts/product.yaml` → `metadata.confidence`

> Is the concept “Product” (entity) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:product_category#confidence`

- origin: register · owner role: not declared · concept: [product_category](concepts/product_category.md)
- source: `ontology/concepts/product_category.yaml` → `metadata.confidence`

> Is the concept “Product Category” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:store#confidence`

- origin: register · owner role: not declared · concept: [store](concepts/store.md)
- source: `ontology/concepts/store.yaml` → `metadata.confidence`

> Is the concept “Store” (entity) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `rule:Brand.not_manufacturer#state`

- origin: register · owner role: not declared · concept: [brand](concepts/brand.md), [product](concepts/product.md)
- source: `ontology/rules/Brand.not_manufacturer.yaml` → `rule`

> Is the rule “Brand.not_manufacturer” right? It is recorded as proposed, not ruled: A brand is the name a customer buys a product under; a manufacturer is who made it. The two sets overlap in names but are two notions, and a question asking who is behind a product says which it means rather than treating them as interchangeable.

### `rule:Brand.not_manufacturer#wording`

- origin: register · owner role: not declared · concept: [brand](concepts/brand.md), [product](concepts/product.md)
- source: `ontology/rules/Brand.not_manufacturer.yaml` → `rule`

> Is this how you would state the rule “Brand.not_manufacturer”? The wording was sharpened for a reader and awaits your acceptance: A brand is the name a customer buys a product under; a manufacturer is who made it. The two sets overlap in names but are two notions, and a question asking who is behind a product says which it means rather than treating them as interchangeable.

### `rule:Color.one_spelling#wording`

- origin: register · owner role: not declared · concept: [color](concepts/color.md)
- source: `ontology/rules/Color.one_spelling.yaml` → `rule`

> Is this how you would state the rule “Color.one_spelling”? The wording was sharpened for a reader and awaits your acceptance: A colour is one member however the source spells its case: colour names are capitalised, so Blue and blue are one colour. A breakdown or count by colour never lists two spellings of one colour.

### `rule:Country.rows#state`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/rules/Country.rows.yaml` → `rule`

> Is the rule “Country.rows” right? It is recorded as proposed, not ruled: The placeholder country code `--` is not a country. It marks rows that carry no real country, such as the online store. Questions about countries count and list real countries only, unless they name the placeholder.

### `rule:Country.rows#wording`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/rules/Country.rows.yaml` → `rule`

> Is this how you would state the rule “Country.rows”? The wording was sharpened for a reader and awaits your acceptance: The placeholder country code `--` is not a country. It marks rows that carry no real country, such as the online store. Questions about countries count and list real countries only, unless they name the placeholder.

### `rule:Country.where_we_have_customers#wording`

- origin: register · owner role: not declared · concept: [country](concepts/country.md), [customer](concepts/customer.md)
- source: `ontology/rules/Country.where_we_have_customers.yaml` → `rule`

> Is this how you would state the rule “Country.where_we_have_customers”? The wording was sharpened for a reader and awaits your acceptance: A question asking for the countries where we have customers asks for countries: the countries at least one customer lives in, one answer row per country, never one row per customer. Country is the subject and Customer the restriction. The same reading holds for other existence phrasings — countries that have a customer, with any customer — and the question must be answered, not refused.

### `rule:Country.whose#wording`

- origin: register · owner role: not declared · concept: [country](concepts/country.md), [order](concepts/order.md), [store](concepts/store.md), [customer](concepts/customer.md)
- source: `ontology/rules/Country.whose.yaml` → `rule`

> Is this how you would state the rule “Country.whose”? The wording was sharpened for a reader and awaits your acceptance: When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.

### `rule:Currency.code_is_not_the_unit#state`

- origin: register · owner role: not declared · concept: [currency](concepts/currency.md), [order](concepts/order.md)
- source: `ontology/rules/Currency.code_is_not_the_unit.yaml` → `rule`

> Is the rule “Currency.code_is_not_the_unit” right? It is recorded as proposed, not ruled: Every amount on a sale is in US dollars. A sale's currency is the currency the customer transacted in, not the unit of its amounts: filtering by that currency does not turn the amounts into it. Sales asked for in a named currency are converted through the exchange rate.

### `rule:Currency.code_is_not_the_unit#wording`

- origin: register · owner role: not declared · concept: [currency](concepts/currency.md), [order](concepts/order.md)
- source: `ontology/rules/Currency.code_is_not_the_unit.yaml` → `rule`

> Is this how you would state the rule “Currency.code_is_not_the_unit”? The wording was sharpened for a reader and awaits your acceptance: Every amount on a sale is in US dollars. A sale's currency is the currency the customer transacted in, not the unit of its amounts: filtering by that currency does not turn the amounts into it. Sales asked for in a named currency are converted through the exchange rate.

### `rule:Customer.age#state`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md), [store](concepts/store.md)
- source: `ontology/rules/Customer.age.yaml` → `rule`

> Is the rule “Customer.age” right? It is recorded as proposed, not ruled: An age is computed, never stored: a customer's age from the birth date and a store's age from its opening date, both measured at the sampling date rather than at today's date. Which age arithmetic is meant — completed years counting the birthday, or calendar year boundaries crossed — has not been ruled.

### `rule:Customer.age#wording`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md), [store](concepts/store.md)
- source: `ontology/rules/Customer.age.yaml` → `rule`

> Is this how you would state the rule “Customer.age”? The wording was sharpened for a reader and awaits your acceptance: An age is computed, never stored: a customer's age from the birth date and a store's age from its opening date, both measured at the sampling date rather than at today's date. Which age arithmetic is meant — completed years counting the birthday, or calendar year boundaries crossed — has not been ruled.

### `rule:Customer.as_of_now_or_sale#state`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md), [order](concepts/order.md)
- source: `ontology/rules/Customer.as_of_now_or_sale.yaml` → `rule`

> Is the rule “Customer.as_of_now_or_sale” right? It is recorded as proposed, not ruled: The customer register keeps history: a row is a version of a person, valid over a window. The customer as they are now and the customer a past sale was made to can be different rows, and reading one as the other moves old sales to new addresses. A question joining customers to sales over a period says which it means; neither reading is declared the default.

### `rule:Customer.as_of_now_or_sale#wording`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md), [order](concepts/order.md)
- source: `ontology/rules/Customer.as_of_now_or_sale.yaml` → `rule`

> Is this how you would state the rule “Customer.as_of_now_or_sale”? The wording was sharpened for a reader and awaits your acceptance: The customer register keeps history: a row is a version of a person, valid over a window. The customer as they are now and the customer a past sale was made to can be different rows, and reading one as the other moves old sales to new addresses. A question joining customers to sales over a period says which it means; neither reading is declared the default.

### `rule:Customer.register_not_buyers#state`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md)
- source: `ontology/rules/Customer.register_not_buyers.yaml` → `rule`

> Is the rule “Customer.register_not_buyers” right? It is recorded as proposed, not ruled: The customer register is wider than the buyers: a customer is a person on the register, and many registered customers have never bought anything. This is by design of the source, not a defect. "Customers" and "buyers" are two populations, and an answer counting customers says which one it counted.

### `rule:Customer.register_not_buyers#wording`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md)
- source: `ontology/rules/Customer.register_not_buyers.yaml` → `rule`

> Is this how you would state the rule “Customer.register_not_buyers”? The wording was sharpened for a reader and awaits your acceptance: The customer register is wider than the buyers: a customer is a person on the register, and many registered customers have never bought anything. This is by design of the source, not a defect. "Customers" and "buyers" are two populations, and an answer counting customers says which one it counted.

### `rule:ExchangeRate.convert_per_day#state`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/rules/ExchangeRate.convert_per_day.yaml` → `rule`

> Is the rule “ExchangeRate.convert_per_day” right? It is recorded as proposed, not ruled: An amount is converted at its own day's rate, never at a rate averaged over a period. A rate is not a quantity to add up: over time it can at most be averaged, and across currency pairs it is not combined at all.

### `rule:ExchangeRate.convert_per_day#wording`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/rules/ExchangeRate.convert_per_day.yaml` → `rule`

> Is this how you would state the rule “ExchangeRate.convert_per_day”? The wording was sharpened for a reader and awaits your acceptance: An amount is converted at its own day's rate, never at a rate averaged over a period. A rate is not a quantity to add up: over time it can at most be averaged, and across currency pairs it is not combined at all.

### `rule:ExchangeRate.to_currency.scoped_by#state`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md), [currency](concepts/currency.md)
- source: `ontology/rules/ExchangeRate.to_currency.scoped_by.yaml` → `rule`

> Is the rule “ExchangeRate.to_currency.scoped_by” right? It is recorded as proposed, not ruled: An exchange rate's target currency means something only together with its source currency: the direction is part of the rate's identity, so a rate is never picked or grouped by its target currency alone.

### `rule:ExchangeRate.to_currency.scoped_by#wording`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md), [currency](concepts/currency.md)
- source: `ontology/rules/ExchangeRate.to_currency.scoped_by.yaml` → `rule`

> Is this how you would state the rule “ExchangeRate.to_currency.scoped_by”? The wording was sharpened for a reader and awaits your acceptance: An exchange rate's target currency means something only together with its source currency: the direction is part of the rate's identity, so a rate is never picked or grouped by its target currency alone.

### `rule:Location.channel#state`

- origin: register · owner role: not declared · concept: [location](concepts/location.md)
- source: `ontology/rules/Location.channel.yaml` → `rule`

> Is the rule “Location.channel” right? It is recorded as proposed, not ruled: The online store is recorded as a location, but it is not a place. Questions about locations and places cover physical locations only, unless they name the online channel.

### `rule:Location.channel#wording`

- origin: register · owner role: not declared · concept: [location](concepts/location.md)
- source: `ontology/rules/Location.channel.yaml` → `rule`

> Is this how you would state the rule “Location.channel”? The wording was sharpened for a reader and awaits your acceptance: The online store is recorded as a location, but it is not a place. Questions about locations and places cover physical locations only, unless they name the online channel.

### `rule:Location.site#wording`

- origin: register · owner role: not declared · concept: [location](concepts/location.md)
- source: `ontology/rules/Location.site.yaml` → `rule`

> Is this how you would state the rule “Location.site”? The wording was sharpened for a reader and awaits your acceptance: Site and location name the same notion: the place a store stands on, described by its country and its state or region. A store's place has no city in this business's data — its finest geography is the state or region — and a city is only where a customer lives, so a question about the cities stores are in has no answer here and must say so rather than offer site codes.

### `rule:Order.cost_is_procurement#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.cost_is_procurement.yaml` → `rule`

> Is this how you would state the rule “Order.cost_is_procurement”? The wording was sharpened for a reader and awaits your acceptance: Cost means only what the goods cost Contoso to buy — the procurement cost. Every other money figure on a sale, gross, net, discount and margin, is revenue or income, never a cost.

### `rule:Order.date#state`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.date.yaml` → `rule`

> Is the rule “Order.date” right? It is recorded as proposed, not ruled: An order's date is the day it was placed, not the day it was delivered. A question that says when, or names a period, without saying delivery is answered on the order date; a question that says delivered or shipped is answered on the delivery date.

### `rule:Order.date#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.date.yaml` → `rule`

> Is this how you would state the rule “Order.date”? The wording was sharpened for a reader and awaits your acceptance: An order's date is the day it was placed, not the day it was delivered. A question that says when, or names a period, without saying delivery is answered on the order date; a question that says delivered or shipped is answered on the delivery date.

### `rule:Order.discount_amount.percent#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.discount_amount.percent.yaml` → `rule`

> Is this how you would state the rule “Order.discount_amount.percent”? The wording was sharpened for a reader and awaits your acceptance: A discount percentage is the money given away divided by the gross amount before discount — not by the net amount.

### `rule:Order.discount_amount.total#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.discount_amount.total.yaml` → `rule`

> Is this how you would state the rule “Order.discount_amount.total”? The wording was sharpened for a reader and awaits your acceptance: A total discount is money: the sum of what was given away below the regular price on every discounted sale in scope. It is never a sum or an average of discount rates. The rate is meant only when the question names it — discount percentage, discount rate, average discount.

### `rule:Order.how_many#state`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.how_many.yaml` → `rule`

> Is the rule “Order.how_many” right? It is recorded as proposed, not ruled: How many is three questions. Purchases are counted as orders; items sold are the quantity summed; order lines are how the data is stored and are not a business quantity. "How many did we sell" asks for items, "how many times did we sell" or "how many orders" asks for purchases.

### `rule:Order.how_many#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.how_many.yaml` → `rule`

> Is this how you would state the rule “Order.how_many”? The wording was sharpened for a reader and awaits your acceptance: How many is three questions. Purchases are counted as orders; items sold are the quantity summed; order lines are how the data is stored and are not a business quantity. "How many did we sell" asks for items, "how many times did we sell" or "how many orders" asks for purchases.

### `rule:Order.is_the_purchase#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.is_the_purchase.yaml` → `rule`

> Is this how you would state the rule “Order.is_the_purchase”? The wording was sharpened for a reader and awaits your acceptance: An order is the purchase: one customer buying at one store on one day in one currency. Its lines are not orders and not events of their own — a line borrows the when, the who and the where from its order and adds only which product and how many. Counting orders counts purchases, never lines.

### `rule:Order.margin_amount.ratio#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.margin_amount.ratio.yaml` → `rule`

> Is this how you would state the rule “Order.margin_amount.ratio”? The wording was sharpened for a reader and awaits your acceptance: A margin ratio can be stated two ways over the same profit, and the question must say which: margin percent is profit over net revenue, markup is profit over cost. A question naming neither is asked.

### `rule:Order.net_amount.price#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.net_amount.price.yaml` → `rule`

> Is this how you would state the rule “Order.net_amount.price”? The wording was sharpened for a reader and awaits your acceptance: An unqualified price means what the customer paid per article: the net amount divided by the number of units, both summed over the lines asked about — never an average of line prices.

### `rule:Order.net_amount.surfaces#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.net_amount.surfaces.yaml` → `rule`

> Is this how you would state the rule “Order.net_amount.surfaces”? The wording was sharpened for a reader and awaits your acceptance: "Revenue" or "sales" without "net" or "gross" means the net amount — what the customer was charged after discount — and the answer says so. "Gross revenue" means the amount before discount.

### `rule:Order.no_lifecycle_state#state`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.no_lifecycle_state.yaml` → `rule`

> Is the rule “Order.no_lifecycle_state” right? It is recorded as proposed, not ruled: An order has no state beyond its two dates: it was placed on one day and delivered on another. Nothing records a cancellation or a return, so a question about either has no answer in this business's data and says so; an absent state is never read as zero.

### `rule:Order.no_lifecycle_state#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.no_lifecycle_state.yaml` → `rule`

> Is this how you would state the rule “Order.no_lifecycle_state”? The wording was sharpened for a reader and awaits your acceptance: An order has no state beyond its two dates: it was placed on one day and delivered on another. Nothing records a cancellation or a return, so a question about either has no answer in this business's data and says so; an absent state is never read as zero.

### `rule:Order.order_date.anchor#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.order_date.anchor.yaml` → `rule`

> Is this how you would state the rule “Order.order_date.anchor”? The wording was sharpened for a reader and awaits your acceptance: "Now", for this data, is the date of the newest order — measured from the data, not taken from the clock. Relative periods such as "last month" are read against it, and it moves forward by itself when new orders arrive.

### `rule:Order.period#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.period.yaml` → `rule`

> Is this how you would state the rule “Order.period”? The wording was sharpened for a reader and awaits your acceptance: A question that names no period covers all time. There is no implied "this year" and no implied latest month, and the answer states the window it covered.

### `rule:Order.price_terms#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/rules/Order.price_terms.yaml` → `rule`

> Is this how you would state the rule “Order.price_terms”? The wording was sharpened for a reader and awaits your acceptance: Four facts on a sale carry every price and cost. The unit price is the regular, list price of one unit before discount; the net price is the actual selling price of one unit after discount; the unit cost is what one unit cost Contoso; the quantity is how many units. Every amount derives from them: gross is quantity times unit price, net is quantity times net price, cost is quantity times unit cost, discount is gross less net, and margin is net less cost — so margin is profit on the discounted price, not on list. "Unit price" names the regular price, not what was paid.

### `rule:Order.rate_on_order_date#state`

- origin: register · owner role: not declared · concept: [order](concepts/order.md), [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/rules/Order.rate_on_order_date.yaml` → `rule`

> Is the rule “Order.rate_on_order_date” right? It is recorded as proposed, not ruled: An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a target currency alone does not pick a rate.

### `rule:Order.rate_on_order_date#wording`

- origin: register · owner role: not declared · concept: [order](concepts/order.md), [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/rules/Order.rate_on_order_date.yaml` → `rule`

> Is this how you would state the rule “Order.rate_on_order_date”? The wording was sharpened for a reader and awaits your acceptance: An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a target currency alone does not pick a rate.

### `rule:Product.price_is_dated#wording`

- origin: register · owner role: not declared · concept: [product](concepts/product.md), [order](concepts/order.md)
- source: `ontology/rules/Product.price_is_dated.yaml` → `rule`

> Is this how you would state the rule “Product.price_is_dated”? The wording was sharpened for a reader and awaits your acceptance: A product carries no standing price and no standing cost. A price changes over time, so every price and cost is the one on the sale, dated by the sale, and a product's price is reached through its sales. A product's current price is the regular unit price on its latest sale, stated with that sale's date where it matters. A question qualifying products by price — high-value products — selects products by that price and then counts all their sales, never qualifies individual sale lines.

### `rule:ProductCategory.level#state`

- origin: register · owner role: not declared · concept: [product_category](concepts/product_category.md)
- source: `ontology/rules/ProductCategory.level.yaml` → `rule`

> Is the rule “ProductCategory.level” right? It is recorded as proposed, not ruled: A product category is the top level of the product hierarchy. A question saying category is answered on the category; one saying sub-category is answered on the sub-category.

### `rule:ProductCategory.level#wording`

- origin: register · owner role: not declared · concept: [product_category](concepts/product_category.md)
- source: `ontology/rules/ProductCategory.level.yaml` → `rule`

> Is this how you would state the rule “ProductCategory.level”? The wording was sharpened for a reader and awaits your acceptance: A product category is the top level of the product hierarchy. A question saying category is answered on the category; one saying sub-category is answered on the sub-category.

### `rule:Store.channel#wording`

- origin: register · owner role: not declared · concept: [store](concepts/store.md), [order](concepts/order.md)
- source: `ontology/rules/Store.channel.yaml` → `rule`

> Is this how you would state the rule “Store.channel”? The wording was sharpened for a reader and awaits your acceptance: A store is a shop you can walk into. The online channel is recorded as a store, but a question about stores — how many there are, which ones — covers physical shops only unless it names the online channel. That default holds only when the question is about stores: revenue and every other figure of the sale includes both channels, even when the question's route passes through stores.

### `rule:Store.premises_not_place#wording`

- origin: register · owner role: not declared · concept: [store](concepts/store.md), [location](concepts/location.md)
- source: `ontology/rules/Store.premises_not_place.yaml` → `rule`

> Is this how you would state the rule “Store.premises_not_place”? The wording was sharpened for a reader and awaits your acceptance: A store is the premises Contoso sells from: a shop standing on one place for one trading period, with its own name, floor area, opening date and closing date. It is part of a location, not the location itself — one place may hold a succession of premises over time, each of them a store. So one store is counted by its premises, and a count or sum over stores is a different question from the same figure over places; an answer that could be read at either level says which level it used.

### `rule:Store.record_questions#state`

- origin: register · owner role: not declared · concept: [store](concepts/store.md)
- source: `ontology/rules/Store.record_questions.yaml` → `rule`

> Is the rule “Store.record_questions” right? It is recorded as proposed, not ruled: A question about what the store table records — how many store versions or rows there are, or a list of every restructured store — covers every recorded row, the online channel included, with no channel or trading-state restriction. "How many stores do we have" is a different question and keeps the physical and active defaults.

### `rule:Store.record_questions#wording`

- origin: register · owner role: not declared · concept: [store](concepts/store.md)
- source: `ontology/rules/Store.record_questions.yaml` → `rule`

> Is this how you would state the rule “Store.record_questions”? The wording was sharpened for a reader and awaits your acceptance: A question about what the store table records — how many store versions or rows there are, or a list of every restructured store — covers every recorded row, the online channel included, with no channel or trading-state restriction. "How many stores do we have" is a different question and keeps the physical and active defaults.

### `rule:Store.trading#wording`

- origin: register · owner role: not declared · concept: [store](concepts/store.md)
- source: `ontology/rules/Store.trading.yaml` → `rule`

> Is this how you would state the rule “Store.trading”? The wording was sharpened for a reader and awaits your acceptance: A store is active while it has no closing date. A store with a closing date is closed, and a closed store is either shut — closed for good — or restructured — closed and replaced. A question about stores covers active stores unless it names another state.

## Findings — 0 (not questions)

None.

## Operator items — 0 (not SME questions)

None.
