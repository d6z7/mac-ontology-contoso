---
type: Dataset
title: 'Clean: dim_contoso_customer'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_contoso_customer
tags:
- CONTOSO
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `CustomerKey` | integer | primary_key |
| `GeoAreaKey` | integer | value |
| `StartDT` | date | value |
| `EndDT` | date | value |
| `Continent` | varchar | discriminator |
| `CountryFull` | varchar | discriminator |
| `Country` | varchar | discriminator |
| `StateFull` | varchar | discriminator |
| `State` | varchar | discriminator |
| `City` | varchar | discriminator |
| `ZipCode` | varchar | value |
| `Gender` | varchar | discriminator |
| `age_band_5y` | integer | discriminator |