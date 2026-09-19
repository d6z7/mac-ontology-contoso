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

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `OrderKey` | key | `v_contoso_order_line` |  |  |
| `RowNumber` | key | `v_contoso_order_line` |  |  |
| `OrderDate` | dimension | `v_contoso_order_line` |  | [Calendar Day](calendar_day.md) |
| `DeliveryDate` | dimension | `v_contoso_order_line` |  | [Calendar Day](calendar_day.md) |
| `CustomerKey` | key | `v_contoso_order_line` |  | [Customer](customer.md) |
| `StoreKey` | key | `v_contoso_order_line` |  | [Store](store.md) |
| `ProductKey` | key | `v_contoso_order_line` |  | [Product](product.md) |
| `CurrencyCode` | dimension | `v_contoso_order_line` |  |  |
| `Quantity` | measure | `v_contoso_order_line` |  |  |
| `UnitPrice` | measure | `v_contoso_order_line` |  |  |
| `NetPrice` | measure | `v_contoso_order_line` |  |  |
| `UnitCost` | measure | `v_contoso_order_line` |  |  |

## Relationships

*6 join(s) out · 0 in — click a concept to open it.*

**Joins to** — this concept references:

- [Calendar Day](calendar_day.md) — joined on `DeliveryDate`
- [Calendar Day](calendar_day.md) — joined on `OrderDate`
- [Customer](customer.md) — joined on `CustomerKey`
- [Exchange Rate](exchange_rate.md) — joined on `?`
- [Product](product.md) — joined on `ProductKey`
- [Store](store.md) — joined on `StoreKey`

## Source of record
- Full MAC concept: `order_line.yaml` — open the **YAML** tab for the complete typed definition.