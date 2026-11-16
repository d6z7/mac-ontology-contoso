# Currency

> The human account. The declaration is `ontology/concepts/currency.yaml`; read this first,
> whole, then compare it against that file.

## Overview

The money a sale is denominated in: five ISO codes, pointed at by every sale and by both ends of
every exchange rate. Read from the rows: USD on just over half of sales, then EUR, CAD, GBP, AUD.
A2: a controlled set of coded values → `enumeration`. One column, no attributes — a code list. IT
NAMES WHAT A SALE CONVERTS TO, NOT WHAT IT IS IN. The amounts on a sale are USD; this code is the
customer's currency, and getting there goes through [[ExchangeRate]].

## Identity

Established as `iso`.

The canonical key is a COLUMN fact and is not repeated here; this says only HOW identity is
established. ISO 4217 three-letter codes. The standard is the authority, which is why a question
saying 'euros' resolves offline.

## Grain

one row per ISO currency code

## ambiguity.code_is_not_the_unit_of_the_amounts

nothing in the figure reveals it

The declaration states this executably as well, because this rule has no body yet:

- **when** — sales are asked for in a named currency
- **then** — convert each sale through ExchangeRate at its own order date; the amounts are USD
- **never** — filter on `{currency_code}` and present the USD amounts as if they were in that currency

## Notes carried from the declaration

`key: [currency_code]` REMOVED 2026-10-04 — the grain is a COLUMN fact and `currency_code` already
declares `identity: canonical` below. Two homes for one grain can disagree;
decisions/PROPOSED-2026-10-02 measured 38 of 38 agreeing and removed `key:` from 17 concepts —
these four were missed.
