# Discount

> The human account. The declaration is `ontology/concepts/discount.yaml`; read this first,
> whole, then compare it against that file.

## Overview

Σ Quantity × (UnitPrice − NetPrice). Money given away in discounts: 13 787 071.00 USD, 5.93% of
gross sales. Declared by the operator's KPI specification of 2026-09-30 and served as
`discount_amount`.

## Grain

one row per sale (order_key, line_number)

## aggregation.percent_is_over_gross

the operator's KPI specification of 2026-09-30 fixes the denominator as gross sales. The two
denominators differ by the discount itself, so the choice is not presentational: 5,93% over gross
against 6,30% over net, on the same money. The `when/then/never` prose this replaces said so in a
sentence nothing executed -- `Intent.denominator` carries the choice and the planner reads it, so
a model naming NetRevenue went straight through unchallenged.

Declared executably: `mac.canon.ratio_select`.
