---
type: Rule
title: Product.price_is_dated
state: ruled
---

# Product.price_is_dated

> PROJECTED from `ontology/rules/Product.price_is_dated.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A product carries no standing price and no standing cost. A price changes over time, so every price and cost is the one on the sale, dated by the sale, and a product's price is reached through its sales. A product's current price is the regular unit price on its latest sale, stated with that sale's date where it matters. A question qualifying products by price — high-value products — selects products by that price and then counts all their sales, never qualifies individual sale lines.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Product, Order
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — product price, current price, list price, catalogue price, high-value products, cost
- **Decided in** — `meaning-as-code#decisions/HANDOVER-2026-10-26_retire-product-prices.md`

## Examples

| Question | Reading |
|---|---|
| Revenue from high-value products (Price > 1000) | products whose latest-sale unit price is above the threshold, revenue over all their sales |
