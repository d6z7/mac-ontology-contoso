---
type: Dataset
title: 'Clean: dim_contoso_store'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_contoso_store
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
| `CountryCode` | varchar | discriminator |
| `CountryName` | varchar | discriminator |
| `State` | varchar | discriminator |
| `Description` | varchar | value |
| `OpenDate` | date | value |
| `CloseDate` | date | value |
| `SquareMeters` | integer | value |
| `Status` | varchar | discriminator |