---
type: Reference
title: DQ-DANGLINGKEY-GEOAREAKEY — `GeoAreaKey` is key-shaped and no relation in scope carries it as a key
tags: [reference, guardrail]
---

# DQ-DANGLINGKEY-GEOAREAKEY

*medium · open — nobody has ruled · filed under `dim_customer`*

**Finding.** `GeoAreaKey` is key-shaped and no relation in scope carries it as a key

**About.** `source:customer`

**Needs.** Is the parent MISSING from the extract, already INLINE on the row, or is GeoAreaKey just an attribute? ANSWER ONE OF: inline_dimension | attribute_only | missing_extract. NO RECOMMENDATION — no column of customer shares GeoAreaKey's 608 distinct value(s), so it is NOT an inline dimension. Between the remaining two answers the measurement does not lean: whether the absent parent's information is already denormalised beside this key is a question about meaning, not cardinality. What would settle it is a look at customer's other columns — if they already describe what GeoAreaKey points at, it is attribute_only; if nothing does, the extract is incomplete

