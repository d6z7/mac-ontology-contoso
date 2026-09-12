---
type: Dataset
title: 'Clean: orders'
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
| `OrderKey` | bigint | primary_key |
| `CustomerKey` | integer | foreign_key |
| `StoreKey` | integer | foreign_key |
| `DT` | timestamp | value |
| `DeliveryDate` | timestamp | value |
| `CurrencyCode` | string | discriminator |

## Foreign keys
- `CustomerKey` → `customer.CustomerKey`
- `StoreKey` → `store.StoreKey`