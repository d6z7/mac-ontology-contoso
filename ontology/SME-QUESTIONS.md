---
type: Doc
title: SME questions — ontology
description: 6 questions and 18 sign-off requests the model and its tests put to an SME
tags:
- CONTOSO5
- sme-questions
---

What the model and its tests ask a subject-matter expert: **6 question(s)** and **18 sign-off request(s)**, 24 row(s) in all. Consolidated from the register (model conditions and change-record `sme` blocks), concept open-question fields and test oracles flagged needs-SME; projected from ontology_quality.json and acceptance/sme_needs.json, so it stays in sync.

Conversation status is not part of this projection; it lives in the bundle's SME question ledger.

Rows by origin: register 24

## Questions — 6

### `concept:brand#enumeration`

- origin: register · owner role: not declared · concept: [brand](concepts/brand.md)
- source: `ontology/concepts/brand.yaml` → `values`

> Is “Brand” a closed set of values? If it is, what are all of its valid values?

### `concept:color#enumeration`

- origin: register · owner role: not declared · concept: [color](concepts/color.md)
- source: `ontology/concepts/color.yaml` → `values`

> Is “Colour” a closed set of values? If it is, what are all of its valid values?

### `concept:country#enumeration`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/concepts/country.yaml` → `values`

> Is “Country” a closed set of values? If it is, what are all of its valid values?

### `concept:currency#enumeration`

- origin: register · owner role: not declared · concept: [currency](concepts/currency.md)
- source: `ontology/concepts/currency.yaml` → `values`

> Is “Currency” a closed set of values? If it is, what are all of its valid values?

### `concept:exchange_rate#measure_type`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/concepts/exchange_rate.yaml` → `grounding.source.columns[].offers.aggregate.type`

> How does the measure “Exchange Rate” add up across its axes? No column of it declares `offers.aggregate.type` that mac.concept.column.measure_type resolves.

### `concept:product_category#enumeration`

- origin: register · owner role: not declared · concept: [product_category](concepts/product_category.md)
- source: `ontology/concepts/product_category.yaml` → `values`

> Is “Product Category” a closed set of values? If it is, what are all of its valid values?

## Sign-offs — 18

### `concept:brand#confidence`

- origin: register · owner role: not declared · concept: [brand](concepts/brand.md)
- source: `ontology/concepts/brand.yaml` → `metadata.confidence`

> Is the concept “Brand” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:color#confidence`

- origin: register · owner role: not declared · concept: [color](concepts/color.md)
- source: `ontology/concepts/color.yaml` → `metadata.confidence`

> Is the concept “Colour” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:country#confidence`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/concepts/country.yaml` → `metadata.confidence`

> Is the concept “Country” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:currency#confidence`

- origin: register · owner role: not declared · concept: [currency](concepts/currency.md)
- source: `ontology/concepts/currency.yaml` → `metadata.confidence`

> Is the concept “Currency” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:customer#confidence`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md)
- source: `ontology/concepts/customer.yaml` → `metadata.confidence`

> Is the concept “Customer” (entity) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:exchange_rate#confidence`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/concepts/exchange_rate.yaml` → `metadata.confidence`

> Is the concept “Exchange Rate” (measure) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:location#confidence`

- origin: register · owner role: not declared · concept: [location](concepts/location.md)
- source: `ontology/concepts/location.yaml` → `metadata.confidence`

> Is the concept “Location” (entity) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:product#confidence`

- origin: register · owner role: not declared · concept: [product](concepts/product.md)
- source: `ontology/concepts/product.yaml` → `metadata.confidence`

> Is the concept “Product” (entity) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:product_category#confidence`

- origin: register · owner role: not declared · concept: [product_category](concepts/product_category.md)
- source: `ontology/concepts/product_category.yaml` → `metadata.confidence`

> Is the concept “Product Category” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:store#confidence`

- origin: register · owner role: not declared · concept: [store](concepts/store.md)
- source: `ontology/concepts/store.yaml` → `metadata.confidence`

> Is the concept “Store” (entity) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `rule:country.exclusion.sentinel_is_not_a_country#confidence`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/concepts/country.yaml` → `contract.rules[id=country.exclusion.sentinel_is_not_a_country]`

> Is the rule “country.exclusion.sentinel_is_not_a_country” on “Country” correct? It is recorded as proposed, not confirmed.

### `rule:exchange_rate.aggregation.convert_per_day_never_average#confidence`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/concepts/exchange_rate.yaml` → `contract.rules[id=exchange_rate.aggregation.convert_per_day_never_average]`

> Is the rule “exchange_rate.aggregation.convert_per_day_never_average” on “Exchange Rate” correct? It is recorded as proposed, not confirmed.

### `rule:exchange_rate.exclusion.direction_is_part_of_the_key#confidence`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/concepts/exchange_rate.yaml` → `contract.rules[id=exchange_rate.exclusion.direction_is_part_of_the_key]`

> Is the rule “exchange_rate.exclusion.direction_is_part_of_the_key” on “Exchange Rate” correct? It is recorded as proposed, not confirmed.

### `rule:location.exclusion.the_online_row_is_not_a_place#confidence`

- origin: register · owner role: not declared · concept: [location](concepts/location.md)
- source: `ontology/concepts/location.yaml` → `contract.rules[id=location.exclusion.the_online_row_is_not_a_place]`

> Is the rule “location.exclusion.the_online_row_is_not_a_place” on “Location” correct? It is recorded as proposed, not confirmed.

### `rule:order.default.period_is_order_date#confidence`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/concepts/order.yaml` → `contract.rules[id=order.default.period_is_order_date]`

> Is the rule “order.default.period_is_order_date” on “Order” correct? It is recorded as proposed, not confirmed.

### `rule:order.resolution.rate_on_order_date#confidence`

- origin: register · owner role: not declared · concept: [order](concepts/order.md)
- source: `ontology/concepts/order.yaml` → `contract.rules[id=order.resolution.rate_on_order_date]`

> Is the rule “order.resolution.rate_on_order_date” on “Order” correct? It is recorded as proposed, not confirmed.

### `rule:product_category.ambiguity.which_level#confidence`

- origin: register · owner role: not declared · concept: [product_category](concepts/product_category.md)
- source: `ontology/concepts/product_category.yaml` → `contract.rules[id=product_category.ambiguity.which_level]`

> Is the rule “product_category.ambiguity.which_level” on “Product Category” correct? It is recorded as proposed, not confirmed.

### `rule:store.resolution.the_channel_is_the_location_sentinel#confidence`

- origin: register · owner role: not declared · concept: [store](concepts/store.md)
- source: `ontology/concepts/store.yaml` → `contract.rules[id=store.resolution.the_channel_is_the_location_sentinel]`

> Is the rule “store.resolution.the_channel_is_the_location_sentinel” on “Store” correct? It is recorded as proposed, not confirmed.

## Findings — 0 (not questions)

None.

## Operator items — 0 (not SME questions)

None.
