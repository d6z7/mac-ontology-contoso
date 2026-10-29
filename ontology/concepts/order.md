---
type: Event
title: Order
description: One customer's purchase on one date, counted by distinct `order_key` over the line relation.
tags:
- CONTOSO5
- event
- confidence:C
---

One customer's purchase on one date, counted by distinct `order_key` over the line relation. It is also THE FACT NODE of the sales line, one row per order line - every money and quantity measure (net, gross, cost, discount, margin, units, and the per-unit prices) is a column it serves, and every edge from the sale to a dimension starts here. The account is knowledge/order.md.

## Details

- **Version** — 1.1
- **Schema version** — 0.3.1-develop
- **Governance owner** — operator
- **Last reviewed** — 2026-09-30

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

**Default reading** — A QUESTION THAT NAMES NO PERIOD COVERS ALL TIME — operator ruling, 2026-09-30. No implied "this year" and no implied latest month. The extent is `{order_date}` from 2016-05-18 to 2025-12-31; deliveries run six days further, to 2026-01-06. State the window the answer actually covered, because an unscoped total and a year-to-date total are indistinguishable from the figure alone.

## Grounded in

- `v_contoso5_sales_line` — key `order_key`, `line_number` — semantics: [`ontology/relations/v_contoso5_sales_line.yaml`](../relations/v_contoso5_sales_line.md)

## Grain

- One row is one Order, identified by `order_key`, `line_number`.

## Fields

| column | type | role | identity | measure | rulings | register | description | joins → |
|---|---|---|---|---|---|---|---|---|
| `order_key` | integer | key | — | — | — | — | — | — |
| `line_number` | integer | key | — | — | — | — | — | — |
| `order_date` | date | period | — | — | — | — | — | [Exchange Rate](exchange_rate.md) _(business)_ |
| `delivery_date` | date | dimension | — | — | — | — | — | — |
| `customer_key` | integer | key | -> Customer | — | — | — | — | [Customer](customer.md) |
| `store_key` | integer | key | -> Store | — | — | — | — | [Store](store.md) |
| `product_key` | integer | key | -> Product | — | — | — | — | [Product](product.md) |
| `currency_code` | string | dimension | — | — | — | — | — | [Currency](currency.md) |
| `quantity` | integer | measure | — | flow · units | — | — | — | — |
| `net_amount` | decimal | measure | — | flow · USD · **default** | — | — | — | — |
| `gross_amount` | decimal | measure | — | flow · USD | — | — | — | — |
| `cost_amount` | decimal | measure | — | flow · USD | — | — | — | — |
| `discount_amount` | decimal | measure | — | flow · USD | — | — | — | — |
| `margin_amount` | decimal | measure | — | flow · USD | — | — | — | — |
| `unit_price` | decimal | measure | — | intensive · USD | — | — | — | — |
| `net_price` | decimal | measure | — | intensive · USD | — | — | — | — |
| `unit_cost` | decimal | measure | — | intensive · USD | — | — | — | — |

_Declared per column, over 17 columns: type 17 of 17 · role 17 of 17 · identity 3 of 17 · measure 9 of 17 · rulings 0 of 17 · register 0 of 17 · description 0 of 17 · joins → 5 of 17. An em dash is a column for which nothing is declared._

## Axes

Measure type: `flow`.

| axis | axis kind | fold |
|---|---|---|
| `currency_code` | categorical | additive |
| `customer_key` | categorical | additive |
| `delivery_date` | time | additive |
| `order_date` | time | additive |
| `product_key` | categorical | additive |
| `store_key` | categorical | additive |

_The fold is read from the framework registry (`measure_type.<type>.additivity.<axis kind>`), not declared on this concept. An em dash means the crossing is not declared there._

## Relationships


*6 join(s) out · 0 in — click a concept to open it.*

**Joins to** — this concept references:

- [Country](country.md) — joined on `sale_country_code`
- [Currency](currency.md) — joined on `currency_code`
- [Customer](customer.md) — joined on `customer_key`
- [Exchange Rate](exchange_rate.md) — joined on `order_date`
- [Product](product.md) — joined on `product_key`
- [Store](store.md) — joined on `store_key`

## Source of record

- Full MAC concept: `order.yaml` — open the **YAML** tab for the complete typed definition.
