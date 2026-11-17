---
type: DQ Issue
title: '`SubCategoryKey` is key-shaped and no relation in scope carries it as a key'
description: '`SubCategoryKey` is key-shaped and no relation in scope carries it as
  a key'
tags:
- Contoso 5
- severity:medium
- disposition:open
---

`DQ-DANGLINGKEY-SUBCATEGORYKEY` · severity **medium** · disposition **open — nobody has ruled** · filed under [dim_product](../datasets/dim_product.md)

## Finding

`SubCategoryKey` is key-shaped and no relation in scope carries it as a key

## About

- `source:product`

## Needs

**Needs** — Is the parent MISSING from the extract, already INLINE on the row, or is SubCategoryKey just an attribute? ANSWER ONE OF: inline_dimension | attribute_only | missing_extract. RECOMMENDED: inline_dimension — product.SubCategoryName carries the SAME 32 distinct value(s) as SubCategoryKey — the label already travels with the key, so a concept grounds on product and no parent relation is needed at all

**Remedies**

- inline_dimension: a concept is grounded on the carrying relation, using the key for identity and its twin for the label; no parent relation is ever needed and no line is drawn
- attribute_only: SubCategoryKey is an opaque identifier and nothing groups by it — questions use the denormalised attributes beside it instead
- missing_extract: the extract is incomplete and it is recorded as such; until the dimension arrives, anything grouped by this key can report only opaque values, and every answer over it must say so

**Recommended** — inline_dimension

## Disposition

**open**.
- said by **mac_dq_findings.py/1**

## Repaired by

_No transform's `repairs` names this finding._

## Blocks and waives

_It blocks and waives nothing._

## Evidence

- reported on 1 plane-relation(s) (product 32 distinct); 32 distinct value(s) on product. It follows this bundle's own key-naming convention and points at nothing.
