---
type: Source
title: currencyexchange
description: Raw source-of-record — main.currencyexchange
resource: table://main.currencyexchange
tags:
- CONTOSO5
- source
- lifecycle:draft
- confidence:Q
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `Date` | timestamp | PK |  |
| `FromCurrency` | string | PK |  |
| `ToCurrency` | string | PK |  |
| `Exchange` | decimal | value |  |