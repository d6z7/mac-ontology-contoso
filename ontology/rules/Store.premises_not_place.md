# Store.premises_not_place

The account of rule Store.premises_not_place. Written by mac_migrate_v3; each heading after `Cites` carries 0.4.0 prose that has no key in grammar v3 (X-3).

## Cites

- `project`
- `concept:Store`
- `concept:Location`
- `dataset:dim_location.units_ever_here`
- `dataset:dim_store.store_key`
- `dataset:dim_store.store_code`

## State (v3 migration, 2026-11-17)

`proposed`, not `ruled`: Y-7 (RULING-2026-11-16_grammar-v3) takes a ruled rule's words only from a decision record the rule cites, and drops it to `proposed` where none is found. The words were recorded in the 0.4.0 concept file `ontology/concepts/store.yaml`, which the v3 migration replaced (commit eb6eff7), so `said.in` is no longer given; no record under decisions/ carries them. The operator confirms the words (with the record they were said in) to make it `ruled` again.

## A choice since 2026-11-17

The rule was prose (`implemented: prose`, not enforced). It is now a choice between its two readings, so the level is
set in one place and can be switched: `premises` (the default, `dim_store.store_key`, the grain the operator described
on 2026-10-24 and the Store concept's `counts`) and `site` (`dim_store.store_code`, one row per place, the reading of the
superseded Store.counted_by_site). A store name and a site code are one to one in this data, so listing distinct names
is the `site` reading. The state stays `proposed` (Y-7 above). STORE-12 and STORE-13 follow the default; their
references keep the site answers under `site`, and `acceptance/tools/rule_switch_test.py` proves the two differ.
