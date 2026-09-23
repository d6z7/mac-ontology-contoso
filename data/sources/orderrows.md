---
type: Source
title: orderrows
description: Raw landing of data/orderrows.parquet, loaded verbatim by setup.sh (CREATE
  TABLE orderrows AS SELECT * FROM read_parquet(...)); contents unmodified. What one
  row means, and whether this relation is served at all, are decided in P2/P3 — not
  claimed here.
resource: table://main.orderrows
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
| `RowNumber` | integer | composite_key_part |
| `ProductKey` | integer | value |
| `Quantity` | integer | value |
| `UnitPrice` | decimal(20,5) | value |
| `NetPrice` | decimal(20,5) | value |
| `UnitCost` | decimal(20,5) | value |