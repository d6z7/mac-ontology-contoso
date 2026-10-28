---
type: Source
title: orderrows
description: Raw source-of-record — main.orderrows
resource: table://main.orderrows
tags:
- CONTOSO5
- source
- lifecycle:draft
- confidence:Q
---

## Columns

| column | type | role | reference |
|---|---|---|---|
| `OrderKey` | integer | PK |  |
| `RowNumber` | integer | PK |  |
| `ProductKey` | integer | FK |  |
| `Quantity` | integer | value |  |
| `UnitPrice` | decimal | value |  |
| `NetPrice` | decimal | value |  |
| `UnitCost` | decimal | value |  |