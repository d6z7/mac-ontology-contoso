---
type: Source
title: store
description: Raw landing of data/store.parquet, loaded verbatim by setup.sh (CREATE
  TABLE store AS SELECT * FROM read_parquet(...)); contents unmodified. What one row
  means, and whether this relation is served at all, are decided in P2/P3 — not claimed
  here.
resource: table://main.store
tags:
- CONTOSO
- source
- lifecycle:draft
- confidence:I
---

## Columns

| column | type | role |
|---|---|---|
| `StoreKey` | integer | primary_key |
| `StoreCode` | integer | value |
| `GeoAreaKey` | integer | value |
| `CountryCode` | varchar | value |
| `CountryName` | varchar | value |
| `State` | varchar | value |
| `OpenDate` | timestamp | value |
| `CloseDate` | timestamp | value |
| `Description` | varchar | value |
| `SquareMeters` | integer | value |
| `Status` | varchar | value |