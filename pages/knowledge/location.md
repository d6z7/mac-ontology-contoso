# Location

> The human account. The declaration is `ontology/concepts/location.yaml`; read this first,
> whole, then compare it against that file.

## Overview

A place a store is: a country and a state, 67 of them. Read from the rows: `1, AU, Australia,
Australian Capital Territory`. The last of a Sale's direct needs — "where", one hop past the store
— and the eighth served relation to be reached. A2: a keyed dimension that facts point at →
`reference`. Store points at it, measured many:one and mandatory both ways: every location holds a
store, every store has one. COARSER THAN THE STORES IT HOLDS — 67 locations to 73 shops — so a
figure by location is not a figure by store, and the difference is the places with more than one.
ROW -1 IS NOT A PLACE. `-1, --, Online, Online` is the online channel's sentinel, mirrored from
the store table. It is held out by this concept's own `physical` population — the declared default
— exactly as it is on [[Store]], and reached by naming `online`. `units_ever_here` IS A LIFETIME
TOTAL, precomputed somewhere else. It answers no question with a date in it and cannot be filtered
by one; sales in a place come from Sale through Store. NAMES RESOLVE THROUGH
`data/lookups/contoso5_country_code.lookup.yaml` and `data/lookups/contoso5_state.lookup.yaml` — a
question says "Australia" or "Tasmania", never a location code.

## Identity

Established as `code`.

The canonical key is a COLUMN fact and is not repeated here; this says only HOW identity is
established. A `location_code` that IS the identity — 67 codes, one per place, no surrogate behind
it.

## Grain

one row per location (location_code)

## exclusion.the_online_row_is_not_a_place

"In how many countries do we sell" answers 9 with it and 8 without, and 8 is true

Declared executably: `mac.canon.population_select`.

Stated in the declaration as:

- **never** — count `--` as a country

## Notes carried from the declaration

NO `when:`/`then:`, 2026-10-01 — the body below states both.

The same fact as Store's channel axis and Country's, on THIS relation's own rows. MEASURED on
`dim_location`: 67 rows, 1 sentinel, 66 real places.
