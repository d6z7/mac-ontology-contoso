---
type: Entity
title: Customer
description: 'A person on Contoso''s customer register: 104,990 of them, each with
  a name, a birth date and a place — continent, country, state, city.'
tags:
- CONTOSO5
- entity
- confidence:I
timestamp: '2026-09-29'
---

# Customer

A person on Contoso's customer register: 104,990 of them, each with a name, a birth date and a place — continent, country, state, city. HALF HAVE NEVER ORDERED: 52,189 of the 104,990 appear on a sale, so the register is not the buyer list. The account is knowledge/customer.md.

## Relationships

- **customer__based_in__country** → [Country](/Country.md) (cardinality 1; grounded join `dim_customer.country_code = dim_country.country_code`)
- inverse of **order__placed_by__customer** ← [Order](/Order.md) (grounded join `v_contoso5_sales_line.customer_key = dim_customer.customer_key`)

# Citations

1. MAC concept source of record: `concepts/customer.yaml` (schema_version 0.3.0-develop, confidence I).
