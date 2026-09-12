---
type: Metric
title: Gross profit (gross margin)
description: 'GROSS PROFIT: net revenue minus cost of goods, per order line, converted to the reporting base currency and summed — Quantity x (NetPrice - UnitCost) x ExchangeRate.'
tags:
- CONTOSO
- measure
- confidence:C
resource: table://sales
rule_pages:
- rules/margin.gross_basis_disclosed.md
- rules/margin.net_revenue_side.md
- rules/margin.single_currency_basis.md
---

GROSS PROFIT: net revenue minus cost of goods, per order line, converted to the reporting base currency and summed — Quantity x (NetPrice - UnitCost) x ExchangeRate. Revenue is taken NET of discount (consistent with Sales); cost is the per-unit cost of goods (UnitCost = COGS). Only cost of goods is subtracted, so this is GROSS profit / gross margin — operating, logistics and overhead costs are NOT in the data and NOT modelled. "Margin %" is this value over net sales, but the headline measure is the currency amount.

## Details

- **Identity** — code
- **Version** — 0.1
- **Schema version** — 0.1.9
- **Status** — draft
- **Owner** — demo-team
- **Governance owner** — demo-team
- **Last reviewed** — 2026-07-19

## Grounded in

- `sales` — key `['OrderKey', 'LineNumber']`

## Grain
one sales order line

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `Quantity` | — | `sales` |  |  |
| `NetPrice` | — | `sales` |  |  |
| `UnitCost` | — | `sales` |  |  |
| `ExchangeRate` | — | `sales` |  |  |
| `CurrencyCode` | — | `sales` |  |  |

## Source of record
- Full MAC concept: `margin.yaml` — open the **YAML** tab for the complete typed definition.