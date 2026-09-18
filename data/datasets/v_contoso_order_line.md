---
type: Dataset
title: 'Clean: v_contoso_order_line'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.v_contoso_order_line
tags:
- CONTOSO
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `OrderKey` | bigint | composite_key_part |
| `RowNumber` | integer | composite_key_part |
| `OrderDate` | timestamp | foreign_key |
| `DeliveryDate` | timestamp | foreign_key |
| `CustomerKey` | integer | foreign_key |
| `StoreKey` | integer | foreign_key |
| `ProductKey` | integer | foreign_key |
| `CurrencyCode` | varchar | discriminator |
| `Quantity` | integer | value |
| `UnitPrice` | decimal(20,5) | value |
| `NetPrice` | decimal(20,5) | value |
| `UnitCost` | decimal(20,5) | value |

## Foreign keys
- `ProductKey` → `dim_contoso_product.ProductKey`
- `StoreKey` → `dim_contoso_store.StoreKey`
- `CustomerKey` → `dim_contoso_customer.CustomerKey`
- `OrderDate` → `dim_contoso_calendar_day.Date`
- `DeliveryDate` → `dim_contoso_calendar_day.Date`