---
type: Dataset
title: 'Clean: customer'
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
| `CustomerKey` | integer | primary_key |
| `GeoAreaKey` | integer | value |
| `Continent` | string | discriminator |
| `Country` | string | discriminator |
| `State` | string | value |
| `City` | string | value |
| `Age` | integer | value |