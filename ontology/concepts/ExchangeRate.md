# ExchangeRate

The account of concept ExchangeRate.

## Overview

What one currency was worth in another on one day: quoted rates over a date and an ordered pair of currencies. nothing about a rate moves through phases. It is quoted, and it is aggregated by rule — an amount is never converted at a rate averaged across days; the rate's own average over days is the plain mean of the daily rates (below). ALL THREE KEY PARTS ARE ALSO REFERENCES — the day is a date and needs no dimension, both currencies to [[Currency]] — which makes this the one bridge in the bundle. THE PAIR IS ORDERED: inverting it returns a number wrong by a factor of the rate squared.

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

## How the rate averages

The rate is declared `plain_mean: true` (law L2, disclosed) beside its `over_time: average`: its average over a period is the plain mean of the daily rates. There is nothing to weight it by. One rate is quoted per day and ordered pair, and no traded volume stands behind it.

The evidence is the generator's source (https://github.com/sql-bi/Contoso-Data-Generator-V2, commit eaeb57a, `DatabaseGenerator/ECBExchangesReader.cs`). The rates are the European Central Bank's euro reference rates (`eurofxref-hist`); its comment says the file "contains exchange rate from Euro to other currencies" and "only contains data for effective days of currencies exchange. So, there are holes to be filled." Each pair's rate is `1 / fromExchange * toExchange`, rounded to five decimals, and every day between two quotes takes the earlier quote. The published documentation names the rates as static data the generator downloads (https://docs.sqlbi.com/contoso-data-generator/details: "The tool needs some files containing static data: fake customers, exchange rates, postal codes, etc."). Our rows agree: one row per day and pair over an unbroken calendar, and every weekend rate equals the Friday before it.

The plain mean is a statistic OF THE RATE ("the average euro to dollar rate in 2024"). It is never a conversion rate: an amount is converted at its own day's rate (rule ExchangeRate.convert_per_day), because a period's plain mean weights every day the same whatever sold on it. Across currency pairs the rate is not combined at all (the same rule).

## Cites

- `dataset:v_contoso5_fx_rate.date_day`
- `dataset:v_contoso5_fx_rate.from_currency`
- `dataset:v_contoso5_fx_rate.to_currency`
- `dataset:v_contoso5_fx_rate.rate`
- `rule:ExchangeRate.convert_per_day`
- `rule:ExchangeRate.direction_is_part_of_the_key`
