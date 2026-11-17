---
type: Dataset
title: dim_currency
description: dataset dim_currency
relation: dim_currency
tags:
- Contoso 5
- dataset
- value set
---

- **Served as** — `"contoso_served"."dim_currency"`
- **Key** — `currency_code`
- **Made by** — [dim_currency](../transforms/dim_currency.md)
- **Members** — its rows are the members of a value set: —
- **Trust** — authored

## Columns

| column | is | key | label | measure | names | other | means |
|---|---|---|---|---|---|---|---|
| `currency_code` | dimension | PK | — | — | — | — | the currency's code. Five are used across the sales: USD, EUR, GBP, CAD, AUD. |

## Checks

_This dataset declares no checks._

## Value sets

- ← [`v_contoso5_fx_rate`](v_contoso5_fx_rate.md).`from_currency` links to `currency_code` via edge `exchange_rate__quotes_from__currency`
- ← [`v_contoso5_fx_rate`](v_contoso5_fx_rate.md).`to_currency` links to `currency_code` via edge `exchange_rate__quotes_to__currency`
- ← [`v_contoso5_sales_line`](v_contoso5_sales_line.md).`currency_code` links to `currency_code` via edge `order__paid_in__currency`

## What a question may do

_What each column's kind (`is:`) lets a question do — the L1 kind table (`mac_vocabulary.yaml#law.terms.L1`), read per column; nothing here is declared on the column itself._

| column | is | group | filter | add | count distinct | min/max | words | shown |
|---|---|---|---|---|---|---|---|---|
| `currency_code` | `dimension` | yes (unnests `many`) | member, pattern; threshold if ordinal | — | yes | if ordinal | values + lexicon | yes |

## Bound by

*1 concept(s) take rows from this dataset — a change to a column's declaration reaches every one of them.*

- [Currency](../../ontology/concepts/Currency.md) — serves `currency_code`

## Findings

_No finding is filed under this dataset._
