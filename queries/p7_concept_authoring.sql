-- queries/p7_concept_authoring.sql — P7 · concept-authoring: every measurement behind a
-- concept declaration, with the answer it returned.
--
-- Run read-only on a COPY of contoso.duckdb in which the six served relations were
-- materialised by executing data/transforms/*.sql verbatim (connection.yaml declares
-- read_only: true, so the views do not exist in the bundle's warehouse). Every figure a
-- concept states comes from below. Measured 2026-09-18 by scratchpad/ingest/p7_measure.py.
--
-- Answers are written as comments under each query, so this file is executable as-is.

-- ================================================================================================
-- K1 · the six served relations, materialised on the scratch copy from the authored transforms — the relations every concept below grounds on
-- ================================================================================================
SELECT table_name, (SELECT count(*) FROM information_schema.columns c WHERE c.table_schema='contoso_served' AND c.table_name=t.table_name) AS columns FROM information_schema.tables t WHERE table_schema='contoso_served' ORDER BY 1;
--   ANSWER
--   dim_contoso_calendar_day   17
--   dim_contoso_customer   12
--   dim_contoso_product   14
--   dim_contoso_store   11
--   v_contoso_fx_rate_day   4
--   v_contoso_order_line   12

-- ================================================================================================
-- K2 · OrderLine · the cell key: does (OrderKey, RowNumber) identify exactly one row of the SERVED fact, and is either part ever null? (the `grain` step of the answer path)
-- ================================================================================================
SELECT count(*) AS rows, count(DISTINCT ("OrderKey", "RowNumber")) AS distinct_keys, sum(CASE WHEN "OrderKey" IS NULL THEN 1 ELSE 0 END) AS null_orderkey, sum(CASE WHEN "RowNumber" IS NULL THEN 1 ELSE 0 END) AS null_rownumber FROM contoso_served.v_contoso_order_line;
--   ANSWER
--   223974   223974   0   0

-- ================================================================================================
-- K3 · Order · how many orders, and how many lines does one carry? (the degenerate dimension: OrderKey groups the lines of an order and joins to nothing)
-- ================================================================================================
WITH l AS (SELECT "OrderKey", count(*) n FROM contoso_served.v_contoso_order_line GROUP BY 1) SELECT count(*) AS orders, min(n) AS min_lines, max(n) AS max_lines, round(avg(n),4) AS avg_lines, sum(n) AS lines FROM l;
--   ANSWER
--   93470   1   7   2.3962   223974

-- ================================================================================================
-- K4 · Order · are the five header attributes constant within one OrderKey? (what makes Order a concept ON the line relation rather than a second served relation)
-- ================================================================================================
SELECT count(*) AS orders_with_a_varying_header FROM (SELECT "OrderKey" FROM contoso_served.v_contoso_order_line GROUP BY 1 HAVING count(DISTINCT "OrderDate")>1 OR count(DISTINCT "DeliveryDate")>1 OR count(DISTINCT "CustomerKey")>1 OR count(DISTINCT "StoreKey")>1 OR count(DISTINCT "CurrencyCode")>1);
--   ANSWER
--   0

-- ================================================================================================
-- N1 · the naive reading — SUM(Quantity x NetPrice) over the whole fact with NO currency handling. Five currencies added as if they were one unit: a number, not a total
-- ================================================================================================
SELECT round(sum("Quantity" * "NetPrice"), 2) AS net_MIXED_currency FROM contoso_served.v_contoso_order_line;
--   ANSWER
--   218814471.66

-- ================================================================================================
-- N2 · the same measure per currency — the denominations the naive sum silently added
-- ================================================================================================
SELECT "CurrencyCode", count(*) AS lines, round(sum("Quantity"*"NetPrice"),2) AS net_local, round(sum("Quantity"*"UnitPrice"),2) AS gross_local FROM contoso_served.v_contoso_order_line GROUP BY 1 ORDER BY 3 DESC;
--   ANSWER
--   USD   113614   111862187.56   118909671.98
--   EUR   49203   47300050.59   50272341.05
--   CAD   24250   23242027.53   24708880.13
--   GBP   22829   23049533.37   24512650.21
--   AUD   14078   13360672.61   14197999.29

-- ================================================================================================
-- N3 · the converted reading — every line's amount taken through the fx grid for its OWN day and currency into USD, then summed. This is a total; N1 is not
-- ================================================================================================
SELECT round(sum(f."Quantity"*f."NetPrice"*x."Exchange"), 2) AS net_usd, round(sum(f."Quantity"*f."UnitPrice"*x."Exchange"), 2) AS gross_usd, count(*) AS lines FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date" = f."OrderDate" AND x."FromCurrency" = f."CurrencyCode" AND x."ToCurrency" = 'USD';
--   ANSWER
--   219837066.14   233692568.81   223974

-- ================================================================================================
-- N4 · does the conversion lose a line? (a converted total that silently drops rows is the second way to get a wrong answer that looks right)
-- ================================================================================================
SELECT count(*) AS lines_without_a_usd_quote FROM contoso_served.v_contoso_order_line f LEFT JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode" AND x."ToCurrency"='USD' WHERE x."Exchange" IS NULL;
--   ANSWER
--   0

-- ================================================================================================
-- N5 · the same figure in each of the five base currencies — there is no privileged one, which is why a silent choice of USD is a disclosure, not a default
-- ================================================================================================
SELECT x."ToCurrency" AS base, round(sum(f."Quantity"*f."NetPrice"*x."Exchange"),2) AS net FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode" GROUP BY 1 ORDER BY 2 DESC;
--   ANSWER
--   AUD   319501262.89
--   CAD   291989776.83
--   USD   219837066.14
--   EUR   199897627.86
--   GBP   173419364.11

-- ================================================================================================
-- N6 · the header/detail double count — the SERVED fact against the raw relation that delivers the same lines a second time (main.sales, deliberately NOT served)
-- ================================================================================================
SELECT (SELECT round(sum("Quantity"*"NetPrice"),2) FROM contoso_served.v_contoso_order_line) AS via_served_order_line, (SELECT round(sum("Quantity"*"NetPrice"),2) FROM main.sales) AS via_raw_sales, (SELECT round(sum("Quantity"*"NetPrice"),2) FROM contoso_served.v_contoso_order_line) + (SELECT round(sum("Quantity"*"NetPrice"),2) FROM main.sales) AS what_summing_both_gives;
--   ANSWER
--   218814471.66   218814471.66   437628943.32

-- ================================================================================================
-- N7 · gross vs net — how many lines carry a discount, and how large is the difference in one base currency? (the reading the question is silent about)
-- ================================================================================================
SELECT count(*) AS lines, sum(CASE WHEN f."NetPrice" < f."UnitPrice" THEN 1 ELSE 0 END) AS discounted_lines, sum(CASE WHEN f."NetPrice" > f."UnitPrice" THEN 1 ELSE 0 END) AS net_above_gross, round(sum(f."Quantity"*(f."UnitPrice"-f."NetPrice")*x."Exchange"),2) AS discount_usd FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode" AND x."ToCurrency"='USD';
--   ANSWER
--   223974   136913   0   13855502.67

-- ================================================================================================
-- N8 · is the amount null anywhere, and what are the ranges? (null_semantics: whether an absent figure exists at all on this fact)
-- ================================================================================================
SELECT sum(CASE WHEN "Quantity" IS NULL THEN 1 ELSE 0 END) AS null_qty, sum(CASE WHEN "NetPrice" IS NULL THEN 1 ELSE 0 END) AS null_net, sum(CASE WHEN "UnitPrice" IS NULL THEN 1 ELSE 0 END) AS null_gross, sum(CASE WHEN "UnitCost" IS NULL THEN 1 ELSE 0 END) AS null_cost, min("Quantity") AS min_qty, max("Quantity") AS max_qty, min("NetPrice") AS min_net, max("NetPrice") AS max_net, sum(CASE WHEN "Quantity" <= 0 THEN 1 ELSE 0 END) AS non_positive_qty, sum(CASE WHEN "NetPrice" <= 0 THEN 1 ELSE 0 END) AS non_positive_net FROM contoso_served.v_contoso_order_line;
--   ANSWER
--   0   0   0   0   1   10   0.81700   6247.50000   0   0

-- ================================================================================================
-- N9 · does the figure accrue per period? (the evidence behind a Flow claim: every day in range carries its own lines, so a year is the sum of its days, not a level read at the end)
-- ================================================================================================
WITH d AS (SELECT "OrderDate" AS day, sum("Quantity"*"NetPrice") AS net FROM contoso_served.v_contoso_order_line GROUP BY 1) SELECT count(*) AS days_with_lines, min(day) AS first_day, max(day) AS last_day, round(min(net),2) AS min_day_net, round(max(net),2) AS max_day_net FROM d;
--   ANSWER
--   3450   2016-05-18 00:00:00   2025-12-31 00:00:00   3.77   400721.29

-- ================================================================================================
-- N10 · the same measure by brand and by continent — the two axes the question scope groups by, measured to prove the roll-up is available (top 5 brands shown)
-- ================================================================================================
SELECT p."Brand", round(sum(f."Quantity"*f."NetPrice"*x."Exchange"),2) AS net_usd FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_product p ON p."ProductKey"=f."ProductKey" JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode" AND x."ToCurrency"='USD' GROUP BY 1 ORDER BY 2 DESC;
--   ANSWER
--   Adventure Works   49394588.49
--   Contoso   38456023.81
--   Wide World Importers   35473528.47
--   The Phone Company   31619132.85
--   Fabrikam   19710987.29
--   Proseware   18506485.23
--   Southridge Video   10765640.69
--   Litware   7089269.23
--   A. Datum   4506238.12
--   Northwind Traders   2649890.59
--   Tailspin Toys   1665281.38

-- ================================================================================================
-- N11 · by continent, through the ONLY relation that carries one (the customer dimension); the store side cannot answer it — dim_contoso_store has no continent column
-- ================================================================================================
SELECT c."Continent", count(*) AS lines, round(sum(f."Quantity"*f."NetPrice"*x."Exchange"),2) AS net_usd FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_customer c ON c."CustomerKey"=f."CustomerKey" JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode" AND x."ToCurrency"='USD' GROUP BY 1 ORDER BY 3 DESC;
--   ANSWER
--   North America   137864   129348175.76
--   Europe   72032   81339744.66
--   Australia   14078   9149145.72

-- ================================================================================================
-- L1 · OrderLine lifecycle — the two dated milestones the relation carries, and whether delivery ever precedes the order (is there a status column? no: measured in K1's columns)
-- ================================================================================================
SELECT count(*) AS lines, sum(CASE WHEN "OrderDate" IS NULL THEN 1 ELSE 0 END) AS null_order_date, sum(CASE WHEN "DeliveryDate" IS NULL THEN 1 ELSE 0 END) AS null_delivery_date, sum(CASE WHEN "DeliveryDate" < "OrderDate" THEN 1 ELSE 0 END) AS delivery_before_order, sum(CASE WHEN "DeliveryDate" = "OrderDate" THEN 1 ELSE 0 END) AS same_day, min(date_diff('day', "OrderDate", "DeliveryDate")) AS min_lag_days, max(date_diff('day', "OrderDate", "DeliveryDate")) AS max_lag_days FROM contoso_served.v_contoso_order_line;
--   ANSWER
--   223974   0   0   0   130424   0   17

-- ================================================================================================
-- L2 · the ordered milestones' own ranges — the window the fact actually covers
-- ================================================================================================
SELECT min("OrderDate") AS first_order, max("OrderDate") AS last_order, min("DeliveryDate") AS first_delivery, max("DeliveryDate") AS last_delivery FROM contoso_served.v_contoso_order_line;
--   ANSWER
--   2016-05-18 00:00:00   2025-12-31 00:00:00   2016-05-18 00:00:00   2026-01-06 00:00:00

-- ================================================================================================
-- T1 · the calendar against the fact — 'latest' resolved from the calendar is not the latest day of data (the anchor must come from the measure's own relation)
-- ================================================================================================
SELECT (SELECT count(*) FROM contoso_served.dim_contoso_calendar_day) AS calendar_days, (SELECT max("Date") FROM contoso_served.dim_contoso_calendar_day) AS calendar_max, (SELECT max("OrderDate") FROM contoso_served.v_contoso_order_line) AS fact_max_order_date, (SELECT count(*) FROM contoso_served.dim_contoso_calendar_day WHERE "Date" > (SELECT max("OrderDate") FROM contoso_served.v_contoso_order_line)) AS calendar_days_after_the_last_order, (SELECT count(*) FROM contoso_served.dim_contoso_calendar_day d WHERE NOT EXISTS (SELECT 1 FROM contoso_served.v_contoso_order_line f WHERE f."OrderDate" = d."Date")) AS calendar_days_with_no_order;
--   ANSWER
--   4018   2026-12-31 00:00:00   2025-12-31 00:00:00   365   568

-- ================================================================================================
-- T2 · the period roll-up the calendar holds — how many members at each level, and is a day in exactly one of each? (what makes a period question answerable by GROUP BY)
-- ================================================================================================
SELECT count(*) AS days, count(DISTINCT "Year") AS years, count(DISTINCT "YearQuarter") AS year_quarters, count(DISTINCT "YearMonth") AS year_months, count(DISTINCT ("Date","YearMonth")) AS day_month_pairs, count(DISTINCT "Quarter") AS quarters, count(DISTINCT "Month") AS months, count(DISTINCT "DayofWeek") AS weekdays, count(DISTINCT "WorkingDay") AS workingday_values FROM contoso_served.dim_contoso_calendar_day;
--   ANSWER
--   4018   11   44   132   4018   4   12   7   2

-- ================================================================================================
-- P1 · Product — rows, key uniqueness, and the axes the dimension carries
-- ================================================================================================
SELECT count(*) AS rows, count(DISTINCT "ProductKey") AS product_keys, count(DISTINCT "Brand") AS brands, count(DISTINCT "Manufacturer") AS manufacturers, count(DISTINCT "CategoryName") AS categories, count(DISTINCT "SubCategoryName") AS subcategories, count(DISTINCT "Color") AS colours, sum(CASE WHEN "Brand" IS NULL THEN 1 ELSE 0 END) AS null_brand, sum(CASE WHEN "CategoryName" IS NULL THEN 1 ELSE 0 END) AS null_category FROM contoso_served.dim_contoso_product;
--   ANSWER
--   2517   2517   11   11   8   32   16   0   0

-- ================================================================================================
-- P2 · Brand — is a product in exactly one brand, and how many products does a brand hold? (the membership rule a grouping declares)
-- ================================================================================================
WITH b AS (SELECT "Brand", count(*) n, count(DISTINCT "Manufacturer") mfr FROM contoso_served.dim_contoso_product GROUP BY 1) SELECT count(*) AS brands, min(n) AS min_products, max(n) AS max_products, max(mfr) AS max_manufacturers_per_brand, (SELECT count(*) FROM (SELECT "ProductKey" FROM contoso_served.dim_contoso_product GROUP BY 1 HAVING count(DISTINCT "Brand")>1)) AS products_in_two_brands FROM b;
--   ANSWER
--   11   47   710   1   0

-- ================================================================================================
-- P2b · the brands themselves, with their product counts — the members of the grouping
-- ================================================================================================
SELECT "Brand", count(*) AS products, min("Manufacturer") AS manufacturer FROM contoso_served.dim_contoso_product GROUP BY 1 ORDER BY 2 DESC;
--   ANSWER
--   Contoso   710   Contoso, Ltd
--   Fabrikam   267   Fabrikam, Inc.
--   Litware   264   Litware, Inc.
--   Proseware   244   Proseware, Inc.
--   Southridge Video   192   Southridge Video
--   Adventure Works   192   Adventure Works
--   Wide World Importers   173   Wide World Importers
--   The Phone Company   152   The Phone Company
--   Tailspin Toys   144   Tailspin Toys
--   A. Datum   132   A. Datum Corporation
--   Northwind Traders   47   Northwind Traders

-- ================================================================================================
-- P3 · ProductCategory — is the two-level hierarchy a function? (is every subcategory in exactly one category, and every product in exactly one subcategory)
-- ================================================================================================
SELECT (SELECT count(*) FROM (SELECT "SubCategoryName" FROM contoso_served.dim_contoso_product GROUP BY 1 HAVING count(DISTINCT "CategoryName")>1)) AS subcategories_in_two_categories, (SELECT count(*) FROM (SELECT "ProductKey" FROM contoso_served.dim_contoso_product GROUP BY 1 HAVING count(DISTINCT "SubCategoryName")>1)) AS products_in_two_subcategories, (SELECT count(DISTINCT ("CategoryKey","CategoryName")) FROM contoso_served.dim_contoso_product) AS category_key_name_pairs, (SELECT count(DISTINCT "CategoryKey") FROM contoso_served.dim_contoso_product) AS category_keys;
--   ANSWER
--   0   0   8   8

-- ================================================================================================
-- P3b · the categories, with their subcategory and product counts
-- ================================================================================================
SELECT "CategoryName", count(DISTINCT "SubCategoryName") AS subcategories, count(*) AS products FROM contoso_served.dim_contoso_product GROUP BY 1 ORDER BY 1;
--   ANSWER
--   Audio   3   115
--   Cameras and camcorders   4   372
--   Cell phones   4   285
--   Computers   6   606
--   Games and Toys   2   166
--   Home Appliances   8   661
--   Music, Movies and Audio Books   1   90
--   TV and Video   4   222

-- ================================================================================================
-- P4 · does every line resolve to a product, and does every product sell? (the dimension over-covers the fact; that is normal and is disclosed, never filtered)
-- ================================================================================================
SELECT (SELECT count(*) FROM contoso_served.v_contoso_order_line f WHERE NOT EXISTS (SELECT 1 FROM contoso_served.dim_contoso_product p WHERE p."ProductKey"=f."ProductKey")) AS lines_with_no_product, (SELECT count(DISTINCT "ProductKey") FROM contoso_served.v_contoso_order_line) AS products_on_a_line, (SELECT count(*) FROM contoso_served.dim_contoso_product) AS products_in_the_dimension;
--   ANSWER
--   0   2517   2517

-- ================================================================================================
-- S1 · Store — 74 rows are versions, not stores: how many codes, how many versions, and does the sentinel row carry fact? (what 'a store' means is an open ruling)
-- ================================================================================================
SELECT count(*) AS rows, count(DISTINCT "StoreKey") AS store_keys, count(DISTINCT "StoreCode") AS store_codes, count(DISTINCT ("StoreCode","OpenDate")) AS code_opendate_pairs, count(DISTINCT "CountryName") AS country_names, sum(CASE WHEN "Status" IS NULL THEN 1 ELSE 0 END) AS null_status FROM contoso_served.dim_contoso_store;
--   ANSWER
--   74   74   67   74   9   59

-- ================================================================================================
-- S1b · the store countries, with the version count and the line count each carries — 'Online' sits in the country column of 41.8 % of the fact
-- ================================================================================================
SELECT s."CountryName", count(DISTINCT s."StoreKey") AS versions, (SELECT count(*) FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_store s2 ON s2."StoreKey"=f."StoreKey" WHERE s2."CountryName"=s."CountryName") AS lines FROM contoso_served.dim_contoso_store s GROUP BY 1 ORDER BY 3 DESC;
--   ANSWER
--   Online   1   93550
--   United States   27   66690
--   United Kingdom   7   14406
--   Germany   10   14190
--   Canada   7   13862
--   Australia   7   7739
--   Netherlands   5   5572
--   Italy   3   4105
--   France   7   3860

-- ================================================================================================
-- S2 · the codes carrying more than one version, and whether their windows overlap (the SCD-2 shape: a store word resolves to a SET of versions)
-- ================================================================================================
SELECT count(*) AS codes_with_two_or_more_versions, max(v) AS max_versions_on_one_code FROM (SELECT "StoreCode", count(*) v FROM contoso_served.dim_contoso_store GROUP BY 1 HAVING count(*)>1);
--   ANSWER
--   6   3

-- ================================================================================================
-- C1 · Customer — rows, key uniqueness, and whether anything on the served projection could resolve a customer BY NAME (nothing: 0 name columns)
-- ================================================================================================
SELECT count(*) AS rows, count(DISTINCT "CustomerKey") AS customer_keys, count(DISTINCT "Country") AS countries, count(DISTINCT "Continent") AS continents, count(DISTINCT "City") AS cities, count(DISTINCT "Gender") AS genders FROM contoso_served.dim_contoso_customer;
--   ANSWER
--   104990   104990   8   3   34581   2

-- ================================================================================================
-- C2 · Country / Continent — is country -> continent a function, and is the country code 1:1 with its full name? (what lets a continent roll-up be declared rather than probed)
-- ================================================================================================
SELECT (SELECT count(*) FROM (SELECT "Country" FROM contoso_served.dim_contoso_customer GROUP BY 1 HAVING count(DISTINCT "Continent")>1)) AS countries_in_two_continents, (SELECT count(*) FROM (SELECT "Country" FROM contoso_served.dim_contoso_customer GROUP BY 1 HAVING count(DISTINCT "CountryFull")>1)) AS codes_with_two_names, (SELECT count(DISTINCT "Country") FROM contoso_served.dim_contoso_customer) AS country_codes, (SELECT count(DISTINCT "CountryFull") FROM contoso_served.dim_contoso_customer) AS country_names;
--   ANSWER
--   0   0   8   8

-- ================================================================================================
-- C2b · the countries and their continents, with the customer count — the members of the continent grouping
-- ================================================================================================
SELECT "Continent", "Country", min("CountryFull") AS country_full, count(*) AS customers FROM contoso_served.dim_contoso_customer GROUP BY 1,2 ORDER BY 1,2;
--   ANSWER
--   Australia   AU   Australia   10108
--   Europe   DE   Germany   9981
--   Europe   FR   France   4879
--   Europe   GB   United Kingdom   14781
--   Europe   IT   Italy   5036
--   Europe   NL   Netherlands   4911
--   North America   CA   Canada   10111
--   North America   US   United States   45183

-- ================================================================================================
-- C3 · how much of the customer dimension is on an order? (the dimension over-covers the fact by half — disclosed, not filtered)
-- ================================================================================================
SELECT (SELECT count(DISTINCT "CustomerKey") FROM contoso_served.v_contoso_order_line) AS customers_on_a_line, (SELECT count(*) FROM contoso_served.dim_contoso_customer) AS customers_in_the_dimension, (SELECT count(*) FROM contoso_served.v_contoso_order_line f WHERE NOT EXISTS (SELECT 1 FROM contoso_served.dim_contoso_customer c WHERE c."CustomerKey"=f."CustomerKey")) AS lines_with_no_customer;
--   ANSWER
--   52189   104990   0

-- ================================================================================================
-- C4 · the store country and the customer country on the same line — two different geographies, and a question saying 'region' does not say which
-- ================================================================================================
SELECT count(*) AS lines, sum(CASE WHEN s."CountryCode" = c."Country" THEN 1 ELSE 0 END) AS same_country, sum(CASE WHEN s."CountryCode" <> c."Country" THEN 1 ELSE 0 END) AS different_country FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_store s ON s."StoreKey"=f."StoreKey" JOIN contoso_served.dim_contoso_customer c ON c."CustomerKey"=f."CustomerKey";
--   ANSWER
--   223974   130424   93550

-- ================================================================================================
-- X1 · ExchangeRate — the grid's shape and completeness (one quote per day per ordered pair), and the self-pair identity
-- ================================================================================================
SELECT count(*) AS rows, count(DISTINCT ("Date","FromCurrency","ToCurrency")) AS keys, count(DISTINCT "Date") AS days, count(DISTINCT "FromCurrency") AS from_currencies, count(DISTINCT "ToCurrency") AS to_currencies, sum(CASE WHEN "FromCurrency"="ToCurrency" AND "Exchange" <> 1 THEN 1 ELSE 0 END) AS self_pairs_not_one, sum(CASE WHEN "Exchange" IS NULL OR "Exchange" <= 0 THEN 1 ELSE 0 END) AS non_positive FROM contoso_served.v_contoso_fx_rate_day;
--   ANSWER
--   100450   100450   4018   5   5   0   0

-- ================================================================================================
-- X2 · is a rate foldable? SUM and AVG over a pair's 4 018 daily quotes against the one quote a question actually needs (the evidence for Precomputed: locate the row, read it)
-- ================================================================================================
SELECT "FromCurrency", "ToCurrency", count(*) AS quotes, round(sum("Exchange"),4) AS sum_of_rates, round(avg("Exchange"),6) AS avg_rate, round(min("Exchange"),6) AS min_rate, round(max("Exchange"),6) AS max_rate FROM contoso_served.v_contoso_fx_rate_day WHERE "FromCurrency"='EUR' AND "ToCurrency"='USD' GROUP BY 1,2;
--   ANSWER
--   EUR   USD   4018   4463.3030   1.110827   0.95650   1.24930

-- ================================================================================================
-- X3 · is the pair ordered? (does the grid carry both directions, and is one the reciprocal of the other — a question asking 'the EUR rate' does not say which way)
-- ================================================================================================
SELECT a."Date", round(a."Exchange",6) AS eur_to_usd, round(b."Exchange",6) AS usd_to_eur, round(a."Exchange"*b."Exchange",6) AS product FROM contoso_served.v_contoso_fx_rate_day a JOIN contoso_served.v_contoso_fx_rate_day b ON b."Date"=a."Date" AND b."FromCurrency"=a."ToCurrency" AND b."ToCurrency"=a."FromCurrency" WHERE a."FromCurrency"='EUR' AND a."ToCurrency"='USD' AND a."Date" IN ('2023-01-02','2024-06-03') ORDER BY 1;
--   ANSWER
--   2023-01-02 00:00:00   1.06830   0.93607   1.000004
--   2024-06-03 00:00:00   1.08420   0.92234   1.000001

-- ================================================================================================
-- X4 · does every (order day, order currency) the fact uses have its quote? (the join the currency answer depends on, over the fact's own population)
-- ================================================================================================
SELECT count(*) AS distinct_day_currency_pairs_on_the_fact, sum(CASE WHEN q IS NULL THEN 1 ELSE 0 END) AS pairs_with_no_quote_row, min(q) AS min_quotes, max(q) AS max_quotes FROM (SELECT f."OrderDate" d, f."CurrencyCode" c, (SELECT count(*) FROM contoso_served.v_contoso_fx_rate_day x WHERE x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode") q FROM contoso_served.v_contoso_order_line f GROUP BY 1,2,3);
--   ANSWER
--   14106   0   5   5

-- ================================================================================================
-- R1 · Currency — the codes on the fact, and what the served plane holds to resolve a currency WORD against (nothing: the register's label column is empty on every row)
-- ================================================================================================
SELECT "CurrencyCode", count(*) AS lines FROM contoso_served.v_contoso_order_line GROUP BY 1 ORDER BY 1;
--   ANSWER
--   AUD   14078
--   CAD   24250
--   EUR   49203
--   GBP   22829
--   USD   113614

-- ================================================================================================
-- R2 · Currency — is the denomination the STORE's local currency? (the cross-tab of store country against currency: every real store country carries exactly one, and the sentinel 'Online' store carries all five)
-- ================================================================================================
SELECT s."CountryName", count(DISTINCT f."CurrencyCode") AS currencies, string_agg(DISTINCT f."CurrencyCode", ',' ORDER BY f."CurrencyCode") AS which FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_store s ON s."StoreKey"=f."StoreKey" GROUP BY 1 ORDER BY 2 DESC, 1;
--   ANSWER
--   Online   5   AUD,CAD,EUR,GBP,USD
--   Australia   1   AUD
--   Canada   1   CAD
--   France   1   EUR
--   Germany   1   EUR
--   Italy   1   EUR
--   Netherlands   1   EUR
--   United Kingdom   1   GBP
--   United States   1   USD

-- ================================================================================================
-- R3 · Currency — how many currencies does ONE order carry? (whether a currency question is a per-order property or a per-line one)
-- ================================================================================================
SELECT max(c) AS max_currencies_on_one_order, count(*) AS orders FROM (SELECT "OrderKey", count(DISTINCT "CurrencyCode") c FROM contoso_served.v_contoso_order_line GROUP BY 1);
--   ANSWER
--   1   93470

-- ================================================================================================
-- S3 · Store · what can a store WORD resolve against? (the register's search columns, measured for uniqueness over the 74 versions — a word that resolves to two rows is not an identity)
-- ================================================================================================
SELECT count(*) AS rows, count(DISTINCT "Description") AS descriptions, count(DISTINCT "StoreCode") AS store_codes, count(DISTINCT ("CountryName","State")) AS country_state_pairs, sum(CASE WHEN "Description" IS NULL THEN 1 ELSE 0 END) AS null_description FROM contoso_served.dim_contoso_store;
--   ANSWER
--   74   67   67   67   0

-- ================================================================================================
-- S4 · Store · the sentinel row in full — the one store version that is not a place (the channel sitting in a country column), and what it does and does not carry
-- ================================================================================================
SELECT "StoreKey", "StoreCode", "CountryCode", "CountryName", "State", "Description", "Status", "SquareMeters", "OpenDate", "CloseDate" FROM contoso_served.dim_contoso_store WHERE "CountryName" = 'Online';
--   ANSWER
--   999999   -1   --   Online   Online   Online store   NULL   NULL   2010-01-01 00:00:00   NULL

-- ================================================================================================
-- S5 · Store · does a country word answer over the WHOLE fact on the store side? (the line count each side can attribute to a real country — the reason a market roll-up is declared on the customer side)
-- ================================================================================================
SELECT (SELECT count(*) FROM contoso_served.v_contoso_order_line) AS lines, (SELECT count(*) FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_store s ON s."StoreKey"=f."StoreKey" WHERE s."CountryCode" <> '--') AS lines_with_a_real_store_country, (SELECT count(*) FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_customer c ON c."CustomerKey"=f."CustomerKey" WHERE c."Country" IS NOT NULL) AS lines_with_a_customer_country, (SELECT count(DISTINCT "CountryCode") FROM contoso_served.dim_contoso_store) AS store_country_codes, (SELECT count(DISTINCT "Country") FROM contoso_served.dim_contoso_customer) AS customer_country_codes;
--   ANSWER
--   223974   130424   223974   9   8

-- ================================================================================================
-- T3 · CalendarPeriod · is a period LABEL an identity? (a year-qualified label is unique to one period; a bare label repeats across years — the trap a 'by quarter' question walks into)
-- ================================================================================================
SELECT count(DISTINCT "YearMonth") AS year_month_labels, count(DISTINCT ("Year","MonthNumber")) AS year_month_pairs, count(DISTINCT "YearQuarter") AS year_quarter_labels, count(DISTINCT ("Year","YearQuarterNumber")) AS year_quarter_pairs, count(DISTINCT "Quarter") AS bare_quarter_labels, count(DISTINCT "Month") AS bare_month_labels, count(DISTINCT "Year") AS years FROM contoso_served.dim_contoso_calendar_day;
--   ANSWER
--   132   132   44   44   4   12   11

-- ================================================================================================
-- T4 · CalendarPeriod · is every calendar level a complete partition of the days? (one row per day in exactly one month, one quarter and one year — what makes a period GROUP BY a fold and not a fan-out)
-- ================================================================================================
SELECT count(*) AS days, (SELECT count(*) FROM (SELECT "Date" FROM contoso_served.dim_contoso_calendar_day GROUP BY 1 HAVING count(DISTINCT "YearMonth")>1 OR count(DISTINCT "YearQuarter")>1 OR count(DISTINCT "Year")>1)) AS days_in_two_periods, (SELECT count(*) FROM (SELECT "YearMonth" FROM contoso_served.dim_contoso_calendar_day GROUP BY 1 HAVING count(DISTINCT "YearQuarter")>1)) AS months_in_two_quarters, (SELECT count(*) FROM (SELECT "YearQuarter" FROM contoso_served.dim_contoso_calendar_day GROUP BY 1 HAVING count(DISTINCT "Year")>1)) AS quarters_in_two_years FROM contoso_served.dim_contoso_calendar_day;
--   ANSWER
--   4018   0   0   0

-- ================================================================================================
-- T5 · CalendarPeriod · the latest day of DATA, per relation that carries a date — the anchor a relative period must take from the measure's own relation, never from the calendar and never from one shared maximum
-- ================================================================================================
SELECT 'v_contoso_order_line.OrderDate' AS relation_column, max("OrderDate") AS latest FROM contoso_served.v_contoso_order_line UNION ALL SELECT 'v_contoso_order_line.DeliveryDate', max("DeliveryDate") FROM contoso_served.v_contoso_order_line UNION ALL SELECT 'v_contoso_fx_rate_day.Date', max("Date") FROM contoso_served.v_contoso_fx_rate_day UNION ALL SELECT 'dim_contoso_calendar_day.Date', max("Date") FROM contoso_served.dim_contoso_calendar_day ORDER BY 2 DESC;
--   ANSWER
--   v_contoso_fx_rate_day.Date   2026-12-31 00:00:00
--   dim_contoso_calendar_day.Date   2026-12-31 00:00:00
--   v_contoso_order_line.DeliveryDate   2026-01-06 00:00:00
--   v_contoso_order_line.OrderDate   2025-12-31 00:00:00

-- ================================================================================================
-- C5 · Customer · what could resolve a customer by NAME on the served projection? (the 12 served columns, and how many of them are a person-name column — the reason Customer is authored with no name register)
-- ================================================================================================
SELECT count(*) AS served_columns, sum(CASE WHEN lower(column_name) LIKE '%name%' THEN 1 ELSE 0 END) AS columns_with_name_in_them, string_agg(column_name, ', ' ORDER BY ordinal_position) AS columns FROM information_schema.columns WHERE table_schema='contoso_served' AND table_name='dim_contoso_customer';
--   ANSWER
--   12   0   CustomerKey, GeoAreaKey, StartDT, EndDT, Continent, CountryFull, Country, StateFull, State, City, ZipCode, Gender

-- ================================================================================================
-- Z1 · every `constraints:` block below is a claim about THIS SNAPSHOT, not an enforced invariant — how many constraints does the warehouse itself declare? (the fact that makes each concept's assertions worth running per load rather than trusting once)
-- ================================================================================================
SELECT count(*) AS declared_constraints FROM duckdb_constraints();
--   ANSWER
--   0

-- ================================================================================================
-- X5 · ExchangeRate · how far does the WRONG direction get? The unserved `main.sales.ExchangeRate` reproduced from the served grid each way, over the same 223 974 lines — and how many of those lines carry a rate of exactly 1, where the two directions agree by construction (the reason a direction cannot be inferred from a sample)
-- ================================================================================================
SELECT (SELECT count(*) FROM main.sales s JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=s."OrderDate" AND x."FromCurrency"='USD' AND x."ToCurrency"=s."CurrencyCode" WHERE round(x."Exchange",5)=round(s."ExchangeRate",5)) AS reproduced_usd_to_order_currency, (SELECT count(*) FROM main.sales s JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=s."OrderDate" AND x."FromCurrency"=s."CurrencyCode" AND x."ToCurrency"='USD' WHERE round(x."Exchange",5)=round(s."ExchangeRate",5)) AS reproduced_order_currency_to_usd, (SELECT count(*) FROM main.sales WHERE round("ExchangeRate",5)=1) AS lines_whose_rate_is_one, (SELECT count(*) FROM main.sales) AS lines;
--   ANSWER
--   223974   113627   113627   223974

-- ================================================================================================
-- X6 · ExchangeRate · the same test per denomination — the wrong direction is right on every USD line and on almost nothing else, so a USD-heavy sample cannot tell the two apart
-- ================================================================================================
SELECT s."CurrencyCode", count(*) AS lines, sum(CASE WHEN round(x."Exchange",5)=round(s."ExchangeRate",5) THEN 1 ELSE 0 END) AS reproduced_by_usd_to_ccy, sum(CASE WHEN round(s."ExchangeRate",5)=1 THEN 1 ELSE 0 END) AS rate_is_one FROM main.sales s JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=s."OrderDate" AND x."FromCurrency"='USD' AND x."ToCurrency"=s."CurrencyCode" GROUP BY 1 ORDER BY 2 DESC;
--   ANSWER
--   USD   113614   113614   113614
--   EUR   49203   49203   13
--   CAD   24250   24250   0
--   GBP   22829   22829   0
--   AUD   14078   14078   0

-- ================================================================================================
-- G1 · GeoArea · the delivery's only region key, on both dimensions that carry it — is one key one region? (does it determine a state and a country, and is the same key set used on both sides?)
-- ================================================================================================
SELECT (SELECT count(DISTINCT "GeoAreaKey") FROM contoso_served.dim_contoso_customer) AS areas_on_customer, (SELECT count(DISTINCT "GeoAreaKey") FROM contoso_served.dim_contoso_store) AS areas_on_store, (SELECT count(*) FROM (SELECT "GeoAreaKey" FROM contoso_served.dim_contoso_customer GROUP BY 1 HAVING count(DISTINCT "State")>1 OR count(DISTINCT "Country")>1)) AS areas_with_two_states_or_countries, (SELECT count(*) FROM (SELECT DISTINCT "GeoAreaKey" FROM contoso_served.dim_contoso_store EXCEPT SELECT DISTINCT "GeoAreaKey" FROM contoso_served.dim_contoso_customer)) AS store_areas_not_on_customer;
--   ANSWER
--   608   67   0   4

-- ================================================================================================
-- G2 · Country · the shape of the code and the code-to-name pairing on each side — what lets the code be called an identity, and what the sentinel does to that claim
-- ================================================================================================
SELECT 'dim_contoso_customer.Country' AS relation_column, count(DISTINCT "Country") AS codes, sum(CASE WHEN length("Country")=2 AND "Country" = upper("Country") THEN 0 ELSE 1 END) AS rows_whose_code_is_not_two_upper_letters, count(DISTINCT "CountryFull") AS names FROM contoso_served.dim_contoso_customer UNION ALL SELECT 'dim_contoso_store.CountryCode', count(DISTINCT "CountryCode"), sum(CASE WHEN length("CountryCode")=2 AND "CountryCode" = upper("CountryCode") THEN 0 ELSE 1 END), count(DISTINCT "CountryName") FROM contoso_served.dim_contoso_store;
--   ANSWER
--   dim_contoso_customer.Country   8   0   8
--   dim_contoso_store.CountryCode   9   0   9

-- ================================================================================================
-- S6 · Store · the Status value set over the 74 versions, with the line count each carries — a status word can only resolve to a value the relation actually holds
-- ================================================================================================
WITH v AS (SELECT coalesce("Status", '(absent)') AS status, "StoreKey" FROM contoso_served.dim_contoso_store), l AS (SELECT coalesce(s."Status", '(absent)') AS status, count(*) AS lines FROM contoso_served.v_contoso_order_line f JOIN contoso_served.dim_contoso_store s ON s."StoreKey"=f."StoreKey" GROUP BY 1) SELECT v.status, count(DISTINCT v."StoreKey") AS versions, coalesce(max(l.lines),0) AS lines FROM v LEFT JOIN l ON l.status=v.status GROUP BY 1 ORDER BY 2 DESC;
--   ANSWER
--   (absent)   59   222136
--   Closed   8   1566
--   Restructured   7   272

-- ================================================================================================
-- R4 · the registers the concepts below delegate name resolution to — read from the CSV files themselves: the row count, the code column (header[0]) and, for the currency register, how many rows carry an EMPTY label (a name nothing in the data supplies)
-- ================================================================================================
SELECT 'contoso_brand' AS register, count(*) AS rows, (SELECT count(*) FROM read_csv('data/lookups/contoso_brand.lookup.csv') WHERE label IS NULL OR label='') AS rows_with_no_label FROM read_csv('data/lookups/contoso_brand.lookup.csv') UNION ALL SELECT 'contoso_currency', count(*), (SELECT count(*) FROM read_csv('data/lookups/contoso_currency.lookup.csv') WHERE label IS NULL OR label='') FROM read_csv('data/lookups/contoso_currency.lookup.csv') UNION ALL SELECT 'contoso_country', count(*), (SELECT count(*) FROM read_csv('data/lookups/contoso_country.lookup.csv') WHERE label IS NULL OR label='') FROM read_csv('data/lookups/contoso_country.lookup.csv') UNION ALL SELECT 'contoso_product_category', count(*), (SELECT count(*) FROM read_csv('data/lookups/contoso_product_category.lookup.csv') WHERE label IS NULL OR label='') FROM read_csv('data/lookups/contoso_product_category.lookup.csv') UNION ALL SELECT 'dim_contoso_product', count(*), (SELECT count(*) FROM read_csv('data/lookups/dim_contoso_product.lookup.csv') WHERE label IS NULL OR label='') FROM read_csv('data/lookups/dim_contoso_product.lookup.csv') UNION ALL SELECT 'dim_contoso_store', count(*), (SELECT count(*) FROM read_csv('data/lookups/dim_contoso_store.lookup.csv') WHERE label IS NULL OR label='') FROM read_csv('data/lookups/dim_contoso_store.lookup.csv') UNION ALL SELECT 'contoso_calendar_month', count(*), (SELECT count(*) FROM read_csv('data/lookups/contoso_calendar_month.lookup.csv') WHERE label IS NULL OR label='') FROM read_csv('data/lookups/contoso_calendar_month.lookup.csv') ORDER BY 1;
--   ANSWER
--   contoso_brand   11   0
--   contoso_calendar_month   12   0
--   contoso_country   9   0
--   contoso_currency   5   5
--   contoso_product_category   8   0
--   dim_contoso_product   2517   0
--   dim_contoso_store   74   0

-- ================================================================================================
-- R5 · the code column of every register a concept cites — header[0], read from the file itself (check_no_fabricated_identifiers reads header[0] as the register's declared key; check_lookups rule A requires a cited register to exist and be non-empty). Columns: register, header[0], column count, data rows
-- ================================================================================================
-- read offline from data/lookups/<stem>.lookup.csv (no SQL);
--   ANSWER
--   contoso_brand   Brand   7   11
--   contoso_currency   CurrencyCode   6   5
--   contoso_country   Country   7   9
--   contoso_product_category   CategoryKey   6   8
--   contoso_product_subcategory   SubCategoryKey   7   32
--   contoso_calendar_month   MonthNumber   9   12
--   contoso_calendar_quarter   Quarter   6   4
--   contoso_calendar_weekday   DayofWeekNumber   8   7
--   contoso_working_day   WorkingDay   6   2
--   contoso_geo_area   GeoAreaKey   8   608
--   dim_contoso_product   ProductKey   10   2517
--   dim_contoso_store   StoreKey   10   74

