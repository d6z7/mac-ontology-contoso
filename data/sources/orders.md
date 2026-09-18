---
type: Source
title: orders
description: Raw landing of data/orders.parquet, loaded verbatim by setup.sh (CREATE
  TABLE orders AS SELECT * FROM read_parquet(...)); contents unmodified. What one
  row means, and whether this relation is served at all, are decided in P2/P3 — not
  claimed here.
resource: table://main.orders
tags:
- CONTOSO
- source
- lifecycle:draft
- confidence:C
---

## Columns

| column | type | role | confidence |
|---|---|---|---|
| `OrderKey` | bigint | primary_key |  |
| `CustomerKey` | integer | value |  |
| `StoreKey` | integer | value |  |
| `DT` | timestamp | value |  |
| `DeliveryDate` | timestamp | value |  |
| `CurrencyCode` | varchar | value |  |