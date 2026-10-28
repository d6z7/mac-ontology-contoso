# Margin

> The human account. The declaration is `ontology/concepts/margin.yaml`; read this first,
> whole, then compare it against that file.

## Overview

Σ Quantity × (NetPrice − UnitCost), identical to Revenue − COGS. Absolute profit: 122 332 211.24
USD. Declared by the operator's KPI specification of 2026-09-30 and served as `margin_amount`.

## Grain

one row per sale (order_key, line_number)

## aggregation.two_named_ratios

the operator's KPI specification of 2026-09-30 names both ratios and their denominators. They
differ by more than a factor of two on the same profit -- 55,91% over net against 126,79% over
cost -- so naming one and computing the other is a wrong answer that looks right. NO `default` IS
DECLARED, DELIBERATELY: the prose this replaces said "never use one name for the other", and a
question saying only "margin" names neither, so the honest outcome is to ask with both offered
rather than to pick the commoner reading.

Declared executably: `mac.canon.ratio_select`.
