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

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `OrderKey` | key | `v_contoso_order_line` |  |  |
| `RowNumber` | key | `v_contoso_order_line` |  |  |
| `Quantity` | measure | `v_contoso_order_line` |  |  |
| `NetPrice` | measure | `v_contoso_order_line` |  |  |
| `CurrencyCode` | dimension | `v_contoso_order_line` |  |  |
| `OrderDate` | dimension | `v_contoso_order_line` |  |  |

## Source of record
- Full MAC concept: `net_sales_amount.yaml` — open the **YAML** tab for the complete typed definition.