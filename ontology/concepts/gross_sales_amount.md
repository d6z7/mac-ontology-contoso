---
type: Metric
title: Gross Sales Amount
description: 'The money value of sales BEFORE discount: per order line, Quantity x UnitPrice, summed over the lines in scope.'
tags:
- CONTOSO
- measure
- confidence:I
resource: table://v_contoso_order_line
rule_pages:
- rules/gross_sales_amount.derivation.quantity_times_unit_price.md
---

The money value of sales BEFORE discount: per order line, Quantity x UnitPrice, summed over the lines in scope. This is the LIST-PRICE reading of "total sales".
IT IS NOT THE FIGURE THE BUSINESS REPORTS. The discount is real and large — NetPrice is strictly below UnitPrice on 136 913 of 223 974 lines — so gross overstates the received amount on 61 % of the fact. Ask for it explicitly; a bare "total sales" resolves to NetSalesAmount.
IT IS ALSO NOT A CROSS-CURRENCY FIGURE. Every amount is denominated in the order's own CurrencyCode, so a figure summed over more than one currency is only defined once a conversion direction has been stated.

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
Quantity and UnitPrice are columns of v_contoso_order_line, declared above; the fold along each axis is resolved from measure_type x axis_kinds; the currency of the figure is the row's own CurrencyCode. Names on the axes resolve through the registers the axis concepts declare — Brand, ProductCategory, ProductSubcategory, Product, Country, Continent, GeoArea, Store, Customer — so no warehouse probe is needed to turn a word into a code.
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
| `UnitPrice` | measure | `v_contoso_order_line` |  |  |
| `CurrencyCode` | dimension | `v_contoso_order_line` |  |  |
| `OrderDate` | dimension | `v_contoso_order_line` |  |  |

## Source of record
- Full MAC concept: `gross_sales_amount.yaml` — open the **YAML** tab for the complete typed definition.