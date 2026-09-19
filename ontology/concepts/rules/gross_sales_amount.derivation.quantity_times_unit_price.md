---
type: Rule
title: Gross is quantity times LIST price, per line, then summed
description: aggregation rule · binds Quantity, UnitPrice
tags:
- mac.rule_kind.aggregation
- confidence:P
applies_to: ../gross_sales_amount.md
---

## Rule

- **Kind** — `aggregation`
- **Confidence** — P (proposed)
- **Binds** — `Quantity`, `UnitPrice`
- **Rule id** — `gross_sales_amount.derivation.quantity_times_unit_price`

### When

computing a gross sales figure from `{v_contoso_order_line}`

### Then — do (then)

render the derivation this concept names at `derived_by_rule` — ontology/rules.yaml#rules.gross_sales_amount — which multiplies at the declared line grain BEFORE folding over the scope. The order of the two operations is the whole content of this rule; the arithmetic itself is stated there and not here

### Never — don't (never)

SUM(`{UnitPrice}`) x SUM(`{Quantity}`), or SUM(`{UnitPrice}`) alone — a price is per unit and summing prices across lines is not a money figure

Applies to [Gross Sales Amount](../gross_sales_amount.md).