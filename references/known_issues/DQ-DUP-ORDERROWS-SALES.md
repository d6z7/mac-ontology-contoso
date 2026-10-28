---
type: Reference
title: DQ-DUP-ORDERROWS-SALES — `sales` re-delivers every line of `orderrows` — one fact, twice
tags: [reference, guardrail]
---

# DQ-DUP-ORDERROWS-SALES

*medium · confidence ?*

**Finding.** 223,974 rows each. `sales` carries all but 1 column of `orderrows` (RowNumber is spelled differently there), plus 7: CurrencyCode, CustomerKey, DeliveryDate, ExchangeRate, LineNumber, OrderDate, StoreKey. So `sales` answers at this grain with NO join, and `orderrows` cannot answer at all without a header relation. Only one is served, so the ambiguity is latent rather than live.

**Current handling.** —

**Residual risk.** —

**Resolution.** Not yet reconciled (newly harvested) — an honest open item.

