---
type: Transform
title: 'Cleansing: v_contoso_fx_rate_day'
description: Cleansing → contoso_served.v_contoso_fx_rate_day
relation: contoso_served.v_contoso_fx_rate_day
tags:
- CONTOSO
- transform
- lifecycle:draft
sql_file: data/transforms/v_contoso_fx_rate_day.sql
---

Produces `contoso_served.v_contoso_fx_rate_day` · grain: one row per (Date, FromCurrency, ToCurrency) — one daily quote for one ordered currency pair

## Rules
## Lineage
- Source: [currencyexchange](../sources/currencyexchange.md)
- Clean dataset: [v_contoso_fx_rate_day](../datasets/v_contoso_fx_rate_day.md)

## SQL realization
Realized by `v_contoso_fx_rate_day.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.