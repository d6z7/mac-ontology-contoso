---
type: Dataset
title: 'Clean: dim_contoso_product'
description: AI-friendly clean shape the ontology binds to
relation: contoso_served.dim_contoso_product
tags:
- CONTOSO
- dataset
- lifecycle:draft
---

## Columns

| column | type | role |
|---|---|---|
| `ProductKey` | integer | primary_key |
| `ProductCode` | varchar | value |
| `ProductName` | varchar | value |
| `Manufacturer` | varchar | discriminator |
| `Brand` | varchar | discriminator |
| `Color` | varchar | discriminator |
| `WeightUnit` | varchar | discriminator |
| `Weight` | decimal(20,5) | value |
| `Cost` | decimal(20,5) | value |
| `Price` | decimal(20,5) | value |
| `CategoryKey` | integer | value |
| `CategoryName` | varchar | discriminator |
| `SubCategoryKey` | integer | value |
| `SubCategoryName` | varchar | discriminator |