---
type: Transform
title: 'Cleansing: v_contoso5_fx_rate'
description: Cleansing → contoso_served.v_contoso5_fx_rate
relation: contoso_served.v_contoso5_fx_rate
tags:
- CONTOSO5
- transform
- lifecycle:draft
sql_file: data/transforms/v_contoso5_fx_rate.sql
---

Produces `contoso_served.v_contoso5_fx_rate` · grain: —

## Rules
## Lineage
- Source: [currencyexchange](../sources/currencyexchange.md)
- Clean dataset: [v_contoso5_fx_rate](../datasets/v_contoso5_fx_rate.md)

## SQL realization
Realized by `v_contoso5_fx_rate.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.v_contoso5_fx_rate` · kinds: passthrough + transform

| output column | ← from | rule | kind |
|---|---|---|---|
| `date_day` | `currencyexchange.Date` → _CAST(x.Date AS DATE)_ |  | transform |
| `from_currency` | `currencyexchange.FromCurrency` |  | passthrough |
| `to_currency` | `currencyexchange.ToCurrency` |  | passthrough |
| `rate` | `currencyexchange.Exchange` |  | passthrough |