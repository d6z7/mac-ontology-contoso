---
type: Entity
title: Order
description: An order header (one row per OrderKey in `orders`), whose detail lines live in `orderrows`.
tags:
- CONTOSO
- entity
- confidence:C
resource: table://orders
---

An order header (one row per OrderKey in `orders`), whose detail lines live in `orderrows`. The denormalized `sales` table is `orders` joined to `orderrows` — the SAME facts in two shapes, which is why sales must be summed from one form or the other, never both (see Sales > sales.no_double_count_header_detail).

## Details

- **Identity** — code
- **Version** — 0.1
- **Schema version** — 0.1.9
- **Status** — draft
- **Owner** — demo-team
- **Governance owner** — demo-team
- **Last reviewed** — 2026-07-19

## Grounded in

- `orders` — key `OrderKey`

## Grain
one row per order header

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `CustomerKey` | — | `orders` |  |  |
| `StoreKey` | — | `orders` |  |  |
| `DT` | — | `orders` |  |  |
| `DeliveryDate` | — | `orders` |  |  |
| `CurrencyCode` | — | `orders` |  |  |

## Source of record
- Full MAC concept: `order.yaml` — open the **YAML** tab for the complete typed definition.