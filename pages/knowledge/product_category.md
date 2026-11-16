# ProductCategory

> The human account. The declaration is `ontology/concepts/product_category.yaml`; read this first,
> whole, then compare it against that file.

## Overview

How Contoso groups what it sells: eight categories, each over several of thirty-two
sub-categories, both carried as names on the product row. Read from the distributions: Computers
alone are 43% of net revenue. A2: a controlled set of coded values → `enumeration`, by the same
reading as Brand. A2 lists "Category over Product" under `grouping`, and that branch is checked
AFTER enumeration; eight names with no table of their own are a code list first. THERE IS NO
CATEGORY KEY THAT REACHES ANYTHING. `product.CategoryKey` is key-shaped and points at nothing in
scope — DQ-DANGLINGKEY-CATEGORYKEY, open — so this resolves on the NAME. If that finding is
answered by landing a category relation, this grounding changes. NAMES RESOLVE THROUGH
`data/lookups/contoso5_category_name.lookup.yaml`.

## Identity

Established as `code`.

The canonical key is a COLUMN fact and is not repeated here; this says only HOW identity is
established. Eight category NAMES used as their own key; the key-shaped CategoryKey reaches no
parent.

## Grain

one member per category name — eight, over 2,517 products

## How the set of products in a category is resolved

By the column declaration. `category_name` is declared `identity: canonical` on ProductCategory and
points at its register, so the register's membership IS the set of categories and grouping
`dim_product` on `category_name` reproduces it. The edge `product__belongs_to__product_category`
carries `resolved_by_construction: true`, which `check_edge_definition` verifies against those
declarations rather than accepting as an assertion.

It resolves on the NAME because the key-shaped route is dead: `product.CategoryKey` points at nothing
in scope — **DQ-DANGLINGKEY-CATEGORYKEY, open** — and a join on it returns nothing. That fact belongs
to the finding, where it is recorded, and to the section above.

**There was a rule here and it was retired on 2026-10-06**, with colour's and brand's identical twins.
It said *group `dim_product` on `category_name`*, which the column already says, and forbade resolving
through CategoryKey — a route no query can take, so the prohibition could be neither enforced nor
broken.

## ambiguity.which_level

they are one hierarchy on one row; a list holding both double-counts every sale it touches

The declaration states this executably as well, because this rule has no body yet:

- **when** — sales are broken down by category
- **then** — say which level — eight categories or thirty-two sub-categories
- **never** — mix the two in one breakdown

## Notes carried from the declaration

`key: [category_name]` REMOVED 2026-10-04 — the grain is a COLUMN fact and `category_name` already
declares `identity: canonical` below. Two homes for one grain can disagree;
decisions/PROPOSED-2026-10-02 measured 38 of 38 agreeing and removed `key:` from 17 concepts —
these four were missed.