---
type: Reference
title: DQ-DANGLINGKEY-SUBCATEGORYKEY — `SubCategoryKey` is key-shaped and no relation in scope carries it as a key
tags: [reference, guardrail]
---

# DQ-DANGLINGKEY-SUBCATEGORYKEY

*medium · open — nobody has ruled · filed under `dim_product`*

**Finding.** `SubCategoryKey` is key-shaped and no relation in scope carries it as a key

**About.** `source:product`

**Needs.** Is the parent MISSING from the extract, already INLINE on the row, or is SubCategoryKey just an attribute? ANSWER ONE OF: inline_dimension | attribute_only | missing_extract. RECOMMENDED: inline_dimension — product.SubCategoryName carries the SAME 32 distinct value(s) as SubCategoryKey — the label already travels with the key, so a concept grounds on product and no parent relation is needed at all

**Recommended.** inline_dimension

