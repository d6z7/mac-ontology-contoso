# ExchangeRate

> The human account. The declaration is `ontology/concepts/exchange_rate.yaml`; read this first,
> whole, then compare it against that file.

## Overview

What one currency was worth in another on one day: 100,450 quoted rates over a date and an ordered
pair of currencies. Read from the rows: 2016-01-01, AUD→CAD, 1.0147. A2: a number you aggregate,
with a unit → `measure`. The draft said `event`; nothing about a rate moves through phases. It is
quoted, and it is aggregated by rule — never averaged across days. ALL THREE KEY PARTS ARE ALSO
REFERENCES — the day is a date and needs no dimension, both currencies to [[Currency]] — which
makes this the one bridge in the bundle. THE PAIR IS ORDERED: inverting it returns a number wrong
by a factor of the rate squared.

## Grain

one row per (date_day, from_currency, to_currency)

## aggregation.convert_per_day_never_average

that weights every day the same regardless of what sold on it

The declaration states this executably as well, because this rule has no body yet:

- **when** — a period's sales are converted into another currency
- **then** — convert each sale at its own order_date rate, then sum
- **never** — average the rate over the period and apply it to the total

## exclusion.direction_is_part_of_the_key

the reciprocal is not stored, and that it inverts exactly is a claim this bundle does not measure

The declaration states this executably as well, because this rule has no body yet:

- **when** — a conversion is requested between two currencies
- **then** — match the ordered pair as given
- **never** — substitute the reverse pair when the requested one is missing
