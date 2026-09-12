---
type: Reference
title: Product
description: A sellable item in the Contoso catalogue, identified by ProductKey (ProductCode is the business code).
tags:
- CONTOSO
- reference
- confidence:C
resource: table://product
---

A sellable item in the Contoso catalogue, identified by ProductKey (ProductCode is the business code). Every product belongs to exactly one Brand and one Category -> SubCategory. Order lines reference products so sales can be sliced by product, brand, or category.

## Details

- **Identity** — fk_name
- **Version** — 0.1
- **Schema version** — 0.1.9
- **Status** — draft
- **Owner** — demo-team
- **Governance owner** — demo-team
- **Last reviewed** — 2026-07-19

## Grounded in

- `product` — key `ProductKey`

## Grain
one row per product

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `ProductCode` | — | `product` |  |  |
| `ProductName` | — | `product` |  |  |
| `Brand` | — | `product` |  |  |
| `CategoryName` | — | `product` |  |  |
| `SubCategoryName` | — | `product` |  |  |
| `Price` | — | `product` |  |  |

## Relationships

*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Sales (net revenue)](sales.md) — on `ProductKey`

## Source of record
- Full MAC concept: `product.yaml` — open the **YAML** tab for the complete typed definition.