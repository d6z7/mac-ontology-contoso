---
type: Source
title: orders
description: Raw source-of-record — main.orders
resource: table://main.orders
tags:
- CONTOSO5
- source
- lifecycle:draft
- confidence:Q
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `OrderKey` | integer | PK |  |
| `CustomerKey` | integer | FK |  |
| `StoreKey` | integer | FK |  |
| `DT` | timestamp | FK |  |
| `DeliveryDate` | timestamp | FK |  |
| `CurrencyCode` | string | value |  |