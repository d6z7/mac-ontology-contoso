---
type: Source
title: currencyexchange
description: Raw landing of data/currencyexchange.parquet, loaded verbatim by setup.sh
  (CREATE TABLE currencyexchange AS SELECT * FROM read_parquet(...)); contents unmodified.
  What one row means, and whether this relation is served at all, are decided in P2/P3
  — not claimed here.
resource: table://main.currencyexchange
tags:
- CONTOSO
- source
- lifecycle:draft
- confidence:C
---

## Columns

| column | type | role | confidence |
|---|---|---|---|
| `Date` | timestamp | composite_key_part |  |
| `FromCurrency` | varchar | composite_key_part |  |
| `ToCurrency` | varchar | composite_key_part |  |
| `Exchange` | decimal(20,5) | value |  |