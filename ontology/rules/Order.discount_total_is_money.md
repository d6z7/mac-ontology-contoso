---
type: Rule
title: Order.discount_total_is_money
state: ruled
---

# Order.discount_total_is_money

> PROJECTED from `ontology/rules/Order.discount_total_is_money.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A total discount is money: the sum of what was given away below the regular price on every discounted sale in scope. It is never a sum or an average of discount rates. The rate is meant only when the question names it — discount percentage, discount rate, average discount.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Order
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — discount, total discount, discount amount, money off, rebate, discount rate
- **Decided in** — `meaning-as-code#decisions/RULED-2026-10-13_what-a-total-discount-means.md`
- **Formerly** — `Order.discount_amount.total`

## How and where it is implemented

```
  declared at   ontology/relations/v_contoso5_sales_line.yaml#columns.discount_amount.rules
  tested by     (nothing names a question)
```

## What was said

> *"if i ask what is a total discount then i would expect to get THE DISCOUNTED AMOUNT OF MONEY and not %. total discount in 2024 should be refused to answer to the rate ... but it is the SUM of all discounts allowed in 2024 to ALL customers who got discounts"* — operator, 2026-10-13 (`meaning-as-code#decisions/RULED-2026-10-13_what-a-total-discount-means.md`)


## Examples

| Question | Reading |
|---|---|
| what is the total discount in 2024 | discount amount in USD summed over 2024 sales |
