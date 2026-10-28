---
type: Index
title: CONTOSO5 served plane
tags:
- CONTOSO5
- datasets
- overview
---


22 relation(s) · 432,322 row(s) measured · 80 column(s) · 11 declared reference(s) · 4 register pointer(s)

| relation | rows | columns | key | references | registers |
|---|---:|---:|---|---:|---:|
| [contoso5_brand](contoso5_brand.md) | 11 | 1 | `code` | 0 | 0 |
| [contoso5_category_name](contoso5_category_name.md) | 8 | 1 | `code` | 0 | 0 |
| [contoso5_channel](contoso5_channel.md) | 2 | 1 | `code` | 0 | 0 |
| [contoso5_color](contoso5_color.md) | 16 | 1 | `code` | 0 | 0 |
| [contoso5_continent](contoso5_continent.md) | 3 | 1 | `code` | 0 | 0 |
| [contoso5_country_code](contoso5_country_code.md) | 9 | 2 | `code` | 0 | 1 |
| [contoso5_currency](contoso5_currency.md) | 5 | 1 | `code` | 0 | 0 |
| [contoso5_gender](contoso5_gender.md) | 2 | 1 | `code` | 0 | 0 |
| [contoso5_manufacturer](contoso5_manufacturer.md) | 11 | 1 | `code` | 0 | 0 |
| [contoso5_state](contoso5_state.md) | 67 | 1 | `code` | 0 | 0 |
| [contoso5_status](contoso5_status.md) | 3 | 1 | `code` | 0 | 0 |
| [contoso5_store_name](contoso5_store_name.md) | 67 | 1 | `code` | 0 | 0 |
| [contoso5_sub_category_name](contoso5_sub_category_name.md) | 32 | 1 | `code` | 0 | 0 |
| [dim_country](dim_country.md) | 9 | 2 | `country_code` | 0 | 1 |
| [dim_currency](dim_currency.md) | 5 | 1 | `currency_code` | 0 | 0 |
| [dim_customer](dim_customer.md) | 104990 | 10 | `customer_key` | 1 | 0 |
| [dim_location](dim_location.md) | 67 | 5 | `location_code` | 1 | 1 |
| [dim_product](dim_product.md) | 2517 | 10 | `product_key` | 0 | 0 |
| [dim_store](dim_store.md) | 74 | 9 | `store_key` | 2 | 0 |
| [meta_open_question](meta_open_question.md) | 0 | 6 | **none measured** | 0 | 0 |
| [v_contoso5_fx_rate](v_contoso5_fx_rate.md) | 100450 | 4 | `date_day` + `from_currency` + `to_currency` | 2 | 0 |
| [v_contoso5_sales_line](v_contoso5_sales_line.md) | 223974 | 19 | `order_key` + `line_number` | 5 | 1 |

**1 relation(s) carry NO measured key** — `meta_open_question`. `mac_references` reads the key and will not derive one, so these are not parent endpoints and an ER model cannot draw them.

