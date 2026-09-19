---
type: Rule
title: Net is quantity times DISCOUNTED price, per line, then summed
description: aggregation rule · binds Quantity, NetPrice
tags:
- mac.rule_kind.aggregation
- confidence:P
applies_to: ../net_sales_amount.md
---

## Rule

- **Kind** — `aggregation`
- **Confidence** — P (proposed)
- **Binds** — `Quantity`, `NetPrice`
- **Rule id** — `net_sales_amount.derivation.quantity_times_net_price`

### When

computing a net sales figure from `{v_contoso_order_line}`

### Then — do (then)

render the derivation this concept names at `derived_by_rule` — ontology/rules.yaml#rules.net_sales_amount — which multiplies at the declared line grain BEFORE folding over the scope. The order of the two operations is the whole content of this rule; the arithmetic itself is stated there and not here

### Never — don't (never)

using `{UnitPrice}` — that is gross — or SUM(`{NetPrice}`) x SUM(`{Quantity}`), which is not a money figure at any grain

Applies to [Net Sales Amount](../net_sales_amount.md).