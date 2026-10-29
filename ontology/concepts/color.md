---
type: Enum
title: Colour
description: 'The colour a product comes in — the one attribute that on its own makes a new SKU: "E400 Green" and "E400 Orange" are different products.'
tags:
- CONTOSO5
- enumeration
- confidence:I
---

The colour a product comes in — the one attribute that on its own makes a new SKU: "E400 Green" and "E400 Orange" are different products. The account is knowledge/color.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.3.1-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-30

## How to answer

_No content available — the bundle declares nothing for this section._

## Grounded in

- `dim_product` — key `product_key` — semantics: [`ontology/relations/dim_product.yaml`](../relations/dim_product.md)

## Grain

- One row is one Colour, identified by `product_key`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `color` | string | dimension | — | — | — | — | — | — |
| `product_key` | integer | key | -> Product | — | — | — | — | — |

_Declared per column, over 2 columns: type 2 of 2 · role 2 of 2 · identity 1 of 2 · measure 0 of 2 · rulings 0 of 2 · register 0 of 2 · description 0 of 2 · joins → 0 of 2. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind | fold |
|---|---|---|
| `color` | categorical | — |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Product](product.md) — on `?`

## Source of record

- Full MAC concept: `color.yaml` — open the **YAML** tab for the complete typed definition.
