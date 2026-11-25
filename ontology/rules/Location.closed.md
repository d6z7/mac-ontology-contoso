# Location.closed

The account of rule Location.closed.

## Cites

- `concept:Location`
- `dataset:dim_location.has_closed_store`
- `dataset:dim_location.is_closed_now`

## The choice

Two readings of a closed site, both derived on `dim_location` by its transform: `ever` (`has_closed_store`, a store at
the site has closed) and `now` (`is_closed_now`, no store at the site trades). A site whose store closed and was
replaced is closed under `ever` and not under `now`.

## The default

`ever`, proposed 2026-11-17. It applies and is disclosed as proposed (GRAMMAR_v3 L3, Y-6). STORE-16 follows it (its
signed figure, 14); `acceptance/tools/rule_switch_test.py` shows `now` changes the answer.
