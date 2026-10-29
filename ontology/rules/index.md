---
type: RuleIndex
title: Rules
---

# Rules

> PROJECTED by tools/mac_rules.py from `ontology/rules/*.yaml` — the business rules of this ontology. Search: `python3 tools/mac_rules.py search <bundle> <words>`.

38 rule(s); 17 live prose rule(s) awaiting a symbolic form.

| Rule | State | Formal | Statement |
|---|---|---|---|
| [Brand.not_manufacturer](Brand.not_manufacturer.md) | proposed | prose | A brand is the name a customer buys a product under; a manufacturer is who made it. The two sets overlap in names but are two notions, and a |
| [Color.one_spelling](Color.one_spelling.md) | ruled | prose | A colour is one member however the source spells its case: colour names are capitalised, so Blue and blue are one colour. A breakdown or cou |
| [Country.rows](Country.rows.md) | proposed | symbolic | The placeholder country code `--` is not a country. It marks rows that carry no real country, such as the online store. Questions about coun |
| [Country.where_we_have_customers](Country.where_we_have_customers.md) | ruled | prose | A question asking for the countries where we have customers asks for countries: the countries at least one customer lives in, one answer row |
| [Country.whose](Country.whose.md) | ruled | symbolic | When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to |
| [Country.whose_is_asked](Country.whose_is_asked.md) | superseded | prose | A question asking by country without saying whose country is asked back: no reading is assumed. |
| [Country.whose_is_the_store](Country.whose_is_the_store.md) | superseded | prose | A question asking by country without saying whose country is answered on the country the store stands in. |
| [Currency.code_is_not_the_unit](Currency.code_is_not_the_unit.md) | proposed | prose | Every amount on a sale is in US dollars. A sale's currency is the currency the customer transacted in, not the unit of its amounts: filterin |
| [Customer.active_on_the_reference_date](Customer.active_on_the_reference_date.md) | ruled | symbolic | A customer is active on a reference date when that date falls inside the customer's validity window — on or after the day the record became  |
| [Customer.age](Customer.age.md) | proposed | prose | An age is computed, never stored: a customer's age from the birth date and a store's age from its opening date, both measured at the samplin |
| [Customer.as_of_now_or_sale](Customer.as_of_now_or_sale.md) | proposed | prose | The customer register keeps history: a row is a version of a person, valid over a window. The customer as they are now and the customer a pa |
| [Customer.register_not_buyers](Customer.register_not_buyers.md) | proposed | prose | The customer register is wider than the buyers: a customer is a person on the register, and many registered customers have never bought anyt |
| [ExchangeRate.convert_per_day](ExchangeRate.convert_per_day.md) | proposed | canon: additivity_guard | An amount is converted at its own day's rate, never at a rate averaged over a period. A rate is not a quantity to add up: over time it can a |
| [ExchangeRate.direction_is_part_of_the_key](ExchangeRate.direction_is_part_of_the_key.md) | proposed | symbolic | An exchange rate's target currency means something only together with its source currency: the direction is part of the rate's identity, so  |
| [Location.channel](Location.channel.md) | proposed | symbolic | The online store is recorded as a location, but it is not a place. Questions about locations and places cover physical locations only, unles |
| [Location.site](Location.site.md) | ruled | prose | Site and location name the same notion: the place a store stands on, described by its country and its state or region. A store's place has n |
| [Order.cost_is_procurement](Order.cost_is_procurement.md) | ruled | prose | Cost means only what the goods cost Contoso to buy — the procurement cost. Every other money figure on a sale, gross, net, discount and marg |
| [Order.date](Order.date.md) | proposed | symbolic | An order's date is the day it was placed, not the day it was delivered. A question that says when, or names a period, without saying deliver |
| [Order.discount_percent_is_over_gross](Order.discount_percent_is_over_gross.md) | ruled | symbolic | A discount percentage is the money given away divided by the gross amount before discount — not by the net amount. |
| [Order.discount_total_is_money](Order.discount_total_is_money.md) | ruled | prose | A total discount is money: the sum of what was given away below the regular price on every discounted sale in scope. It is never a sum or an |
| [Order.how_many](Order.how_many.md) | proposed | prose | How many is three questions. Purchases are counted as orders; items sold are the quantity summed; order lines are how the data is stored and |
| [Order.is_the_purchase](Order.is_the_purchase.md) | ruled | prose | An order is the purchase: one customer buying at one store on one day in one currency. Its lines are not orders and not events of their own  |
| [Order.margin_ratio_is_named](Order.margin_ratio_is_named.md) | ruled | symbolic | A margin ratio can be stated two ways over the same profit, and the question must say which: margin percent is profit over net revenue, mark |
| [Order.no_lifecycle_state](Order.no_lifecycle_state.md) | proposed | prose | An order has no state beyond its two dates: it was placed on one day and delivered on another. Nothing records a cancellation or a return, s |
| [Order.now_is_the_newest_order](Order.now_is_the_newest_order.md) | ruled | symbolic | "Now", for this data, is the date of the newest order — measured from the data, not taken from the clock. Relative periods such as "last mon |
| [Order.period](Order.period.md) | ruled | symbolic | A question that names no period covers all time. There is no implied "this year" and no implied latest month, and the answer states the wind |
| [Order.price_is_per_article](Order.price_is_per_article.md) | ruled | symbolic | An unqualified price means what the customer paid per article: the net amount divided by the number of units, both summed over the lines ask |
| [Order.price_terms](Order.price_terms.md) | ruled | prose | Four facts on a sale carry every price and cost. The unit price is the regular, list price of one unit before discount; the net price is the |
| [Order.rate_on_order_date](Order.rate_on_order_date.md) | proposed | canon: composite_key_guard | An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a t |
| [Order.revenue_means_net](Order.revenue_means_net.md) | ruled | symbolic | "Revenue" or "sales" without "net" or "gross" means the net amount — what the customer was charged after discount — and the answer says so.  |
| [Product.price_is_dated](Product.price_is_dated.md) | ruled | prose | A product carries no standing price and no standing cost. A price changes over time, so every price and cost is the one on the sale, dated b |
| [ProductCategory.level](ProductCategory.level.md) | proposed | symbolic | A product category is the top level of the product hierarchy. A question saying category is answered on the category; one saying sub-categor |
| [Store.channel](Store.channel.md) | ruled | symbolic | A store is a shop you can walk into. The online channel is recorded as a store, but a question about stores — how many there are, which ones |
| [Store.counted_by_site](Store.counted_by_site.md) | superseded | prose | One store is its site, not its row: a shop rebuilt or re-let at the same place is one store with several trading periods, so stores are coun |
| [Store.premises_not_place](Store.premises_not_place.md) | ruled | prose | A store is the premises Contoso sells from: a shop standing on one place for one trading period, with its own name, floor area, opening date |
| [Store.record_questions](Store.record_questions.md) | proposed | prose | A question about what the store table records — how many store versions or rows there are, or a list of every restructured store — covers ev |
| [Store.revenue_is_shop_only](Store.revenue_is_shop_only.md) | superseded | prose | If revenue is asked without naming a channel, only shop revenue is assumed. |
| [Store.trading](Store.trading.md) | ruled | symbolic | A store is active while it has no closing date. A store with a closing date is closed, and a closed store is either shut — closed for good — |

## Keyword index

- **active** — [Customer.active_on_the_reference_date](Customer.active_on_the_reference_date.md), [Store.trading](Store.trading.md)
- **additivity** — [ExchangeRate.convert_per_day](ExchangeRate.convert_per_day.md)
- **age** — [Customer.age](Customer.age.md)
- **all stores** — [Store.record_questions](Store.record_questions.md)
- **all time** — [Order.period](Order.period.md)
- **amounts** — [Currency.code_is_not_the_unit](Currency.code_is_not_the_unit.md)
- **anchor** — [Order.now_is_the_newest_order](Order.now_is_the_newest_order.md)
- **as of** — [Customer.active_on_the_reference_date](Customer.active_on_the_reference_date.md), [Customer.as_of_now_or_sale](Customer.as_of_now_or_sale.md)
- **ask** — [Country.whose_is_asked](Country.whose_is_asked.md)
- **attribution** — [Country.whose](Country.whose.md)
- **average age** — [Customer.age](Customer.age.md)
- **average price** — [Order.price_is_per_article](Order.price_is_per_article.md)
- **average rate** — [ExchangeRate.convert_per_day](ExchangeRate.convert_per_day.md)
- **birth date** — [Customer.age](Customer.age.md)
- **blue** — [Color.one_spelling](Color.one_spelling.md)
- **both channels** — [Store.channel](Store.channel.md)
- **brand** — [Brand.not_manufacturer](Brand.not_manufacturer.md)
- **buyer** — [Customer.register_not_buyers](Customer.register_not_buyers.md)
- **by country** — [Country.whose](Country.whose.md)
- **cancellation** — [Order.no_lifecycle_state](Order.no_lifecycle_state.md)
- **cancelled** — [Order.no_lifecycle_state](Order.no_lifecycle_state.md)
- **case** — [Color.one_spelling](Color.one_spelling.md)
- **catalogue price** — [Product.price_is_dated](Product.price_is_dated.md)
- **category** — [ProductCategory.level](ProductCategory.level.md)
- **channel** — [Location.channel](Location.channel.md), [Store.channel](Store.channel.md), [Store.revenue_is_shop_only](Store.revenue_is_shop_only.md)
- **city** — [Location.site](Location.site.md)
- **close date** — [Store.trading](Store.trading.md)
- **closed** — [Store.trading](Store.trading.md)
- **cogs** — [Order.cost_is_procurement](Order.cost_is_procurement.md)
- **color** — [Color.one_spelling](Color.one_spelling.md)
- **colour** — [Color.one_spelling](Color.one_spelling.md)
- **conversion** — [ExchangeRate.convert_per_day](ExchangeRate.convert_per_day.md), [Order.rate_on_order_date](Order.rate_on_order_date.md)
- **convert** — [Currency.code_is_not_the_unit](Currency.code_is_not_the_unit.md)
- **cost** — [Order.cost_is_procurement](Order.cost_is_procurement.md), [Product.price_is_dated](Product.price_is_dated.md)
- **cost of goods** — [Order.cost_is_procurement](Order.cost_is_procurement.md)
- **count customers** — [Customer.register_not_buyers](Customer.register_not_buyers.md)
- **count stores** — [Store.counted_by_site](Store.counted_by_site.md), [Store.premises_not_place](Store.premises_not_place.md)
- **countries** — [Country.rows](Country.rows.md), [Country.where_we_have_customers](Country.where_we_have_customers.md)
- **country** — [Country.rows](Country.rows.md), [Country.whose](Country.whose.md), [Country.whose_is_asked](Country.whose_is_asked.md), [Country.whose_is_the_store](Country.whose_is_the_store.md)
- **currency** — [Currency.code_is_not_the_unit](Currency.code_is_not_the_unit.md), [ExchangeRate.direction_is_part_of_the_key](ExchangeRate.direction_is_part_of_the_key.md), [Order.rate_on_order_date](Order.rate_on_order_date.md)
- **current price** — [Product.price_is_dated](Product.price_is_dated.md)
- **customer** — [Customer.active_on_the_reference_date](Customer.active_on_the_reference_date.md), [Customer.as_of_now_or_sale](Customer.as_of_now_or_sale.md), [Customer.register_not_buyers](Customer.register_not_buyers.md)
- **customer age** — [Customer.age](Customer.age.md)
- **customer country** — [Country.where_we_have_customers](Country.where_we_have_customers.md), [Country.whose](Country.whose.md)
- **daily rate** — [ExchangeRate.convert_per_day](ExchangeRate.convert_per_day.md)
- **default** — [Country.whose_is_the_store](Country.whose_is_the_store.md)
- **delivered** — [Order.date](Order.date.md)
- **delivery date** — [Order.date](Order.date.md)
- **direction** — [ExchangeRate.direction_is_part_of_the_key](ExchangeRate.direction_is_part_of_the_key.md)
- **discount** — [Order.discount_percent_is_over_gross](Order.discount_percent_is_over_gross.md), [Order.discount_total_is_money](Order.discount_total_is_money.md), [Order.price_terms](Order.price_terms.md)
- **discount amount** — [Order.discount_total_is_money](Order.discount_total_is_money.md)
- **discount percentage** — [Order.discount_percent_is_over_gross](Order.discount_percent_is_over_gross.md)
- **discount rate** — [Order.discount_percent_is_over_gross](Order.discount_percent_is_over_gross.md), [Order.discount_total_is_money](Order.discount_total_is_money.md)
- **dollars** — [Currency.code_is_not_the_unit](Currency.code_is_not_the_unit.md)
- **euros** — [Currency.code_is_not_the_unit](Currency.code_is_not_the_unit.md)
- **event** — [Order.is_the_purchase](Order.is_the_purchase.md)
- **exchange rate** — [ExchangeRate.convert_per_day](ExchangeRate.convert_per_day.md), [ExchangeRate.direction_is_part_of_the_key](ExchangeRate.direction_is_part_of_the_key.md), [Order.rate_on_order_date](Order.rate_on_order_date.md)
- **existence** — [Country.where_we_have_customers](Country.where_we_have_customers.md)
- **fold** — [Color.one_spelling](Color.one_spelling.md)
- **from currency** — [ExchangeRate.direction_is_part_of_the_key](ExchangeRate.direction_is_part_of_the_key.md)
- **fx** — [ExchangeRate.convert_per_day](ExchangeRate.convert_per_day.md), [ExchangeRate.direction_is_part_of_the_key](ExchangeRate.direction_is_part_of_the_key.md), [Order.rate_on_order_date](Order.rate_on_order_date.md)
- **geography** — [Location.site](Location.site.md)
- **gross** — [Order.discount_percent_is_over_gross](Order.discount_percent_is_over_gross.md), [Order.price_terms](Order.price_terms.md), [Order.revenue_means_net](Order.revenue_means_net.md)
- **gross revenue** — [Order.revenue_means_net](Order.revenue_means_net.md)
- **hierarchy** — [ProductCategory.level](ProductCategory.level.md)
- **high-value products** — [Product.price_is_dated](Product.price_is_dated.md)
- **history** — [Customer.as_of_now_or_sale](Customer.as_of_now_or_sale.md)
- **how many** — [Order.how_many](Order.how_many.md)
- **how many customers** — [Customer.active_on_the_reference_date](Customer.active_on_the_reference_date.md)
- **how many orders** — [Order.is_the_purchase](Order.is_the_purchase.md)
- **income** — [Order.cost_is_procurement](Order.cost_is_procurement.md)
- **internet** — [Store.channel](Store.channel.md)
- **items** — [Order.how_many](Order.how_many.md)
- **label** — [Brand.not_manufacturer](Brand.not_manufacturer.md)
- **last month** — [Order.now_is_the_newest_order](Order.now_is_the_newest_order.md)
- **latest** — [Order.now_is_the_newest_order](Order.now_is_the_newest_order.md)
- **level** — [ProductCategory.level](ProductCategory.level.md)
- **lifecycle** — [Order.no_lifecycle_state](Order.no_lifecycle_state.md)
- **lines** — [Order.how_many](Order.how_many.md)
- **list countries** — [Country.where_we_have_customers](Country.where_we_have_customers.md)
- **list price** — [Order.price_terms](Order.price_terms.md), [Product.price_is_dated](Product.price_is_dated.md)
- **location** — [Location.channel](Location.channel.md), [Location.site](Location.site.md), [Store.premises_not_place](Store.premises_not_place.md)
- **made by** — [Brand.not_manufacturer](Brand.not_manufacturer.md)
- **maker** — [Brand.not_manufacturer](Brand.not_manufacturer.md)
- **manufacturer** — [Brand.not_manufacturer](Brand.not_manufacturer.md)
- **margin** — [Order.margin_ratio_is_named](Order.margin_ratio_is_named.md), [Order.price_terms](Order.price_terms.md)
- **margin on cost** — [Order.margin_ratio_is_named](Order.margin_ratio_is_named.md)
- **margin percent** — [Order.margin_ratio_is_named](Order.margin_ratio_is_named.md)
- **market** — [Country.whose](Country.whose.md)
- **markup** — [Order.margin_ratio_is_named](Order.margin_ratio_is_named.md)
- **money off** — [Order.discount_total_is_money](Order.discount_total_is_money.md)
- **moved** — [Customer.as_of_now_or_sale](Customer.as_of_now_or_sale.md)
- **net** — [Order.price_terms](Order.price_terms.md), [Order.revenue_means_net](Order.revenue_means_net.md)
- **net margin** — [Order.margin_ratio_is_named](Order.margin_ratio_is_named.md)
- **net price** — [Order.price_is_per_article](Order.price_is_per_article.md), [Order.price_terms](Order.price_terms.md)
- **net revenue** — [Order.revenue_means_net](Order.revenue_means_net.md)
- **never bought** — [Customer.register_not_buyers](Customer.register_not_buyers.md)
- **newest order** — [Order.now_is_the_newest_order](Order.now_is_the_newest_order.md)
- **no country** — [Country.rows](Country.rows.md)
- **no default** — [Country.whose_is_asked](Country.whose_is_asked.md)
- **no period** — [Order.period](Order.period.md)
- **now** — [Order.now_is_the_newest_order](Order.now_is_the_newest_order.md)
- **online** — [Country.rows](Country.rows.md), [Location.channel](Location.channel.md), [Store.channel](Store.channel.md), [Store.revenue_is_shop_only](Store.revenue_is_shop_only.md)
- **open** — [Store.trading](Store.trading.md)
- **opening date** — [Customer.age](Customer.age.md)
- **order** — [Order.is_the_purchase](Order.is_the_purchase.md)
- **order date** — [Order.date](Order.date.md), [Order.rate_on_order_date](Order.rate_on_order_date.md)
- **order line** — [Order.is_the_purchase](Order.is_the_purchase.md)
- **order status** — [Order.no_lifecycle_state](Order.no_lifecycle_state.md)
- **orders** — [Order.how_many](Order.how_many.md)
- **per article** — [Order.price_is_per_article](Order.price_is_per_article.md)
- **per unit** — [Order.price_is_per_article](Order.price_is_per_article.md)
- **percent** — [Order.discount_percent_is_over_gross](Order.discount_percent_is_over_gross.md)
- **period** — [Order.date](Order.date.md), [Order.period](Order.period.md)
- **physical** — [Location.channel](Location.channel.md), [Store.channel](Store.channel.md)
- **place** — [Location.channel](Location.channel.md), [Location.site](Location.site.md), [Store.premises_not_place](Store.premises_not_place.md)
- **placed** — [Order.date](Order.date.md)
- **placeholder** — [Country.rows](Country.rows.md)
- **population** — [Customer.register_not_buyers](Customer.register_not_buyers.md)
- **premises** — [Store.premises_not_place](Store.premises_not_place.md)
- **price** — [Order.price_is_per_article](Order.price_is_per_article.md)
- **procurement cost** — [Order.cost_is_procurement](Order.cost_is_procurement.md)
- **product category** — [ProductCategory.level](ProductCategory.level.md)
- **product price** — [Product.price_is_dated](Product.price_is_dated.md)
- **profit** — [Order.margin_ratio_is_named](Order.margin_ratio_is_named.md)
- **purchase** — [Order.is_the_purchase](Order.is_the_purchase.md)
- **quantity** — [Order.how_many](Order.how_many.md)
- **rebate** — [Order.discount_total_is_money](Order.discount_total_is_money.md)
- **records** — [Store.record_questions](Store.record_questions.md)
- **reference date** — [Customer.active_on_the_reference_date](Customer.active_on_the_reference_date.md)
- **region** — [Location.site](Location.site.md)
- **register** — [Customer.register_not_buyers](Customer.register_not_buyers.md)
- **registered** — [Customer.active_on_the_reference_date](Customer.active_on_the_reference_date.md)
- **relative period** — [Order.now_is_the_newest_order](Order.now_is_the_newest_order.md)
- **restructured** — [Store.counted_by_site](Store.counted_by_site.md), [Store.trading](Store.trading.md)
- **return** — [Order.no_lifecycle_state](Order.no_lifecycle_state.md)
- **returned** — [Order.no_lifecycle_state](Order.no_lifecycle_state.md)
- **revenue** — [Order.revenue_means_net](Order.revenue_means_net.md), [Store.channel](Store.channel.md), [Store.revenue_is_shop_only](Store.revenue_is_shop_only.md)
- **rows** — [Store.record_questions](Store.record_questions.md)
- **sale** — [Order.is_the_purchase](Order.is_the_purchase.md)
- **sales** — [Order.revenue_means_net](Order.revenue_means_net.md)
- **sampling date** — [Order.now_is_the_newest_order](Order.now_is_the_newest_order.md)
- **selling price** — [Order.price_terms](Order.price_terms.md)
- **sentinel** — [Country.rows](Country.rows.md)
- **shipped** — [Order.date](Order.date.md)
- **shop** — [Store.channel](Store.channel.md), [Store.premises_not_place](Store.premises_not_place.md), [Store.revenue_is_shop_only](Store.revenue_is_shop_only.md)
- **shut** — [Store.trading](Store.trading.md)
- **site** — [Location.channel](Location.channel.md), [Location.site](Location.site.md), [Store.counted_by_site](Store.counted_by_site.md), [Store.premises_not_place](Store.premises_not_place.md)
- **spelling** — [Color.one_spelling](Color.one_spelling.md)
- **state** — [Location.site](Location.site.md)
- **stichtag** — [Customer.active_on_the_reference_date](Customer.active_on_the_reference_date.md)
- **store** — [Store.channel](Store.channel.md), [Store.counted_by_site](Store.counted_by_site.md), [Store.premises_not_place](Store.premises_not_place.md), [Store.record_questions](Store.record_questions.md), [Store.trading](Store.trading.md)
- **store age** — [Customer.age](Customer.age.md)
- **store code** — [Store.counted_by_site](Store.counted_by_site.md)
- **store country** — [Country.whose](Country.whose.md), [Country.whose_is_the_store](Country.whose_is_the_store.md)
- **store history** — [Store.record_questions](Store.record_questions.md)
- **sub-category** — [ProductCategory.level](ProductCategory.level.md)
- **tenancy** — [Store.premises_not_place](Store.premises_not_place.md)
- **territory** — [Country.whose](Country.whose.md)
- **this year** — [Order.period](Order.period.md)
- **time window** — [Order.period](Order.period.md)
- **to currency** — [ExchangeRate.direction_is_part_of_the_key](ExchangeRate.direction_is_part_of_the_key.md)
- **today** — [Order.now_is_the_newest_order](Order.now_is_the_newest_order.md)
- **total discount** — [Order.discount_total_is_money](Order.discount_total_is_money.md)
- **trading** — [Store.trading](Store.trading.md)
- **transaction currency** — [Currency.code_is_not_the_unit](Currency.code_is_not_the_unit.md)
- **turnover** — [Order.revenue_means_net](Order.revenue_means_net.md)
- **unit cost** — [Order.price_terms](Order.price_terms.md)
- **unit price** — [Order.price_is_per_article](Order.price_is_per_article.md), [Order.price_terms](Order.price_terms.md)
- **units sold** — [Order.how_many](Order.how_many.md)
- **unknown country** — [Country.rows](Country.rows.md)
- **unscoped** — [Order.period](Order.period.md)
- **usd** — [Currency.code_is_not_the_unit](Currency.code_is_not_the_unit.md)
- **valid** — [Customer.active_on_the_reference_date](Customer.active_on_the_reference_date.md)
- **valid from** — [Customer.as_of_now_or_sale](Customer.as_of_now_or_sale.md)
- **valid to** — [Customer.as_of_now_or_sale](Customer.as_of_now_or_sale.md)
- **version** — [Customer.as_of_now_or_sale](Customer.as_of_now_or_sale.md)
- **versions** — [Store.record_questions](Store.record_questions.md)
- **volume** — [Order.how_many](Order.how_many.md)
- **web** — [Store.channel](Store.channel.md)
- **what it cost us** — [Order.cost_is_procurement](Order.cost_is_procurement.md)
- **when** — [Order.date](Order.date.md)
- **where we have customers** — [Country.where_we_have_customers](Country.where_we_have_customers.md)
- **who makes** — [Brand.not_manufacturer](Brand.not_manufacturer.md)
- **whose country** — [Country.whose](Country.whose.md), [Country.whose_is_asked](Country.whose_is_asked.md)
