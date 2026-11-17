---
type: DQ Issue
title: '`sales` re-delivers every line of `orderrows` — one fact, twice'
description: '`sales` re-delivers every line of `orderrows` — one fact, twice'
tags:
- Contoso 5
- severity:medium
- disposition:open
---

`DQ-DUP-ORDERROWS-SALES` · severity **medium** · disposition **open — nobody has ruled** · filed under [v_contoso5_sales_line](../datasets/v_contoso5_sales_line.md)

## Finding

`sales` re-delivers every line of `orderrows` — one fact, twice

## About

- `source:orderrows`

## Needs

**Needs** — Which is the FACT OF RECORD? ANSWER ONE OF: orderrows | sales | both_are_distinct_facts | neither_serve_a_transform. RECOMMENDED: serve exactly ONE — see the ruling.

**Remedies**

- orderrows: the normalised detail is the record, and every question at this grain must JOIN a header relation to reach the attributes `sales` already carries. `sales` must STOP being served, or the ambiguity remains whatever is declared.
- sales: the pre-joined relation is the record and answers with no join, including the 7 attributes the normalised route reaches only through a header. `orderrows` must stop being served.
- both_are_distinct_facts: each is declared a fact in its own right, which requires a reason the measurement contradicts — they agree row for row — and every total over them becomes a sum a reader must know not to take twice.
- neither_serve_a_transform: a curated relation is authored over one of them and BOTH landings stop being served — the route a curated bundle took, which is available here and is what the passthrough cannot do for you.

**Recommended** — serve exactly ONE of them

## Disposition

**open**.
- said by **mac_dq_findings.py/1**

## Repaired by

_No transform's `repairs` names this finding._

## Blocks and waives

_It blocks and waives nothing._

## Evidence

- 223,974 rows each. `sales` carries all but 1 column of `orderrows` (RowNumber is spelled differently there), plus 7: CurrencyCode, CustomerKey, DeliveryDate, ExchangeRate, LineNumber, OrderDate, StoreKey. So `sales` answers at this grain with NO join, and `orderrows` cannot answer at all without a header relation. Only one is served, so the ambiguity is latent rather than live.
