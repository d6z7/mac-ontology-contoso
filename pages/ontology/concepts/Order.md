---
type: Concept
title: Order
description: One customer's purchase on one date, counted by distinct `order_key` over the line relation.
tags:
- Contoso 5
- concept
resource: table://v_contoso5_sales_line
rule_pages:
- ../rules/Country.whose.md
- ../rules/Currency.code_is_not_the_unit.md
- ../rules/Currency.whose.md
- ../rules/Customer.as_of_now_or_sale.md
- ../rules/Customer.per_customer.md
- ../rules/Order.channel.md
- ../rules/Order.cost_is_procurement.md
- ../rules/Order.date.md
- ../rules/Order.default_measure.md
- ../rules/Order.discount_percent_is_over_gross.md
- ../rules/Order.discount_total_is_money.md
- ../rules/Order.how_many.md
- ../rules/Order.is_the_purchase.md
- ../rules/Order.margin_ratio_is_named.md
- ../rules/Order.no_lifecycle_state.md
- ../rules/Order.now_is_the_newest_order.md
- ../rules/Order.period.md
- ../rules/Order.price_is_per_article.md
- ../rules/Order.price_terms.md
- ../rules/Order.rate_on_order_date.md
- ../rules/Order.revenue_means_net.md
- ../rules/Product.price_is_dated.md
- ../rules/Store.channel.md
---

One customer's purchase on one date, counted by distinct `order_key` over the line relation. It is also THE FACT NODE of the sales line, one row per order line - every money and quantity measure (net, gross, cost, discount, margin, units, and the per-unit prices) is a column it serves, and every edge from the sale to a dimension starts here. The account is pages/knowledge/order.md.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`v_contoso5_sales_line`](../../data/datasets/v_contoso5_sales_line.md)
- **Counts** — `order_key`
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*23 rule(s) are about this concept, 23 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Country.whose](../rules/Country.whose.md) — **ruled** · names it · choice over `territory`, `store`, `customer`, `location` — default `territory` — When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.
- [Currency.code_is_not_the_unit](../rules/Currency.code_is_not_the_unit.md) — **proposed** · names it · prose — not enforced (owner operator) — Every amount on a sale is in US dollars. A sale's currency is the currency the customer transacted in, not the unit of its amounts: filtering by that currency does not turn the amounts into it. Sales asked for in a named currency are converted through the exchange rate.
- [Currency.whose](../rules/Currency.whose.md) — **proposed** · names it · choice over `paid_in`, `rate_source`, `rate_target` — default `paid_in` — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- [Customer.as_of_now_or_sale](../rules/Customer.as_of_now_or_sale.md) — **proposed** · names it · prose — not enforced (owner operator) — The customer register keeps history: a row is a version of a person, valid over a window. The customer as they are now and the customer a past sale was made to can be different rows, and reading one as the other moves old sales to new addresses. A question joining customers to sales over a period says which it means; neither reading is declared the default.
- [Customer.per_customer](../rules/Customer.per_customer.md) — **proposed** · names it · choice over `buyers`, `active`, `registered` — default `buyers` — A figure "per customer" divides by a count of customers, and which customers it counts is a choice. By default it counts the buyers: the distinct customers on the sales lines the figure is summed over, so revenue per customer by country divides each country's revenue by the customers who bought in that country. The other options count the customers active on the reference date, or every customer on the register. The answer says which customers it divided by.
- [Order.channel](../rules/Order.channel.md) — **proposed** · parent · choice over `both`, `shops`, `online` — default `both` — A sale is made in one of two channels: a shop you can walk into or the web shop. A figure of the sale that names no channel covers both channels, even when the question reaches the sale through stores; a question that names the shops or the web shop gets that channel. The answer says which channels it covered.
- [Order.cost_is_procurement](../rules/Order.cost_is_procurement.md) — **ruled** · parent · prose — not enforced (owner operator) — Cost means only what the goods cost Contoso to buy — the procurement cost. Every other money figure on a sale, gross, net, discount and margin, is revenue or income, never a cost.
- [Order.date](../rules/Order.date.md) — **proposed** · parent · choice over `ordered`, `delivered` — default `ordered` — An order's date is the day it was placed, not the day it was delivered. A question that says when, or names a period, without saying delivery is answered on the order date; a question that says delivered or shipped is answered on the delivery date.
- [Order.default_measure](../rules/Order.default_measure.md) — **proposed** · parent · choice over `quantity`, `net_amount`, `gross_amount`, `cost_amount`, `discount_amount`, `margin_amount`, `unit_price`, `net_price`, `unit_cost` — default `net_amount` — A question about Order that names no figure reads `net_amount`; the other figures are read when named.
- [Order.discount_percent_is_over_gross](../rules/Order.discount_percent_is_over_gross.md) — **proposed** · parent · choice over `percent` — default `percent` — A discount percentage is the money given away divided by the gross amount before discount — not by the net amount.
- [Order.discount_total_is_money](../rules/Order.discount_total_is_money.md) — **ruled** · parent · prose — not enforced (owner operator) — A total discount is money: the sum of what was given away below the regular price on every discounted sale in scope. It is never a sum or an average of discount rates. The rate is meant only when the question names it — discount percentage, discount rate, average discount.
- [Order.how_many](../rules/Order.how_many.md) — **proposed** · parent · prose — not enforced (owner operator) — How many is three questions. Purchases are counted as orders; items sold are the quantity summed; order lines are how the data is stored and are not a business quantity. "How many did we sell" asks for items, "how many times did we sell" or "how many orders" asks for purchases.
- [Order.is_the_purchase](../rules/Order.is_the_purchase.md) — **proposed** · parent · prose — not enforced (owner operator) — An order is the purchase: one customer buying at one store on one day in one currency. Its lines are not orders and not events of their own — a line borrows the when, the who and the where from its order and adds only which product and how many. Counting orders counts purchases, never lines.
- [Order.margin_ratio_is_named](../rules/Order.margin_ratio_is_named.md) — **proposed** · parent · choice over `margin_percent`, `markup_percent` — default `ask` — A margin ratio can be stated two ways over the same profit, and the question must say which: margin percent is profit over net revenue, markup is profit over cost. A question naming neither is asked.
- [Order.no_lifecycle_state](../rules/Order.no_lifecycle_state.md) — **proposed** · parent · prose — not enforced (owner operator) — An order has no state beyond its two dates: it was placed on one day and delivered on another. Nothing records a cancellation or a return, so a question about either has no answer in this business's data and says so; an absent state is never read as zero.
- [Order.now_is_the_newest_order](../rules/Order.now_is_the_newest_order.md) — **ruled** · parent · implemented by `dataset:v_contoso5_sales_line.order_date` = `date` — "Now", for this data, is the date of the newest order — measured from the data, not taken from the clock. Relative periods such as "last month" are read against it, and it moves forward by itself when new orders arrive.
- [Order.period](../rules/Order.period.md) — **proposed** · parent · choice over `all_time` — default `all_time` — A question that names no period covers all time. There is no implied "this year" and no implied latest month, and the answer states the window it covered.
- [Order.price_is_per_article](../rules/Order.price_is_per_article.md) — **proposed** · parent · choice over `price_per_article` — default `price_per_article` — An unqualified price means what the customer paid per article: the net amount divided by the number of units, both summed over the lines asked about — never an average of line prices.
- [Order.price_terms](../rules/Order.price_terms.md) — **ruled** · parent · prose — not enforced (owner operator) — Four facts on a sale carry every price and cost. The unit price is the regular, list price of one unit before discount; the net price is the actual selling price of one unit after discount; the unit cost is what one unit cost Contoso; the quantity is how many units. Every amount derives from them: gross is quantity times unit price, net is quantity times net price, cost is quantity times unit cost, discount is gross less net, and margin is net less cost — so margin is profit on the discounted price, not on list. "Unit price" names the regular price, not what was paid.
- [Order.rate_on_order_date](../rules/Order.rate_on_order_date.md) — **proposed** · parent · implemented by `law.L0` = `dataset:v_contoso5_fx_rate`, `dataset:v_contoso5_fx_rate.to_currency` = `dimension`, `dataset:v_contoso5_fx_rate.date_day` = `date`, `dataset:v_contoso5_fx_rate.from_currency` = `dimension` — An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a target currency alone does not pick a rate.
- [Order.revenue_means_net](../rules/Order.revenue_means_net.md) — **ruled** · parent · implemented by `dataset:v_contoso5_sales_line.net_amount` = `measure` — "Revenue" or "sales" without "net" or "gross" means the net amount — what the customer was charged after discount — and the answer says so. "Gross revenue" means the amount before discount.
- [Product.price_is_dated](../rules/Product.price_is_dated.md) — **proposed** · names it · prose — not enforced (owner operator) — A product carries no standing price and no standing cost. A price changes over time, so every price and cost is the one on the sale, dated by the sale, and a product's price is reached through its sales. A product's current price is the regular unit price on its latest sale, stated with that sale's date where it matters. A question qualifying products by price — high-value products — selects products by that price and then counts all their sales, never qualifies individual sale lines.
- [Store.channel](../rules/Store.channel.md) — **ruled** · names it · choice over `physical`, `online` — default `physical` — A store is a shop you can walk into. The online channel is recorded as a store, but a question about stores — how many there are, which ones — covers physical shops only unless it names the online channel. That default holds only when the question is about stores: revenue and every other figure of the sale includes both channels, even when the question's route passes through stores.

**Words**

*191 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| cogs | `dataset:v_contoso5_sales_line.cost_amount` | binds | — | — | — |
| cost | `dataset:v_contoso5_sales_line.cost_amount` | binds | — | — | — |
| cost of goods | `dataset:v_contoso5_sales_line.cost_amount` | binds | — | — | — |
| cost of sales | `dataset:v_contoso5_sales_line.cost_amount` | binds | — | — | — |
| procurement cost | `dataset:v_contoso5_sales_line.cost_amount` | binds | — | — | — |
| purchase cost | `dataset:v_contoso5_sales_line.cost_amount` | binds | — | — | — |
| what it cost us | `dataset:v_contoso5_sales_line.cost_amount` | binds | — | — | — |
| currency | `dataset:v_contoso5_sales_line.currency_code` | binds | — | — | — |
| currency of the sale | `dataset:v_contoso5_sales_line.currency_code` | binds | — | — | — |
| transaction currency | `dataset:v_contoso5_sales_line.currency_code` | binds | — | — | — |
| buyer | `dataset:v_contoso5_sales_line.customer_key` | binds | — | — | — |
| customer | `dataset:v_contoso5_sales_line.customer_key` | binds | — | — | — |
| who bought | `dataset:v_contoso5_sales_line.customer_key` | binds | — | — | — |
| delivery | `dataset:v_contoso5_sales_line.delivery_date` | binds | — | — | — |
| discount | `dataset:v_contoso5_sales_line.discount_amount` | binds | — | — | — |
| money off | `dataset:v_contoso5_sales_line.discount_amount` | binds | — | — | — |
| rebate | `dataset:v_contoso5_sales_line.discount_amount` | binds | — | — | — |
| reduction | `dataset:v_contoso5_sales_line.discount_amount` | binds | — | — | — |
| before discount | `dataset:v_contoso5_sales_line.gross_amount` | binds | — | — | — |
| gross | `dataset:v_contoso5_sales_line.gross_amount` | binds | — | — | — |
| gross revenue | `dataset:v_contoso5_sales_line.gross_amount` | binds | — | — | — |
| gross sales | `dataset:v_contoso5_sales_line.gross_amount` | binds | — | — | — |
| list value | `dataset:v_contoso5_sales_line.gross_amount` | binds | — | — | — |
| line | `dataset:v_contoso5_sales_line.line_number` | binds | — | — | — |
| line item | `dataset:v_contoso5_sales_line.line_number` | binds | — | — | — |
| order line | `dataset:v_contoso5_sales_line.line_number` | binds | — | — | — |
| contribution | `dataset:v_contoso5_sales_line.margin_amount` | binds | — | — | — |
| gross margin | `dataset:v_contoso5_sales_line.margin_amount` | binds | — | — | — |
| margin | `dataset:v_contoso5_sales_line.margin_amount` | binds | — | — | — |
| profit | `dataset:v_contoso5_sales_line.margin_amount` | binds | — | — | — |
| income | `dataset:v_contoso5_sales_line.net_amount` | binds | — | — | — |
| net | `dataset:v_contoso5_sales_line.net_amount` | binds | — | — | — |
| net revenue | `dataset:v_contoso5_sales_line.net_amount` | binds | — | — | — |
| net sales | `dataset:v_contoso5_sales_line.net_amount` | binds | — | — | — |
| revenue | `dataset:v_contoso5_sales_line.net_amount` | binds | — | — | — |
| sales | `dataset:v_contoso5_sales_line.net_amount` | binds | — | — | — |
| takings | `dataset:v_contoso5_sales_line.net_amount` | binds | — | — | — |
| turnover | `dataset:v_contoso5_sales_line.net_amount` | binds | — | — | — |
| what we charged | `dataset:v_contoso5_sales_line.net_amount` | binds | — | — | — |
| actual price | `dataset:v_contoso5_sales_line.net_price` | binds | — | — | — |
| net price | `dataset:v_contoso5_sales_line.net_price` | binds | — | — | — |
| price paid | `dataset:v_contoso5_sales_line.net_price` | binds | — | — | — |
| selling price | `dataset:v_contoso5_sales_line.net_price` | binds | — | — | — |
| date | `dataset:v_contoso5_sales_line.order_date` | binds | — | — | — |
| when | `dataset:v_contoso5_sales_line.order_date` | binds | — | — | — |
| order | `dataset:v_contoso5_sales_line.order_key` | binds | — | — | — |
| order number | `dataset:v_contoso5_sales_line.order_key` | binds | — | — | — |
| orders | `dataset:v_contoso5_sales_line.order_key` | binds | — | — | — |
| article | `dataset:v_contoso5_sales_line.product_key` | binds | — | — | — |
| item | `dataset:v_contoso5_sales_line.product_key` | binds | — | — | — |
| what was sold | `dataset:v_contoso5_sales_line.product_key` | binds | — | — | — |
| how many | `dataset:v_contoso5_sales_line.quantity` | binds | — | — | — |
| pieces | `dataset:v_contoso5_sales_line.quantity` | binds | — | — | — |
| units | `dataset:v_contoso5_sales_line.quantity` | binds | — | — | — |
| units sold | `dataset:v_contoso5_sales_line.quantity` | binds | — | — | — |
| volume | `dataset:v_contoso5_sales_line.quantity` | binds | — | — | — |
| outlet | `dataset:v_contoso5_sales_line.store_key` | binds | — | — | — |
| where it was sold | `dataset:v_contoso5_sales_line.store_key` | binds | — | — | — |
| catalogue cost | `dataset:v_contoso5_sales_line.unit_cost` | binds | — | — | — |
| cost per article | `dataset:v_contoso5_sales_line.unit_cost` | binds | — | — | — |
| cost per unit | `dataset:v_contoso5_sales_line.unit_cost` | binds | — | — | — |
| list cost | `dataset:v_contoso5_sales_line.unit_cost` | binds | — | — | — |
| procurement cost per unit | `dataset:v_contoso5_sales_line.unit_cost` | binds | — | — | — |
| standard cost | `dataset:v_contoso5_sales_line.unit_cost` | binds | — | — | — |
| unit cost | `dataset:v_contoso5_sales_line.unit_cost` | binds | — | — | — |
| catalogue price | `dataset:v_contoso5_sales_line.unit_price` | binds | — | — | — |
| full price | `dataset:v_contoso5_sales_line.unit_price` | binds | — | — | — |
| list price | `dataset:v_contoso5_sales_line.unit_price` | binds | — | — | — |
| price before discount | `dataset:v_contoso5_sales_line.unit_price` | binds | — | — | — |
| regular price | `dataset:v_contoso5_sales_line.unit_price` | binds | — | — | — |
| rrp | `dataset:v_contoso5_sales_line.unit_price` | binds | — | — | — |
| sticker price | `dataset:v_contoso5_sales_line.unit_price` | binds | — | — | — |
| undiscounted price | `dataset:v_contoso5_sales_line.unit_price` | binds | — | — | — |
| unit price | `dataset:v_contoso5_sales_line.unit_price` | binds | — | — | — |
| cogs | `rule:Order.cost_is_procurement` | finds | — | — | — |
| cost | `rule:Order.cost_is_procurement` | finds | — | — | — |
| cost of goods | `rule:Order.cost_is_procurement` | finds | — | — | — |
| income | `rule:Order.cost_is_procurement` | finds | — | — | — |
| procurement cost | `rule:Order.cost_is_procurement` | finds | — | — | — |
| what it cost us | `rule:Order.cost_is_procurement` | finds | — | — | — |
| delivered | `rule:Order.date` | finds | — | — | — |
| delivery date | `rule:Order.date` | finds | — | — | — |
| order date | `rule:Order.date` | finds | — | — | — |
| period | `rule:Order.date` | finds | — | — | — |
| placed | `rule:Order.date` | finds | — | — | — |
| shipped | `rule:Order.date` | finds | — | — | — |
| when | `rule:Order.date` | finds | — | — | — |
| delivered | `rule:Order.date.delivered` | binds | — | — | — |
| delivery date | `rule:Order.date.delivered` | binds | — | — | — |
| shipped | `rule:Order.date.delivered` | binds | — | — | — |
| when it arrived | `rule:Order.date.delivered` | binds | — | — | — |
| order date | `rule:Order.date.ordered` | binds | — | — | — |
| ordered | `rule:Order.date.ordered` | binds | — | — | — |
| placed | `rule:Order.date.ordered` | binds | — | — | — |
| when it was ordered | `rule:Order.date.ordered` | binds | — | — | — |
| discount | `rule:Order.discount_percent_is_over_gross` | finds | — | — | — |
| discount percentage | `rule:Order.discount_percent_is_over_gross` | finds | — | — | — |
| discount rate | `rule:Order.discount_percent_is_over_gross` | finds | — | — | — |
| gross | `rule:Order.discount_percent_is_over_gross` | finds | — | — | — |
| percent | `rule:Order.discount_percent_is_over_gross` | finds | — | — | — |
| discount % | `rule:Order.discount_percent_is_over_gross.percent` | binds | — | — | — |
| discount as a percentage | `rule:Order.discount_percent_is_over_gross.percent` | binds | — | — | — |
| discount percentage | `rule:Order.discount_percent_is_over_gross.percent` | binds | — | — | — |
| discount rate | `rule:Order.discount_percent_is_over_gross.percent` | binds | — | — | — |
| discount | `rule:Order.discount_total_is_money` | finds | — | — | — |
| discount amount | `rule:Order.discount_total_is_money` | finds | — | — | — |
| discount rate | `rule:Order.discount_total_is_money` | finds | — | — | — |
| money off | `rule:Order.discount_total_is_money` | finds | — | — | — |
| rebate | `rule:Order.discount_total_is_money` | finds | — | — | — |
| total discount | `rule:Order.discount_total_is_money` | finds | — | — | — |
| how many | `rule:Order.how_many` | finds | — | — | — |
| items | `rule:Order.how_many` | finds | — | — | — |
| lines | `rule:Order.how_many` | finds | — | — | — |
| orders | `rule:Order.how_many` | finds | — | — | — |
| quantity | `rule:Order.how_many` | finds | — | — | — |
| units sold | `rule:Order.how_many` | finds | — | — | — |
| volume | `rule:Order.how_many` | finds | — | — | — |
| event | `rule:Order.is_the_purchase` | finds | — | — | — |
| how many orders | `rule:Order.is_the_purchase` | finds | — | — | — |
| order | `rule:Order.is_the_purchase` | finds | — | — | — |
| order line | `rule:Order.is_the_purchase` | finds | — | — | — |
| purchase | `rule:Order.is_the_purchase` | finds | — | — | — |
| sale | `rule:Order.is_the_purchase` | finds | — | — | — |
| margin | `rule:Order.margin_ratio_is_named` | finds | — | — | — |
| margin on cost | `rule:Order.margin_ratio_is_named` | finds | — | — | — |
| margin percent | `rule:Order.margin_ratio_is_named` | finds | — | — | — |
| markup | `rule:Order.margin_ratio_is_named` | finds | — | — | — |
| net margin | `rule:Order.margin_ratio_is_named` | finds | — | — | — |
| profit | `rule:Order.margin_ratio_is_named` | finds | — | — | — |
| margin % | `rule:Order.margin_ratio_is_named.margin_percent` | binds | — | — | — |
| margin on net | `rule:Order.margin_ratio_is_named.margin_percent` | binds | — | — | — |
| margin percentage | `rule:Order.margin_ratio_is_named.margin_percent` | binds | — | — | — |
| margin rate | `rule:Order.margin_ratio_is_named.margin_percent` | binds | — | — | — |
| net margin | `rule:Order.margin_ratio_is_named.margin_percent` | binds | — | — | — |
| margin on cost | `rule:Order.margin_ratio_is_named.markup_percent` | binds | — | — | — |
| markup | `rule:Order.margin_ratio_is_named.markup_percent` | binds | — | — | — |
| markup % | `rule:Order.margin_ratio_is_named.markup_percent` | binds | — | — | — |
| markup percentage | `rule:Order.margin_ratio_is_named.markup_percent` | binds | — | — | — |
| cancellation | `rule:Order.no_lifecycle_state` | finds | — | — | — |
| cancelled | `rule:Order.no_lifecycle_state` | finds | — | — | — |
| lifecycle | `rule:Order.no_lifecycle_state` | finds | — | — | — |
| order status | `rule:Order.no_lifecycle_state` | finds | — | — | — |
| return | `rule:Order.no_lifecycle_state` | finds | — | — | — |
| returned | `rule:Order.no_lifecycle_state` | finds | — | — | — |
| anchor | `rule:Order.now_is_the_newest_order` | finds | — | — | — |
| last month | `rule:Order.now_is_the_newest_order` | finds | — | — | — |
| latest | `rule:Order.now_is_the_newest_order` | finds | — | — | — |
| newest order | `rule:Order.now_is_the_newest_order` | finds | — | — | — |
| now | `rule:Order.now_is_the_newest_order` | finds | — | — | — |
| relative period | `rule:Order.now_is_the_newest_order` | finds | — | — | — |
| sampling date | `rule:Order.now_is_the_newest_order` | finds | — | — | — |
| today | `rule:Order.now_is_the_newest_order` | finds | — | — | — |
| all time | `rule:Order.period` | finds | — | — | — |
| no period | `rule:Order.period` | finds | — | — | — |
| period | `rule:Order.period` | finds | — | — | — |
| this year | `rule:Order.period` | finds | — | — | — |
| time window | `rule:Order.period` | finds | — | — | — |
| unscoped | `rule:Order.period` | finds | — | — | — |
| average price | `rule:Order.price_is_per_article` | finds | — | — | — |
| net price | `rule:Order.price_is_per_article` | finds | — | — | — |
| per article | `rule:Order.price_is_per_article` | finds | — | — | — |
| per unit | `rule:Order.price_is_per_article` | finds | — | — | — |
| price | `rule:Order.price_is_per_article` | finds | — | — | — |
| unit price | `rule:Order.price_is_per_article` | finds | — | — | — |
| average price | `rule:Order.price_is_per_article.price_per_article` | binds | — | — | — |
| per article | `rule:Order.price_is_per_article.price_per_article` | binds | — | — | — |
| per unit | `rule:Order.price_is_per_article.price_per_article` | binds | — | — | — |
| price | `rule:Order.price_is_per_article.price_per_article` | binds | — | — | — |
| price per article | `rule:Order.price_is_per_article.price_per_article` | binds | — | — | — |
| price per unit | `rule:Order.price_is_per_article.price_per_article` | binds | — | — | — |
| discount | `rule:Order.price_terms` | finds | — | — | — |
| gross | `rule:Order.price_terms` | finds | — | — | — |
| list price | `rule:Order.price_terms` | finds | — | — | — |
| margin | `rule:Order.price_terms` | finds | — | — | — |
| net | `rule:Order.price_terms` | finds | — | — | — |
| net price | `rule:Order.price_terms` | finds | — | — | — |
| selling price | `rule:Order.price_terms` | finds | — | — | — |
| unit cost | `rule:Order.price_terms` | finds | — | — | — |
| unit price | `rule:Order.price_terms` | finds | — | — | — |
| conversion | `rule:Order.rate_on_order_date` | finds | — | — | — |
| currency | `rule:Order.rate_on_order_date` | finds | — | — | — |
| exchange rate | `rule:Order.rate_on_order_date` | finds | — | — | — |
| fx | `rule:Order.rate_on_order_date` | finds | — | — | — |
| order date | `rule:Order.rate_on_order_date` | finds | — | — | — |
| gross | `rule:Order.revenue_means_net` | finds | — | — | — |
| gross revenue | `rule:Order.revenue_means_net` | finds | — | — | — |
| net | `rule:Order.revenue_means_net` | finds | — | — | — |
| net revenue | `rule:Order.revenue_means_net` | finds | — | — | — |
| revenue | `rule:Order.revenue_means_net` | finds | — | — | — |
| sales | `rule:Order.revenue_means_net` | finds | — | — | — |
| turnover | `rule:Order.revenue_means_net` | finds | — | — | — |

## Grounded in

- [`v_contoso5_sales_line`](../../data/datasets/v_contoso5_sales_line.md) — served as `"contoso_served"."v_contoso5_sales_line"`

## Grain

- One row of `v_contoso5_sales_line` is identified by `order_key`, `line_number` (the dataset key).
- One Order is one distinct `order_key` (`counts`, the instance).

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `order_key` | identifier | — | — | — | — | the order this line belongs to; with `line_number` it is this relation's key. An order has one or more lines. The order header is a degenerate dimension here, not a second fact (rule Order.is_the_purchase). | — |
| `line_number` | identifier | — | — | — | — | which line of the order this is, 0 to 6. One order can hold several products, and the line is the grain of this fact. | — |
| `order_date` | date | — | — | — | — | the day the order was placed. THE PERIOD COLUMN: an unqualified question about when is answered on this and not on `delivery_date` (Order.date). | [ExchangeRate](ExchangeRate.md) via `order__converts_at__exchange_rate` |
| `delivery_date` | date | — | — | — | — | the day the order was delivered. Measured: never before `order_date` and never null. NOT the period a question is answered on unless it says delivery. | — |
| `customer_key` | dimension | — | — | — | — | the customer who bought, joining dim_customer. The only route from a sale to a PERSON, and so the only way to attribute internet sales to a country. | [Customer](Customer.md) via `order__placed_by__customer` |
| `store_key` | dimension | — | — | — | — | the store the sale was rung up at, joining dim_store. Store key `999999` is the single online outlet, and `channel` beside this column states that split on the fact itself — so a question no longer has to reach dim_store to learn which channel a sale was in. | [Store](Store.md) via `order__placed_at__store` |
| `is_web_sale` | identifier | — | — | — | — | true on every web-shop line, false on every shop line, never empty; the same split as `channel`, as true / false. Made by the transform so that rule Order.channel reads its `shops` and `online` options from a column instead of a stored value. | — |
| `product_key` | dimension | — | — | — | — | the product sold, joining dim_product. | [Product](Product.md) via `order__of__product` |
| `currency_code` | dimension | — | — | — | [`dim_currency`](../../data/datasets/dim_currency.md).`currency_code` via `order__paid_in__currency` | THE CURRENCY THE SALE WAS TRANSACTED IN, and NOT the unit of the amounts on this row. The amounts are USD. Filtering on this and presenting the amounts as if they were in that currency is forbidden by currency.ambiguity.code_is_not_the_unit_of_the_amounts. | [Currency](Currency.md) via `order__paid_in__currency`, [ExchangeRate](ExchangeRate.md) via `order__converts_at__exchange_rate` |
| `quantity` | measure | — | flow · units | — | — | how many units of the product the line sold. | — |
| `net_amount` | measure | — | flow · USD | — | — | what the customer was actually charged for the line, in USD, after discount: exactly `quantity * net_price`. THE DEFAULT MONEY COLUMN: a question saying revenue or sales without saying net or gross is answered here (rule Order.revenue_means_net). AN UNQUALIFIED PRICE means what the customer paid per article: this column summed and divided by `quantity` summed (operator ruling, 2026-09-30; rule Order.price_is_per_article). When a question says store, shop, product, or placed without naming a competing figure, those words are read on this same sales-line figure. | — |
| `gross_amount` | measure | — | flow · USD | — | — | what the line would have cost at list price, in USD: exactly `quantity * unit_price`, on every line. The figure BEFORE discount. | — |
| `cost_amount` | measure | — | flow · USD | — | — | what the goods on the line cost Contoso, in USD. Measured: exactly `quantity * unit_cost`. | — |
| `discount_amount` | measure | — | flow · USD | — | — | the money given away on the line, in USD. Measured: exactly `gross_amount - net_amount`. Upstream the discount is an integer percent from a closed set of 15 steps, 0 to 14. | — |
| `margin_amount` | measure | — | flow · USD | — | — | the profit on the line, in USD. Measured: exactly `net_amount - cost_amount`, so it is margin on the DISCOUNTED price and not on list. | — |
| `unit_price` | measure | — | rate · USD | — | — | what ONE UNIT ON THIS LINE was charged before discount, in USD. Measured against the source: `unit_price = product.Price × f`, where `f` is the same per-line factor used for `unit_cost = product.Cost × f`. From 2024 onward `f = 1.0`, so this is the current list price level for all products sold in that period. `gross_amount` is exactly `quantity * unit_price`. | — |
| `net_price` | measure | — | rate · USD | — | — | the price actually paid for one unit, in USD, after discount. Upstream: `unit_price * (1 - discount/100)`, and measured never above `unit_price`. | — |
| `unit_cost` | measure | — | rate · USD | — | — | what one unit cost Contoso, in USD. Upstream it is scaled by the same price factor as `unit_price`, so margin PERCENT is stable within a category while absolute margin moves — a margin-erosion story read off this data is an artefact of the generator. | — |

_Declared per column, over 18 served columns: is 18 of 18 · label 0 of 18 · measure 9 of 18 · names 0 of 18 · value set 1 of 18 · means 18 of 18 · joins → 5 of 18. An em dash is a column for which nothing is declared._

## Axes

Measure `quantity`: quantity `flow` · average: fold ÷ count distinct instance.
Measure `net_amount`: quantity `flow` · average: fold ÷ count distinct instance.
Measure `gross_amount`: quantity `flow` · average: fold ÷ count distinct instance.
Measure `cost_amount`: quantity `flow` · average: fold ÷ count distinct instance.
Measure `discount_amount`: quantity `flow` · average: fold ÷ count distinct instance.
Measure `margin_amount`: quantity `flow` · average: fold ÷ count distinct instance.
Measure `unit_price`: quantity `rate` · average: `weighted_by`, or `plain_mean` (disclosed); else refused; a total = Σ(rate × `weighted_by`).
Measure `net_price`: quantity `rate` · average: `weighted_by`, or `plain_mean` (disclosed); else refused; a total = Σ(rate × `weighted_by`).
Measure `unit_cost`: quantity `rate` · average: `weighted_by`, or `plain_mean` (disclosed); else refused; a total = Σ(rate × `weighted_by`).

| axis | axis kind | fold `quantity` | fold `net_amount` | fold `gross_amount` | fold `cost_amount` | fold `discount_amount` | fold `margin_amount` | fold `unit_price` | fold `net_price` | fold `unit_cost` |
|---|---|---|---|---|---|---|---|---|---|---|
| `order_date` | date | sum | sum | sum | sum | sum | sum | never (`over_time: average` allowed) | never (`over_time: average` allowed) | never (`over_time: average` allowed) |
| `delivery_date` | date | sum | sum | sum | sum | sum | sum | never (`over_time: average` allowed) | never (`over_time: average` allowed) | never (`over_time: average` allowed) |
| `customer_key` | dimension | sum | sum | sum | sum | sum | sum | never | never | never |
| `store_key` | dimension | sum | sum | sum | sum | sum | sum | never | never | never |
| `product_key` | dimension | sum | sum | sum | sum | sum | sum | never | never | never |
| `currency_code` | dimension | sum | sum | sum | sum | sum | sum | never | never | never |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

*6 edge(s) out · 0 in — the only joins (L7), walked in both directions.*

**Joins to** — edges from this concept:

- [Country](Country.md) — `order__attributed_to__country` on `sale_country_code` = `country_code`
- [Currency](Currency.md) — `order__paid_in__currency` on `currency_code` = `currency_code`
- [Customer](Customer.md) — `order__placed_by__customer` on `customer_key` = `customer_key`
- [ExchangeRate](ExchangeRate.md) — `order__converts_at__exchange_rate` on `order_date` = `date_day`, `currency_code` = `to_currency`, `unit_currency` = `from_currency`
- [Product](Product.md) — `order__of__product` on `product_key` = `product_key`
- [Store](Store.md) — `order__placed_at__store` on `store_key` = `store_key`

## Source of record

- Declaration: `ontology/concepts/Order.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/Order.md`](../../../ontology/concepts/Order.md) — the authored account (X-3); this page cites it and never writes it.
