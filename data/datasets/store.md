---
type: Dataset
title: 'Clean: store'
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
| `StoreKey` | integer | primary_key |
| `StoreCode` | integer | value |
| `GeoAreaKey` | integer | value |
| `CountryCode` | string | discriminator |
| `CountryName` | string | discriminator |
| `State` | string | value |
| `OpenDate` | timestamp | value |
| `CloseDate` | timestamp | value |
| `SquareMeters` | integer | value |
| `Status` | string | discriminator |