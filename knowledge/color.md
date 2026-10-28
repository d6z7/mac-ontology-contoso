# Color

> The human account. The declaration is `ontology/concepts/color.yaml`; read this first,
> whole, then compare it against that file.

## Overview

The colour a product comes in: sixteen values on the served row, and the one attribute that on its
own makes a new SKU — "E400 Green" and "E400 Orange" are two products. A2: a controlled set of
coded values → `enumeration`. WHY IT IS A CONCEPT. "Green MP3 players" is how a question reaches a
product. Nobody says a SKU's name. SIXTEEN, AND THE FOLD HAPPENS UPSTREAM. The landing row carried
both `Blue` (197) and `blue` (3); `data/transforms/dim_product.sql` capitalises the first letter,
so the served `color` holds `Blue` 200 and sixteen members in total — operator's ruling of
2026-09-30, taken as a rule about capitalisation rather than a patch naming one value. Measured on
the served plane 2026-10-02: 16 distinct, 0 case variants, and `color = 'blue'` returns 0 rows.
Nothing is folded at read time, and these rules must not ask for it. NAMES RESOLVE THROUGH
`data/lookups/contoso5_color.lookup.yaml`.

## Identity

Established as `code`.

The canonical key is a COLUMN fact and is not repeated here; this says only HOW identity is
established. Sixteen colour NAMES used as their own key.

## Grain

one member per colour name — sixteen, stored and meant

## How the set of products carrying a colour is resolved

By the column declaration, and by nothing else. `color` is declared `identity: canonical` on Colour
and points at the register `contoso5_color.lookup.yaml`, so the register's membership IS the set of
colours and grouping the served `dim_product` on `color` reproduces it exactly. The edge
`product__comes_in__color` says so in one word — `resolved_by_construction: true` — which
`check_edge_definition` verifies rather than takes on trust.

**There was a rule here and it was retired on 2026-10-06**, with `brand`'s identical twin before it
(2026-10-05, *"the column already runs it"*). It said *group the served `dim_product` on `color`* —
which is what the column declaration already says — and forbade reading `main.product."Color"`, a
relation **outside the served schema**: `connection.yaml` serves `contoso_served`, so the rule was
unenforceable and unviolatable at once. The colour fold itself is the transform's guarantee and lives
in its lineage; what a reader needs to know about it is the section below.

## ambiguity.blue_is_spelled_twice

the landing row spells it two ways and the transform folds it; a breakdown that lists both is off
by a line, which is what RC03 measured at 17 against an approved 16

The declaration states this executably as well, because this rule has no body yet:

- **when** — a question asks about blue products, or breaks products down by colour
- **then** — answer over the served `color`, where the two spellings are already one member
- **never** — report `Blue` and `blue` as two colours

## Notes carried from the declaration

`key: [color]` REMOVED 2026-10-04 — the grain is a COLUMN fact and `color` already declares
`identity: canonical` below. Two homes for one grain can disagree; decisions/PROPOSED-2026-10-02
measured 38 of 38 agreeing and removed `key:` from 17 concepts — these four were missed.
