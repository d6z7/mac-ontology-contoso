---
type: Dataset
title: 'Clean: orderrows'
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
| `RowNumber` | integer | value |
| `ProductKey` | integer | foreign_key |
| `Quantity` | integer | value |
| `UnitPrice` | decimal | value |
| `NetPrice` | decimal | value |
| `UnitCost` | decimal | value |

## Foreign keys
- `OrderKey` → `orders.OrderKey`
- `ProductKey` → `product.ProductKey`