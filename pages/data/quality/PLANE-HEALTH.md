---
type: Doc
title: Plane health — chain, lineage & trust
description: Chain integrity, lineage coverage and trust
tags:
- Contoso 5
- plane-health
---

The structural health of this bundle's data plane, read from the same declarations the gates read. **The gates remain authoritative**; this page is a read view.

## Chain — `source → transform → dataset → concept`

| link | count |
|---|---|
| sources | 8 |
| transforms | 21 |
| datasets | 21 (8 served, 13 kept as files) |
| concepts | 11 |

✅ every served dataset is produced by a transform.

## Lineage coverage

| transform | covered | of | coverage |
|---|---|---|---|
| `contoso_served.contoso5_brand` | 1 | 1 | 100% |
| `contoso_served.contoso5_category_name` | 1 | 1 | 100% |
| `contoso_served.contoso5_channel` | 1 | 1 | 100% |
| `contoso_served.contoso5_color` | 1 | 1 | 100% |
| `contoso_served.contoso5_continent` | 1 | 1 | 100% |
| `contoso_served.contoso5_country_code` | 2 | 2 | 100% |
| `contoso_served.contoso5_currency` | 1 | 1 | 100% |
| `contoso_served.contoso5_gender` | 1 | 1 | 100% |
| `contoso_served.contoso5_manufacturer` | 1 | 1 | 100% |
| `contoso_served.contoso5_state` | 1 | 1 | 100% |
| `contoso_served.contoso5_status` | 1 | 1 | 100% |
| `contoso_served.contoso5_store_name` | 1 | 1 | 100% |
| `contoso_served.contoso5_sub_category_name` | 1 | 1 | 100% |
| `contoso_served.dim_country` | 2 | 2 | 100% |
| `contoso_served.dim_currency` | 1 | 1 | 100% |
| `contoso_served.dim_customer` | 9 | 10 | 90% |
| `contoso_served.dim_location` | 4 | 5 | 80% |
| `contoso_served.dim_product` | 10 | 10 | 100% |
| `contoso_served.dim_store` | 8 | 9 | 89% |
| `contoso_served.v_contoso5_fx_rate` | 4 | 4 | 100% |
| `contoso_served.v_contoso5_sales_line` | 13 | 19 | 68% |

## Change protocol — authored vs generated

| layer | authored | generated |
|---|---:|---:|
| sources | 8 | 0 |
| transforms | 21 | 0 |
| datasets | 21 | 0 |
| concepts | 11 | 0 |
| rules | 38 | 1 |

_`generated: true` marks a file a tool harvested — the weakest trust, disclosed when an answer touches it (L14); absent = authored._
