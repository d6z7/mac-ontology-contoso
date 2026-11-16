# Product

> The human account. The declaration is `ontology/concepts/product.yaml`; read this first,
> whole, then compare it against that file.

## Overview

A thing Contoso sells, at the level the shelf knows it: a SKU. 2,517 of them. Read from the rows —
"Contoso 4G MP3 Player E400 Green" and "... E400 Orange" are two product keys — so a product here
is a colour variant of a model, and the name carries brand, capacity, type, model and colour all
at once.

Operator ruling, 2026-10-26: Product carries **no served price and no served cost**. The source
has `main.product.Price` / `main.product.Cost`, but those are deliberately not promoted: they are
undated standing values, while questions about money must read dated sales-line facts
(`unit_price`, `net_price`, `unit_cost`) on `v_contoso5_sales_line`.

## Identity

Established as `fk_name`.

The canonical key is a COLUMN fact and is not repeated here; this says only HOW identity is
established. A surrogate `product_key` annotated by `product_name` and `product_code`, both 1:1
with it and neither the identity.

## Grain

one row per product (`product_key`)

## Price and cost

A product's money facts are reached over its FK to sales lines. For "current price", the standing
reading is the product's **latest line `unit_price`** (with its date disclosed where needed), not
an undated catalogue column on Product.
