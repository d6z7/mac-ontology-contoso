---
type: Concept
title: ExchangeRate
description: 'What one currency was worth in another on one day: a quoted rate over a date and an ordered pair of currencies.'
tags:
- Contoso 5
- concept
resource: table://v_contoso5_fx_rate
rule_pages:
- ../rules/Currency.whose.md
- ../rules/ExchangeRate.convert_per_day.md
- ../rules/ExchangeRate.direction_is_part_of_the_key.md
- ../rules/Order.rate_on_order_date.md
---

What one currency was worth in another on one day: a quoted rate over a date and an ordered pair of currencies. The account is pages/knowledge/exchange_rate.md.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`v_contoso5_fx_rate`](../../data/datasets/v_contoso5_fx_rate.md)
- **Counts** — `date_day`, `from_currency`, `to_currency` (no `counts`: the dataset key)
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*4 rule(s) are about this concept, 4 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Currency.whose](../rules/Currency.whose.md) — **proposed** · names it · choice over `paid_in`, `rate_source`, `rate_target` — default `paid_in` — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- [ExchangeRate.convert_per_day](../rules/ExchangeRate.convert_per_day.md) — **proposed** · parent · implemented by `law.L2` = `dataset:v_contoso5_fx_rate`, `dataset:v_contoso5_fx_rate.rate` = `measure` — An amount is converted at its own day's rate, never at a rate averaged over a period. A rate is not a quantity to add up: over time it can at most be averaged, and across currency pairs it is not combined at all.
- [ExchangeRate.direction_is_part_of_the_key](../rules/ExchangeRate.direction_is_part_of_the_key.md) — **proposed** · parent · implemented by `dataset:v_contoso5_fx_rate.to_currency` = `dimension` — An exchange rate's target currency means something only together with its source currency: the direction is part of the rate's identity, so a rate is never picked or grouped by its target currency alone.
- [Order.rate_on_order_date](../rules/Order.rate_on_order_date.md) — **proposed** · names it · implemented by `law.L0` = `dataset:v_contoso5_fx_rate`, `dataset:v_contoso5_fx_rate.to_currency` = `dimension`, `dataset:v_contoso5_fx_rate.date_day` = `date`, `dataset:v_contoso5_fx_rate.from_currency` = `dimension` — An amount is converted at the exchange rate of the order's own day. A rate is identified by its day and both of its currencies together; a target currency alone does not pick a rate.

**Words**

*25 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| Exchange Rate | `concept:ExchangeRate` | binds | — | — | — |
| date | `dataset:v_contoso5_fx_rate.date_day` | binds | — | — | — |
| day | `dataset:v_contoso5_fx_rate.date_day` | binds | — | — | — |
| rate date | `dataset:v_contoso5_fx_rate.date_day` | binds | — | — | — |
| convert from | `dataset:v_contoso5_fx_rate.from_currency` | binds | — | — | — |
| from | `dataset:v_contoso5_fx_rate.from_currency` | binds | — | — | — |
| source currency | `dataset:v_contoso5_fx_rate.from_currency` | binds | — | — | — |
| conversion rate | `dataset:v_contoso5_fx_rate.rate` | binds | — | — | — |
| exchange rate | `dataset:v_contoso5_fx_rate.rate` | binds | — | — | — |
| fx rate | `dataset:v_contoso5_fx_rate.rate` | binds | — | — | — |
| convert into | `dataset:v_contoso5_fx_rate.to_currency` | binds | — | — | — |
| target currency | `dataset:v_contoso5_fx_rate.to_currency` | binds | — | — | — |
| to | `dataset:v_contoso5_fx_rate.to_currency` | binds | — | — | — |
| additivity | `rule:ExchangeRate.convert_per_day` | finds | — | — | — |
| average rate | `rule:ExchangeRate.convert_per_day` | finds | — | — | — |
| conversion | `rule:ExchangeRate.convert_per_day` | finds | — | — | — |
| daily rate | `rule:ExchangeRate.convert_per_day` | finds | — | — | — |
| exchange rate | `rule:ExchangeRate.convert_per_day` | finds | — | — | — |
| fx | `rule:ExchangeRate.convert_per_day` | finds | — | — | — |
| currency | `rule:ExchangeRate.direction_is_part_of_the_key` | finds | — | — | — |
| direction | `rule:ExchangeRate.direction_is_part_of_the_key` | finds | — | — | — |
| exchange rate | `rule:ExchangeRate.direction_is_part_of_the_key` | finds | — | — | — |
| from currency | `rule:ExchangeRate.direction_is_part_of_the_key` | finds | — | — | — |
| fx | `rule:ExchangeRate.direction_is_part_of_the_key` | finds | — | — | — |
| to currency | `rule:ExchangeRate.direction_is_part_of_the_key` | finds | — | — | — |

## Grounded in

- [`v_contoso5_fx_rate`](../../data/datasets/v_contoso5_fx_rate.md) — served as `"contoso_served"."v_contoso5_fx_rate"`

## Grain

- One row of `v_contoso5_fx_rate` is identified by `date_day`, `from_currency`, `to_currency` (the dataset key).
- One ExchangeRate is one row — no `counts`, so the instance is the dataset key.

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `date_day` | date | — | — | — | — | the day the rate held. | ← [Order](Order.md) via `order__converts_at__exchange_rate` |
| `from_currency` | dimension | — | — | — | [`dim_currency`](../../data/datasets/dim_currency.md).`currency_code` via `exchange_rate__quotes_from__currency` | the currency being converted FROM. Every currency appears as a source, so the view is a full matrix of currency pairs and not a USD-only lookup. | [Currency](Currency.md) via `exchange_rate__quotes_from__currency`, ← [Order](Order.md) via `order__converts_at__exchange_rate` |
| `to_currency` | dimension | — | — | — | [`dim_currency`](../../data/datasets/dim_currency.md).`currency_code` via `exchange_rate__quotes_to__currency` | the currency being converted TO. | [Currency](Currency.md) via `exchange_rate__quotes_to__currency`, ← [Order](Order.md) via `order__converts_at__exchange_rate` |
| `rate` | measure | — | rate · to-currency per from-currency · over_time `average` | — | — | what one unit of `from_currency` was worth in `to_currency` on `date_day`. Same-currency pairs are present and are exactly 1. THE AMOUNTS ON A SALES LINE ARE ALREADY USD, so converting them with this is how a figure silently becomes the wrong currency. | — |

_Declared per column, over 4 served columns: is 4 of 4 · label 0 of 4 · measure 1 of 4 · names 0 of 4 · value set 2 of 4 · means 4 of 4 · joins → 3 of 4. An em dash is a column for which nothing is declared._

## Axes

Measure `rate`: quantity `rate` · average: `weighted_by`, or `plain_mean` (disclosed); else refused; a total = Σ(rate × `weighted_by`).

| axis | axis kind | fold `rate` |
|---|---|---|
| `date_day` | date | never (`over_time: average` allowed) |
| `from_currency` | dimension | never |
| `to_currency` | dimension | never |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

*2 edge(s) out · 1 in — the only joins (L7), walked in both directions.*

**Joins to** — edges from this concept:

- [Currency](Currency.md) — `exchange_rate__quotes_from__currency` on `from_currency` = `currency_code`
- [Currency](Currency.md) — `exchange_rate__quotes_to__currency` on `to_currency` = `currency_code`

**Joined from** — edges into this concept:

- [Order](Order.md) — `order__converts_at__exchange_rate` on `date_day` = `order_date`, `to_currency` = `currency_code`, `from_currency` = `unit_currency`

## Source of record

- Declaration: `ontology/concepts/ExchangeRate.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/ExchangeRate.md`](../../../ontology/concepts/ExchangeRate.md) — the authored account (X-3); this page cites it and never writes it.
