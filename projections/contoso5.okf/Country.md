---
type: Enumeration
title: Country
description: A country Contoso sells in — 8 of them, plus one `--` sentinel that is
  not a place.
tags:
- CONTOSO5
- enumeration
- confidence:I
timestamp: '2026-09-30'
---

# Country

A country Contoso sells in — 8 of them, plus one `--` sentinel that is not a place. The account is knowledge/country.md.

## Relationships

- inverse of **customer__based_in__country** ← [Customer](/Customer.md) (grounded join `dim_customer.country_code = dim_country.country_code`)
- inverse of **store__trades_in__country** ← [Store](/Store.md) (grounded join `dim_store.country_code = dim_country.country_code`)
- inverse of **location__in__country** ← [Location](/Location.md) (grounded join `dim_location.country_code = dim_country.country_code`)
- inverse of **order__attributed_to__country** ← [Order](/Order.md) (grounded join `v_contoso5_sales_line.sale_country_code = dim_country.country_code`)

# Citations

1. MAC concept source of record: `concepts/country.yaml` (schema_version 0.3.0-develop, confidence I).
