---
type: Reference
title: DQ-DANGLINGKEY-CATEGORYKEY — `CategoryKey` is key-shaped and no relation in scope carries it as a key
tags: [reference, guardrail]
---

# DQ-DANGLINGKEY-CATEGORYKEY

*medium · open — nobody has ruled · filed under `dim_product`*

**Finding.** `CategoryKey` is key-shaped and no relation in scope carries it as a key

**About.** `source:product`

**Needs.** Is the parent MISSING from the extract, already INLINE on the row, or is CategoryKey just an attribute? ANSWER ONE OF: inline_dimension | attribute_only | missing_extract. RECOMMENDED: inline_dimension — product.CategoryName carries the SAME 8 distinct value(s) as CategoryKey, dense over 1..8 — the label already travels with the key, so a concept grounds on product and no parent relation is needed at all

**Recommended.** inline_dimension

