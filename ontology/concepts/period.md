---
type: Reference
title: Period
description: 'The WHEN axis of a sale: the order date carried on each `sales` line (OrderDate), with DeliveryDate as a secondary date.'
tags:
- CONTOSO
- reference
- confidence:C
resource: table://sales
---

The WHEN axis of a sale: the order date carried on each `sales` line (OrderDate), with DeliveryDate as a secondary date. Because the date is a native column on the fact, sales can be sliced or grouped by day and rolled up to month, quarter or year without a separate calendar table. "Period" with no stated window means the full available range, disclosed (see measure.period_resolution).

## Details

- **Identity** — code
- **Version** — 0.1
- **Schema version** — 0.1.9
- **Status** — draft
- **Owner** — demo-team
- **Governance owner** — demo-team
- **Last reviewed** — 2026-07-19

## Grounded in

- `sales` — key `OrderDate`

## Grain
one day — rolls up to month / quarter / year

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `OrderDate` | — | `sales` (key) |  |  |
| `DeliveryDate` | — | `sales` |  |  |

## Source of record
- Full MAC concept: `period.yaml` — open the **YAML** tab for the complete typed definition.