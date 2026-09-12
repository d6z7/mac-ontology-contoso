---
type: Dataset
title: 'Clean: sales'
description: AI-friendly clean shape the ontology binds to
relation: null
tags:
- CONTOSO
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `OrderKey` | bigint | foreign_key |
| `LineNumber` | integer | value |
| `OrderDate` | timestamp | value |
| `DeliveryDate` | timestamp | value |
| `CustomerKey` | integer | foreign_key |
| `StoreKey` | integer | foreign_key |
| `ProductKey` | integer | foreign_key |
| `Quantity` | integer | value |
| `UnitPrice` | decimal | value |
| `NetPrice` | decimal | value |
| `UnitCost` | decimal | value |
| `CurrencyCode` | string | discriminator |
| `ExchangeRate` | decimal | value |

## Foreign keys
- `ProductKey` → `product.ProductKey`
- `StoreKey` → `store.StoreKey`
- `CustomerKey` → `customer.CustomerKey`
- `OrderKey` → `orders.OrderKey`