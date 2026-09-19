---
type: Metric
title: Exchange Rate
description: 'The rate at which one currency converted into another on one calendar day: the number of ToCurrency units per one unit of FromCurrency, quoted per (Date, FromCurrency, ToCurrency).'
tags:
- CONTOSO
- measure
- confidence:I
resource: table://v_contoso_fx_rate_day
rule_pages:
- rules/exchange_rate.direction.usd_base_as_of_order_date.md
- rules/exchange_rate.pair.never_half_a_pair.md
---

The rate at which one currency converted into another on one calendar day: the number of ToCurrency units per one unit of FromCurrency, quoted per (Date, FromCurrency, ToCurrency). Served at its own grain rather than carried on the sales line.
IT IS NOT AN AMOUNT, and it is not additive in any direction. Summing rates across days or across pairs produces a number with no meaning; averaging them is a different, unweighted figure from converting each amount at its own day's rate. It is joined and multiplied, never folded.
IT IS ALSO NOT DIRECTIONLESS. (USD, EUR) and (EUR, USD) are two different rows with two different values, and picking the wrong one inverts every non-USD figure while leaving every USD figure untouched.

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
The quote is read from v_contoso_fx_rate_day at its full composite key; the currency codes resolve through data/lookups/contoso_currency.lookup.csv, whose 5 members are the same 5 measured on both this relation's code columns; the fold is none on both axes, resolved from measure_type x axis_kinds. No probe is needed to discover which pairs exist — the grid is complete by measurement.
```

## Grounded in

- `v_contoso_fx_rate_day` — key `['Date', 'FromCurrency', 'ToCurrency']`

## Grain
one row = one day's quote for one ORDERED currency pair — (Date, FromCurrency, ToCurrency)

## Fields

| column | role | grounded in | description | joins → |
|---|---|---|---|---|
| `Date` | key | `v_contoso_fx_rate_day` |  |  |
| `FromCurrency` | key | `v_contoso_fx_rate_day` |  |  |
| `ToCurrency` | key | `v_contoso_fx_rate_day` |  |  |
| `Exchange` | measure | `v_contoso_fx_rate_day` |  |  |

## Relationships

*0 join(s) out · 1 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `?`

## Source of record
- Full MAC concept: `exchange_rate.yaml` — open the **YAML** tab for the complete typed definition.