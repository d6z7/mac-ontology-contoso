# Order

> The human account. The declaration is `ontology/concepts/order.yaml`; read this first, whole, then compare it against that
> file. Every ruling below is dated and every figure measured.

## What an order is

THE PURCHASE. Somebody bought something, at a store, on a day, in a currency: 93,470 of them over
ten years. Read from the rows: order 139000 is two products bought by one customer at one store on
2016-05-18. A2: does it HAPPEN and move through phases? Placed on a day, delivered on another →
`event`. It is the only event in this bundle. IT IS THE EVENT AND ITS LINES ARE NOT — operator
ruling, 2026-09-30, and the rows prove it. An event needs a when, a who and a where. Across all
93,470 orders the number that differ across their own lines is ZERO for `order_date`,
`delivery_date`, `customer_key`, `store_key` and `currency_code`. Only product, quantity and price
vary: 61,042, 55,704 and 61,045 orders respectively. So a line owns nothing that makes it an
occurrence; it borrows the when, the who and the where from the order and adds which product and
how many. WHAT THE LINE GRAIN IS FOR. The six measures — [[NetRevenue]], [[GrossRevenue]],
[[SalesCost]], [[Discount]], [[Margin]] and [[UnitsSold]] — are all keyed on `order_key` and
`line_number`. They ARE the line, and they needed no concept to stand for it. A `Sale` concept was
carried here until 2026-09-30 and deleted: its columns were this concept's six with `product_key`
and `line_number` added, so it was the order repeated once per product with the header copied onto
every copy. HOW MANY IS THREE QUESTIONS, NOT ONE. Purchases are 93,470 (this concept). Items are
703,621 ([[UnitsSold]]). Rows are 223,974, which is how the storage holds the other two and is not
a business quantity. IT DECLARES `product_key` BECAUSE ITS ROWS CARRY ONE. The relation is at line
grain and this concept reaches order grain by counting distinct `order_key`, never by collapsing,
so every row it reads has exactly one product. Declaring it is what makes this concept findable as
the FACT a countable dimension anchors on: `planner/joins.py#_find_fact_anchor` looks for an
EVENT-class concept declaring the counted key on its own table, and without it "how many distinct
products were sold in 2023" refused, because Product has no date and the period could bind to
nothing. IT HAS NO RELATION OF ITS OWN, AND THAT IS RIGHT. The raw `orders` landing repeats the
header on every line and carries no measure; `sales` subsumes it column for column and row for
row. So this concept reads the served line relation at order grain, by the rule below.

## How identity is established

An `order_key` carried on every line of the order. The identity of a group with no relation of its
own, so no surrogate and no name to annotate it.

## The grain

one row per order (order_key), reached by counting distinct keys over the line relation — NOT
collapsed, so each row it reads carries exactly one product

## One row per line, grouped to the order

it is a landing no dataset reads, carries no measure, and would be a second home under a notion
this one computes

The declaration states this executably as well, because this rule has no body yet:

- **when** — orders are needed as instances rather than as a filter
- **then** — group `{v_contoso5_sales_line}` on `{order_key}`; the header attributes are constant within each
- **never** — read the raw `orders` landing

## The rate is the order date's rate

the rate's key is a triple; on one column the join is many:many and multiplies each line by every
day the pair was quoted — 100,450 rows of it

The declaration states this executably as well, because this rule has no body yet:

- **when** — an order's USD amount is wanted in the customer's currency
- **then** — join `{v_contoso5_fx_rate}` on `{order_date}` against the rate's day AND `{currency_code}` against its to-currency, with the from-currency fixed at USD — the whole rate key minus the unit the amounts are already in.
- **never** — join on currency alone

## Which date puts an order in a period

both dates are on every line and they differ, so the choice moves revenue between periods without
changing the total — invisible in any one figure. Order date is the reporting convention; delivery
is a logistics question.

The declaration states this executably as well, because this rule has no body yet:

- **when** — orders are put in a period and the question does not say which date
- **then** — bind the period to `{order_date}` — the column declared `period` — and say so in the answer; `{delivery_date}` is used only when the question asks about delivery
- **never** — bind the period to `{delivery_date}` unasked, or to `{order_date}` without saying so

## An order has no state beyond its two dates

both dates are on every line and constant within the order, and there is no status column, so an
order has no observable state beyond "placed on this day, delivered on that one". Nothing records
cancellation or return; a question about either is unanswerable here and must say so rather than
read an absent state as a negative.

That last sentence is the one that matters at answer time. An absent column is not a zero: if
nothing records a cancellation, "how many orders were cancelled" has no answer in this warehouse,
and returning 0 would be a claim the data does not support. The two dates are what the rows carry,
so they are the whole of what an order's lifecycle can be asked about here.

## An unscoped question covers all time

an unscoped total and a year-to-date total are different numbers and a reader cannot tell them
apart from the figure alone. The operator ruled on 2026-09-30 that an unspecified period is always
over all time, which makes the default safe as long as it is disclosed — the extent is ten years
wide, so silently narrowing it would be the larger error. Confidence is C because a person ruled
it.

The declaration states this executably as well, because this rule has no body yet:

- **when** — a measure is asked for and the question names no period
- **then** — cover the full extent of `{order_date}` and state the first and last date the answer included
- **never** — assume the current year, the latest month, or any other window the question did not name
