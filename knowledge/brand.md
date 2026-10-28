# Brand

> The human account. The declaration is `ontology/concepts/brand.yaml`; read this first,
> whole, then compare it against that file.

## Overview

Whose name a product is sold under: eleven names, carried as a column on the product row with no
table and no key of their own. A2, top to bottom: not an event, not a measure; "a controlled set
of allowed coded values" — yes, eleven of them, and A2 says take the first branch that fits. So
`enumeration`, checked before `grouping`. The leaner bundle calls this a grouping; A2's own
tie-breaker — "a small fixed code set with no attributes of its own → enumeration" — decides it
the other way, and the log records the disagreement rather than copying the neighbour. WHY IT IS A
CONCEPT AT ALL. "Contoso products" is something a question says. As a column flag inside Product
it resolves against nothing; as a concept with a register it resolves offline — and, because
Product grounds the same column, Product's own names are reached THROUGH it. IT IS NOT THE
MANUFACTURER. Both are eleven-member sets on the same row and most names appear in both: a brand
is what the customer sees, a manufacturer is who made it. NAMES RESOLVE THROUGH
`data/lookups/contoso5_brand.lookup.yaml`.

## Identity

Established as `code`.

The canonical key is a COLUMN fact and is not repeated here; this says only HOW identity is
established. Eleven brand NAMES used as their own key — a closed set with no surrogate and no
relation behind it.

## Grain

one member per brand name — eleven, over 2,517 products

## resolution.by_grouping_products

none exists, and inventing one gives eleven names a surrogate the warehouse does not have

The declaration states this executably as well, because this rule has no body yet:

- **when** — the set of products carrying one brand is needed
- **then** — group dim_product on `brand`. The relation is computed — there is no brand table and no brand key, so the instance set IS the distinct names on the product row.
- **never** — join to a brand relation

## exclusion.is_not_manufacturer

The declaration states this executably as well, because this rule has no body yet:

- **when** — a question asks who is behind a product
- **then** — decide whether it means the brand the customer buys or the manufacturer, and say which
- **never** — treat the two columns as interchangeable because their member sets overlap

## Notes carried from the declaration

`key: [brand]` REMOVED 2026-10-04 — the grain is a COLUMN fact and `brand` already declares
`identity: canonical` below. Two homes for one grain can disagree; decisions/PROPOSED-2026-10-02
measured 38 of 38 agreeing and removed `key:` from 17 concepts — these four were missed.