---
type: Rule
title: ProductCategory.level
state: proposed
---

# ProductCategory.level

> PROJECTED from `ontology/rules/ProductCategory.level.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A product category is the top level of the product hierarchy. A question saying category is answered on the category; one saying sub-category is answered on the sub-category.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — ProductCategory
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — category, sub-category, product category, hierarchy, level
- **Formerly** — `product_category.ambiguity.which_level`

## How and where it is implemented

```
  declared at   ontology/concepts/product_category.yaml#readings.level
  realized by   mac.canon.column_select  (kind default)   default: category
                category: column: category_name
                sub_category: column: sub_category_name
  executed by   canons/column_select.py + planner/columns.py — WHICH COLUMN OR JOIN PATH a named reading resolves to. The third member of the family population_select and ratio
  tested by     ADV-14  'Revenue from products in the Electronics category sold in German stores'  board: not_established (stale)
```
