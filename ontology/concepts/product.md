---
type: Entity
title: Product
description: 'A thing Contoso sells, at the level the shelf knows it: a SKU.'
tags:
- CONTOSO5
- entity
- confidence:I
---

A thing Contoso sells, at the level the shelf knows it: a SKU. The account is knowledge/product.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.3.1-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-29

## How to answer

_No content available — the bundle declares nothing for this section._

## Grounded in

- `dim_product` — key `product_key` — semantics: [`ontology/relations/dim_product.yaml`](../relations/dim_product.md)

## Grain

- One row is one Product, identified by `product_key`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `product_key` | integer | key | -> Product | — | — | — | — | — |
| `product_code` | string | dimension | — | — | label_of `product_key` (code) | — | — | — |
| `product_name` | string | dimension | — | — | label_of `product_key` (common) | — | — | — |
| `manufacturer` | string | dimension | — | — | label_of `brand` (legal) | — | — | — |
| `brand` | string | dimension | — | — | — | — | — | — |
| `color` | string | dimension | — | — | — | — | — | — |
| `category_name` | string | dimension | — | — | — | — | — | — |
| `sub_category_name` | string | dimension | — | — | finer_than `category_name` | — | — | — |

_Declared per column, over 8 columns: type 8 of 8 · role 8 of 8 · identity 1 of 8 · measure 0 of 8 · rulings 4 of 8 · register 0 of 8 · description 0 of 8 · joins → 0 of 8. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind | fold |
|---|---|---|
| `brand` | categorical | — |
| `category_name` | categorical | — |
| `color` | categorical | — |
| `manufacturer` | categorical | — |
| `product_code` | categorical | — |
| `product_name` | categorical | — |
| `sub_category_name` | categorical | — |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*3 join(s) out · 1 in — click a concept to open it.*

**Joins to** — this concept references:

- [Brand](brand.md) — joined on `?`
- [Colour](color.md) — joined on `?`
- [Product Category](product_category.md) — joined on `?`

**Referenced by** — these point at this concept:

- [Order](order.md) — on `product_key`

## Source of record

- Full MAC concept: `product.yaml` — open the **YAML** tab for the complete typed definition.
- Source table: [product](../../data/sources/product.md)
