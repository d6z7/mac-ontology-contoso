---
type: Doc
title: SME questions — data & data quality
description: 48 open ask(s)
tags:
- Contoso 5
- sme-questions
---

The open asks the findings carry — each finding's `needs` (the ask), its `remedies` (the answer set) and the `recommended` one, prioritised by severity. Projected from `data/quality/*.yaml`.

## High priority — 27 question(s)

| ask | answer one of | recommended | asked in | on (finding) | dataset |
|---|---|---|---|---|---|
| Which of currencyexchange.FromCurrency, currencyexchange.ToCurrency is THE reference for CurrencyCode? ANSWER ONE OF: currencyexchange.FromCurrency \| currencyexchange.ToCurrency \| both_are_real \| n | currencyexchange.FromCurrency: CurrencyCode references currencyexchange.FromCurrency, the reference to currencyexchange. | the endpoint the child is DENOMINATED IN — for an amount and | — | [DQ-AMBIGREF-CURRENCYCODE](DQ-AMBIGREF-CURRENCYCODE.md) | v_contoso5_fx_rate |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_brand-COLUMNS](DQ-CASE-G-contoso5_brand-COLUMNS.md) | contoso5_brand |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_brand-KEY](DQ-CASE-G-contoso5_brand-KEY.md) | contoso5_brand |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_category_name-COLUMNS](DQ-CASE-G-contoso5_category_name-COLUMNS.md) | contoso5_category_name |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_category_name-KEY](DQ-CASE-G-contoso5_category_name-KEY.md) | contoso5_category_name |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_channel-COLUMNS](DQ-CASE-G-contoso5_channel-COLUMNS.md) | contoso5_channel |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_channel-KEY](DQ-CASE-G-contoso5_channel-KEY.md) | contoso5_channel |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_color-COLUMNS](DQ-CASE-G-contoso5_color-COLUMNS.md) | contoso5_color |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_color-KEY](DQ-CASE-G-contoso5_color-KEY.md) | contoso5_color |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_continent-COLUMNS](DQ-CASE-G-contoso5_continent-COLUMNS.md) | contoso5_continent |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_continent-KEY](DQ-CASE-G-contoso5_continent-KEY.md) | contoso5_continent |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_country_code-COLUMNS](DQ-CASE-G-contoso5_country_code-COLUMNS.md) | contoso5_country_code |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_country_code-KEY](DQ-CASE-G-contoso5_country_code-KEY.md) | contoso5_country_code |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_currency-COLUMNS](DQ-CASE-G-contoso5_currency-COLUMNS.md) | contoso5_currency |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_currency-KEY](DQ-CASE-G-contoso5_currency-KEY.md) | contoso5_currency |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_gender-COLUMNS](DQ-CASE-G-contoso5_gender-COLUMNS.md) | contoso5_gender |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_gender-KEY](DQ-CASE-G-contoso5_gender-KEY.md) | contoso5_gender |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_manufacturer-COLUMNS](DQ-CASE-G-contoso5_manufacturer-COLUMNS.md) | contoso5_manufacturer |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_manufacturer-KEY](DQ-CASE-G-contoso5_manufacturer-KEY.md) | contoso5_manufacturer |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_state-COLUMNS](DQ-CASE-G-contoso5_state-COLUMNS.md) | contoso5_state |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_state-KEY](DQ-CASE-G-contoso5_state-KEY.md) | contoso5_state |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_status-COLUMNS](DQ-CASE-G-contoso5_status-COLUMNS.md) | contoso5_status |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_status-KEY](DQ-CASE-G-contoso5_status-KEY.md) | contoso5_status |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_store_name-COLUMNS](DQ-CASE-G-contoso5_store_name-COLUMNS.md) | contoso5_store_name |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_store_name-KEY](DQ-CASE-G-contoso5_store_name-KEY.md) | contoso5_store_name |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_sub_category_name-COLUMNS](DQ-CASE-G-contoso5_sub_category_name-COLUMNS.md) | contoso5_sub_category_name |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_sub_category_name-KEY](DQ-CASE-G-contoso5_sub_category_name-KEY.md) | contoso5_sub_category_name |

## Medium priority — 21 question(s)

| ask | answer one of | recommended | asked in | on (finding) | dataset |
|---|---|---|---|---|---|
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_brand-NULLS](DQ-CASE-G-contoso5_brand-NULLS.md) | contoso5_brand |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_category_name-NULLS](DQ-CASE-G-contoso5_category_name-NULLS.md) | contoso5_category_name |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_channel-NULLS](DQ-CASE-G-contoso5_channel-NULLS.md) | contoso5_channel |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_color-NULLS](DQ-CASE-G-contoso5_color-NULLS.md) | contoso5_color |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_continent-NULLS](DQ-CASE-G-contoso5_continent-NULLS.md) | contoso5_continent |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_country_code-NULLS](DQ-CASE-G-contoso5_country_code-NULLS.md) | contoso5_country_code |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_currency-NULLS](DQ-CASE-G-contoso5_currency-NULLS.md) | contoso5_currency |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_gender-NULLS](DQ-CASE-G-contoso5_gender-NULLS.md) | contoso5_gender |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_manufacturer-NULLS](DQ-CASE-G-contoso5_manufacturer-NULLS.md) | contoso5_manufacturer |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_state-NULLS](DQ-CASE-G-contoso5_state-NULLS.md) | contoso5_state |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_store_name-NULLS](DQ-CASE-G-contoso5_store_name-NULLS.md) | contoso5_store_name |
| a disposition: fix the data, or accept the reading with a reason. | — | — | — | [DQ-CASE-G-contoso5_sub_category_name-NULLS](DQ-CASE-G-contoso5_sub_category_name-NULLS.md) | contoso5_sub_category_name |
| Is the parent MISSING from the extract, already INLINE on the row, or is CategoryKey just an attribute? ANSWER ONE OF: inline_dimension \| attribute_only \| missing_extract. RECOMMENDED: inline_dimens | inline_dimension: a concept is grounded on the carrying relation, using the key for identity and its twin for the label; | inline_dimension | — | [DQ-DANGLINGKEY-CATEGORYKEY](DQ-DANGLINGKEY-CATEGORYKEY.md) | dim_product |
| Is the parent MISSING from the extract, already INLINE on the row, or is GeoAreaKey just an attribute? ANSWER ONE OF: inline_dimension \| attribute_only \| missing_extract. NO RECOMMENDATION — no colu | inline_dimension: a concept is grounded on the carrying relation, using the key for identity and its twin for the label; | — | — | [DQ-DANGLINGKEY-GEOAREAKEY](DQ-DANGLINGKEY-GEOAREAKEY.md) | dim_customer |
| Is the parent MISSING from the extract, already INLINE on the row, or is SubCategoryKey just an attribute? ANSWER ONE OF: inline_dimension \| attribute_only \| missing_extract. RECOMMENDED: inline_dim | inline_dimension: a concept is grounded on the carrying relation, using the key for identity and its twin for the label; | inline_dimension | — | [DQ-DANGLINGKEY-SUBCATEGORYKEY](DQ-DANGLINGKEY-SUBCATEGORYKEY.md) | dim_product |
| Which is the FACT OF RECORD? ANSWER ONE OF: orderrows \| sales \| both_are_distinct_facts \| neither_serve_a_transform. RECOMMENDED: serve exactly ONE — see the ruling. | orderrows: the normalised detail is the record, and every question at this grain must JOIN a header relation to reach th | serve exactly ONE of them | — | [DQ-DUP-ORDERROWS-SALES](DQ-DUP-ORDERROWS-SALES.md) | v_contoso5_sales_line |
| a ruling on the concept that grounds `dim_customer.city`: `rulings: {never_axis: privacy, evidence: DQ-IDENTIFYING-DIM_CUSTOMER-CITY}` on the column, or a written reason the axis is safe to offer. Unt | — | — | — | [DQ-IDENTIFYING-DIM_CUSTOMER-CITY](DQ-IDENTIFYING-DIM_CUSTOMER-CITY.md) | dim_customer |
| a ruling on the concept that grounds `dim_customer.customer_name`: `rulings: {never_axis: privacy, evidence: DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME}` on the column, or a written reason the axis is  | — | — | — | [DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME](DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME.md) | dim_customer |
| a ruling: is this relation OUT OF SCOPE for this bundle, or is a served relation missing? | — | — | — | [DQ-ORPHAN-DATE](DQ-ORPHAN-DATE.md) | v_contoso5_sales_line |
| a ruling: is this relation OUT OF SCOPE for this bundle, or is a served relation missing? | — | — | — | [DQ-ORPHAN-ORDERROWS](DQ-ORPHAN-ORDERROWS.md) | v_contoso5_sales_line |
| a ruling: is this relation OUT OF SCOPE for this bundle, or is a served relation missing? | — | — | — | [DQ-ORPHAN-ORDERS](DQ-ORPHAN-ORDERS.md) | v_contoso5_sales_line |

