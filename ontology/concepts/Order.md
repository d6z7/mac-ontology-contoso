# Order

The account of concept Order.

## What an order is

THE PURCHASE. Somebody bought something, at a store, on a day, in a currency. Read from the rows: one order can be several products bought by one customer at one store on one day. IT IS THE EVENT AND ITS LINES ARE NOT — operator ruling, and the rows prove it. An event needs a when, a who and a where. No order differs across its own lines in `order_date`, `delivery_date`, `customer_key`, `store_key` or `currency_code`. Only product, quantity and price vary. So a line owns nothing that makes it an occurrence; it borrows the when, the who and the where from the order and adds which product and how many. WHAT THE LINE GRAIN IS FOR. The six measures — [[NetRevenue]], [[GrossRevenue]], [[SalesCost]], [[Discount]], [[Margin]] and [[UnitsSold]] — are all keyed on `order_key` and `line_number`. They ARE the line, and they need no concept to stand for it. HOW MANY IS THREE QUESTIONS, NOT ONE. Purchases are counted by this concept. Items are [[UnitsSold]]. Rows are how the storage holds the other two and are not a business quantity. IT DECLARES `product_key` BECAUSE ITS ROWS CARRY ONE. The relation is at line grain and this concept reaches order grain by counting distinct `order_key`, never by collapsing, so every row it reads has exactly one product. Declaring it is what makes this concept findable as the FACT a countable dimension anchors on: a question counting distinct products sold in a period binds its period here, because Product has no date. IT HAS NO RELATION OF ITS OWN, AND THAT IS RIGHT. The raw `orders` landing holds one row per order and carries no measure; `sales` carries every one of its columns on every line of the order. So this concept reads the served line relation at order grain, by the rule below.

## How identity is established

An `order_key` carried on every line of the order. The identity of a group with no relation of its own, so no surrogate and no name to annotate it.

## The grain

one row per order (order_key), reached by counting distinct keys over the line relation — NOT collapsed, so each row it reads carries exactly one product

## One row per line, grouped to the order

it is a landing no dataset reads, carries no measure, and would be a second home under a notion this one computes

- **when** — orders are needed as instances rather than as a filter
- **then** — group `{v_contoso5_sales_line}` on `{order_key}`; the header attributes are constant within each
- **never** — read the raw `orders` landing

## The rate is the order date's rate

the rate's key is a triple; on one column the join is many:many and multiplies each line by every day the pair was quoted

- **when** — an order's USD amount is wanted in the customer's currency
- **then** — join `{v_contoso5_fx_rate}` on `{order_date}` against the rate's day AND `{currency_code}` against its to-currency, with the from-currency fixed at USD — the whole rate key minus the unit the amounts are already in.
- **never** — join on currency alone

## Which date puts an order in a period

both dates are on every line and they differ, so the choice moves revenue between periods without changing the total — invisible in any one figure. Order date is the reporting convention; delivery is a logistics question.

- **when** — orders are put in a period and the question does not say which date
- **then** — bind the period to `{order_date}` — the default (`ordered`) of rule Order.date — and say so in the answer; `{delivery_date}` is used only when the question asks about delivery
- **never** — bind the period to `{delivery_date}` unasked, or to `{order_date}` without saying so

## An order has no state beyond its two dates

both dates are on every line and constant within the order, and there is no status column, so an order has no observable state beyond "placed on this day, delivered on that one". Nothing records cancellation or return; a question about either is unanswerable here and must say so rather than read an absent state as a negative.

That last sentence is the one that matters at answer time. An absent column is not a zero: if nothing records a cancellation, "how many orders were cancelled" has no answer in this warehouse, and returning 0 would be a claim the data does not support. The two dates are what the rows carry, so they are the whole of what an order's lifecycle can be asked about here.

## An unscoped question covers all time

an unscoped total and a year-to-date total are different numbers and a reader cannot tell them apart from the figure alone. An unspecified period is always over all time (rule Order.period), which makes the default safe as long as it is disclosed — the extent is many years wide, so silently narrowing it would be the larger error.

- **when** — a measure is asked for and the question names no period
- **then** — cover the full extent of `{order_date}` and state the first and last date the answer included
- **never** — assume the current year, the latest month, or any other window the question did not name

## NetRevenue — measure `net_amount`

### Overview

What Contoso actually charged: quantity times the discounted price, per sale, summed. Read from the rows: net is below gross on a discounted sale — the gap is the discount. THE DEFAULT READING OF "REVENUE", and it is after discount. [[GrossRevenue]] is the same figure before it. Answering one when a question meant the other moves every derived figure — margin most of all — in a direction somebody will like. IT IS IN USD. The sale's `currency_code` names what the customer paid in, not what this is stated in; conversion goes through [[ExchangeRate]] at the sale's own order date.

### Grain

one row per sale (order_key, line_number)

### Order.revenue_means_net

the gap between net and gross is the discount, so the wrong choice moves every derived figure by exactly the amount somebody wanted to see

- **when** — a question says "revenue" or "sales" without saying net or gross
- **then** — answer with `{net_amount}` and say NET — it is after discount; the figure before discount is [[GrossRevenue]]
- **never** — pick one silently

### Order.price_is_per_article

the average is what the customer paid per article, so the denominator is articles sold and not sale lines. All three readings look like a unit price and only one answers the question.

THREE READINGS LOOK LIKE A UNIT PRICE AND ONE ANSWERS THE QUESTION, and their figures differ, which is why the choice is not presentational:

| reading | arithmetic |
|---|---|
| **price per article** — what this rule declares | `SUM(net_amount) / SUM(quantity)` |
| averaging `net_price` | weights a one-unit sale like a fifty-unit one |
| averaging `net_amount` | the value of a LINE, not of an article |

The pre-discount figure is [[GrossRevenue]] over the same denominator, reached by naming gross — a different axis, held by `Order.revenue_means_net`.

`default: price_per_article` carries this reading: a question naming no reading commits to this one and discloses that it did. The surfaces a person may say are declared — price, average price, price per unit, per unit, price per article, per article — and matched exactly, case/space/underscore folded.

The prohibitions are declarations, not sentences.

## GrossRevenue — measure `gross_amount`

### Overview

What Contoso would have charged at list: quantity times the undiscounted price, per sale, summed. IT IS NOT WHAT WAS RECEIVED — [[NetRevenue]] is. This exists so the discount can be measured, gross minus net; presented as revenue it overstates by exactly that amount.

### Grain

one row per sale (order_key, line_number)

## SalesCost — measure `cost_amount`

### Overview

What the goods on a sale cost Contoso: quantity times unit cost, per sale, summed. MARGIN IS STORED, as `margin_amount`: exactly [[NetRevenue]] minus this on every line, summed at whatever grain the question asks for — never a per-sale margin averaged, which weights a one-unit sale the same as a fifty-unit one.

### Grain

one row per sale (order_key, line_number)

## Discount — measure `discount_amount`

### Overview

Σ Quantity × (UnitPrice − NetPrice). Money given away in discounts, served as `discount_amount`.

### Grain

one row per sale (order_key, line_number)

### Order.discount_percent_is_over_gross

the denominator is gross sales. The two denominators differ by the discount itself, so the choice is not presentational.

## Margin — measure `margin_amount`

### Overview

Σ Quantity × (NetPrice − UnitCost), identical to Revenue − COGS. Absolute profit, served as `margin_amount`.

### Grain

one row per sale (order_key, line_number)

### Order.margin_ratio_is_named

both ratios and their denominators are named. They differ widely on the same profit, so naming one and computing the other is a wrong answer that looks right. a question saying only "margin" names neither, so the honest outcome is to ask with both offered rather than to pick the commoner reading.

## UnitsSold — measure `quantity`

### Overview

How many items went out: the quantity on a sale, summed. IT IS NOT A COUNT OF SALES OR ORDERS. Every sale line carries a quantity and most carry more than one — so "how many did we sell" and "how many times did we sell" are different questions with different answers, and this column answers the first.

### Grain

one row per sale (order_key, line_number)

## Cites

- `dataset:v_contoso5_sales_line.order_key`
- `dataset:v_contoso5_sales_line.line_number`
- `dataset:v_contoso5_sales_line.order_date`
- `dataset:v_contoso5_sales_line.delivery_date`
- `dataset:v_contoso5_sales_line.customer_key`
- `dataset:v_contoso5_sales_line.store_key`
- `dataset:v_contoso5_sales_line.is_web_sale`
- `dataset:v_contoso5_sales_line.product_key`
- `dataset:v_contoso5_sales_line.currency_code`
- `dataset:v_contoso5_sales_line.quantity`
- `dataset:v_contoso5_sales_line.net_amount`
- `dataset:v_contoso5_sales_line.gross_amount`
- `dataset:v_contoso5_sales_line.cost_amount`
- `dataset:v_contoso5_sales_line.discount_amount`
- `dataset:v_contoso5_sales_line.margin_amount`
- `dataset:v_contoso5_sales_line.unit_price`
- `dataset:v_contoso5_sales_line.net_price`
- `dataset:v_contoso5_sales_line.unit_cost`
- `rule:Order.channel`
- `rule:Order.cost_is_procurement`
- `rule:Order.date`
- `rule:Order.default_measure`
- `rule:Order.discount_percent_is_over_gross`
- `rule:Order.discount_total_is_money`
- `rule:Order.how_many`
- `rule:Order.is_the_purchase`
- `rule:Order.margin_ratio_is_named`
- `rule:Order.no_lifecycle_state`
- `rule:Order.now_is_the_newest_order`
- `rule:Order.period`
- `rule:Order.price_is_per_article`
- `rule:Order.price_terms`
- `rule:Order.rate_on_order_date`
- `rule:Order.revenue_means_net`

## grounding.note

reached by counting distinct order_key over the line relation — NOT collapsed, so each row it reads carries exactly one product

## contract.default_reading

A QUESTION THAT NAMES NO PERIOD COVERS ALL TIME (rule Order.period). No implied "this year" and no implied latest month. State the window the answer actually covered — its first and last `order_date` — because an unscoped total and a year-to- date total are indistinguishable from the figure alone.
