# ExchangeRate

The account of concept ExchangeRate.

## Overview

What one currency was worth in another on one day: quoted rates over a date and an ordered pair of currencies. nothing about a rate moves through phases. It is quoted, and it is aggregated by rule — never averaged across days. ALL THREE KEY PARTS ARE ALSO REFERENCES — the day is a date and needs no dimension, both currencies to [[Currency]] — which makes this the one bridge in the bundle. THE PAIR IS ORDERED: inverting it returns a number wrong by a factor of the rate squared.

## Grain

one row per (date_day, from_currency, to_currency)

## ExchangeRate.convert_per_day

that weights every day the same regardless of what sold on it

- **when** — a period's sales are converted into another currency
- **then** — convert each sale at its own order_date rate, then sum
- **never** — average the rate over the period and apply it to the total

## ExchangeRate.direction_is_part_of_the_key

the reciprocal is not stored, and that it inverts exactly is a claim this bundle does not measure

- **when** — a conversion is requested between two currencies
- **then** — match the ordered pair as given
- **never** — substitute the reverse pair when the requested one is missing

## Cites

- `dataset:v_contoso5_fx_rate.date_day`
- `dataset:v_contoso5_fx_rate.from_currency`
- `dataset:v_contoso5_fx_rate.to_currency`
- `dataset:v_contoso5_fx_rate.rate`
- `rule:ExchangeRate.convert_per_day`
- `rule:ExchangeRate.direction_is_part_of_the_key`
