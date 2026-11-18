# Currency

The account of concept Currency.

## Overview

The money a sale is denominated in: five ISO codes, pointed at by every sale and by both ends of every exchange rate. Read from the rows: USD on just over half of sales, then EUR, CAD, GBP, AUD. One column, no attributes — a code list. IT NAMES WHAT A SALE CONVERTS TO, NOT WHAT IT IS IN. The amounts on a sale are USD; this code is the customer's currency, and getting there goes through [[ExchangeRate]].

## Identity

ISO 4217 three-letter codes. The standard is the authority, which is why a question saying 'euros' resolves offline.

## Grain

one row per ISO currency code

## Currency.code_is_not_the_unit

nothing in the figure reveals it

- **when** — sales are asked for in a named currency
- **then** — convert each sale through ExchangeRate at its own order date; the amounts are USD
- **never** — filter on `{currency_code}` and present the USD amounts as if they were in that currency

## Cites

- `dataset:dim_currency.currency_code`
- `rule:Currency.code_is_not_the_unit`
- `rule:Currency.whose`
