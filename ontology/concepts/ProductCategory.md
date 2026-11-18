# ProductCategory

The account of concept ProductCategory.

## Overview

How Contoso groups what it sells: eight categories, each over several of thirty-two sub-categories, both carried as names on the product row. Read from the distributions: Computers alone are 43% of net revenue. THERE IS NO CATEGORY KEY THAT REACHES ANYTHING. `product.CategoryKey` is key-shaped and points at nothing in scope — DQ-DANGLINGKEY-CATEGORYKEY, open — so this resolves on the NAME. If that finding is answered by landing a category relation, this grounding changes.

## Identity

Eight category NAMES used as their own key; the key-shaped CategoryKey reaches no parent.

## Grain

one member per category name — eight, over 2,517 products

## How the set of products in a category is resolved

By the column declaration.

It resolves on the NAME because the key-shaped route is dead: `product.CategoryKey` points at nothing in scope — **DQ-DANGLINGKEY-CATEGORYKEY, open** — and a join on it returns nothing. That fact belongs to the finding, where it is recorded, and to the section above.

## ProductCategory.level

they are one hierarchy on one row; a list holding both double-counts every sale it touches

- **when** — sales are broken down by category
- **then** — say which level — eight categories or thirty-two sub-categories
- **never** — mix the two in one breakdown

## Cites

- `dataset:dim_product.category_name`
- `dataset:dim_product.sub_category_name`
- `dataset:dim_product.product_key`
- `rule:ProductCategory.level`

## edge product__belongs_to__product_category, from Product

(no notes)
