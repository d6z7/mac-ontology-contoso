# Store.premises_not_place

The account of rule Store.premises_not_place. Written by mac_migrate_v3; each heading after `Cites` carries 0.4.0 prose that has no key in grammar v3 (X-3).

## Cites

- `project`
- `concept:Store`
- `concept:Location`
- `dataset:dim_location.units_ever_here`
- `dataset:dim_store.store_key`
- `dataset:dim_store.store_code`

## State

`proposed`, not `ruled`: Y-7 (RULING-2026-11-16_grammar-v3) takes a ruled rule's words only from a decision record the rule cites, and drops it to `proposed` where none is found. No record under decisions/ carries the words, so `said.in` is not given. The operator confirms the words (with the record they were said in) to make it `ruled`.

## The choice

The level is set in one place and can be switched: `premises` (the default, `dim_store.store_key`, the grain the
operator described on 2026-10-24 and the Store concept's `counts`) and `site` (`dim_store.store_code`, one row per
place). A store name and a site code are one to one in this data, so listing distinct names is the `site` reading. The
state is `proposed` (see State above). STORE-12 and STORE-13 follow the default; their references carry the site
answers under `site`, and `acceptance/tools/rule_switch_test.py` proves the two differ.
