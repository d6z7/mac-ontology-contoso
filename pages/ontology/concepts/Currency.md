---
type: Concept
title: Currency
description: 'The money a sale is denominated in: five ISO codes, pointed at by every sale and by both ends of every exchange rate.'
tags:
- Contoso 5
- concept
resource: table://dim_currency
rule_pages:
- ../rules/Currency.code_is_not_the_unit.md
- ../rules/Currency.whose.md
- ../rules/ExchangeRate.direction_is_part_of_the_key.md
---

The money a sale is denominated in: five ISO codes, pointed at by every sale and by both ends of every exchange rate. The account is ontology/concepts/Currency.md.

## Details

- **Label** — none declared (the spaced name is shown)
- **Table** — [`dim_currency`](../../data/datasets/dim_currency.md)
- **Counts** — `currency_code` (no `counts`: the dataset key)
- **Where** — every row of the table (no `where`)
- **Trust** — authored

## How to answer

*3 rule(s) are about this concept, 3 of them act (only `proposed` and `ruled` rules act, L3). Each rule's full text is its own page.*

- [Currency.code_is_not_the_unit](../rules/Currency.code_is_not_the_unit.md) — **proposed** · parent · prose — not enforced (owner operator) — Every amount on a sale is in US dollars. A sale's currency is the currency the customer transacted in, not the unit of its amounts: filtering by that currency does not turn the amounts into it. Sales asked for in a named currency are converted through the exchange rate.
- [Currency.whose](../rules/Currency.whose.md) — **proposed** · parent · choice over `paid_in`, `rate_source`, `rate_target` — default `paid_in` — A currency is reached by three routes: the currency a sale was paid in, or one of the two currencies of an exchange rate — its source (the currency it converts from; for a sale, the currency the amounts are stored in) or its target (the currency it converts to; for a sale, the sale's own currency). A question that reaches a currency without saying which — from a sale, a store, a site or an exchange rate — is answered on the currency the sale was paid in; a question may name the rate's source or target currency instead. The answer says which currency it used.
- [ExchangeRate.direction_is_part_of_the_key](../rules/ExchangeRate.direction_is_part_of_the_key.md) — **proposed** · names it · implemented by `dataset:v_contoso5_fx_rate.to_currency` = `dimension` — An exchange rate's target currency means something only together with its source currency: the direction is part of the rate's identity, so a rate is never picked or grouped by its target currency alone.

**Words**

*8 lexicon row(s) — the only home of words (L-1); several `binds` rows for one word take the `default` row, else ASK (L8).*

| word | address | use | value | scope | language |
|---|---|---|---|---|---|
| currency | `dataset:dim_currency.currency_code` | binds | — | — | — |
| amounts | `rule:Currency.code_is_not_the_unit` | finds | — | — | — |
| convert | `rule:Currency.code_is_not_the_unit` | finds | — | — | — |
| currency | `rule:Currency.code_is_not_the_unit` | finds | — | — | — |
| dollars | `rule:Currency.code_is_not_the_unit` | finds | — | — | — |
| euros | `rule:Currency.code_is_not_the_unit` | finds | — | — | — |
| transaction currency | `rule:Currency.code_is_not_the_unit` | finds | — | — | — |
| usd | `rule:Currency.code_is_not_the_unit` | finds | — | — | — |

## Grounded in

- [`dim_currency`](../../data/datasets/dim_currency.md) — served as `"contoso_served"."dim_currency"`
- Its rows are the members of a value set: —.

## Grain

- One row of `dim_currency` is identified by `currency_code` (the dataset key).
- One Currency is one row — no `counts`, so the instance is the dataset key.

## Fields

| column | is | label | measure | names | value set | means | joins → |
|---|---|---|---|---|---|---|---|
| `currency_code` | dimension | — | — | — | — | the currency's code. Five are used across the sales: USD, EUR, GBP, CAD, AUD. | ← [ExchangeRate](ExchangeRate.md) via `exchange_rate__quotes_from__currency`, ← [ExchangeRate](ExchangeRate.md) via `exchange_rate__quotes_to__currency`, ← [Order](Order.md) via `order__paid_in__currency` |

_Declared per column, over 1 served column: is 1 of 1 · label 0 of 1 · measure 0 of 1 · names 0 of 1 · value set 0 of 1 · means 1 of 1 · joins → 1 of 1. An em dash is a column for which nothing is declared._

## Axes

| axis | axis kind |
|---|---|
| `currency_code` | dimension |

_The fold is read from the framework's L2 table (`law.terms.L2` of the vocabulary, by the measure's `quantity`), not declared on this concept. An em dash means the table leaves the cell empty._

## Relationships

*0 edge(s) out · 3 in — the only joins (L7), walked in both directions.*

**Joined from** — edges into this concept:

- [ExchangeRate](ExchangeRate.md) — `exchange_rate__quotes_from__currency` on `currency_code` = `from_currency`
- [ExchangeRate](ExchangeRate.md) — `exchange_rate__quotes_to__currency` on `currency_code` = `to_currency`
- [Order](Order.md) — `order__paid_in__currency` on `currency_code` = `currency_code`

## Source of record

- Declaration: `ontology/concepts/Currency.yaml` — open the **YAML** tab for the complete typed definition.
- Account: [`ontology/concepts/Currency.md`](../../../ontology/concepts/Currency.md) — the authored account (X-3); this page cites it and never writes it.
