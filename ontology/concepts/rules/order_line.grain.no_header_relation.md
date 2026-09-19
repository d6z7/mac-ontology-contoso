---
type: Rule
title: An order-grain figure comes from the line, because no header relation is served
description: resolution rule · binds OrderKey
tags:
- mac.rule_kind.resolution
- confidence:P
applies_to: ../order_line.md
---

## Rule

- **Kind** — `resolution`
- **Confidence** — P (proposed)
- **Binds** — `OrderKey`
- **Rule id** — `order_line.grain.no_header_relation`

### When

a question asks about ORDERS rather than order lines — how many orders, orders per month, average order

### Then — do (then)

answer from `{v_contoso_order_line}` by count(DISTINCT `{OrderKey}`) and by grouping on the header attributes the line repeats (`{OrderDate}`, `{DeliveryDate}`, `{CustomerKey}`, `{StoreKey}`, `{CurrencyCode}`), which are functionally determined by `{OrderKey}` (measured)

### Never — don't (never)

joining to an order header relation — none is served (NS-ORDERS-02) — or counting rows of `{v_contoso_order_line}` as orders, which overstates 93 470 orders as 223 974

Applies to [Order Line](../order_line.md).