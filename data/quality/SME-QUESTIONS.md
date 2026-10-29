---
type: Doc
title: SME questions — data & data quality
description: 61 sign-offs + 0 proposed changes awaiting SME
tags:
- CONTOSO5
- sme-questions
---

The open **SME sign-offs** the data + data-quality work surfaces — 61 from the quality register plus proposed transform changes awaiting ratification. Prioritised by severity; each links to the finding it unblocks. This list is projected from the register + transforms, so it stays in sync.

## High priority — 27 question(s)

| ask | answer one of | owner | on (finding) | status | table |
|---|---|---|---|---|---|
| CurrencyCode includes perfectly into all of currencyexchange.FromCurrency, currencyexchange.ToCurrency. Which is THE reference? | currencyexchange.FromCurrency \| currencyexchange.ToCurrency \| both_are_real \| neither | domain-owner | [`CurrencyCode` includes perfectly into 2 different keys ](DQ-AMBIGREF-CURRENCYCODE.md) | unreconciled | currencyexchange |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_brand-COLUMNS did not pass](DQ-CASE-G-contoso5_brand-COLUMNS.md) | unreconciled | product |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_brand-KEY did not pass](DQ-CASE-G-contoso5_brand-KEY.md) | unreconciled | product |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_category_name-COLUMNS did no](DQ-CASE-G-contoso5_category_name-COLUMNS.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_category_name-KEY did not pa](DQ-CASE-G-contoso5_category_name-KEY.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_channel-COLUMNS did not pass](DQ-CASE-G-contoso5_channel-COLUMNS.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_channel-KEY did not pass](DQ-CASE-G-contoso5_channel-KEY.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_color-COLUMNS did not pass](DQ-CASE-G-contoso5_color-COLUMNS.md) | unreconciled | product |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_color-KEY did not pass](DQ-CASE-G-contoso5_color-KEY.md) | unreconciled | product |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_continent-COLUMNS did not pa](DQ-CASE-G-contoso5_continent-COLUMNS.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_continent-KEY did not pass](DQ-CASE-G-contoso5_continent-KEY.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_country_code-COLUMNS did not](DQ-CASE-G-contoso5_country_code-COLUMNS.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_country_code-KEY did not pas](DQ-CASE-G-contoso5_country_code-KEY.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_currency-COLUMNS did not pas](DQ-CASE-G-contoso5_currency-COLUMNS.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_currency-KEY did not pass](DQ-CASE-G-contoso5_currency-KEY.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_gender-COLUMNS did not pass](DQ-CASE-G-contoso5_gender-COLUMNS.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_gender-KEY did not pass](DQ-CASE-G-contoso5_gender-KEY.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_manufacturer-COLUMNS did not](DQ-CASE-G-contoso5_manufacturer-COLUMNS.md) | unreconciled | product |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_manufacturer-KEY did not pas](DQ-CASE-G-contoso5_manufacturer-KEY.md) | unreconciled | product |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_state-COLUMNS did not pass](DQ-CASE-G-contoso5_state-COLUMNS.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_state-KEY did not pass](DQ-CASE-G-contoso5_state-KEY.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_status-COLUMNS did not pass](DQ-CASE-G-contoso5_status-COLUMNS.md) | unreconciled | store |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_status-KEY did not pass](DQ-CASE-G-contoso5_status-KEY.md) | unreconciled | store |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_store_name-COLUMNS did not p](DQ-CASE-G-contoso5_store_name-COLUMNS.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_store_name-KEY did not pass](DQ-CASE-G-contoso5_store_name-KEY.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_sub_category_name-COLUMNS di](DQ-CASE-G-contoso5_sub_category_name-COLUMNS.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_sub_category_name-KEY did no](DQ-CASE-G-contoso5_sub_category_name-KEY.md) | unreconciled | — |

## Medium priority — 34 question(s)

| ask | answer one of | owner | on (finding) | status | table |
|---|---|---|---|---|---|
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_brand-NULLS did not pass](DQ-CASE-G-contoso5_brand-NULLS.md) | unreconciled | product |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_category_name-NULLS did not ](DQ-CASE-G-contoso5_category_name-NULLS.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_channel-NULLS did not pass](DQ-CASE-G-contoso5_channel-NULLS.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_color-NULLS did not pass](DQ-CASE-G-contoso5_color-NULLS.md) | unreconciled | product |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_continent-NULLS did not pass](DQ-CASE-G-contoso5_continent-NULLS.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_country_code-NULLS did not p](DQ-CASE-G-contoso5_country_code-NULLS.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_currency-NULLS did not pass](DQ-CASE-G-contoso5_currency-NULLS.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_gender-NULLS did not pass](DQ-CASE-G-contoso5_gender-NULLS.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_manufacturer-NULLS did not p](DQ-CASE-G-contoso5_manufacturer-NULLS.md) | unreconciled | product |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_state-NULLS did not pass](DQ-CASE-G-contoso5_state-NULLS.md) | unreconciled | customer |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_store_name-NULLS did not pas](DQ-CASE-G-contoso5_store_name-NULLS.md) | unreconciled | — |
| a disposition: fix the data, or accept the reading with a reason. | — | domain-owner | [data-sanity case G-contoso5_sub_category_name-NULLS did ](DQ-CASE-G-contoso5_sub_category_name-NULLS.md) | unreconciled | — |
| CategoryKey is key-shaped with no parent in scope. Which absence is it? | inline_dimension \| attribute_only \| missing_extract | domain-owner | [`CategoryKey` is key-shaped and no relation in scope car](DQ-DANGLINGKEY-CATEGORYKEY.md) | unreconciled | product |
| GeoAreaKey is key-shaped with no parent in scope. Which absence is it? | inline_dimension \| attribute_only \| missing_extract | domain-owner | [`GeoAreaKey` is key-shaped and no relation in scope carr](DQ-DANGLINGKEY-GEOAREAKEY.md) | unreconciled | customer |
| SubCategoryKey is key-shaped with no parent in scope. Which absence is it? | inline_dimension \| attribute_only \| missing_extract | domain-owner | [`SubCategoryKey` is key-shaped and no relation in scope ](DQ-DANGLINGKEY-SUBCATEGORYKEY.md) | unreconciled | product |
| `orderrows` and `sales` deliver the same 223,974 rows. Which is the fact of record? | orderrows \| sales \| both_are_distinct_facts \| neither_serve_a_transform | domain-owner | [`sales` re-delivers every line of `orderrows` — one fact](DQ-DUP-ORDERROWS-SALES.md) | unreconciled | sales |
| a ruling on the concept that grounds `dim_customer.city`: `rulings: {never_axis: privacy, evidence: DQ-IDENTIFYING-DIM_CUSTOMER-CITY}` on the column, or a written reason the axis is safe to offer. Unt | — | domain-owner | [`dim_customer.city` names individuals — 21,317 of 34,581](DQ-IDENTIFYING-DIM_CUSTOMER-CITY.md) | unreconciled | customer |
| a ruling on the concept that grounds `dim_customer.customer_name`: `rulings: {never_axis: privacy, evidence: DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME}` on the column, or a written reason the axis is  | — | domain-owner | [`dim_customer.customer_name` names individuals — 94,488 ](DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME.md) | unreconciled | — |
| a ruling: is this relation OUT OF SCOPE for this bundle, or is a served relation missing? | — | domain-owner | [raw landing `date` is consumed by no transformation](DQ-ORPHAN-DATE.md) | unreconciled | currencyexchange |
| a ruling: is this relation OUT OF SCOPE for this bundle, or is a served relation missing? | — | domain-owner | [raw landing `orderrows` is consumed by no transformation](DQ-ORPHAN-ORDERROWS.md) | unreconciled | — |
| a ruling: is this relation OUT OF SCOPE for this bundle, or is a served relation missing? | — | domain-owner | [raw landing `orders` is consumed by no transformation](DQ-ORPHAN-ORDERS.md) | unreconciled | — |
| `contoso5_brand` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_brand` is claimed by no concep](DQ-UNCLAIMED-CONTOSO5_BRAND.md) | unreconciled | product |
| `contoso5_category_name` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_category_name` is claimed by n](DQ-UNCLAIMED-CONTOSO5_CATEGORY_NAME.md) | unreconciled | — |
| `contoso5_channel` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_channel` is claimed by no conc](DQ-UNCLAIMED-CONTOSO5_CHANNEL.md) | unreconciled | — |
| `contoso5_color` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_color` is claimed by no concep](DQ-UNCLAIMED-CONTOSO5_COLOR.md) | unreconciled | product |
| `contoso5_continent` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_continent` is claimed by no co](DQ-UNCLAIMED-CONTOSO5_CONTINENT.md) | unreconciled | customer |
| `contoso5_country_code` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_country_code` is claimed by no](DQ-UNCLAIMED-CONTOSO5_COUNTRY_CODE.md) | unreconciled | customer |
| `contoso5_currency` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_currency` is claimed by no con](DQ-UNCLAIMED-CONTOSO5_CURRENCY.md) | unreconciled | — |
| `contoso5_gender` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_gender` is claimed by no conce](DQ-UNCLAIMED-CONTOSO5_GENDER.md) | unreconciled | customer |
| `contoso5_manufacturer` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_manufacturer` is claimed by no](DQ-UNCLAIMED-CONTOSO5_MANUFACTURER.md) | unreconciled | product |
| `contoso5_state` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_state` is claimed by no concep](DQ-UNCLAIMED-CONTOSO5_STATE.md) | unreconciled | customer |
| `contoso5_status` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_status` is claimed by no conce](DQ-UNCLAIMED-CONTOSO5_STATUS.md) | unreconciled | store |
| `contoso5_store_name` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_store_name` is claimed by no c](DQ-UNCLAIMED-CONTOSO5_STORE_NAME.md) | unreconciled | — |
| `contoso5_sub_category_name` is served and claimed by no concept. Which is it? | model_a_concept \| stop_serving_it \| backs_no_notion | domain-owner | [served relation `contoso5_sub_category_name` is claimed ](DQ-UNCLAIMED-CONTOSO5_SUB_CATEGORY_NAME.md) | unreconciled | — |
