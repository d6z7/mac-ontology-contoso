---
type: Reference
title: DQ-DUP-ORDERROWS-SALES — `sales` re-delivers every line of `orderrows` — one fact, twice
tags: [reference, guardrail]
---

# DQ-DUP-ORDERROWS-SALES

*medium · open — nobody has ruled · filed under `v_contoso5_sales_line`*

**Finding.** `sales` re-delivers every line of `orderrows` — one fact, twice

**About.** `source:orderrows`

**Needs.** Which is the FACT OF RECORD? ANSWER ONE OF: orderrows | sales | both_are_distinct_facts | neither_serve_a_transform. RECOMMENDED: serve exactly ONE — see the ruling.

**Recommended.** serve exactly ONE of them

