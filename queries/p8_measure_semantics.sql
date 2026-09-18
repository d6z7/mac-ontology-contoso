-- queries/p8_measure_semantics.sql — P8 · measure-semantics: every measurement this step
-- made, with the answer it returned. Observed 2026-09-18.
--
-- WHAT THIS STEP CLASSIFIES: the three concepts with `class: measure`. Additivity is an
-- ARITHMETIC claim (the parts add up to the whole, or they do not), so each classification
-- is measured here rather than asserted, and the cost of the wrong classification is
-- measured too. The law itself is NOT here: it lives once, in the framework's closed value
-- domain mac_vocabulary.yaml#MeasureType, and data/lookups/contoso_measure.lookup.csv is a
-- generated projection of it (data/lookups/contoso_measure.lookup.build.py).
--
-- HOW TO RE-RUN: connection.yaml declares read_only: true, so the six served relations do
-- not exist in contoso.duckdb. Every query below reads contoso_served.*, which is
-- materialised by executing data/transforms/*.sql on a COPY of the warehouse. Run from the
-- bundle root (the register paths are relative to it).

-- ================================================================================================
-- A1 · every numeric column of every served relation — the population a measure classification could possibly cover, so the 3 classified ones have a denominator
-- ================================================================================================
SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_schema='contoso_served' AND (data_type LIKE 'DECIMAL%' OR data_type IN ('BIGINT','INTEGER','DOUBLE','HUGEINT','SMALLINT')) ORDER BY table_name, ordinal_position;
--   ANSWER:
--   dim_contoso_calendar_day   Year   INTEGER
--   dim_contoso_calendar_day   YearQuarterNumber   INTEGER
--   dim_contoso_calendar_day   YearMonthNumber   INTEGER
--   dim_contoso_calendar_day   MonthNumber   INTEGER
--   dim_contoso_calendar_day   DayofWeekNumber   INTEGER
--   dim_contoso_calendar_day   WorkingDay   INTEGER
--   dim_contoso_calendar_day   WorkingDayNumber   INTEGER
--   dim_contoso_customer   CustomerKey   INTEGER
--   dim_contoso_customer   GeoAreaKey   INTEGER
--   dim_contoso_product   ProductKey   INTEGER
--   dim_contoso_product   Weight   DECIMAL(20,5)
--   dim_contoso_product   Cost   DECIMAL(20,5)
--   dim_contoso_product   Price   DECIMAL(20,5)
--   dim_contoso_product   CategoryKey   INTEGER
--   dim_contoso_product   SubCategoryKey   INTEGER
--   dim_contoso_store   StoreKey   INTEGER
--   dim_contoso_store   StoreCode   INTEGER
--   dim_contoso_store   GeoAreaKey   INTEGER
--   dim_contoso_store   SquareMeters   INTEGER
--   v_contoso_fx_rate_day   Exchange   DECIMAL(20,5)
--   v_contoso_order_line   OrderKey   BIGINT
--   v_contoso_order_line   RowNumber   INTEGER
--   v_contoso_order_line   CustomerKey   INTEGER
--   v_contoso_order_line   StoreKey   INTEGER
--   v_contoso_order_line   ProductKey   INTEGER
--   v_contoso_order_line   Quantity   INTEGER
--   v_contoso_order_line   UnitPrice   DECIMAL(20,5)
--   v_contoso_order_line   NetPrice   DECIMAL(20,5)
--   v_contoso_order_line   UnitCost   DECIMAL(20,5)

-- ================================================================================================
-- A2 · the served fact's four `value`-role columns: is each one a per-row EVENT quantity (a Flow) or a per-unit magnitude (an Intensive rate)? — rows, distinct values, and what a SUM of each would come to
-- ================================================================================================
SELECT count(*) AS rows, count(DISTINCT "Quantity") AS d_quantity, sum("Quantity") AS sum_quantity, count(DISTINCT "UnitPrice") AS d_unitprice, round(sum("UnitPrice"),2) AS sum_unitprice, round(avg("UnitPrice"),5) AS avg_unitprice, count(DISTINCT "NetPrice") AS d_netprice, round(sum("NetPrice"),2) AS sum_netprice, round(avg("NetPrice"),5) AS avg_netprice, count(DISTINCT "UnitCost") AS d_unitcost, round(sum("UnitCost"),2) AS sum_unitcost, round(avg("UnitCost"),5) AS avg_unitcost FROM contoso_served.v_contoso_order_line;
--   ANSWER:
--   223974   10   703621   1760   73784598.88   329.43377   18407   69401718.80   309.86507   1955   30622170.44   136.72199

-- ================================================================================================
-- B1 · OrderLine · does one row belong to exactly ONE period, or does the same entity recur period after period? (a row that recurs is a level = Stock; a row that occurs once is an event = Flow). Measured over the calendar month of OrderDate
-- ================================================================================================
WITH k AS (SELECT "OrderKey", "RowNumber", count(DISTINCT date_trunc('month', "OrderDate")) AS months, count(DISTINCT date_trunc('year', "OrderDate")) AS years FROM contoso_served.v_contoso_order_line GROUP BY 1,2) SELECT count(*) AS lines, max(months) AS max_months_per_line, max(years) AS max_years_per_line, sum(CASE WHEN months > 1 THEN 1 ELSE 0 END) AS lines_in_more_than_one_month FROM k;
--   ANSWER:
--   223974   1   1   0

-- ================================================================================================
-- B2 · OrderLine · the same question for the SET: are two adjacent periods' line sets disjoint, and do the monthly row counts add up to the whole? (a Stock relation re-delivers rows into every period, so the parts exceed the whole)
-- ================================================================================================
WITH per AS (SELECT date_trunc('month', "OrderDate") AS ym, count(*) AS lines FROM contoso_served.v_contoso_order_line GROUP BY 1) SELECT count(*) AS months, sum(lines) AS lines_summed_over_months, (SELECT count(*) FROM contoso_served.v_contoso_order_line) AS lines_in_the_relation, sum(lines) - (SELECT count(*) FROM contoso_served.v_contoso_order_line) AS difference FROM per;
--   ANSWER:
--   116   223974   223974   0

-- ================================================================================================
-- B3 · NetSalesAmount + GrossSalesAmount · the additivity claim on the TIME axis, to the cent: the sum of the monthly totals against the total over the whole delivery (own-denomination arithmetic — the partition identity a Flow must satisfy)
-- ================================================================================================
WITH per AS (SELECT date_trunc('month', "OrderDate") AS ym, sum("Quantity" * "NetPrice") AS net, sum("Quantity" * "UnitPrice") AS gross FROM contoso_served.v_contoso_order_line GROUP BY 1) SELECT count(*) AS months, round(sum(net),2) AS net_summed_over_months, (SELECT round(sum("Quantity" * "NetPrice"),2) FROM contoso_served.v_contoso_order_line) AS net_whole, round(sum(net) - (SELECT sum("Quantity" * "NetPrice") FROM contoso_served.v_contoso_order_line),10) AS net_difference, round(sum(gross),2) AS gross_summed_over_months, (SELECT round(sum("Quantity" * "UnitPrice"),2) FROM contoso_served.v_contoso_order_line) AS gross_whole, round(sum(gross) - (SELECT sum("Quantity" * "UnitPrice") FROM contoso_served.v_contoso_order_line),10) AS gross_difference FROM per;
--   ANSWER:
--   116   218814471.66   218814471.66   0.00000   232601542.66   232601542.66   0.00000

-- ================================================================================================
-- B4 · the same claim on the four CATEGORICAL axes that are columns of the fact (store, product, customer, denomination): does each partition reproduce the whole exactly? (Flow is additive along every categorical axis — this is that claim, measured)
-- ================================================================================================
WITH st AS (SELECT "StoreKey" k, sum("Quantity" * "NetPrice") v FROM contoso_served.v_contoso_order_line GROUP BY 1), pr AS (SELECT "ProductKey" k, sum("Quantity" * "NetPrice") v FROM contoso_served.v_contoso_order_line GROUP BY 1), cu AS (SELECT "CustomerKey" k, sum("Quantity" * "NetPrice") v FROM contoso_served.v_contoso_order_line GROUP BY 1), cc AS (SELECT "CurrencyCode" k, sum("Quantity" * "NetPrice") v FROM contoso_served.v_contoso_order_line GROUP BY 1), w AS (SELECT sum("Quantity" * "NetPrice") v FROM contoso_served.v_contoso_order_line) SELECT (SELECT count(*) FROM st) AS stores, (SELECT round(sum(v) - (SELECT v FROM w),10) FROM st) AS store_difference, (SELECT count(*) FROM pr) AS products, (SELECT round(sum(v) - (SELECT v FROM w),10) FROM pr) AS product_difference, (SELECT count(*) FROM cu) AS customers, (SELECT round(sum(v) - (SELECT v FROM w),10) FROM cu) AS customer_difference, (SELECT count(*) FROM cc) AS denominations, (SELECT round(sum(v) - (SELECT v FROM w),10) FROM cc) AS denomination_difference;
--   ANSWER:
--   64   0.00000   2517   0.00000   52189   0.00000   5   0.00000

-- ================================================================================================
-- B5 · the axes the fact does NOT carry as columns (brand, category, country, continent) — do they partition the fact through their dimension join without fan-out or loss? (an axis declared in axis_kinds that loses rows on the join is not an axis of this measure)
-- ================================================================================================
WITH j AS (SELECT f."OrderKey", f."RowNumber", "Quantity" * "NetPrice" AS net, p."Brand", p."CategoryKey", c."Country", c."Continent" FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_product p ON p."ProductKey" = f."ProductKey" JOIN contoso_served.dim_contoso_customer c ON c."CustomerKey" = f."CustomerKey") SELECT (SELECT count(*) FROM j) AS joined_rows, (SELECT count(*) FROM contoso_served.v_contoso_order_line) AS fact_rows, (SELECT count(DISTINCT "Brand") FROM j) AS brands, (SELECT count(DISTINCT "CategoryKey") FROM j) AS categories, (SELECT count(DISTINCT "Country") FROM j) AS countries, (SELECT count(DISTINCT "Continent") FROM j) AS continents, (SELECT round(sum(net),2) FROM j) AS net_over_the_join, (SELECT round(sum("Quantity" * "NetPrice"),2) FROM contoso_served.v_contoso_order_line) AS net_over_the_fact, (SELECT round((SELECT sum(net) FROM j) - (SELECT sum("Quantity" * "NetPrice") FROM contoso_served.v_contoso_order_line),10)) AS difference;
--   ANSWER:
--   223974   223974   11   8   8   3   218814471.66   218814471.66   0.00000

-- ================================================================================================
-- B6 · WHAT A WRONG CLASSIFICATION WOULD COST, measured. If these Flows were typed Stock, a bare period would RESOLVE the end-of-period row instead of summing (mac.resolve.period_reading). The two readings of calendar 2025
-- ================================================================================================
SELECT count(*) AS lines_ordered_in_2025, round(sum("Quantity" * "NetPrice"),2) AS net_2025_summed_as_a_flow, round(sum(CASE WHEN "OrderDate" = (SELECT max("OrderDate") FROM contoso_served.v_contoso_order_line WHERE "OrderDate" < TIMESTAMP '2026-01-01') THEN "Quantity" * "NetPrice" ELSE 0 END),2) AS net_2025_read_as_a_stock_end_cell, (SELECT max("OrderDate") FROM contoso_served.v_contoso_order_line WHERE "OrderDate" < TIMESTAMP '2026-01-01') AS the_end_cell_day FROM contoso_served.v_contoso_order_line WHERE "OrderDate" >= TIMESTAMP '2025-01-01' AND "OrderDate" < TIMESTAMP '2026-01-01';
--   ANSWER:
--   37708   29277489.59   129290.35   2025-12-31 00:00:00

-- ================================================================================================
-- B7 · and what typing them Intensive would cost: the mean of the per-line amounts against their sum, over the whole delivery (an average is not a smaller total — the two answer different questions)
-- ================================================================================================
SELECT count(*) AS lines, round(sum("Quantity" * "NetPrice"),2) AS net_sum, round(avg("Quantity" * "NetPrice"),5) AS net_mean, round(median("Quantity" * "NetPrice"),5) AS net_median, round(min("Quantity" * "NetPrice"),5) AS net_min, round(max("Quantity" * "NetPrice"),5) AS net_max FROM contoso_served.v_contoso_order_line;
--   ANSWER:
--   223974   218814471.66   976.96372   385.44000   0.82650   49980.00000

-- ================================================================================================
-- C1 · is there a MEASURE-SELECTOR column on the served fact — a discriminator whose value picks a DIFFERENT measure (so no fold along it means anything)? Every column of the fact with its distinct count; a selector would be a small code set that partitions the amounts into different quantities
-- ================================================================================================
SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='contoso_served' AND table_name='v_contoso_order_line' ORDER BY ordinal_position;
--   ANSWER:
--   OrderKey   BIGINT
--   RowNumber   INTEGER
--   OrderDate   TIMESTAMP
--   DeliveryDate   TIMESTAMP
--   CustomerKey   INTEGER
--   StoreKey   INTEGER
--   ProductKey   INTEGER
--   CurrencyCode   VARCHAR
--   Quantity   INTEGER
--   UnitPrice   DECIMAL(20,5)
--   NetPrice   DECIMAL(20,5)
--   UnitCost   DECIMAL(20,5)

-- ================================================================================================
-- C2 · the one code column on the fact (CurrencyCode) is a UNIT discriminator and not a measure selector — measured: BOTH measures exist for EVERY one of its values, so changing the value does not change which measure is being read
-- ================================================================================================
SELECT "CurrencyCode", count(*) AS lines, round(sum("Quantity" * "NetPrice"),2) AS net, round(sum("Quantity" * "UnitPrice"),2) AS gross, count(*) FILTER (WHERE "Quantity" * "NetPrice" IS NULL) AS net_missing, count(*) FILTER (WHERE "Quantity" * "UnitPrice" IS NULL) AS gross_missing FROM contoso_served.v_contoso_order_line GROUP BY 1 ORDER BY 1;
--   ANSWER:
--   AUD   14078   13360672.61   14197999.29   0   0
--   CAD   24250   23242027.53   24708880.13   0   0
--   EUR   49203   47300050.59   50272341.05   0   0
--   GBP   22829   23049533.37   24512650.21   0   0
--   USD   113614   111862187.56   118909671.98   0   0

-- ================================================================================================
-- C3 · and why the denomination is still not an aggregation axis: the five per-code sums added as if they were one unit, against the same lines converted per line through their own day's quote — the axis the framework law cannot rule on, because mac.axis_kind has no term for a per-row UNIT
-- ================================================================================================
SELECT round((SELECT sum("Quantity" * "NetPrice") FROM contoso_served.v_contoso_order_line),2) AS five_denominations_added_as_one_number, round((SELECT sum(net_usd) FROM (SELECT f.*, f."Quantity" * f."NetPrice" * x."Exchange" AS net_usd, f."Quantity" * f."UnitPrice" * x."Exchange" AS gross_usd FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date" = f."OrderDate" AND x."FromCurrency" = f."CurrencyCode" AND x."ToCurrency" = 'USD')),2) AS converted_per_line_to_usd, round((SELECT sum(net_usd) FROM (SELECT f.*, f."Quantity" * f."NetPrice" * x."Exchange" AS net_usd, f."Quantity" * f."UnitPrice" * x."Exchange" AS gross_usd FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date" = f."OrderDate" AND x."FromCurrency" = f."CurrencyCode" AND x."ToCurrency" = 'USD')) - (SELECT sum("Quantity" * "NetPrice") FROM contoso_served.v_contoso_order_line),2) AS difference;
--   ANSWER:
--   218814471.66   219837066.14   1022594.48

-- ================================================================================================
-- C4 · is there a RESTATING axis in the served fact — a column carrying both a rolled-up total row and the rows composing it? Test the one candidate: the sentinel StoreKey 999999 ('Online'), which 41.8 % of lines point at. If it were a roll-up its amount would equal the sum of the other stores'
-- ================================================================================================
SELECT round(sum(CASE WHEN "StoreKey" = 999999 THEN "Quantity" * "NetPrice" ELSE 0 END),2) AS sentinel_net, round(sum(CASE WHEN "StoreKey" <> 999999 THEN "Quantity" * "NetPrice" ELSE 0 END),2) AS other_stores_net, count(*) FILTER (WHERE "StoreKey" = 999999) AS sentinel_lines, count(DISTINCT "StoreKey") FILTER (WHERE "StoreKey" <> 999999) AS other_stores FROM contoso_served.v_contoso_order_line;
--   ANSWER:
--   86790054.13   132024417.53   93550   63

-- ================================================================================================
-- C5 · the restating relation the fact is NOT — main.sales delivers the same lines a second time (register NS-ORDERS-01, not served). Summing the served fact together with it is the double count the concept rule forbids; measured here so the rule has its number
-- ================================================================================================
SELECT (SELECT count(*) FROM contoso_served.v_contoso_order_line) AS served_lines, (SELECT count(*) FROM main.sales) AS raw_sales_rows, round((SELECT sum("Quantity" * "NetPrice") FROM contoso_served.v_contoso_order_line),2) AS served_net, round((SELECT sum("Quantity" * "NetPrice") FROM main.sales),2) AS raw_sales_net, round((SELECT sum("Quantity" * "NetPrice") FROM contoso_served.v_contoso_order_line) + (SELECT sum("Quantity" * "NetPrice") FROM main.sales),2) AS the_doubled_figure;
--   ANSWER:
--   223974   223974   218814471.66   218814471.66   437628943.32

-- ================================================================================================
-- D1 · ExchangeRate · the grid and its grain: one row per (Date, FromCurrency, ToCurrency), and NO finer or coarser stored grain exists — so there is nothing to fold from and nothing to fold into
-- ================================================================================================
SELECT count(*) AS rows, count(DISTINCT ("Date","FromCurrency","ToCurrency")) AS distinct_keys, count(DISTINCT "Date") AS days, count(DISTINCT ("FromCurrency","ToCurrency")) AS pairs, count(DISTINCT "Date") * count(DISTINCT ("FromCurrency","ToCurrency")) AS days_x_pairs, count(*) - count(DISTINCT ("Date","FromCurrency","ToCurrency")) AS duplicate_rows FROM contoso_served.v_contoso_fx_rate_day;
--   ANSWER:
--   100450   100450   4018   25   100450   0

-- ================================================================================================
-- D2 · is any coarser reading STORED? (a Precomputed measure may only be read at a grain it was computed for — if a month row existed, a month question would resolve it). Rows per (year, month, pair) against rows per (day, pair)
-- ================================================================================================
SELECT count(*) AS day_pair_rows, (SELECT count(*) FROM (SELECT date_trunc('month',"Date"), "FromCurrency", "ToCurrency" FROM contoso_served.v_contoso_fx_rate_day GROUP BY 1,2,3)) AS month_pair_groups, (SELECT count(*) FROM contoso_served.v_contoso_fx_rate_day WHERE "Date" <> date_trunc('day', "Date")) AS intraday_rows FROM contoso_served.v_contoso_fx_rate_day;
--   ANSWER:
--   100450   3300   0

-- ================================================================================================
-- D3 · no fold over TIME is valid: the three candidate folds of one pair over one month against each other — a SUM (a number with no meaning), an AVERAGE, and the end-of-period cell the law actually resolves (mac.resolve.period_reading). EUR->USD, 2025-01
-- ================================================================================================
SELECT count(*) AS days_in_the_month, round(sum("Exchange"),5) AS summed, round(avg("Exchange"),5) AS averaged, round(min("Exchange"),5) AS lowest, round(max("Exchange"),5) AS highest, (SELECT round("Exchange",5) FROM contoso_served.v_contoso_fx_rate_day WHERE "FromCurrency"='EUR' AND "ToCurrency"='USD' AND "Date" = (SELECT max("Date") FROM contoso_served.v_contoso_fx_rate_day WHERE "FromCurrency"='EUR' AND "ToCurrency"='USD' AND "Date" < TIMESTAMP '2025-02-01')) AS end_of_period_cell FROM contoso_served.v_contoso_fx_rate_day WHERE "FromCurrency"='EUR' AND "ToCurrency"='USD' AND "Date" >= TIMESTAMP '2025-01-01' AND "Date" < TIMESTAMP '2025-02-01';
--   ANSWER:
--   31   33.15350   1.06947   1.05370   1.09550   1.05910

-- ================================================================================================
-- D4 · no fold over the PAIR axis is valid either, and the cells are not derivable from one another: the triangular test rate(A->B) x rate(B->C) against the stored rate(A->C) on one day, over all 125 triples — if the product equalled the stored cell, a cell COULD be computed from narrower ones
-- ================================================================================================
WITH d AS (SELECT * FROM contoso_served.v_contoso_fx_rate_day WHERE "Date" = TIMESTAMP '2025-06-30'), t AS (SELECT ab."FromCurrency" a, ab."ToCurrency" b, bc."ToCurrency" c, ab."Exchange" * bc."Exchange" AS via_b, ac."Exchange" AS stored FROM d ab JOIN d bc ON bc."FromCurrency" = ab."ToCurrency" JOIN d ac ON ac."FromCurrency" = ab."FromCurrency" AND ac."ToCurrency" = bc."ToCurrency") SELECT count(*) AS triples, sum(CASE WHEN via_b = stored THEN 1 ELSE 0 END) AS exactly_equal, round(max(abs(via_b - stored)),8) AS max_absolute_deviation, round(max(abs(via_b - stored) / stored) * 100, 6) AS max_relative_deviation_pct FROM t;
--   ANSWER:
--   125   45   0.00001292   0.001078

-- ================================================================================================
-- D5 · and the SUM across the pair axis, for the record: the number a `SUM(Exchange)` produces for one day, which is what the `none` effect on this measure's categorical axis forbids
-- ================================================================================================
SELECT count(*) AS rows_for_the_day, round(sum("Exchange"),5) AS summed_across_25_pairs, round(avg("Exchange"),5) AS averaged, round(min("Exchange"),5) AS lowest, round(max("Exchange"),5) AS highest FROM contoso_served.v_contoso_fx_rate_day WHERE "Date" = TIMESTAMP '2025-06-30';
--   ANSWER:
--   25   26.46074   1.05843   0.52784   1.89451

-- ================================================================================================
-- D6 · THE CONTESTABLE CALL, measured: Precomputed (resolve the day's cell, never fold) against Intensive (average the period's cells). The same 223 974 lines converted to USD three ways — per line by its own day's quote (the concept's method), by each month's average quote, and by the delivery's last quote
-- ================================================================================================
WITH per_line AS (SELECT f.*, f."Quantity" * f."NetPrice" * x."Exchange" AS net_usd, f."Quantity" * f."UnitPrice" * x."Exchange" AS gross_usd FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date" = f."OrderDate" AND x."FromCurrency" = f."CurrencyCode" AND x."ToCurrency" = 'USD'), mo AS (SELECT date_trunc('month',"Date") ym, "FromCurrency", avg("Exchange") AS avg_rate FROM contoso_served.v_contoso_fx_rate_day WHERE "ToCurrency"='USD' GROUP BY 1,2), last_q AS (SELECT "FromCurrency", "Exchange" FROM contoso_served.v_contoso_fx_rate_day WHERE "ToCurrency"='USD' AND "Date" = (SELECT max("Date") FROM contoso_served.v_contoso_fx_rate_day)) SELECT round(sum(pl.net_usd),2) AS per_line_own_day_quote, round(sum(pl."Quantity" * pl."NetPrice" * mo.avg_rate),2) AS via_each_months_average_rate, round(sum(pl."Quantity" * pl."NetPrice" * lq."Exchange"),2) AS via_the_last_quote, round(sum(pl."Quantity" * pl."NetPrice" * mo.avg_rate) - sum(pl.net_usd),2) AS monthly_average_error, round((sum(pl."Quantity" * pl."NetPrice" * mo.avg_rate) - sum(pl.net_usd)) / sum(pl.net_usd) * 100, 6) AS monthly_average_error_pct, round(sum(pl."Quantity" * pl."NetPrice" * lq."Exchange") - sum(pl.net_usd),2) AS last_quote_error, round((sum(pl."Quantity" * pl."NetPrice" * lq."Exchange") - sum(pl.net_usd)) / sum(pl.net_usd) * 100, 6) AS last_quote_error_pct FROM per_line pl JOIN mo ON mo.ym = date_trunc('month', pl."OrderDate") AND mo."FromCurrency" = pl."CurrencyCode" JOIN last_q lq ON lq."FromCurrency" = pl."CurrencyCode";
--   ANSWER:
--   219837066.14   219851416.44   224269223.90   14350.3   0.006528   4432157.76   2.01611

-- ================================================================================================
-- D7 · the same contest per MONTH, because the delivery-wide error CANCELS: for each of the 116 months, the per-line conversion against the monthly-average fold — the worst month is the size of the error an averaged rate can actually produce
-- ================================================================================================
WITH per_line AS (SELECT f.*, f."Quantity" * f."NetPrice" * x."Exchange" AS net_usd, f."Quantity" * f."UnitPrice" * x."Exchange" AS gross_usd FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date" = f."OrderDate" AND x."FromCurrency" = f."CurrencyCode" AND x."ToCurrency" = 'USD'), mo AS (SELECT date_trunc('month',"Date") ym, "FromCurrency", avg("Exchange") AS avg_rate FROM contoso_served.v_contoso_fx_rate_day WHERE "ToCurrency"='USD' GROUP BY 1,2), j AS (SELECT date_trunc('month', pl."OrderDate") AS ym, sum(pl.net_usd) AS own_day, sum(pl."Quantity" * pl."NetPrice" * mo.avg_rate) AS averaged FROM per_line pl JOIN mo ON mo.ym = date_trunc('month', pl."OrderDate") AND mo."FromCurrency" = pl."CurrencyCode" GROUP BY 1) SELECT count(*) AS months, round(max(abs(averaged - own_day)),2) AS worst_month_abs_error, round(max(abs(averaged - own_day) / own_day) * 100, 6) AS worst_month_error_pct, round(avg(abs(averaged - own_day) / own_day) * 100, 6) AS mean_month_error_pct FROM j;
--   ANSWER:
--   116   8602.15   0.523494   0.055058

-- ================================================================================================
-- E1 · the numeric columns on the four served DIMENSIONS — are any of them quantities a question would fold, or are they all attributes of one entity? Cardinality against the relation's own row count answers it
-- ================================================================================================
SELECT 'dim_contoso_product' AS relation, count(*) AS rows, count(DISTINCT "ProductKey") AS d_key, count(DISTINCT "Price") AS d_price, count(DISTINCT "Cost") AS d_cost, count(DISTINCT "Weight") AS d_size_column, count(*) FILTER (WHERE "Weight" IS NULL) AS size_column_nulls FROM contoso_served.dim_contoso_product UNION ALL SELECT 'dim_contoso_store', count(*), count(DISTINCT "StoreKey"), NULL, NULL, count(DISTINCT "SquareMeters"), count(*) FILTER (WHERE "SquareMeters" IS NULL) FROM contoso_served.dim_contoso_store;
--   ANSWER:
--   dim_contoso_product   2517   2517   426   480   296   284
--   dim_contoso_store   74   74   NULL   NULL   39   1

-- ================================================================================================
-- E2 · the product dimension's own Price/Cost columns against the fact's UnitPrice/UnitCost — is the dimension's price the same number (a second home for the same figure) or a catalogue price the fact departs from? (a quantity classified on the fact must not be silently re-classifiable on a dimension)
-- ================================================================================================
SELECT count(*) AS lines_joined, count(*) FILTER (WHERE f."UnitPrice" = p."Price") AS fact_unitprice_equals_catalogue_price, count(*) FILTER (WHERE f."UnitPrice" <> p."Price") AS unitprice_differs, round(min(f."UnitPrice" - p."Price"),5) AS min_price_delta, round(max(f."UnitPrice" - p."Price"),5) AS max_price_delta, count(*) FILTER (WHERE f."UnitCost" = p."Cost") AS fact_unitcost_equals_catalogue_cost, count(*) FILTER (WHERE f."UnitCost" <> p."Cost") AS unitcost_differs FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_product p ON p."ProductKey" = f."ProductKey";
--   ANSWER:
--   223974   101021   122953   -799.99750   3748.50000   101021   122953

-- ================================================================================================
-- E3 · the calendar: WorkingDayNumber and the period-label columns are not measures either — they are labels of one day. Row count against the distinct count of the candidate columns
-- ================================================================================================
SELECT count(*) AS days, count(DISTINCT "Date") AS d_date, count(DISTINCT "DateKey") AS d_datekey, count(DISTINCT "WorkingDayNumber") AS d_wdn, count(DISTINCT "Year") AS d_year, count(DISTINCT "YearMonth") AS d_yearmonth FROM contoso_served.dim_contoso_calendar_day;
--   ANSWER:
--   4018   4018   4018   2761   11   132
