---
type: Index
title: Contoso 5 served plane
tags:
- Contoso 5
- datasets
- overview
---

21 dataset(s); rows are measured (`data/profiles`), `?` = not measured.

| dataset | stored | rows | columns | key | concepts | findings |
|---|---|---:|---:|---|---:|---:|
| [contoso5_brand](contoso5_brand.md) | file | 11 | 1 | `code` | 0 | 4 |
| [contoso5_category_name](contoso5_category_name.md) | file | 8 | 1 | `code` | 0 | 4 |
| [contoso5_channel](contoso5_channel.md) | file | 2 | 1 | `code` | 0 | 4 |
| [contoso5_color](contoso5_color.md) | file | 16 | 1 | `code` | 0 | 4 |
| [contoso5_continent](contoso5_continent.md) | file | 3 | 1 | `code` | 0 | 4 |
| [contoso5_country_code](contoso5_country_code.md) | file | 9 | 2 | `code` | 0 | 4 |
| [contoso5_currency](contoso5_currency.md) | file | 5 | 1 | `code` | 0 | 4 |
| [contoso5_gender](contoso5_gender.md) | file | 2 | 1 | `code` | 0 | 4 |
| [contoso5_manufacturer](contoso5_manufacturer.md) | file | 11 | 1 | `code` | 0 | 4 |
| [contoso5_state](contoso5_state.md) | file | 67 | 1 | `code` | 0 | 4 |
| [contoso5_status](contoso5_status.md) | file | 2 | 1 | `code` | 0 | 3 |
| [contoso5_store_name](contoso5_store_name.md) | file | 67 | 1 | `code` | 0 | 4 |
| [contoso5_sub_category_name](contoso5_sub_category_name.md) | file | 32 | 1 | `code` | 0 | 4 |
| [dim_country](dim_country.md) | served | 9 | 3 | `country_code` | 1 | 0 |
| [dim_currency](dim_currency.md) | served | 5 | 1 | `currency_code` | 1 | 0 |
| [dim_customer](dim_customer.md) | served | 104990 | 11 | `customer_key` | 1 | 3 |
| [dim_location](dim_location.md) | served | 67 | 8 | `location_code` | 1 | 0 |
| [dim_product](dim_product.md) | served | 2517 | 10 | `product_key` | 4 | 2 |
| [dim_store](dim_store.md) | served | 74 | 12 | `store_key` | 1 | 0 |
| [v_contoso5_fx_rate](v_contoso5_fx_rate.md) | served | 100450 | 4 | `date_day`, `from_currency`, `to_currency` | 1 | 1 |
| [v_contoso5_sales_line](v_contoso5_sales_line.md) | served | 223974 | 21 | `order_key`, `line_number` | 1 | 4 |
