# Store

The account of concept Store. Written by mac_migrate_v3 from the 0.4.0 declaration; each heading after `Cites` carries 0.4.0 prose that has no key in grammar v3 (X-3).

## Cites

- `dataset:dim_store.store_key`
- `dataset:dim_store.store_code`
- `dataset:dim_store.store_name`
- `dataset:dim_store.country_code`
- `dataset:dim_store.state`
- `dataset:dim_store.open_date`
- `dataset:dim_store.close_date`
- `dataset:dim_store.status_annotation`
- `dataset:dim_store.square_metres`
- `dataset:dim_store.is_online`
- `dataset:dim_store.is_shut`
- `dataset:dim_store.is_restructured`
- `rule:Store.channel`
- `rule:Store.counted_by_site`
- `rule:Store.premises_not_place`
- `rule:Store.record_questions`
- `rule:Store.revenue_is_shop_only`
- `rule:Store.trading`

## grounding.note

Nothing is collapsed: once the `active` population has selected the trading rows there is one row per store already, one per location code, because a location has at most one store with no close date (the row count is measured in data/profiles). Why, and the collapse this replaced, is in knowledge/store.md.
