---
type: Metric
title: Net Sales Amount
description: 'The money value of sales AFTER discount: per order line, Quantity x NetPrice, summed over the lines in scope.'
tags:
- CONTOSO
- measure
- confidence:I
resource: table://v_contoso_order_line
rule_pages:
- rules/net_sales_amount.derivation.quantity_times_net_price.md
- rules/net_sales_amount.ambiguity.gross_or_net.md
- rules/net_sales_amount.evidence.no_line_is_not_a_zero.md
---

The money value of sales AFTER discount: per order line, Quantity x NetPrice, summed over the lines in scope. This is what "total sales" means here when the question does not say otherwise.
IT IS NOT GROSS. NetPrice is measured at or below UnitPrice on every line and strictly below it on 136 913 of 223 974, so the two differ on 61 % of the fact and are not one figure under two names. Gross is a separate concept, asked for explicitly.
IT IS NOT A MARGIN EITHER. UnitCost is served on the same row and no margin measure is declared over it, so "profit" is not answerable from this bundle today.
AND IT IS NOT A CROSS-CURRENCY FIGURE without a stated conversion: every amount is in the order's own CurrencyCode.

## Details

- **Identity** — code
- **Version** — 1.0
- **Schema version** — 0.1.14
- **Status** — draft
- **Owner** — operator
- **Governance owner** — operator
- **Last reviewed** — 2026-09-18

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
Quantity and NetPrice are columns of v_contoso_order_line, declared above; the fold along each axis resolves from measure_type x axis_kinds; the figure's currency is the row's own CurrencyCode. Axis words resolve through the registers the axis concepts declare — Brand, ProductCategory, ProductSubcategory, Product, Country, Continent, GeoArea, Store, Customer — so no probe is needed to turn a name into a code.
```

## Grounded in

- `v_contoso_order_line` — key `['OrderKey', 'RowNumber']`

## Grain
computed per order line — (OrderKey, RowNumber) — then folded over the axes above

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `OrderKey` | bigint | key | `v_contoso_order_line` | part 1 of the cell key. A DEGENERATE DIMENSION here: the order header is not served as a relation of its own (NS-ORDERS-02), so this column groups the lines of an order and joins to nothing. | — |
| `RowNumber` | integer | key | `v_contoso_order_line` | part 2 of the cell key; indispensable — (OrderKey, ProductKey) is NOT unique (223 713 pairs over 223 974 rows, P2 G2). Numbering starts at 0 and 1 448 orders have gaps, so a dense line index may not be assumed (P1 U5). `sales` carries the identical values under the name LineNumber (0 rows either way on EXCEPT, S4). | — |
| `Quantity` | integer | measure | `v_contoso_order_line` | — | [Order Line](order_line.md) _(business)_ |
| `NetPrice` | decimal(20,5) | measure | `v_contoso_order_line` | price per unit after discount; measured <= UnitPrice on every row, below it on 136 913/223 974 lines (S6). | — |
| `CurrencyCode` | varchar | dimension | `v_contoso_order_line` | the denomination of every amount on the row; 5 measured values. Joins to the fx grid as FromCurrency together with the day, not by itself. | — |
| `OrderDate` | date | dimension | `v_contoso_order_line` | RENAMED from the landing's `DT` to the name this same value carries in the `sales` delivery (measured identical on 223 974/223 974 rows, S5 diff_orderdate = 0). The only renamed column in this bundle; every other served column keeps its landing name. DATE since 2026-09-19, cast in the transform from the landing's TIMESTAMP on the operator's ruling; lossless and measured, not assumed — 0 non-midnight over 223 974 of 223 974 rows immediately before the cast. main.orders (and the unread main.sales) keep TIMESTAMP. Both joins that cross this column were cast on both sides in the same change: the conversion join to v_contoso_fx_rate_day.Date and the ordered role to dim_contoso_calendar_day.Date. | — |

_Declared per column, over 6 columns: description 5 of 6 · type 6 of 6 · joins → 1 of 6. An em dash is a column for which nothing is declared._

## Axes

Measure type: `Flow` — `mac.MeasureType.Flow`.

| axis | axis kind | fold |
|---|---|---|
| `brand` | categorical | additive |
| `continent` | categorical | additive |
| `country` | categorical | additive |
| `customer` | categorical | additive |
| `product` | categorical | additive |
| `product_category` | categorical | additive |
| `store` | categorical | additive |
| `time` | time | additive |

_The fold is read from the framework registry (`MeasureType.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships

*1 join(s) out · 0 in — click a concept to open it.*

**Joins to** — this concept references:

- [Order Line](order_line.md) — joined on `Quantity`

## Source of record
- Full MAC concept: `net_sales_amount.yaml` — open the **YAML** tab for the complete typed definition.