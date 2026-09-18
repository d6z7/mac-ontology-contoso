---
type: Index
title: CONTOSO data plane
---

8 sources · 6 quality issues · 6 transforms · 6 clean datasets

**Resolution scoreboard** — how the recorded impurities are dissolved by the gold transforms: **1 ✓ resolved · 1 ◐ partial · 1 ⚠ open gap**.

📋 **[Issues & inconsistencies — the full overview](quality/0-issues-overview.md)**

❓ **[SME questions — data & data quality](quality/SME-QUESTIONS.md)**

## Sources
- [currencyexchange](sources/currencyexchange.md)
- [customer](sources/customer.md)
- [date](sources/date.md)
- [orderrows](sources/orderrows.md)
- [orders](sources/orders.md)
- [product](sources/product.md)
- [sales](sources/sales.md)
- [store](sources/store.md)

## Data quality (by severity → resolution)
- **medium** [`customer.Age` is a derived attribute frozen five years before the facts it would describe](quality/DQ-CUSTOMER-01.md) — ◐ partial
- **medium** [15 leftover views in the warehouse, measured, neither treated as sources nor served](quality/NS-SERVING-01.md)
- **low** [the served customer row is a quasi-identifier — ZipCode alone singles out 29 193 of 104 990 customers, and the age band nearly doubles that](quality/DQ-CUSTOMER-02.md) — ⚠ open gap
- **low** [`sales` measured, deliberately not served — it is the served order line delivered a second time](quality/NS-ORDERS-01.md) — ✓ resolved
- **low** [the order header measured, deliberately not served as a relation of its own](quality/NS-ORDERS-02.md)
- **low** [12 of the 24 customer columns measured, deliberately not served](quality/NS-CUSTOMER-01.md)

## Clean datasets
- [dim_contoso_calendar_day](datasets/dim_contoso_calendar_day.md)
- [dim_contoso_customer](datasets/dim_contoso_customer.md)
- [dim_contoso_product](datasets/dim_contoso_product.md)
- [dim_contoso_store](datasets/dim_contoso_store.md)
- [v_contoso_fx_rate_day](datasets/v_contoso_fx_rate_day.md)
- [v_contoso_order_line](datasets/v_contoso_order_line.md)

## Reference lookups
- [contoso_brand.lookup](lookups/contoso_brand.lookup.md)
- [contoso_calendar_month.lookup](lookups/contoso_calendar_month.lookup.md)
- [contoso_calendar_quarter.lookup](lookups/contoso_calendar_quarter.lookup.md)
- [contoso_calendar_weekday.lookup](lookups/contoso_calendar_weekday.lookup.md)
- [contoso_color.lookup](lookups/contoso_color.lookup.md)
- [contoso_country.lookup](lookups/contoso_country.lookup.md)
- [contoso_currency.lookup](lookups/contoso_currency.lookup.md)
- [contoso_gender.lookup](lookups/contoso_gender.lookup.md)
- [contoso_geo_area.lookup](lookups/contoso_geo_area.lookup.md)
- [contoso_measure.lookup](lookups/contoso_measure.lookup.md)
- [contoso_product_category.lookup](lookups/contoso_product_category.lookup.md)
- [contoso_product_subcategory.lookup](lookups/contoso_product_subcategory.lookup.md)
- [contoso_store_status.lookup](lookups/contoso_store_status.lookup.md)
- [contoso_weight_unit.lookup](lookups/contoso_weight_unit.lookup.md)
- [contoso_working_day.lookup](lookups/contoso_working_day.lookup.md)
- [dim_contoso_product.lookup](lookups/dim_contoso_product.lookup.md)
- [dim_contoso_store.lookup](lookups/dim_contoso_store.lookup.md)
