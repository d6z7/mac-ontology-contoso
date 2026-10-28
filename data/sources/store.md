---
type: Source
title: store
description: Raw source-of-record — main.store
resource: table://main.store
tags:
- CONTOSO5
- source
- lifecycle:draft
- confidence:Q
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `StoreKey` | integer | PK |  |
| `StoreCode` | integer | value |  |
| `GeoAreaKey` | integer | value |  |
| `CountryCode` | string | value |  |
| `CountryName` | string | value |  |
| `State` | string | value |  |
| `OpenDate` | timestamp | value |  |
| `CloseDate` | timestamp | value |  |
| `Description` | string | value |  |
| `SquareMeters` | integer | value |  |
| `Status` | string | value |  |