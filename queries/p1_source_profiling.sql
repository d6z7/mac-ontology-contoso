-- queries/p1_source_profiling.sql — P1 · the ANOMALY pass, with the answer each query gave.
--
-- WHY THIS FILE EXISTS. data/profiles/*.yaml is written by mac_profile.py and may not be
-- hand-edited (ProfileFile: additionalProperties false, and a human editing it is a MAC002
-- error), so the census's numbers carry their provenance as `method: mac_profile.py/5` —
-- reproduce that SQL with `mac_profile.py <root> <stem> --dry-run`. The queries BELOW are the
-- ones the census cannot express: multi-column uniqueness, referential orphans, impossible
-- values, and the redundancy between the two fact relations. They are recorded verbatim, with
-- the answer measured on the date in the header, so any later reader can re-run and diff.
--
-- Engine: DuckDB 1.5.5, contoso.duckdb (read-only). Measured: 2026-09-18.
-- Answers are evidence, not assertions: nothing here declares a key, a grain or an edge.

-- ── U1 · orderrows: is (OrderKey, RowNumber) unique?
-- answer: rows=223974, pairs=223974
SELECT (SELECT count(*) FROM main.orderrows) AS rows,
       (SELECT count(*) FROM (SELECT DISTINCT OrderKey, RowNumber FROM main.orderrows)) AS pairs;

-- ── U2 · sales: is (OrderKey, LineNumber) unique?
-- answer: rows=223974, pairs=223974
SELECT (SELECT count(*) FROM main.sales) AS rows,
       (SELECT count(*) FROM (SELECT DISTINCT OrderKey, LineNumber FROM main.sales)) AS pairs;

-- ── U3 · currencyexchange: is (Date, FromCurrency, ToCurrency) unique, and is the grid complete?
-- answer: rows=100450, triples=100450, full_grid=100450
SELECT (SELECT count(*) FROM main.currencyexchange) AS rows,
       (SELECT count(*) FROM (SELECT DISTINCT Date, FromCurrency, ToCurrency
                              FROM main.currencyexchange)) AS triples,
       (SELECT count(DISTINCT Date) * count(DISTINCT FromCurrency) * count(DISTINCT ToCurrency)
        FROM main.currencyexchange) AS full_grid;

-- ── U4 · store: which StoreCode values repeat, and how often?
-- answer: {StoreCode=7, n=3} ; {StoreCode=3, n=2} ; {StoreCode=25, n=2} ; {StoreCode=46, n=2} ; {StoreCode=58, n=2} ; {StoreCode=60, n=2}
SELECT StoreCode, count(*) AS n FROM main.store GROUP BY 1 HAVING count(*) > 1 ORDER BY 2 DESC;

-- ── U5 · orderrows/sales: does every order's line numbering start at 0 and run contiguously?
-- answer: orders_with_gaps=1448
SELECT count(*) AS orders_with_gaps FROM (
  SELECT OrderKey FROM main.orderrows GROUP BY 1
  HAVING min(RowNumber) <> 0 OR max(RowNumber) + 1 <> count(*));

-- ── O1 · sales.OrderKey with no orders row
-- answer: orphan_rows=0, orphan_keys=0
SELECT count(*) AS orphan_rows, count(DISTINCT s.OrderKey) AS orphan_keys
FROM main.sales s LEFT JOIN main.orders o USING (OrderKey) WHERE o.OrderKey IS NULL;

-- ── O2 · orderrows.OrderKey with no orders row
-- answer: orphan_rows=0, orphan_keys=0
SELECT count(*) AS orphan_rows, count(DISTINCT r.OrderKey) AS orphan_keys
FROM main.orderrows r LEFT JOIN main.orders o USING (OrderKey) WHERE o.OrderKey IS NULL;

-- ── O3 · orders with no line in orderrows, and none in sales
-- answer: headers_without_orderrows=0, headers_without_sales=0
SELECT (SELECT count(*) FROM main.orders o
        WHERE NOT EXISTS (SELECT 1 FROM main.orderrows r WHERE r.OrderKey = o.OrderKey))
         AS headers_without_orderrows,
       (SELECT count(*) FROM main.orders o
        WHERE NOT EXISTS (SELECT 1 FROM main.sales s WHERE s.OrderKey = o.OrderKey))
         AS headers_without_sales;

-- ── O4 · CustomerKey with no customer row (sales, orders)
-- answer: sales_orphans=0, orders_orphans=0
SELECT (SELECT count(*) FROM main.sales s
        WHERE NOT EXISTS (SELECT 1 FROM main.customer c WHERE c.CustomerKey = s.CustomerKey))
         AS sales_orphans,
       (SELECT count(*) FROM main.orders o
        WHERE NOT EXISTS (SELECT 1 FROM main.customer c WHERE c.CustomerKey = o.CustomerKey))
         AS orders_orphans;

-- ── O5 · ProductKey with no product row (sales, orderrows)
-- answer: sales_orphans=0, orderrows_orphans=0
SELECT (SELECT count(*) FROM main.sales s
        WHERE NOT EXISTS (SELECT 1 FROM main.product p WHERE p.ProductKey = s.ProductKey))
         AS sales_orphans,
       (SELECT count(*) FROM main.orderrows r
        WHERE NOT EXISTS (SELECT 1 FROM main.product p WHERE p.ProductKey = r.ProductKey))
         AS orderrows_orphans;

-- ── O6 · StoreKey with no store row (sales, orders)
-- answer: sales_orphans=0, orders_orphans=0
SELECT (SELECT count(*) FROM main.sales s
        WHERE NOT EXISTS (SELECT 1 FROM main.store t WHERE t.StoreKey = s.StoreKey))
         AS sales_orphans,
       (SELECT count(*) FROM main.orders o
        WHERE NOT EXISTS (SELECT 1 FROM main.store t WHERE t.StoreKey = o.StoreKey))
         AS orders_orphans;

-- ── O7 · CurrencyCode not quoted in currencyexchange (as ToCurrency / as FromCurrency)
-- answer: sales_codes_unquoted_to=0, order_codes_unquoted_from=0
SELECT (SELECT count(DISTINCT CurrencyCode) FROM main.sales s
        WHERE NOT EXISTS (SELECT 1 FROM main.currencyexchange x
                          WHERE x.ToCurrency = s.CurrencyCode)) AS sales_codes_unquoted_to,
       (SELECT count(DISTINCT CurrencyCode) FROM main.orders o
        WHERE NOT EXISTS (SELECT 1 FROM main.currencyexchange x
                          WHERE x.FromCurrency = o.CurrencyCode)) AS order_codes_unquoted_from;

-- ── O8 · event dates absent from the date relation
-- answer: sales_orderdate_missing=0, sales_deliverydate_missing=0, orders_dt_missing=0, fx_date_missing=0
SELECT (SELECT count(*) FROM main.sales s
        WHERE NOT EXISTS (SELECT 1 FROM main.date d WHERE d.Date = s.OrderDate))
         AS sales_orderdate_missing,
       (SELECT count(*) FROM main.sales s
        WHERE NOT EXISTS (SELECT 1 FROM main.date d WHERE d.Date = s.DeliveryDate))
         AS sales_deliverydate_missing,
       (SELECT count(*) FROM main.orders o
        WHERE NOT EXISTS (SELECT 1 FROM main.date d WHERE d.Date = o.DT))
         AS orders_dt_missing,
       (SELECT count(*) FROM main.currencyexchange x
        WHERE NOT EXISTS (SELECT 1 FROM main.date d WHERE d.Date = x.Date))
         AS fx_date_missing;

-- ── O9 · GeoAreaKey: customer's values vs store's — is either a subset of the other?
-- answer: customer_distinct=608, store_distinct=67, store_keys_not_in_customer=4
SELECT (SELECT count(DISTINCT GeoAreaKey) FROM main.customer) AS customer_distinct,
       (SELECT count(DISTINCT GeoAreaKey) FROM main.store) AS store_distinct,
       (SELECT count(*) FROM (SELECT DISTINCT GeoAreaKey FROM main.store) t
        WHERE NOT EXISTS (SELECT 1 FROM main.customer c WHERE c.GeoAreaKey = t.GeoAreaKey))
         AS store_keys_not_in_customer;

-- ── O10 · rows nothing points at: unsold products, unused stores, customers with no order
-- answer: products_never_sold=0, stores_never_selling=10, customers_without_order=52801, dates_without_sales=568
SELECT (SELECT count(*) FROM main.product p
        WHERE NOT EXISTS (SELECT 1 FROM main.sales s WHERE s.ProductKey = p.ProductKey))
         AS products_never_sold,
       (SELECT count(*) FROM main.store t
        WHERE NOT EXISTS (SELECT 1 FROM main.sales s WHERE s.StoreKey = t.StoreKey))
         AS stores_never_selling,
       (SELECT count(*) FROM main.customer c
        WHERE NOT EXISTS (SELECT 1 FROM main.orders o WHERE o.CustomerKey = c.CustomerKey))
         AS customers_without_order,
       (SELECT count(*) FROM main.date d
        WHERE NOT EXISTS (SELECT 1 FROM main.sales s WHERE s.OrderDate = d.Date))
         AS dates_without_sales;

-- ── V1 · non-positive quantities and money (orderrows, sales)
-- answer: or_qty_le0=0, or_money_le0=0, s_qty_le0=0, s_money_le0=0, fx_rate_le0=0
SELECT (SELECT count(*) FROM main.orderrows WHERE Quantity <= 0) AS or_qty_le0,
       (SELECT count(*) FROM main.orderrows WHERE UnitPrice <= 0 OR NetPrice <= 0
                                               OR UnitCost <= 0) AS or_money_le0,
       (SELECT count(*) FROM main.sales WHERE Quantity <= 0) AS s_qty_le0,
       (SELECT count(*) FROM main.sales WHERE UnitPrice <= 0 OR NetPrice <= 0
                                           OR UnitCost <= 0) AS s_money_le0,
       (SELECT count(*) FROM main.currencyexchange WHERE Exchange <= 0) AS fx_rate_le0;

-- ── V2 · price relations: net above list, net below cost (sales)
-- answer: net_above_list=0, net_below_cost=0, list_below_cost=0
SELECT count(*) FILTER (WHERE NetPrice > UnitPrice) AS net_above_list,
       count(*) FILTER (WHERE NetPrice < UnitCost) AS net_below_cost,
       count(*) FILTER (WHERE UnitPrice < UnitCost) AS list_below_cost
FROM main.sales;

-- ── V3 · delivery before order (sales, orders)
-- answer: sales_rows=0, orders_rows=0
SELECT (SELECT count(*) FROM main.sales WHERE DeliveryDate < OrderDate) AS sales_rows,
       (SELECT count(*) FROM main.orders WHERE DeliveryDate < DT) AS orders_rows;

-- ── V4 · store: closed before opened, and the shape of 'missing'
-- answer: closed_before_open=0, storecode_sentinel=1, geoarea_sentinel=1, countrycode_sentinel=1, status_blank=58, status_null=1, sqm_null=1, closedate_null=58
SELECT count(*) FILTER (WHERE CloseDate < OpenDate) AS closed_before_open,
       count(*) FILTER (WHERE StoreCode = -1) AS storecode_sentinel,
       count(*) FILTER (WHERE GeoAreaKey = -1) AS geoarea_sentinel,
       count(*) FILTER (WHERE CountryCode = '--') AS countrycode_sentinel,
       count(*) FILTER (WHERE Status = '') AS status_blank,
       count(*) FILTER (WHERE Status IS NULL) AS status_null,
       count(*) FILTER (WHERE SquareMeters IS NULL) AS sqm_null,
       count(*) FILTER (WHERE CloseDate IS NULL) AS closedate_null
FROM main.store;

-- ── V5 · product: is a missing Weight the same row as a blank WeightUnit?
-- answer: weight_null=284, unit_blank=222, disagree=62
SELECT count(*) FILTER (WHERE Weight IS NULL) AS weight_null,
       count(*) FILTER (WHERE WeightUnit = '') AS unit_blank,
       count(*) FILTER (WHERE (Weight IS NULL) <> (WeightUnit = '')) AS disagree
FROM main.product;

-- ── V6 · product: colour values differing only by case
-- answer: folded=blue, spellings=2, seen=Blue | blue
SELECT lower(Color) AS folded, count(DISTINCT Color) AS spellings,
       array_join(array_sort(array_agg(DISTINCT Color)), ' | ') AS seen
FROM main.product GROUP BY 1 HAVING count(DISTINCT Color) > 1;

-- ── V7 · customer: validity window inverted, and whether Age agrees with Birthday
-- answer: window_inverted=1, implied_ref_year_min=2020, implied_ref_year_max=2021
SELECT count(*) FILTER (WHERE EndDT <= StartDT) AS window_inverted,
       min(year(Birthday) + Age) AS implied_ref_year_min,
       max(year(Birthday) + Age) AS implied_ref_year_max
FROM main.customer;

-- ── V8 · date: one row per calendar day with no gaps?
-- answer: rows=4018, distinct_days=4018, days_in_span=4018
SELECT count(*) AS rows, count(DISTINCT Date) AS distinct_days,
       date_diff('day', min(Date), max(Date)) + 1 AS days_in_span
FROM main.date;

-- ── V9 · date: does DateKey encode the date as YYYYMMDD on every row?
-- answer: not_yyyymmdd=0, min_key=20160101, max_key=20261231
SELECT count(*) FILTER (WHERE DateKey <> strftime(Date, '%Y%m%d')) AS not_yyyymmdd,
       min(DateKey) AS min_key, max(DateKey) AS max_key
FROM main.date;

-- ── V10 · timestamps that are not midnight (i.e. a real time-of-day anywhere)
-- answer: orders_dt=0, sales_orderdate=0, customer_startdt=0
SELECT (SELECT count(*) FROM main.orders WHERE DT <> date_trunc('day', DT)) AS orders_dt,
       (SELECT count(*) FROM main.sales WHERE OrderDate <> date_trunc('day', OrderDate))
         AS sales_orderdate,
       (SELECT count(*) FROM main.customer WHERE StartDT <> date_trunc('day', StartDT))
         AS customer_startdt;

-- ── V11 · currencyexchange: is the self-rate always 1?
-- answer: self_rows=20090, self_rate_not_one=0, min_rate=1.00000, max_rate=1.00000
SELECT count(*) AS self_rows, count(*) FILTER (WHERE Exchange <> 1) AS self_rate_not_one,
       min(Exchange) AS min_rate, max(Exchange) AS max_rate
FROM main.currencyexchange WHERE FromCurrency = ToCurrency;

-- ── V12 · orders.StoreKey 999999 — how many rows carry the out-of-range key?
-- answer: orders_rows=38968, sales_rows=93550, store_rows=1
SELECT (SELECT count(*) FROM main.orders WHERE StoreKey = 999999) AS orders_rows,
       (SELECT count(*) FROM main.sales WHERE StoreKey = 999999) AS sales_rows,
       (SELECT count(*) FROM main.store WHERE StoreKey = 999999) AS store_rows;

-- ── R1 · sales vs orderrows: same line population?
-- answer: in_sales_only=0, in_orderrows_only=0
SELECT (SELECT count(*) FROM (SELECT OrderKey, LineNumber FROM main.sales
                              EXCEPT SELECT OrderKey, RowNumber FROM main.orderrows))
         AS in_sales_only,
       (SELECT count(*) FROM (SELECT OrderKey, RowNumber FROM main.orderrows
                              EXCEPT SELECT OrderKey, LineNumber FROM main.sales))
         AS in_orderrows_only;

-- ── R2 · sales vs orderrows: do the shared measures agree line by line?
-- answer: joined_rows=223974, productkey_differs=0, quantity_differs=0, unitprice_differs=0, netprice_differs=0, unitcost_differs=0
SELECT count(*) AS joined_rows,
       count(*) FILTER (WHERE s.ProductKey <> r.ProductKey) AS productkey_differs,
       count(*) FILTER (WHERE s.Quantity <> r.Quantity) AS quantity_differs,
       count(*) FILTER (WHERE s.UnitPrice <> r.UnitPrice) AS unitprice_differs,
       count(*) FILTER (WHERE s.NetPrice <> r.NetPrice) AS netprice_differs,
       count(*) FILTER (WHERE s.UnitCost <> r.UnitCost) AS unitcost_differs
FROM main.sales s JOIN main.orderrows r
  ON s.OrderKey = r.OrderKey AND s.LineNumber = r.RowNumber;

-- ── R3 · sales vs orders: does the line carry the header's own values unchanged?
-- answer: joined_rows=223974, customer_differs=0, store_differs=0, orderdate_differs=0, deliverydate_differs=0, currency_differs=0
SELECT count(*) AS joined_rows,
       count(*) FILTER (WHERE s.CustomerKey <> o.CustomerKey) AS customer_differs,
       count(*) FILTER (WHERE s.StoreKey <> o.StoreKey) AS store_differs,
       count(*) FILTER (WHERE s.OrderDate <> o.DT) AS orderdate_differs,
       count(*) FILTER (WHERE s.DeliveryDate <> o.DeliveryDate) AS deliverydate_differs,
       count(*) FILTER (WHERE s.CurrencyCode <> o.CurrencyCode) AS currency_differs
FROM main.sales s JOIN main.orders o USING (OrderKey);

-- ── R4 · sales.ExchangeRate: does it match the fx quote for that day and currency?
-- answer: rows_checked=223974, no_quote_found=0, rate_differs=0
SELECT count(*) AS rows_checked,
       count(*) FILTER (WHERE x.Exchange IS NULL) AS no_quote_found,
       count(*) FILTER (WHERE x.Exchange IS NOT NULL AND s.ExchangeRate <> x.Exchange)
         AS rate_differs
FROM main.sales s
LEFT JOIN main.currencyexchange x
  ON x.Date = s.OrderDate AND x.FromCurrency = 'USD' AND x.ToCurrency = s.CurrencyCode;

-- ── U4b · store: the rows behind the repeated StoreCode values
-- answer: {StoreKey=30, StoreCode=3, GeoAreaKey=5, CountryCode=AU, Status=Restructured, opened=2012-01-07, closed=2015-08-08} ; {StoreKey=35, StoreCode=3, GeoAreaKey=5, CountryCode=AU, Status=, opened=2015-12-08, closed=None} ; {StoreKey=70, StoreCode=7, GeoAreaKey=12, CountryCode=CA, Status=Restructured, opened=2007-05-07, closed=2014-03-09} ; {StoreKey=72, StoreCode=7, GeoAreaKey=12, CountryCode=CA, Status=Restructured, opened=2015-01-11, closed=2018-02-02} ; {StoreKey=74, StoreCode=7, GeoAreaKey=12, CountryCode=CA, Status=, opened=2018-06-02, closed=None} ; {StoreKey=250, StoreCode=25, GeoAreaKey=29, CountryCode=DE, Status=Restructured, opened=2010-01-01, closed=2015-04-04} ; {StoreKey=255, StoreCode=25, GeoAreaKey=29, CountryCode=DE, Status=, opened=2015-08-08, closed=None} ; {StoreKey=460, StoreCode=46, GeoAreaKey=574, CountryCode=US, Status=Restructured, opened=2012-08-08, closed=2015-03-03} ; …(13 rows)
SELECT StoreKey, StoreCode, GeoAreaKey, CountryCode, Status,
       CAST(OpenDate AS DATE) AS opened, CAST(CloseDate AS DATE) AS closed
FROM main.store WHERE StoreCode IN (SELECT StoreCode FROM main.store
                                    GROUP BY 1 HAVING count(*) > 1)
ORDER BY StoreCode, StoreKey;

-- ── U5b · orderrows: which kind of line-numbering break — not starting at 0, or gaps?
-- answer: not_starting_at_zero=0, max_plus_one_not_count=1448, starts_at_zero_with_gap=1448
SELECT count(*) FILTER (WHERE first_row <> 0) AS not_starting_at_zero,
       count(*) FILTER (WHERE last_row + 1 <> n) AS max_plus_one_not_count,
       count(*) FILTER (WHERE first_row = 0 AND last_row + 1 <> n) AS starts_at_zero_with_gap
FROM (SELECT min(RowNumber) AS first_row, max(RowNumber) AS last_row, count(*) AS n
      FROM main.orderrows GROUP BY OrderKey);

-- ── V4b · store: are all the sentinels the same single row?
-- answer: StoreKey=999999, StoreCode=-1, GeoAreaKey=-1, CountryCode=--, CountryName=Online, State=Online, Status=None, SquareMeters=None
SELECT StoreKey, StoreCode, GeoAreaKey, CountryCode, CountryName, State, Status, SquareMeters
FROM main.store
WHERE StoreKey = 999999 OR StoreCode = -1 OR GeoAreaKey = -1 OR CountryCode = '--'
   OR SquareMeters IS NULL OR Status IS NULL;

-- ── V5b · product: the two spellings of a missing weight, both ways round
-- answer: both_missing=222, null_weight_named_unit=62, weight_without_unit=0
SELECT count(*) FILTER (WHERE Weight IS NULL AND WeightUnit = '') AS both_missing,
       count(*) FILTER (WHERE Weight IS NULL AND WeightUnit <> '') AS null_weight_named_unit,
       count(*) FILTER (WHERE Weight IS NOT NULL AND WeightUnit = '') AS weight_without_unit
FROM main.product;

-- ── V6b · product: how many rows carry each spelling of the case-variant colour
-- answer: {Color=Blue, products=197} ; {Color=blue, products=3}
SELECT Color, count(*) AS products FROM main.product
WHERE lower(Color) = 'blue' GROUP BY 1 ORDER BY 1;

-- ── V7b · customer: the row whose validity window is inverted
-- answer: CustomerKey=816905, start_dt=2010-08-01, end_dt=2010-08-01
SELECT CustomerKey, CAST(StartDT AS DATE) AS start_dt, CAST(EndDT AS DATE) AS end_dt
FROM main.customer WHERE EndDT <= StartDT;

-- ── O10b · date: days with no sales INSIDE the fact's own date range
-- answer: first_sale=2016-05-18, last_sale=2025-12-31, days_in_span_without_sales=65
WITH span AS (SELECT min(OrderDate) AS lo, max(OrderDate) AS hi FROM main.sales)
SELECT (SELECT CAST(lo AS DATE) FROM span) AS first_sale,
       (SELECT CAST(hi AS DATE) FROM span) AS last_sale,
       count(*) AS days_in_span_without_sales
FROM main.date d, span
WHERE d.Date BETWEEN span.lo AND span.hi
  AND NOT EXISTS (SELECT 1 FROM main.sales s WHERE s.OrderDate = d.Date);

-- ── U4c · store: do two rows sharing a StoreCode ever cover overlapping open windows?
-- answer: overlapping_pairs=0
SELECT count(*) AS overlapping_pairs FROM main.store a JOIN main.store b
  ON a.StoreCode = b.StoreCode AND a.StoreKey < b.StoreKey
WHERE coalesce(a.CloseDate, DATE '9999-12-31') >= b.OpenDate
  AND coalesce(b.CloseDate, DATE '9999-12-31') >= a.OpenDate;
