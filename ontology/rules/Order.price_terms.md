---
type: Rule
title: Order.price_terms
state: ruled
---

# Order.price_terms

> PROJECTED from `ontology/rules/Order.price_terms.yaml` by tools/mac_rules.py — do not edit; change the yaml.

Four facts on a sale carry every price and cost. The unit price is the regular, list price of one unit before discount; the net price is the actual selling price of one unit after discount; the unit cost is what one unit cost Contoso; the quantity is how many units. Every amount derives from them: gross is quantity times unit price, net is quantity times net price, cost is quantity times unit cost, discount is gross less net, and margin is net less cost — so margin is profit on the discounted price, not on list. "Unit price" names the regular price, not what was paid.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — unit price, list price, net price, selling price, unit cost, gross, net, margin, discount

## What was said

> *"UnitPrice = regular/list price per unit"* — operator, 2026-10-26 (`meaning-as-code#decisions/HANDOVER-2026-10-26_retire-product-prices.md`)


## Examples

| Question | Reading |
|---|---|
| what was the unit price | the regular price before discount, not the price paid |
