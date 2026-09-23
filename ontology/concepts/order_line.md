---
type: Event
title: Order Line
description: 'One line of one customer order: one product, in one quantity, at one list price and one discounted price, placed at one store on one day and delivered on one day.'
tags:
- CONTOSO
- event
- confidence:I
resource: table://v_contoso_order_line
rule_pages:
- rules/order_line.grain.no_header_relation.md
- rules/order_line.currency.no_bare_cross_currency_sum.md
---

One line of one customer order: one product, in one quantity, at one list price and one discounted price, placed at one store on one day and delivered on one day. This is the fact of record for every sales figure in this bundle, at line grain (OrderKey, RowNumber).
IT IS NOT AN ORDER. An order is a group of these lines sharing one OrderKey; the order header is consumed into this relation and deliberately not served as a relation of its own (NS-ORDERS-02), so an order-grain question is answered by count(DISTINCT OrderKey) and by grouping on the header attributes this row repeats — never by joining to a header relation, which does not exist.
IT IS ALSO NOT `main.sales`. That relation delivers the identical 223 974 lines a second time and is measured, described and not served (NS-ORDERS-01); a figure summed from both is exactly double.

## Details

- **Identity** — composite
- **Version** — 1.0
- **Schema version** — 0.1.14
- **Status** — draft
- **Owner** — operator
- **Governance owner** — operator
- **Last reviewed** — 2026-09-18

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
Read v_contoso_order_line at its declared key; the two date roles and the four dimension keys are the columns whitelisted above. Nothing here needs a warehouse probe, and nothing here needs the header relation, which does not exist.
```

## Grounded in

- `v_contoso_order_line` — key `['OrderKey', 'RowNumber']`

## Grain
one row = one line of one order — (OrderKey, RowNumber)

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `OrderKey` | bigint | key | `v_contoso_order_line` | part 1 of the cell key. A DEGENERATE DIMENSION here: the order header is not served as a relation of its own (NS-ORDERS-02), so this column groups the lines of an order and joins to nothing. | — |
| `RowNumber` | integer | key | `v_contoso_order_line` | part 2 of the cell key; indispensable — (OrderKey, ProductKey) is NOT unique (223 713 pairs over 223 974 rows, P2 G2). Numbering starts at 0 and 1 448 orders have gaps, so a dense line index may not be assumed (P1 U5). `sales` carries the identical values under the name LineNumber (0 rows either way on EXCEPT, S4). | — |
| `OrderDate` | date | dimension | `v_contoso_order_line` | RENAMED from the landing's `DT` to the name this same value carries in the `sales` delivery (measured identical on 223 974/223 974 rows, S5 diff_orderdate = 0). The only renamed column in this bundle; every other served column keeps its landing name. DATE since 2026-09-19, cast in the transform from the landing's TIMESTAMP on the operator's ruling; lossless and measured, not assumed — 0 non-midnight over 223 974 of 223 974 rows immediately before the cast. main.orders (and the unread main.sales) keep TIMESTAMP. Both joins that cross this column were cast on both sides in the same change: the conversion join to v_contoso_fx_rate_day.Date and the ordered role to dim_contoso_calendar_day.Date. | [Calendar Day](calendar_day.md) |
| `DeliveryDate` | date | dimension | `v_contoso_order_line` | second role of the one calendar (role_playing_dimension): 0 values off the calendar (S15). Runs to 2026-01-06, six days past the last order. DATE since 2026-09-19, same cast and same evidence as OrderDate: 0 non-midnight over 223 974 of 223 974 rows. Re-measured after the cast — 3 498 of 4 018 delivered days, inclusion 1.0, 0 orphans. | [Calendar Day](calendar_day.md) |
| `CustomerKey` | integer | key | `v_contoso_order_line` | — | [Customer](customer.md) |
| `StoreKey` | integer | key | `v_contoso_order_line` | 93 550/223 974 lines (41.8 %) carry the sentinel StoreKey 999999 ('Online'), which IS served (S18): filtering it would silently drop 41.8 % of the fact. | [Store](store.md) |
| `ProductKey` | integer | key | `v_contoso_order_line` | — | [Product](product.md) |
| `CurrencyCode` | varchar | dimension | `v_contoso_order_line` | the denomination of every amount on the row; 5 measured values. Joins to the fx grid as FromCurrency together with the day, not by itself. | [Currency](currency.md) _(business)_ |
| `Quantity` | integer | measure | `v_contoso_order_line` | Quantity — units on the line; measured > 0 on all 223 974 rows. | — |
| `UnitPrice` | decimal(20,5) | measure | `v_contoso_order_line` | list price per unit (the GROSS side of the scope's gross/net question). | — |
| `NetPrice` | decimal(20,5) | measure | `v_contoso_order_line` | price per unit after discount; measured <= UnitPrice on every row, below it on 136 913/223 974 lines (S6). | — |
| `UnitCost` | decimal(20,5) | measure | `v_contoso_order_line` | UnitCost — cost per unit; served, and no margin measure is declared over it yet. | — |

_Declared per column, over 12 columns: description 10 of 12 · type 12 of 12 · joins → 6 of 12. An em dash is a column for which nothing is declared._

## Relationships

*7 join(s) out · 2 in — click a concept to open it.*

**Joins to** — this concept references:

- [Calendar Day](calendar_day.md) — joined on `DeliveryDate`
- [Calendar Day](calendar_day.md) — joined on `OrderDate`
- [Currency](currency.md) — joined on `CurrencyCode`
- [Customer](customer.md) — joined on `CustomerKey`
- [Exchange Rate](exchange_rate.md) — joined on `?`
- [Product](product.md) — joined on `ProductKey`
- [Store](store.md) — joined on `StoreKey`

**Referenced by** — these point at this concept:

- [Gross Sales Amount](gross_sales_amount.md) — on `Quantity`
- [Net Sales Amount](net_sales_amount.md) — on `Quantity`

## Source of record
- Full MAC concept: `order_line.yaml` — open the **YAML** tab for the complete typed definition.