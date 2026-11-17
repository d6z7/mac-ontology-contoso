---
type: Dataset
title: v_contoso5_sales_line
description: dataset v_contoso5_sales_line
relation: v_contoso5_sales_line
tags:
- Contoso 5
- dataset
---

- **Served as** — `"contoso_served"."v_contoso5_sales_line"`
- **Key** — `order_key`, `line_number`
- **Made by** — [v_contoso5_sales_line](../transforms/v_contoso5_sales_line.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `order_key` | identifier | PK1 | — | — | — | — | the order this line belongs to; with `line_number` it is this relation's key. An order has one or more lines. The order header is a degenerate dimension here, not a second fact (rule Order.is_the_purchase). |
| `line_number` | identifier | PK2 | — | — | — | — | which line of the order this is, 0 to 6. One order can hold several products, and the line is the grain of this fact. |
| `order_date` | date | — | — | — | — | — | the day the order was placed. THE PERIOD COLUMN: an unqualified question about when is answered on this and not on `delivery_date` (Order.date). |
| `delivery_date` | date | — | — | — | — | — | the day the order was delivered. Measured: never before `order_date` and never null. NOT the period a question is answered on unless it says delivery. |
| `customer_key` | dimension | — | — | — | — | — | the customer who bought, joining dim_customer. The only route from a sale to a PERSON, and so the only way to attribute internet sales to a country. |
| `store_key` | dimension | — | — | — | — | — | the store the sale was rung up at, joining dim_store. Store key `999999` is the single online outlet, and `channel` beside this column states that split on the fact itself — so a question no longer has to reach dim_store to learn which channel a sale was in. |
| `product_key` | dimension | — | — | — | — | — | the product sold, joining dim_product. |
| `channel` | dimension | — | — | — | — | — | WHICH CHANNEL THE SALE WAS IN — `physical` for a shop you can walk into, `online` for the web shop. Derived on the fact from the store key (`store_key = 999999` is the web shop), so it needs no join and is reachable from every question whatever route it takes. Measured equivalent to `dim_store.location_code = -1` on 2026-10-23, with zero disagreements. The value names are the populations rule Store.channel declares, so the axis has one vocabulary. A FINANCIAL QUESTION THAT NAMES NO CHANNEL COVERS BOTH, by the operator's ruling of 2026-10-18 (rule Store.channel). Before this column that reading was the ABSENCE of a predicate, which no gate could check and no answer could disclose; now it can be grouped, stated and verified. |
| `is_web_sale` | identifier | — | — | — | — | — | true on every web-shop line, false on every shop line, never empty; the same split as `channel`, as true / false. Made by the transform so that rule Order.channel reads its `shops` and `online` options from a column instead of a stored value. |
| `sale_country_code` | dimension | — | — | — | — | — | THE COUNTRY OF THE SALE — the ISO code of the country this line is trade IN. A shop sale is attributed to the country the SHOP stands in; a web sale to the country the CUSTOMER lives in. Derived on the fact from `channel` and the two keys, so it needs no join and is reachable from every question whatever route the question takes. This is the reading an unqualified country question means (operator ruling 2026-10-25); the store's, the customer's and the site's own country stay askable BY NAME through their own relations. EVERY LINE REACHES A COUNTRY and none carries the `--` sentinel: the sentinel leaves the country axis of a sale entirely, because a web sale is attributed to a person and a person has a real country. The axis PARTITIONS the sales line — the parts sum to the whole, with no leakage and nothing double counted. The figures that prove it are in the ruling, which is their one home; a figure restated here would be a second home that goes stale on the next load. WHY IT IS NOT `dim_customer.country_code` UNDER ANOTHER NAME, though it is row-for-row identical to it here: no physical sale in this warehouse crosses a border, so the two readings AGREE BY ACCIDENT OF THE DATA. They do not mean the same thing — a German tourist buying in Paris is French trade on this column and German trade on the customer's — and the operator refused `default: customer` on 2026-10-22 for exactly that reason. |
| `currency_code` | dimension | — | — | — | — | — | THE CURRENCY THE SALE WAS TRANSACTED IN, and NOT the unit of the amounts on this row. The amounts are USD. Filtering on this and presenting the amounts as if they were in that currency is forbidden by currency.ambiguity.code_is_not_the_unit_of_the_amounts. |
| `unit_currency` | identifier | — | — | — | — | — | THE CURRENCY THE AMOUNTS ON THIS ROW ARE IN — USD on every line, made by the transform. The upstream publishes it and the warehouse confirms it: the source's own exchange rate on each line is the USD-to-line-currency rate. It is the source currency the exchange-rate edge joins on (order__converts_at__exchange_rate), so the join reads a column instead of a constant. Offered to no question on its own; `currency_code` is the currency a sale was transacted in. |
| `quantity` | measure | — | — | flow · units | — | — | how many units of the product the line sold. |
| `net_price` | measure | — | — | rate · USD | — | — | the price actually paid for one unit, in USD, after discount. Upstream: `unit_price * (1 - discount/100)`, and measured never above `unit_price`. |
| `unit_price` | measure | — | — | rate · USD | — | — | what ONE UNIT ON THIS LINE was charged before discount, in USD. Measured against the source: `unit_price = product.Price × f`, where `f` is the same per-line factor used for `unit_cost = product.Cost × f`. From 2024 onward `f = 1.0`, so this is the current list price level for all products sold in that period. `gross_amount` is exactly `quantity * unit_price`. |
| `unit_cost` | measure | — | — | rate · USD | — | — | what one unit cost Contoso, in USD. Upstream it is scaled by the same price factor as `unit_price`, so margin PERCENT is stable within a category while absolute margin moves — a margin-erosion story read off this data is an artefact of the generator. |
| `net_amount` | measure | — | — | flow · USD | — | — | what the customer was actually charged for the line, in USD, after discount: exactly `quantity * net_price`. THE DEFAULT MONEY COLUMN: a question saying revenue or sales without saying net or gross is answered here (rule Order.revenue_means_net). AN UNQUALIFIED PRICE means what the customer paid per article: this column summed and divided by `quantity` summed (operator ruling, 2026-09-30; rule Order.price_is_per_article). When a question says store, shop, product, or placed without naming a competing figure, those words are read on this same sales-line figure. |
| `gross_amount` | measure | — | — | flow · USD | — | — | what the line would have cost at list price, in USD: exactly `quantity * unit_price`, on every line. The figure BEFORE discount. |
| `cost_amount` | measure | — | — | flow · USD | — | — | what the goods on the line cost Contoso, in USD. Measured: exactly `quantity * unit_cost`. |
| `discount_amount` | measure | — | — | flow · USD | — | — | the money given away on the line, in USD. Measured: exactly `gross_amount - net_amount`. Upstream the discount is an integer percent from a closed set of 15 steps, 0 to 14. |
| `margin_amount` | measure | — | — | flow · USD | — | — | the profit on the line, in USD. Measured: exactly `net_amount - cost_amount`, so it is margin on the DISCOUNTED price and not on list. |

## Checks

_This dataset declares no checks._

## Value sets

- `currency_code` → value set [`dim_currency`](dim_currency.md).`currency_code` via edge `order__paid_in__currency`
- `sale_country_code` → value set [`dim_country`](dim_country.md).`country_code` via edge `order__attributed_to__country`

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `order_key` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `line_number` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `order_date` | `date` | grains | period | — | yes | yes | calendar words | yes |
| `delivery_date` | `date` | grains | period | — | yes | yes | calendar words | yes |
| `customer_key` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `store_key` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `product_key` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `channel` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `is_web_sale` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `sale_country_code` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `currency_code` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `unit_currency` | `identifier` | through its concept | exact; pattern with `match: pattern` | — | yes | — | exact | yes |
| `quantity` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `net_price` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `unit_price` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `unit_cost` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `net_amount` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `gross_amount` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `cost_amount` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `discount_amount` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |
| `margin_amount` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |

## Bound by

*1 concept(s) take rows from this dataset — a change to a column's declaration reaches every one of them.*

- [Order](../../ontology/concepts/Order.md) — serves `order_key`, `line_number`, `order_date`, `delivery_date`, `customer_key`, `store_key`, `is_web_sale`, `product_key`, `currency_code`, `quantity`, `net_amount`, `gross_amount`, `cost_amount`, `discount_amount`, `margin_amount`, `unit_price`, `net_price`, `unit_cost`

## Findings

- [DQ-DUP-ORDERROWS-SALES](../quality/DQ-DUP-ORDERROWS-SALES.md) — medium · open — nobody has ruled — `sales` re-delivers every line of `orderrows` — one fact, twice
- [DQ-ORPHAN-ORDERROWS](../quality/DQ-ORPHAN-ORDERROWS.md) — medium · open — nobody has ruled — raw landing `orderrows` is consumed by no transformation
- [DQ-ORPHAN-ORDERS](../quality/DQ-ORPHAN-ORDERS.md) — medium · open — nobody has ruled — raw landing `orders` is consumed by no transformation
- [DQ-ORPHAN-DATE](../quality/DQ-ORPHAN-DATE.md) — medium · open — nobody has ruled — raw landing `date` is consumed by no transformation
