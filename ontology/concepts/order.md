---
type: Event
title: Order
description: One customer's purchase on one date, counted by distinct `order_key` over the line relation.
tags:
- CONTOSO5
- event
- confidence:C
resource: table://v_contoso5_sales_line
---

One customer's purchase on one date, counted by distinct `order_key` over the line relation. It is also THE FACT NODE of the sales line, one row per order line - every money and quantity measure (net, gross, cost, discount, margin, units, and the per-unit prices) is a column it serves, and every edge from the sale to a dimension starts here. The account is knowledge/order.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.4.0-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-30

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

**Default reading** — A QUESTION THAT NAMES NO PERIOD COVERS ALL TIME — operator ruling, 2026-09-30 (rule Order.period). No implied "this year" and no implied latest month. State the window the answer actually covered — its first and last `order_date` — because an unscoped total and a year-to- date total are indistinguishable from the figure alone.

## Grounded in

- `v_contoso5_sales_line` — key `order_key`, `line_number` — semantics: [`data/datasets/v_contoso5_sales_line.yaml`](../../data/datasets/v_contoso5_sales_line.md)

## Grain

- One row is one Order, identified by `order_key`, `line_number`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `order_key` | integer | key | — | — | — | — | the order this line belongs to; with `line_number` it is this relation's key. An order has one or more lines. The order header is a degenerate dimension here, not a second fact (rule Order.is_the_purchase). | — |
| `line_number` | integer | key | — | — | — | — | which line of the order this is, 0 to 6. One order can hold several products, and the line is the grain of this fact. | — |
| `order_date` | date | period | — | — | — | — | the day the order was placed. THE PERIOD COLUMN: an unqualified question about when is answered on this and not on `delivery_date` (order.default.period_is_order_date). | [Exchange Rate](exchange_rate.md) _(business)_ |
| `delivery_date` | date | dimension | — | — | — | — | the day the order was delivered. Measured: never before `order_date` and never null. NOT the period a question is answered on unless it says delivery. | — |
| `customer_key` | integer | key | -> Customer | — | — | — | the customer who bought, joining dim_customer. The only route from a sale to a PERSON, and so the only way to attribute internet sales to a country. | [Customer](customer.md) |
| `store_key` | integer | key | -> Store | — | — | — | the store the sale was rung up at, joining dim_store. Store key `999999` is the single online outlet, and `channel` beside this column states that split on the fact itself — so a question no longer has to reach dim_store to learn which channel a sale was in. | [Store](store.md) |
| `product_key` | integer | key | -> Product | — | — | — | the product sold, joining dim_product. | [Product](product.md) |
| `currency_code` | string | dimension | — | — | — | — | THE CURRENCY THE SALE WAS TRANSACTED IN, and NOT the unit of the amounts on this row. The amounts are USD. Filtering on this and presenting the amounts as if they were in that currency is forbidden by currency.ambiguity.code_is_not_the_unit_of_the_amounts. | [Currency](currency.md) |
| `quantity` | integer | measure | — | flow · units | — | — | how many units of the product the line sold. | — |
| `net_amount` | decimal | measure | — | flow · USD · **default** | — | — | what the customer was actually charged for the line, in USD, after discount: exactly `quantity * net_price`. THE DEFAULT MONEY COLUMN: a question saying revenue or sales without saying net or gross is answered here (rule Order.revenue_means_net). AN UNQUALIFIED PRICE means what the customer paid per article: this column summed and divided by `quantity` summed (operator ruling, 2026-09-30; rule Order.price_is_per_article). When a question says store, shop, product, or placed without naming a competing figure, those words are read on this same sales-line figure. | — |
| `gross_amount` | decimal | measure | — | flow · USD | — | — | what the line would have cost at list price, in USD: exactly `quantity * unit_price`, on every line. The figure BEFORE discount. | — |
| `cost_amount` | decimal | measure | — | flow · USD | — | — | what the goods on the line cost Contoso, in USD. Measured: exactly `quantity * unit_cost`. | — |
| `discount_amount` | decimal | measure | — | flow · USD | — | — | the money given away on the line, in USD. Measured: exactly `gross_amount - net_amount`. Upstream the discount is an integer percent from a closed set of 15 steps, 0 to 14. | — |
| `margin_amount` | decimal | measure | — | flow · USD | — | — | the profit on the line, in USD. Measured: exactly `net_amount - cost_amount`, so it is margin on the DISCOUNTED price and not on list. | — |
| `unit_price` | decimal | measure | — | intensive · USD | — | — | what ONE UNIT ON THIS LINE was charged before discount, in USD. Measured against the source: `unit_price = product.Price × f`, where `f` is the same per-line factor used for `unit_cost = product.Cost × f`. From 2024 onward `f = 1.0`, so this is the current list price level for all products sold in that period. `gross_amount` is exactly `quantity * unit_price`. | — |
| `net_price` | decimal | measure | — | intensive · USD | — | — | the price actually paid for one unit, in USD, after discount. Upstream: `unit_price * (1 - discount/100)`, and measured never above `unit_price`. | — |
| `unit_cost` | decimal | measure | — | intensive · USD | — | — | what one unit cost Contoso, in USD. Upstream it is scaled by the same price factor as `unit_price`, so margin PERCENT is stable within a category while absolute margin moves — a margin-erosion story read off this data is an artefact of the generator. | — |

_Declared per column, over 17 columns: type 17 of 17 · role 17 of 17 · identity 3 of 17 · measure 9 of 17 · rulings 0 of 17 · register 0 of 17 · description 17 of 17 · joins → 5 of 17. An em dash is a column for which nothing is declared._

## Axes

Measure type: `flow`.

| axis | axis kind | fold |
|---|---|---|
| `currency_code` | categorical | additive |
| `customer_key` | categorical | additive |
| `delivery_date` | time | additive |
| `order_date` | time | additive |
| `product_key` | categorical | additive |
| `store_key` | categorical | additive |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*6 join(s) out · 0 in — click a concept to open it.*

**Joins to** — this concept references:

- [Country](country.md) — joined on `sale_country_code`
- [Currency](currency.md) — joined on `currency_code`
- [Customer](customer.md) — joined on `customer_key`
- [Exchange Rate](exchange_rate.md) — joined on `order_date`
- [Product](product.md) — joined on `product_key`
- [Store](store.md) — joined on `store_key`

## Source of record

- Full MAC concept: `order.yaml` — open the **YAML** tab for the complete typed definition.
