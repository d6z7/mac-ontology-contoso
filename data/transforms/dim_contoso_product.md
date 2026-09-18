---
type: Transform
title: 'Cleansing: dim_contoso_product'
description: Cleansing → contoso_served.dim_contoso_product
relation: contoso_served.dim_contoso_product
tags:
- CONTOSO
- transform
- lifecycle:draft
sql_file: data/transforms/dim_contoso_product.sql
---

Produces `contoso_served.dim_contoso_product` · grain: one row per ProductKey — one product

## Rules
### case_variant_vocabulary — `canonicalise-colour-case` · authored
- **defect** Color is a closed vocabulary drifting by case: 17 spellings over 16 colours, 0 nulls, and exactly one case-insensitive group carrying more than one spelling — Blue on 197 rows and blue on 3 (T6a, T6b; P1 #7). A GROUP BY Color therefore reports one colour as two groups.

- **rule** Fold every spelling onto the most-used spelling of its case-insensitive group, with the canonical spelling MEASURED from the data (color_spelling counts each spelling, color_canon keeps the majority one per lower(Color)) rather than transcribed as a hand-written value list. A lower() or title-case fold was refused: 14 of the 17 spellings contain a space ('Silver Grey'), which a per-word title-case fold corrupts, and DuckDB 1.5.5 has no initcap at all (measured).

- **guarantee** One spelling per colour in the served relation: 16 distinct values over 2 517 rows, 3 rows respelled, and the fold cannot fan the dimension out — color_canon holds 16 rows / 16 distinct keys and the LEFT JOIN returns 2 517 rows for 2 517 in (T6c). A consumer may GROUP BY Color and count colours without case-folding it first.


### absence_semantics — `empty-string-is-missing` · authored
- **defect** WeightUnit spells missing as '' on 222 of 2 517 rows and never as NULL, so the delivery has two spellings of absence across its relations (store.Status is the other) and a consumer testing `IS NULL` finds none of them. The 222 are exactly the rows whose Weight is null (T7; P1 #6).

- **rule** Read '' as absent: nullif the empty string to NULL. No value is invented for the 222 rows.
- **guarantee** Missing is spelled exactly one way — NULL on 222 of 2 517 rows — and the served vocabulary is the 3 real units (pounds, ounces, grams), so `count(DISTINCT WeightUnit)` returns 3 rather than 4 and `WHERE WeightUnit IS NULL` finds every row that has no unit (T7).


## Open — needs SME
- **contradictory_pair** NONE until the meaning is ruled. If the weight is MISSING, the unit is a promise the data cannot keep and both columns should read absent; if it is NOT APPLICABLE (a product that is not weighed), the unit is meaningful and nothing is wrong. The two rulings imply opposite SQL, and neither can be derived from the data.
 _(PROPOSED)_

## Lineage
- Source: [product](../sources/product.md)
- Clean dataset: [dim_contoso_product](../datasets/dim_contoso_product.md)

## SQL realization
Realized by `dim_contoso_product.sql` (a deployed `CREATE VIEW`) — open it with the **SQL** button in the header, or in the Source browser.

## Lineage (column-level)

`contoso_served.dim_contoso_product` · kinds: passthrough

| output column | ← from | rule | kind |
|---|---|---|---|
| `Color` | `product.Color` | canonicalise-colour-case | passthrough |
| `WeightUnit` | `product.WeightUnit` | empty-string-is-missing | passthrough |
| `ProductKey` | `product.ProductKey` | None | passthrough |
| `ProductCode` | `product.ProductCode` | None | passthrough |
| `ProductName` | `product.ProductName` | None | passthrough |
| `Manufacturer` | `product.Manufacturer` | None | passthrough |
| `Brand` | `product.Brand` | None | passthrough |
| `Weight` | `product.Weight` | None | passthrough |
| `Cost` | `product.Cost` | None | passthrough |
| `Price` | `product.Price` | None | passthrough |
| `CategoryKey` | `product.CategoryKey` | None | passthrough |
| `CategoryName` | `product.CategoryName` | None | passthrough |
| `SubCategoryKey` | `product.SubCategoryKey` | None | passthrough |
| `SubCategoryName` | `product.SubCategoryName` | None | passthrough |