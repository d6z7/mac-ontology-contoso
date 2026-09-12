---
type: Enum
title: Brand
description: The set of 11 Contoso house brands a product belongs to (product.Brand).
tags:
- CONTOSO
- enumeration
- confidence:C
resource: table://product
---

The set of 11 Contoso house brands a product belongs to (product.Brand). A closed set — a twelfth would be a portfolio change, not an undocumented value.

## Details

- **Identity** — code
- **Version** — 0.1
- **Schema version** — 0.1.9
- **Status** — draft
- **Owner** — demo-team
- **Governance owner** — demo-team
- **Last reviewed** — 2026-07-19

## Grounded in

- `product` — key `ProductKey`

## Grain
the Brand column of product (11 brands)

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `Brand` | — | `product` |  |  |

## Source of record
- Full MAC concept: `brand.yaml` — open the **YAML** tab for the complete typed definition.