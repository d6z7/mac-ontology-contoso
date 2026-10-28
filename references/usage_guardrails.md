---
type: Reference
title: Usage guardrails — how to answer CONTOSO5 safely
tags: [reference, guardrail]
---

# Usage guardrails (read first)

This page is projected from the ontology — every routing decision, default, and prohibition below
is authored on a concept, not invented here. **Only interpretation is probabilistic; generate SQL
from the question + this ontology ALONE, never from a live probe.** A fact the ontology does not
state is a GAP to flag, not a value to guess.

## Routing — which serving relation answers what

| concept | class | relation | answer with |
|---|---|---|---|
| [Brand](../ontology/concepts/brand.md) | enumeration | `dim_product` | nothing declared |
| [Colour](../ontology/concepts/color.md) | enumeration | `dim_product` | nothing declared |
| [Country](../ontology/concepts/country.md) | enumeration | `dim_country` | 2 binding rule(s) — see below |
| [Currency](../ontology/concepts/currency.md) | enumeration | `dim_currency` | nothing declared |
| [Customer](../ontology/concepts/customer.md) | entity | `dim_customer` | nothing declared |
| [Exchange Rate](../ontology/concepts/exchange_rate.md) | measure | `v_contoso5_fx_rate` | 2 binding rule(s) — see below |
| [Location](../ontology/concepts/location.md) | entity | `dim_location` | 1 binding rule(s) — see below |
| [Order](../ontology/concepts/order.md) | event | `v_contoso5_sales_line` | A QUESTION THAT NAMES NO PERIOD COVERS ALL TIME — operator ruling, 2026-09-30. No implied  |
| [Product](../ontology/concepts/product.md) | entity | `dim_product` | nothing declared |
| [Product Category](../ontology/concepts/product_category.md) | enumeration | `dim_product` | 1 binding rule(s) — see below |
| [Store](../ontology/concepts/store.md) | entity | `dim_store` | 2 binding rule(s) — see below |

## How to answer — per-concept playbooks (`contract`: `default_reading`, `resolution`, `rules`)

### Country — `dim_country`


### Exchange Rate — `v_contoso5_fx_rate`


### Location — `dim_location`


### Order — `v_contoso5_sales_line`

- **Default reading** — A QUESTION THAT NAMES NO PERIOD COVERS ALL TIME — operator ruling, 2026-09-30. No implied "this year" and no implied latest month. The extent is `{order_date}` from 2016-05-18 to 2025-12-31; deliveries run six days further, to 2026-01-06. State the window the answer actually covered, because an unscoped total and a year-to-date total are indistinguishable from the figure alone.

### Product Category — `dim_product`


### Store — `dim_store`


## Filter traps & known issues

Recorded data-quality findings that change how you must query. Full detail in `references/known_issues/`.

- [DQ-AMBIGREF-CURRENCYCODE](known_issues/DQ-AMBIGREF-CURRENCYCODE.md) — _high_ · `CurrencyCode` includes perfectly into 2 different keys — which is THE reference? · **not yet reconciled**
- [DQ-CASE-G-contoso5_brand-COLUMNS](known_issues/DQ-CASE-G-contoso5_brand-COLUMNS.md) — _high_ · data-sanity case G-contoso5_brand-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_brand-KEY](known_issues/DQ-CASE-G-contoso5_brand-KEY.md) — _high_ · data-sanity case G-contoso5_brand-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_brand-NULLS](known_issues/DQ-CASE-G-contoso5_brand-NULLS.md) — _medium_ · data-sanity case G-contoso5_brand-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_category_name-COLUMNS](known_issues/DQ-CASE-G-contoso5_category_name-COLUMNS.md) — _high_ · data-sanity case G-contoso5_category_name-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_category_name-KEY](known_issues/DQ-CASE-G-contoso5_category_name-KEY.md) — _high_ · data-sanity case G-contoso5_category_name-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_category_name-NULLS](known_issues/DQ-CASE-G-contoso5_category_name-NULLS.md) — _medium_ · data-sanity case G-contoso5_category_name-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_channel-COLUMNS](known_issues/DQ-CASE-G-contoso5_channel-COLUMNS.md) — _high_ · data-sanity case G-contoso5_channel-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_channel-KEY](known_issues/DQ-CASE-G-contoso5_channel-KEY.md) — _high_ · data-sanity case G-contoso5_channel-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_channel-NULLS](known_issues/DQ-CASE-G-contoso5_channel-NULLS.md) — _medium_ · data-sanity case G-contoso5_channel-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_color-COLUMNS](known_issues/DQ-CASE-G-contoso5_color-COLUMNS.md) — _high_ · data-sanity case G-contoso5_color-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_color-KEY](known_issues/DQ-CASE-G-contoso5_color-KEY.md) — _high_ · data-sanity case G-contoso5_color-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_color-NULLS](known_issues/DQ-CASE-G-contoso5_color-NULLS.md) — _medium_ · data-sanity case G-contoso5_color-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_continent-COLUMNS](known_issues/DQ-CASE-G-contoso5_continent-COLUMNS.md) — _high_ · data-sanity case G-contoso5_continent-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_continent-KEY](known_issues/DQ-CASE-G-contoso5_continent-KEY.md) — _high_ · data-sanity case G-contoso5_continent-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_continent-NULLS](known_issues/DQ-CASE-G-contoso5_continent-NULLS.md) — _medium_ · data-sanity case G-contoso5_continent-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_country_code-COLUMNS](known_issues/DQ-CASE-G-contoso5_country_code-COLUMNS.md) — _high_ · data-sanity case G-contoso5_country_code-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_country_code-KEY](known_issues/DQ-CASE-G-contoso5_country_code-KEY.md) — _high_ · data-sanity case G-contoso5_country_code-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_country_code-NULLS](known_issues/DQ-CASE-G-contoso5_country_code-NULLS.md) — _medium_ · data-sanity case G-contoso5_country_code-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_currency-COLUMNS](known_issues/DQ-CASE-G-contoso5_currency-COLUMNS.md) — _high_ · data-sanity case G-contoso5_currency-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_currency-KEY](known_issues/DQ-CASE-G-contoso5_currency-KEY.md) — _high_ · data-sanity case G-contoso5_currency-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_currency-NULLS](known_issues/DQ-CASE-G-contoso5_currency-NULLS.md) — _medium_ · data-sanity case G-contoso5_currency-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_gender-COLUMNS](known_issues/DQ-CASE-G-contoso5_gender-COLUMNS.md) — _high_ · data-sanity case G-contoso5_gender-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_gender-KEY](known_issues/DQ-CASE-G-contoso5_gender-KEY.md) — _high_ · data-sanity case G-contoso5_gender-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_gender-NULLS](known_issues/DQ-CASE-G-contoso5_gender-NULLS.md) — _medium_ · data-sanity case G-contoso5_gender-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_manufacturer-COLUMNS](known_issues/DQ-CASE-G-contoso5_manufacturer-COLUMNS.md) — _high_ · data-sanity case G-contoso5_manufacturer-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_manufacturer-KEY](known_issues/DQ-CASE-G-contoso5_manufacturer-KEY.md) — _high_ · data-sanity case G-contoso5_manufacturer-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_manufacturer-NULLS](known_issues/DQ-CASE-G-contoso5_manufacturer-NULLS.md) — _medium_ · data-sanity case G-contoso5_manufacturer-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_state-COLUMNS](known_issues/DQ-CASE-G-contoso5_state-COLUMNS.md) — _high_ · data-sanity case G-contoso5_state-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_state-KEY](known_issues/DQ-CASE-G-contoso5_state-KEY.md) — _high_ · data-sanity case G-contoso5_state-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_state-NULLS](known_issues/DQ-CASE-G-contoso5_state-NULLS.md) — _medium_ · data-sanity case G-contoso5_state-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_status-COLUMNS](known_issues/DQ-CASE-G-contoso5_status-COLUMNS.md) — _high_ · data-sanity case G-contoso5_status-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_status-KEY](known_issues/DQ-CASE-G-contoso5_status-KEY.md) — _high_ · data-sanity case G-contoso5_status-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_store_name-COLUMNS](known_issues/DQ-CASE-G-contoso5_store_name-COLUMNS.md) — _high_ · data-sanity case G-contoso5_store_name-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_store_name-KEY](known_issues/DQ-CASE-G-contoso5_store_name-KEY.md) — _high_ · data-sanity case G-contoso5_store_name-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_store_name-NULLS](known_issues/DQ-CASE-G-contoso5_store_name-NULLS.md) — _medium_ · data-sanity case G-contoso5_store_name-NULLS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_sub_category_name-COLUMNS](known_issues/DQ-CASE-G-contoso5_sub_category_name-COLUMNS.md) — _high_ · data-sanity case G-contoso5_sub_category_name-COLUMNS did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_sub_category_name-KEY](known_issues/DQ-CASE-G-contoso5_sub_category_name-KEY.md) — _high_ · data-sanity case G-contoso5_sub_category_name-KEY did not pass · **not yet reconciled**
- [DQ-CASE-G-contoso5_sub_category_name-NULLS](known_issues/DQ-CASE-G-contoso5_sub_category_name-NULLS.md) — _medium_ · data-sanity case G-contoso5_sub_category_name-NULLS did not pass · **not yet reconciled**
- [DQ-DANGLINGKEY-CATEGORYKEY](known_issues/DQ-DANGLINGKEY-CATEGORYKEY.md) — _medium_ · `CategoryKey` is key-shaped and no relation in scope carries it as a key · **not yet reconciled**
- [DQ-DANGLINGKEY-GEOAREAKEY](known_issues/DQ-DANGLINGKEY-GEOAREAKEY.md) — _medium_ · `GeoAreaKey` is key-shaped and no relation in scope carries it as a key · **not yet reconciled**
- [DQ-DANGLINGKEY-SUBCATEGORYKEY](known_issues/DQ-DANGLINGKEY-SUBCATEGORYKEY.md) — _medium_ · `SubCategoryKey` is key-shaped and no relation in scope carries it as a key · **not yet reconciled**
- [DQ-DUP-ORDERROWS-SALES](known_issues/DQ-DUP-ORDERROWS-SALES.md) — _medium_ · `sales` re-delivers every line of `orderrows` — one fact, twice · **not yet reconciled**
- [DQ-IDENTIFYING-DIM_CUSTOMER-CITY](known_issues/DQ-IDENTIFYING-DIM_CUSTOMER-CITY.md) — _medium_ · `dim_customer.city` names individuals — 21,317 of 34,581 values are held by exactly one row · **not yet reconciled**
- [DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME](known_issues/DQ-IDENTIFYING-DIM_CUSTOMER-CUSTOMER_NAME.md) — _medium_ · `dim_customer.customer_name` names individuals — 94,488 of 99,200 values are held by exactly one row · **not yet reconciled**
- [DQ-NOKEY-META_OPEN_QUESTION](known_issues/DQ-NOKEY-META_OPEN_QUESTION.md) — _high_ · `meta_open_question` carries no measured key · **not yet reconciled**
- [DQ-ORPHAN-DATE](known_issues/DQ-ORPHAN-DATE.md) — _medium_ · raw landing `date` is consumed by no transformation · **not yet reconciled**
- [DQ-ORPHAN-ORDERROWS](known_issues/DQ-ORPHAN-ORDERROWS.md) — _medium_ · raw landing `orderrows` is consumed by no transformation · **not yet reconciled**
- [DQ-ORPHAN-ORDERS](known_issues/DQ-ORPHAN-ORDERS.md) — _medium_ · raw landing `orders` is consumed by no transformation · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_BRAND](known_issues/DQ-UNCLAIMED-CONTOSO5_BRAND.md) — _medium_ · served relation `contoso5_brand` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_CATEGORY_NAME](known_issues/DQ-UNCLAIMED-CONTOSO5_CATEGORY_NAME.md) — _medium_ · served relation `contoso5_category_name` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_CHANNEL](known_issues/DQ-UNCLAIMED-CONTOSO5_CHANNEL.md) — _medium_ · served relation `contoso5_channel` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_COLOR](known_issues/DQ-UNCLAIMED-CONTOSO5_COLOR.md) — _medium_ · served relation `contoso5_color` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_CONTINENT](known_issues/DQ-UNCLAIMED-CONTOSO5_CONTINENT.md) — _medium_ · served relation `contoso5_continent` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_COUNTRY_CODE](known_issues/DQ-UNCLAIMED-CONTOSO5_COUNTRY_CODE.md) — _medium_ · served relation `contoso5_country_code` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_CURRENCY](known_issues/DQ-UNCLAIMED-CONTOSO5_CURRENCY.md) — _medium_ · served relation `contoso5_currency` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_GENDER](known_issues/DQ-UNCLAIMED-CONTOSO5_GENDER.md) — _medium_ · served relation `contoso5_gender` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_MANUFACTURER](known_issues/DQ-UNCLAIMED-CONTOSO5_MANUFACTURER.md) — _medium_ · served relation `contoso5_manufacturer` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_STATE](known_issues/DQ-UNCLAIMED-CONTOSO5_STATE.md) — _medium_ · served relation `contoso5_state` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_STATUS](known_issues/DQ-UNCLAIMED-CONTOSO5_STATUS.md) — _medium_ · served relation `contoso5_status` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_STORE_NAME](known_issues/DQ-UNCLAIMED-CONTOSO5_STORE_NAME.md) — _medium_ · served relation `contoso5_store_name` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-CONTOSO5_SUB_CATEGORY_NAME](known_issues/DQ-UNCLAIMED-CONTOSO5_SUB_CATEGORY_NAME.md) — _medium_ · served relation `contoso5_sub_category_name` is claimed by no concept · **not yet reconciled**
- [DQ-UNCLAIMED-META_OPEN_QUESTION](known_issues/DQ-UNCLAIMED-META_OPEN_QUESTION.md) — _medium_ · served relation `meta_open_question` is claimed by no concept · **not yet reconciled**
