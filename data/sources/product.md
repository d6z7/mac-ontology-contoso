---
type: Source
title: product
description: Raw landing of data/product.parquet, loaded verbatim by setup.sh (CREATE
  TABLE product AS SELECT * FROM read_parquet(...)); contents unmodified. What one
  row means, and whether this relation is served at all, are decided in P2/P3 — not
  claimed here.
resource: table://main.product
tags:
- CONTOSO
- source
- lifecycle:draft
- confidence:I
---

## Columns

| column | type | role |
|---|---|---|
| `ProductKey` | integer | primary_key |
| `ProductCode` | varchar | value |
| `ProductName` | varchar | value |
| `Manufacturer` | varchar | value |
| `Brand` | varchar | value |
| `Color` | varchar | value |
| `WeightUnit` | varchar | value |
| `Weight` | decimal(20,5) | value |
| `Cost` | decimal(20,5) | value |
| `Price` | decimal(20,5) | value |
| `CategoryKey` | integer | value |
| `CategoryName` | varchar | value |
| `SubCategoryKey` | integer | value |
| `SubCategoryName` | varchar | value |