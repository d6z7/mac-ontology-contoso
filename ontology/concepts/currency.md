---
type: Enum
title: Currency
description: The transaction/reporting currencies present in the sales facts.
tags:
- CONTOSO
- enumeration
- confidence:C
resource: table://sales
---

The transaction/reporting currencies present in the sales facts. A sales line's CurrencyCode is the store's local currency. Sales summed across currencies are meaningless unless first converted to a single base currency (via the line's ExchangeRate). See Sales > sales.single_currency_basis.

## Details

- **Identity** — code
- **Version** — 0.1
- **Schema version** — 0.1.9
- **Status** — draft
- **Owner** — demo-team
- **Governance owner** — demo-team
- **Last reviewed** — 2026-07-19

## Grounded in

- `sales` — key `CurrencyCode`

## Grain
the CurrencyCode column of sales (5 currencies)

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `CurrencyCode` | — | `sales` (key) |  |  |

## Source of record
- Full MAC concept: `currency.yaml` — open the **YAML** tab for the complete typed definition.