---
type: Source
title: customer
description: Raw landing of data/customer.parquet, loaded verbatim by setup.sh (CREATE
  TABLE customer AS SELECT * FROM read_parquet(...)); contents unmodified. What one
  row means, and whether this relation is served at all, are decided in P2/P3 — not
  claimed here.
resource: table://main.customer
tags:
- CONTOSO
- source
- lifecycle:draft
- confidence:I
---

## Columns

| column | type | role |
|---|---|---|
| `CustomerKey` | integer | primary_key |
| `GeoAreaKey` | integer | value |
| `StartDT` | timestamp | value |
| `EndDT` | timestamp | value |
| `Continent` | varchar | value |
| `Gender` | varchar | value |
| `Title` | varchar | value |
| `GivenName` | varchar | value |
| `MiddleInitial` | varchar | value |
| `Surname` | varchar | value |
| `StreetAddress` | varchar | value |
| `City` | varchar | value |
| `State` | varchar | value |
| `StateFull` | varchar | value |
| `ZipCode` | varchar | value |
| `Country` | varchar | value |
| `CountryFull` | varchar | value |
| `Birthday` | timestamp | value |
| `Age` | integer | value |
| `Occupation` | varchar | value |
| `Company` | varchar | value |
| `Vehicle` | varchar | value |
| `Latitude` | decimal(20,5) | value |
| `Longitude` | decimal(20,5) | value |