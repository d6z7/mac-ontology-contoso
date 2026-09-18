---
type: Doc
title: Issues & inconsistencies
description: 4 findings — the full overview
tags:
- CONTOSO
- overview
---

Everything the harvest + reconciliation found for this source: **4 findings** across 8 tables.

- **Severity** — 0 high · 1 medium · 3 low
- **Resolution** — 1 ✓ resolved · 0 ◐ partial · 0 ⚠ open gap · 3 not yet reconciled (newly harvested)

## All findings

| severity | finding | table | impurity | resolution |
|---|---|---|---|---|
| medium | [15 leftover views in the warehouse, measured, neither treated as](NS-SERVING-01.md) | — |  | not yet reconciled  |
| low | [`sales` measured, deliberately not served — it is the served ord](NS-ORDERS-01.md) | sales |  | ✓ resolved `v_contoso_order_line` |
| low | [the order header measured, deliberately not served as a relation](NS-ORDERS-02.md) | orders |  | not yet reconciled  |
| low | [12 of the 24 customer columns measured, deliberately not served](NS-CUSTOMER-01.md) | customer |  | not yet reconciled  |

_Full narrative: [RECONCILIATION](RECONCILIATION.md)._