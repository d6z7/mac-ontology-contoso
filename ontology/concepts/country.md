---
type: Reference
title: Country
description: 'A national market, identified by its two-letter code, in either of the two roles a line carries it in: the country of the CUSTOMER who bought, and the country of the STORE that sold.'
tags:
- CONTOSO
- reference
- confidence:I
resource: table://dim_contoso_customer
rule_pages:
- rules/country.roles.customer_or_store_never_both.md
- rules/country.sentinel.online_is_a_member.md
---

A national market, identified by its two-letter code, in either of the two roles a line carries it in: the country of the CUSTOMER who bought, and the country of the STORE that sold. Eight real countries: AU, CA, DE, FR, GB, IT, NL, US.
THE NINTH STORE VALUE IS NOT A COUNTRY. The 'Online' store version carries CountryCode '--' with CountryName and State both 'Online' — a sales channel sitting in a country column. It is kept as a catalogued member so a store row always resolves, and 93 550 of 223 974 lines point at it, so dropping it would silently remove 41.8 % of the fact. It has no continent because the data states none.
CUSTOMER COUNTRY AND STORE COUNTRY ARE NOT THE SAME AXIS. They are two roles of this one concept and they do not agree: the store side has no continent column at all, and it carries the '--' sentinel the customer side does not. A country breakdown must say whose country it means.

## Details

- **Identity** — iso
- **Version** — 1.0
- **Schema version** — 0.1.14
- **Status** — draft
- **Owner** — operator
- **Governance owner** — operator
- **Last reviewed** — 2026-09-18

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
All nine members and their continents are in data/lookups/contoso_country.lookup.csv, cut from the served plane, carrying both the code and a search key — so a country word resolves offline and the country-to-continent roll-up needs no probe. The long names are in the relations as display columns. A name that does not resolve to one of the nine is a refusal derived from the register, not an empty query.
```

## Grounded in

- `dim_contoso_customer` — key `CustomerKey`
- `dim_contoso_store` — key `StoreKey`

## Grain
one row = one country code, in the dimension that carries it

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `Country` | dimension | `dim_contoso_customer` |  |  |
| `CountryFull` | attribute | `dim_contoso_customer` |  |  |
| `Continent` | — | `dim_contoso_customer` |  |  |
| `CountryCode` | dimension | `dim_contoso_store` |  |  |
| `CountryName` | attribute | `dim_contoso_store` |  |  |

## Source of record
- Full MAC concept: `country.yaml` — open the **YAML** tab for the complete typed definition.