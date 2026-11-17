# Order

The account of concept Order. Written by mac_migrate_v3 from the 0.4.0 declaration; each heading after `Cites` carries 0.4.0 prose that has no key in grammar v3 (X-3).

## Cites

- `dataset:v_contoso5_sales_line.order_key`
- `dataset:v_contoso5_sales_line.line_number`
- `dataset:v_contoso5_sales_line.order_date`
- `dataset:v_contoso5_sales_line.delivery_date`
- `dataset:v_contoso5_sales_line.customer_key`
- `dataset:v_contoso5_sales_line.store_key`
- `dataset:v_contoso5_sales_line.is_web_sale`
- `dataset:v_contoso5_sales_line.product_key`
- `dataset:v_contoso5_sales_line.currency_code`
- `dataset:v_contoso5_sales_line.quantity`
- `dataset:v_contoso5_sales_line.net_amount`
- `dataset:v_contoso5_sales_line.gross_amount`
- `dataset:v_contoso5_sales_line.cost_amount`
- `dataset:v_contoso5_sales_line.discount_amount`
- `dataset:v_contoso5_sales_line.margin_amount`
- `dataset:v_contoso5_sales_line.unit_price`
- `dataset:v_contoso5_sales_line.net_price`
- `dataset:v_contoso5_sales_line.unit_cost`
- `rule:Order.channel`
- `rule:Order.cost_is_procurement`
- `rule:Order.date`
- `rule:Order.default_measure`
- `rule:Order.discount_percent_is_over_gross`
- `rule:Order.discount_total_is_money`
- `rule:Order.how_many`
- `rule:Order.is_the_purchase`
- `rule:Order.margin_ratio_is_named`
- `rule:Order.no_lifecycle_state`
- `rule:Order.now_is_the_newest_order`
- `rule:Order.period`
- `rule:Order.price_is_per_article`
- `rule:Order.price_terms`
- `rule:Order.rate_on_order_date`
- `rule:Order.revenue_means_net`

## grounding.note

reached by counting distinct order_key over the line relation — NOT collapsed, so each row it reads carries exactly one product

## contract.default_reading

A QUESTION THAT NAMES NO PERIOD COVERS ALL TIME — operator ruling, 2026-09-30 (rule Order.period). No implied "this year" and no implied latest month. State the window the answer actually covered — its first and last `order_date` — because an unscoped total and a year-to- date total are indistinguishable from the figure alone.
