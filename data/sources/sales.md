---
type: Source
title: sales
description: Raw landing of data/sales.parquet, loaded verbatim by setup.sh (CREATE
  TABLE sales AS SELECT * FROM read_parquet(...)); contents unmodified. What one row
  means, and whether this relation is served at all, are decided in P2/P3 — not claimed
  here.
resource: table://main.sales
tags:
- CONTOSO
- source
- lifecycle:draft
- confidence:I
---

## Columns

| column | type | role |
|---|---|---|
| `OrderKey` | bigint | composite_key_part |
| `LineNumber` | integer | composite_key_part |
| `OrderDate` | timestamp | value |
| `DeliveryDate` | timestamp | value |
| `CustomerKey` | integer | value |
| `StoreKey` | integer | value |
| `ProductKey` | integer | value |
| `Quantity` | integer | value |
| `UnitPrice` | decimal(20,5) | value |
| `NetPrice` | decimal(20,5) | value |
| `UnitCost` | decimal(20,5) | value |
| `CurrencyCode` | varchar | value |
| `ExchangeRate` | decimal(20,5) | value |