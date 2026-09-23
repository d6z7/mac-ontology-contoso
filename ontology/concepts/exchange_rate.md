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

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `Date` | date | key | `v_contoso_fx_rate_day` | DATE since 2026-09-19, cast in the transform from the landing's TIMESTAMP on the operator's ruling; lossless and measured, not assumed — 0 non-midnight over 100 450 of 100 450 rows immediately before the cast. main.currencyexchange keeps TIMESTAMP. THE CONVERSION JOIN CROSSES THIS COLUMN: rules.yaml#order_line_usd_conversion matches it to v_contoso_order_line.OrderDate on exact equality, and both sides were cast in the same change. Re-measured after, identical: 223 974 join rows over 223 974 lines, 0 lines without a quote, min 1 / max 1 quotes per line, sum(Quantity * NetPrice * Exchange) = 223 597 710.61. | — |
| `FromCurrency` | varchar | key | `v_contoso_fx_rate_day` | 5 measured values. | [Currency](currency.md) _(business)_ |
| `ToCurrency` | varchar | key | `v_contoso_fx_rate_day` | 5 measured values. | [Currency](currency.md) _(business)_ |
| `Exchange` | decimal(20,5) | measure | `v_contoso_fx_rate_day` | the rate; exactly 1 on all 20 090 self-pairs (P1 V11), > 0 on every row (P1 V1). NOT additive — its additivity class is P8's to register. | — |

_Declared per column, over 4 columns: description 4 of 4 · type 4 of 4 · joins → 2 of 4. An em dash is a column for which nothing is declared._

## Axes

Measure type: `Precomputed` — `mac.MeasureType.Precomputed`.

| axis | axis kind | fold |
|---|---|---|
| `currency_pair` | categorical | none |
| `time` | time | none |

_The fold is read from the framework registry (`MeasureType.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships

*2 join(s) out · 1 in — click a concept to open it.*

**Joins to** — this concept references:

- [Currency](currency.md) — joined on `FromCurrency`
- [Currency](currency.md) — joined on `ToCurrency`

**Referenced by** — these point at this concept:

- [Order Line](order_line.md) — on `?`

## Source of record
- Full MAC concept: `exchange_rate.yaml` — open the **YAML** tab for the complete typed definition.