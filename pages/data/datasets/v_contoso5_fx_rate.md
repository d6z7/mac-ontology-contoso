---
type: Dataset
title: v_contoso5_fx_rate
description: dataset v_contoso5_fx_rate
relation: v_contoso5_fx_rate
tags:
- Contoso 5
- dataset
---

- **Served as** — `"contoso_served"."v_contoso5_fx_rate"`
- **Key** — `date_day`, `from_currency`, `to_currency`
- **Made by** — [v_contoso5_fx_rate](../transforms/v_contoso5_fx_rate.md)
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `date_day` | date | PK1 | — | — | — | — | the day the rate held. |
| `from_currency` | dimension | PK2 | — | — | — | — | the currency being converted FROM. Every currency appears as a source, so the view is a full matrix of currency pairs and not a USD-only lookup. |
| `to_currency` | dimension | PK3 | — | — | — | within=`from_currency` | the currency being converted TO. |
| `rate` | measure | — | — | rate · to-currency per from-currency · over_time `average` · plain mean | — | — | what one unit of `from_currency` was worth in `to_currency` on `date_day`. Same-currency pairs are present and are exactly 1. THE AMOUNTS ON A SALES LINE ARE ALREADY USD, so converting them with this is how a figure silently becomes the wrong currency. ITS AVERAGE IS THE PLAIN MEAN OF THE DAILY RATES, disclosed — one rate per day and ordered pair, the European Central Bank euro reference rate crossed through EUR, a day without a quote carrying the last quoted day's rate, and no traded volume behind any rate to weight it by (evidence in ontology/concepts/ExchangeRate.md, "How the rate averages"). An amount is still converted at its own day's rate, never at an averaged one (rule ExchangeRate.convert_per_day). |

## Checks

_This dataset declares no checks._

## Value sets

- `from_currency` → value set [`dim_currency`](dim_currency.md).`currency_code` via edge `exchange_rate__quotes_from__currency`
- `to_currency` → value set [`dim_currency`](dim_currency.md).`currency_code` via edge `exchange_rate__quotes_to__currency`

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `date_day` | `date` | grains | period | — | yes | yes | calendar words | yes |
| `from_currency` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `to_currency` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |
| `rate` | `measure` | — | threshold | L2 | — | yes | lexicon | yes |

## Bound by

*1 concept(s) take rows from this dataset — a change to a column's declaration reaches every one of them.*

- [ExchangeRate](../../ontology/concepts/ExchangeRate.md) — serves `date_day`, `from_currency`, `to_currency`, `rate`

## Findings

- [DQ-AMBIGREF-CURRENCYCODE](../quality/DQ-AMBIGREF-CURRENCYCODE.md) — high · open — nobody has ruled — `CurrencyCode` includes perfectly into 2 different keys — which is THE reference?
