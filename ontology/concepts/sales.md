---
type: Metric
title: Sales (net revenue)
description: The monetary value of sales order lines.
tags:
- CONTOSO
- measure
- confidence:C
resource: table://sales
rule_pages:
- rules/sales.net_of_discount.md
- rules/sales.single_currency_basis.md
- rules/sales.ask_currency_when_ambiguous.md
- rules/sales.no_double_count_header_detail.md
---

The monetary value of sales order lines. Each line carries a list price (UnitPrice) and a post-discount price (NetPrice) in the store's local CurrencyCode, plus an ExchangeRate to the reporting base currency. "Sales" without qualification means NET revenue (Quantity x NetPrice) converted to the base currency; GROSS (Quantity x UnitPrice) is reported only when asked. The grain is one order line; the denormalized `sales` table is the same facts as orders x orderrows.

## Details

- **Identity** — code
- **Version** — 0.1
- **Schema version** — 0.1.9
- **Status** — draft
- **Owner** — demo-team
- **Governance owner** — demo-team
- **Last reviewed** — 2026-07-19

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
Everything needed to answer "total sales" is here. Use NET sales (Quantity x NetPrice) converted to the base currency via ExchangeRate (rule net_sales_base_currency). Never SUM(NetPrice) across mixed currencies, never sum `sales` and orderrows together, and disclose the currency basis and gross/net choice. Wanting to probe the warehouse to settle these means this concept is incomplete — fix it here.
```

## Grounded in

- `sales` — key `['OrderKey', 'LineNumber']`

## Grain
one sales order line

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `Quantity` | — | `sales` |  |  |
| `UnitPrice` | — | `sales` |  |  |
| `NetPrice` | — | `sales` |  |  |
| `UnitCost` | — | `sales` |  |  |
| `CurrencyCode` | — | `sales` |  |  |
| `ExchangeRate` | — | `sales` |  |  |
| `StoreKey` | — | `sales` |  | [Store](store.md) |
| `ProductKey` | — | `sales` |  | [Product](product.md) |

## Relationships

*2 join(s) out · 0 in — click a concept to open it.*

**Joins to** — this concept references:

- [Product](product.md) — joined on `ProductKey`
- [Store](store.md) — joined on `StoreKey`

## Source of record
- Full MAC concept: `sales.yaml` — open the **YAML** tab for the complete typed definition.