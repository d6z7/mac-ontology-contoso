---
type: Grouping
title: Continent
description: 'The continent a country belongs to: the top of the bundle''s declared country-to-continent roll-up.'
tags:
- CONTOSO
- grouping
- confidence:I
resource: table://dim_contoso_customer
rule_pages:
- rules/continent.side.customer_only.md
---

The continent a country belongs to: the top of the bundle's declared country-to-continent roll-up. Three members over eight countries, and the map is a FUNCTION — measured, 0 countries carrying two continents.
IT IS NOT A GEOGRAPHY OF STORES. The store dimension has no continent column at all, so this roll-up exists only on the customer side. A question asking for sales by continent is answered through the customer, and a store-side continent figure is not available — a refusal with a reason, not an empty result.
IT IS ALSO NOT A COMPLETE WORLD. 'Australia' here is the continent a single country (AU) sits in, and the three members are only the continents the eight delivered countries reach. Asia, Africa and South America are absent because no customer is in them, which is a coverage fact rather than a modelling one.

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
The three members and their country lists are enumerated above; the same map is in data/lookups/contoso_country.lookup.csv, which carries the continent alongside each country code, so a continent word resolves offline and so does the roll-up from a country. Nothing here needs a probe, and a continent the delivery does not reach is a refusal derived from a closed member list.
```

## Grounded in

- `dim_contoso_customer` — key `CustomerKey`

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `CustomerKey` | integer | key | `dim_contoso_customer` (key) | — | — |
| `Continent` | varchar | dimension | `dim_contoso_customer` | 3 measured values; the only continent column in the delivery (S10/S11). | — |
| `Country` | varchar | dimension | `dim_contoso_customer` | 8 measured values; covers every store country except the sentinel '--' (S11, S12). | — |

_Declared per column, over 3 columns: description 2 of 3 · type 3 of 3 · joins → 0 of 3. An em dash is a column for which nothing is declared._

## Relationships

*0 join(s) out · 0 in — click a concept to open it.*

**Groups** → **Country** — the leaf concept this rolls up.

## Source of record
- Full MAC concept: `continent.yaml` — open the **YAML** tab for the complete typed definition.