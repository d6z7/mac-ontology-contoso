# Location

The account of concept Location.

## Overview

A place a store is: a country and a state. Store points at it, measured many:one and mandatory both ways: every location holds a store, every store has one. COARSER THAN THE STORES IT HOLDS, so a figure by location is not a figure by store, and the difference is the places with more than one. ROW -1 IS NOT A PLACE. `-1, --, Online, Online` is the online channel's sentinel, mirrored from the store table. It is held out by this concept's own `physical` population — the declared default — exactly as it is on [[Store]], and reached by naming `online`. `units_ever_here` IS A LIFETIME TOTAL, precomputed somewhere else. It answers no question with a date in it and cannot be filtered by one; sales in a place come from Order through Store. a question says "Australia" or "Tasmania", never a location code.

## Identity

A `location_code` that IS the identity — one per place, no surrogate behind it.

## Grain

one row per location (location_code)

## Location.channel

"In how many countries do we sell" counts one country too many with it, and the answer without it is true

- **never** — count `--` as a country

The same fact as Store's channel axis and Country's, on THIS relation's own rows. `dim_location` holds one sentinel row; every other row is a real place.

## Cites

- `dataset:dim_location.location_code`
- `dataset:dim_location.country_code`
- `dataset:dim_location.country_name`
- `dataset:dim_location.state`
- `dataset:dim_location.units_ever_here`
- `dataset:dim_location.is_online`
- `dataset:dim_location.has_closed_store`
- `dataset:dim_location.is_closed_now`
- `rule:Location.channel`
- `rule:Location.closed`
- `rule:Location.site`
