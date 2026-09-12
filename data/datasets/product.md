---
type: Dataset
title: 'Clean: product'
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
| `ProductKey` | integer | primary_key |
| `ProductCode` | string | value |
| `ProductName` | string | value |
| `Manufacturer` | string | value |
| `Brand` | string | discriminator |
| `Color` | string | value |
| `Weight` | decimal | value |
| `Cost` | decimal | value |
| `Price` | decimal | value |
| `CategoryKey` | integer | value |
| `CategoryName` | string | discriminator |
| `SubCategoryKey` | integer | value |
| `SubCategoryName` | string | discriminator |