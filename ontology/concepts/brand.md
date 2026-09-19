---
type: Grouping
title: Brand
description: 'The brand a product is sold under: 11 members over 2 517 products, held as a column of the product dimension.'
tags:
- CONTOSO
- grouping
- confidence:I
resource: table://dim_contoso_product
rule_pages:
- rules/brand.axis.orthogonal_to_category.md
---

The brand a product is sold under: 11 members over 2 517 products, held as a column of the product dimension. This is the axis the bundle's "by brand" question groups by.
IT IS NOT A MANUFACTURER. The two are 1:1 in this delivery (measured, 0 brands carrying two manufacturers) but they are different notions and the coincidence is not declared to be law — 'Contoso' the brand against 'Contoso, Ltd' the manufacturer. Manufacturer is served as a display attribute of the product, not as a second grouping.
IT IS NOT A PRODUCT LINE OR A CATEGORY EITHER. Brands cut ACROSS the category hierarchy: a brand's products appear in several categories and a category's products in several brands, so brand and category are two orthogonal axes and neither rolls up into the other.

## Details

- **Identity** — code
- **Version** — 1.0
- **Schema version** — 0.1.14
- **Status** — draft
- **Owner** — operator
- **Governance owner** — operator
- **Last reviewed** — 2026-09-18

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
All 11 members, their product counts and their manufacturers are enumerated above and in data/lookups/contoso_brand.lookup.csv, cut from the served plane with a search key per member — so a brand word resolves offline and a brand the delivery does not carry is a refusal derived from a closed member list rather than from an empty query. Membership needs no probe either: it is the product row's own column.
```

## Grounded in

- `dim_contoso_product` — key `ProductKey`

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `ProductKey` | key | `dim_contoso_product` (key) |  |  |
| `Brand` | dimension | `dim_contoso_product` |  |  |
| `Manufacturer` | attribute | `dim_contoso_product` |  |  |

## Relationships

*0 join(s) out · 0 in — click a concept to open it.*

**Groups** → **Product** — the leaf concept this rolls up.

## Source of record
- Full MAC concept: `brand.yaml` — open the **YAML** tab for the complete typed definition.