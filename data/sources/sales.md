---
type: Source
title: sales
description: Raw source-of-record — main.sales
resource: table://main.sales
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
| `LineNumber` | integer | PK |  |
| `OrderDate` | timestamp | FK |  |
| `DeliveryDate` | timestamp | FK |  |
| `CustomerKey` | integer | FK |  |
| `StoreKey` | integer | FK |  |
| `ProductKey` | integer | FK |  |
| `Quantity` | integer | value |  |
| `UnitPrice` | decimal | value |  |
| `NetPrice` | decimal | value |  |
| `UnitCost` | decimal | value |  |
| `CurrencyCode` | string | value |  |
| `ExchangeRate` | decimal | value |  |