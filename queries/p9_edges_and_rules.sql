-- queries/p9_edges_and_rules.sql
-- P9 · edges-and-rules — EVERY measurement behind every edge this step ruled on, with the answer
-- it returned. Measured read-only on 2026-09-18 against the SIX SERVED VIEWS, materialised on a
-- scratch COPY of contoso.duckdb by executing data/transforms/*.sql verbatim (connection.yaml
-- declares read_only: true, so the served schema does not exist in the warehouse file). The copy
-- was deleted. Nothing was written to contoso.duckdb.
--
-- THE SQL SHAPES ARE THE FRAMEWORK'S OWN, copied from tools/mac_measure_edges.py:
--   join_predicate   -> lhs / matched / fanout        (containment AND fan, never one alone)
--   column_presence  -> population / missing          (NULL *and* empty string count as missing)
--   value_uniqueness -> population / keys_with_many / keys_with_none
-- That tool could not be run here, for two independent reasons, and both are recorded rather than
-- worked around: it refuses without ontology/edges.yaml (the ontology plane is operator-locked and
-- P9 authored no file under it), and its executor is Athena-only while this warehouse is a local
-- DuckDB file. Reproduce: python3 scratchpad/ingest/p9_edges.py — byte-identical on re-run.
--
-- A NUMBER HERE IS NOT AN EDGE. No edge, and no rule, was authored by this step: every path under
-- ontology/ is denied by .claude/hooks/ontology_guard.py [mac.ontology-guard/3], whose refusal also
-- forbids writing the content anywhere else. What follows is the evidence an edge WOULD carry, in
-- the shape the framework's gates read, held until a human opens the plane.

-- ================================================================================================
-- J1 · fact -> catalogue. `v_contoso_order_line.ProductKey = dim_contoso_product.ProductKey`, the FK data/datasets/v_contoso_order_line.yaml declares as fk_product. CONTAINMENT (does every key find a partner) and FANOUT (does it find at most one) counted separately
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   2517   2517   1
SELECT (SELECT COUNT(DISTINCT ProductKey) FROM contoso_served.v_contoso_order_line) AS lhs, (SELECT COUNT(*) FROM (SELECT DISTINCT ProductKey v FROM contoso_served.v_contoso_order_line) a JOIN (SELECT DISTINCT ProductKey k FROM contoso_served.dim_contoso_product) b ON a.v = b.k) AS matched, (SELECT COALESCE(MAX(c), 0) FROM (SELECT ProductKey, COUNT(*) c FROM contoso_served.dim_contoso_product GROUP BY 1)) AS fanout;

-- ================================================================================================
-- J2 · fact -> stores. fk_store. The sentinel StoreKey 999999 ('Online') is a served row and is INCLUDED on purpose: it carries 93 550 of 223 974 lines
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   64   64   1
SELECT (SELECT COUNT(DISTINCT StoreKey) FROM contoso_served.v_contoso_order_line) AS lhs, (SELECT COUNT(*) FROM (SELECT DISTINCT StoreKey v FROM contoso_served.v_contoso_order_line) a JOIN (SELECT DISTINCT StoreKey k FROM contoso_served.dim_contoso_store) b ON a.v = b.k) AS matched, (SELECT COALESCE(MAX(c), 0) FROM (SELECT StoreKey, COUNT(*) c FROM contoso_served.dim_contoso_store GROUP BY 1)) AS fanout;

-- ================================================================================================
-- J3 · fact -> customers. fk_customer. The dimension is far wider than the fact; see N3
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   52189   52189   1
SELECT (SELECT COUNT(DISTINCT CustomerKey) FROM contoso_served.v_contoso_order_line) AS lhs, (SELECT COUNT(*) FROM (SELECT DISTINCT CustomerKey v FROM contoso_served.v_contoso_order_line) a JOIN (SELECT DISTINCT CustomerKey k FROM contoso_served.dim_contoso_customer) b ON a.v = b.k) AS matched, (SELECT COALESCE(MAX(c), 0) FROM (SELECT CustomerKey, COUNT(*) c FROM contoso_served.dim_contoso_customer GROUP BY 1)) AS fanout;

-- ================================================================================================
-- J4 · fact -> calendar, ROLE 'ordered on'. fk_order_date. The default period role
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   3450   3450   1
SELECT (SELECT COUNT(DISTINCT OrderDate) FROM contoso_served.v_contoso_order_line) AS lhs, (SELECT COUNT(*) FROM (SELECT DISTINCT OrderDate v FROM contoso_served.v_contoso_order_line) a JOIN (SELECT DISTINCT Date k FROM contoso_served.dim_contoso_calendar_day) b ON a.v = b.k) AS matched, (SELECT COALESCE(MAX(c), 0) FROM (SELECT Date, COUNT(*) c FROM contoso_served.dim_contoso_calendar_day GROUP BY 1)) AS fanout;

-- ================================================================================================
-- J5 · fact -> calendar, ROLE 'delivered on'. fk_delivery_date. THE SECOND ROLE OF ONE DIMENSION (role_playing_dimension), not a second dimension
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   3498   3498   1
SELECT (SELECT COUNT(DISTINCT DeliveryDate) FROM contoso_served.v_contoso_order_line) AS lhs, (SELECT COUNT(*) FROM (SELECT DISTINCT DeliveryDate v FROM contoso_served.v_contoso_order_line) a JOIN (SELECT DISTINCT Date k FROM contoso_served.dim_contoso_calendar_day) b ON a.v = b.k) AS matched, (SELECT COALESCE(MAX(c), 0) FROM (SELECT Date, COUNT(*) c FROM contoso_served.dim_contoso_calendar_day GROUP BY 1)) AS fanout;

-- ================================================================================================
-- J6 · quote grid -> calendar. fk_quote_date. Whether the grid covers the calendar decides whether a conversion can ever lose a line
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   4018   4018   1
SELECT (SELECT COUNT(DISTINCT Date) FROM contoso_served.v_contoso_fx_rate_day) AS lhs, (SELECT COUNT(*) FROM (SELECT DISTINCT Date v FROM contoso_served.v_contoso_fx_rate_day) a JOIN (SELECT DISTINCT Date k FROM contoso_served.dim_contoso_calendar_day) b ON a.v = b.k) AS matched, (SELECT COALESCE(MAX(c), 0) FROM (SELECT Date, COUNT(*) c FROM contoso_served.dim_contoso_calendar_day GROUP BY 1)) AS fanout;

-- ================================================================================================
-- C1 · OrderKey on the fact — a DEGENERATE DIMENSION (the order header is not served, NS-ORDERS-02), so 'every line belongs to exactly one order' is a PRESENCE claim, not a join
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   223974   0
SELECT COUNT(*) AS population, SUM(CASE WHEN OrderKey IS NULL OR CAST(OrderKey AS VARCHAR) = '' THEN 1 ELSE 0 END) AS missing FROM contoso_served.v_contoso_order_line;

-- ================================================================================================
-- C2 · CurrencyCode on the fact — the denomination of every amount on the row; no served currency relation exists, the population is a register
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   223974   0
SELECT COUNT(*) AS population, SUM(CASE WHEN CurrencyCode IS NULL OR CAST(CurrencyCode AS VARCHAR) = '' THEN 1 ELSE 0 END) AS missing FROM contoso_served.v_contoso_order_line;

-- ================================================================================================
-- C3 · FromCurrency on the quote grid — the source side of a quote
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   100450   0
SELECT COUNT(*) AS population, SUM(CASE WHEN FromCurrency IS NULL OR CAST(FromCurrency AS VARCHAR) = '' THEN 1 ELSE 0 END) AS missing FROM contoso_served.v_contoso_fx_rate_day;

-- ================================================================================================
-- C4 · ToCurrency on the quote grid — THE ROLE A CONVERSION MUST PIN; see X3/X4
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   100450   0
SELECT COUNT(*) AS population, SUM(CASE WHEN ToCurrency IS NULL OR CAST(ToCurrency AS VARCHAR) = '' THEN 1 ELSE 0 END) AS missing FROM contoso_served.v_contoso_fx_rate_day;

-- ================================================================================================
-- V1 · customer -> country, as a key->value pair on ONE relation (Country has no served relation of its own). 'exactly one' means both: no key with two values AND no key with none
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   104990   0   0
SELECT COUNT(*) AS population, SUM(CASE WHEN c > 1 THEN 1 ELSE 0 END) AS keys_with_many, SUM(CASE WHEN c = 0 THEN 1 ELSE 0 END) AS keys_with_none FROM (SELECT CustomerKey, COUNT(DISTINCT Country) c FROM contoso_served.dim_contoso_customer GROUP BY 1);

-- ================================================================================================
-- V2 · customer -> geo area, same shape. Read with G1/G2
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   104990   0   0
SELECT COUNT(*) AS population, SUM(CASE WHEN c > 1 THEN 1 ELSE 0 END) AS keys_with_many, SUM(CASE WHEN c = 0 THEN 1 ELSE 0 END) AS keys_with_none FROM (SELECT CustomerKey, COUNT(DISTINCT GeoAreaKey) c FROM contoso_served.dim_contoso_customer GROUP BY 1);

-- ================================================================================================
-- V3 · store -> country code, same shape
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   74   0   0
SELECT COUNT(*) AS population, SUM(CASE WHEN c > 1 THEN 1 ELSE 0 END) AS keys_with_many, SUM(CASE WHEN c = 0 THEN 1 ELSE 0 END) AS keys_with_none FROM (SELECT StoreKey, COUNT(DISTINCT CountryCode) c FROM contoso_served.dim_contoso_store GROUP BY 1);

-- ================================================================================================
-- V4 · store -> geo area, same shape. Read with G1/G2
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   74   0   0
SELECT COUNT(*) AS population, SUM(CASE WHEN c > 1 THEN 1 ELSE 0 END) AS keys_with_many, SUM(CASE WHEN c = 0 THEN 1 ELSE 0 END) AS keys_with_none FROM (SELECT StoreKey, COUNT(DISTINCT GeoAreaKey) c FROM contoso_served.dim_contoso_store GROUP BY 1);

-- ================================================================================================
-- V5 · product -> brand. MEASURED BUT NOT WIRED: Brand declares `members.over: Product`, and FRAMEWORK.md §7 rules containment to be concept structure, not an edge. The number is taken so the decision is not hiding an unknown
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   2517   0   0
SELECT COUNT(*) AS population, SUM(CASE WHEN c > 1 THEN 1 ELSE 0 END) AS keys_with_many, SUM(CASE WHEN c = 0 THEN 1 ELSE 0 END) AS keys_with_none FROM (SELECT ProductKey, COUNT(DISTINCT Brand) c FROM contoso_served.dim_contoso_product GROUP BY 1);

-- ================================================================================================
-- V6 · product -> category key. MEASURED BUT NOT WIRED, same reason (ProductCategory declares two ordered levels over Product)
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   2517   0   0
SELECT COUNT(*) AS population, SUM(CASE WHEN c > 1 THEN 1 ELSE 0 END) AS keys_with_many, SUM(CASE WHEN c = 0 THEN 1 ELSE 0 END) AS keys_with_none FROM (SELECT ProductKey, COUNT(DISTINCT CategoryKey) c FROM contoso_served.dim_contoso_product GROUP BY 1);

-- ================================================================================================
-- V7 · calendar day -> month label. MEASURED BUT NOT WIRED, same reason (CalendarPeriod declares three levels over CalendarDay); T1 takes all three levels at once
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   4018   0   0
SELECT COUNT(*) AS population, SUM(CASE WHEN c > 1 THEN 1 ELSE 0 END) AS keys_with_many, SUM(CASE WHEN c = 0 THEN 1 ELSE 0 END) AS keys_with_none FROM (SELECT Date, COUNT(DISTINCT YearMonth) c FROM contoso_served.dim_contoso_calendar_day GROUP BY 1);

-- ================================================================================================
-- V8 · country -> continent. MEASURED BUT NOT WIRED, same reason — and this is the framework pattern index's own example of a rollup that is concept structure
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   8   0   0
SELECT COUNT(*) AS population, SUM(CASE WHEN c > 1 THEN 1 ELSE 0 END) AS keys_with_many, SUM(CASE WHEN c = 0 THEN 1 ELSE 0 END) AS keys_with_none FROM (SELECT Country, COUNT(DISTINCT Continent) c FROM contoso_served.dim_contoso_customer GROUP BY 1);

-- ================================================================================================
-- G1 · IS 'GeoArea' ONE POPULATION OR TWO? The concept grounds on BOTH dimensions, and neither carries a relation of record. The two key domains, and their overlap
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   608   67   63
SELECT (SELECT COUNT(DISTINCT "GeoAreaKey") FROM contoso_served.dim_contoso_customer) AS customer_areas, (SELECT COUNT(DISTINCT "GeoAreaKey") FROM contoso_served.dim_contoso_store) AS store_areas, (SELECT COUNT(*) FROM (SELECT DISTINCT "GeoAreaKey" k FROM contoso_served.dim_contoso_store) a JOIN (SELECT DISTINCT "GeoAreaKey" k FROM contoso_served.dim_contoso_customer) b ON a.k = b.k) AS shared;

-- ================================================================================================
-- G2 · the store areas no customer is in — named, not counted
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   -1
--   79
--   291
--   519
SELECT DISTINCT "GeoAreaKey" FROM contoso_served.dim_contoso_store WHERE "GeoAreaKey" NOT IN (SELECT "GeoAreaKey" FROM contoso_served.dim_contoso_customer) ORDER BY 1;

-- ================================================================================================
-- G3 · IS 'Country' ONE VOCABULARY OR TWO? Same question for the country code, which the Country concept also takes from both dimensions
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   8   9   8
SELECT (SELECT COUNT(DISTINCT "Country") FROM contoso_served.dim_contoso_customer) AS customer_codes, (SELECT COUNT(DISTINCT "CountryCode") FROM contoso_served.dim_contoso_store) AS store_codes, (SELECT COUNT(*) FROM (SELECT DISTINCT "CountryCode" k FROM contoso_served.dim_contoso_store) a JOIN (SELECT DISTINCT "Country" k FROM contoso_served.dim_contoso_customer) b ON a.k = b.k) AS shared;

-- ================================================================================================
-- G4 · the two code sets side by side — the whole domain, so 'shared' can be read rather than trusted
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   --   False   True
--   AU   True   True
--   CA   True   True
--   DE   True   True
--   FR   True   True
--   GB   True   True
--   IT   True   True
--   NL   True   True
--   US   True   True
SELECT coalesce(c.k, s.k) AS code, c.k IS NOT NULL AS on_customer, s.k IS NOT NULL AS on_store FROM (SELECT DISTINCT "Country" k FROM contoso_served.dim_contoso_customer) c FULL JOIN (SELECT DISTINCT "CountryCode" k FROM contoso_served.dim_contoso_store) s ON c.k = s.k ORDER BY 1;

-- ================================================================================================
-- X1 · the shape of the quote grid: is it complete?
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   100450   4018   5   5
SELECT count(*) AS rows, count(DISTINCT "Date") AS days, count(DISTINCT "FromCurrency") AS from_codes, count(DISTINCT "ToCurrency") AS to_codes FROM contoso_served.v_contoso_fx_rate_day;

-- ================================================================================================
-- X2 · the ToCurrency members and their row counts
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   AUD   20090
--   CAD   20090
--   EUR   20090
--   GBP   20090
--   USD   20090
SELECT "ToCurrency", count(*) AS rows FROM contoso_served.v_contoso_fx_rate_day GROUP BY 1 ORDER BY 1;

-- ================================================================================================
-- X3 · THE CONVERSION SEAM, UNPINNED. The composite key (order day, denomination) -> (Date, FromCurrency): containment, and the fanout that key meets in the grid
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   14106   14106   5
SELECT (SELECT COUNT(*) FROM (SELECT DISTINCT "OrderDate","CurrencyCode" FROM contoso_served.v_contoso_order_line)) AS lhs, (SELECT COUNT(*) FROM (SELECT DISTINCT "OrderDate" d,"CurrencyCode" c FROM contoso_served.v_contoso_order_line) a JOIN (SELECT DISTINCT "Date" d,"FromCurrency" c FROM contoso_served.v_contoso_fx_rate_day) b ON a.d=b.d AND a.c=b.c) AS matched, (SELECT COALESCE(MAX(n),0) FROM (SELECT "Date","FromCurrency", count(*) n FROM contoso_served.v_contoso_fx_rate_day GROUP BY 1,2)) AS fanout;

-- ================================================================================================
-- X4 · THE SAME SEAM, PINNED to one target denomination. The fan collapses to 1 and containment is unchanged — which is what makes the pin a requirement and not a preference
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   14106   14106   1
SELECT (SELECT COUNT(*) FROM (SELECT DISTINCT "OrderDate","CurrencyCode" FROM contoso_served.v_contoso_order_line)) AS lhs, (SELECT COUNT(*) FROM (SELECT DISTINCT "OrderDate" d,"CurrencyCode" c FROM contoso_served.v_contoso_order_line) a JOIN (SELECT DISTINCT "Date" d,"FromCurrency" c FROM contoso_served.v_contoso_fx_rate_day WHERE "ToCurrency" = 'USD') b ON a.d=b.d AND a.c=b.c) AS matched, (SELECT COALESCE(MAX(n),0) FROM (SELECT "Date","FromCurrency", count(*) n FROM contoso_served.v_contoso_fx_rate_day WHERE "ToCurrency" = 'USD' GROUP BY 1,2)) AS fanout;

-- ================================================================================================
-- X5 · WHAT AN UNPINNED CONVERSION ACTUALLY COSTS, in rows and in money. Not an adjective: the same expression over the two joins
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   223974   1119870   223974   1204645097.83   219837066.14
SELECT (SELECT count(*) FROM contoso_served.v_contoso_order_line) AS lines, (SELECT count(*) FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode") AS rows_unpinned, (SELECT count(*) FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode" AND x."ToCurrency"='USD') AS rows_pinned, (SELECT round(sum(f."Quantity"*f."NetPrice"*x."Exchange"),2) FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode") AS sum_unpinned, (SELECT round(sum(f."Quantity"*f."NetPrice"*x."Exchange"),2) FROM contoso_served.v_contoso_order_line f JOIN contoso_served.v_contoso_fx_rate_day x ON x."Date"=f."OrderDate" AND x."FromCurrency"=f."CurrencyCode" AND x."ToCurrency"='USD') AS sum_pinned;

-- ================================================================================================
-- X6 · the self-quotes (From = To). If they are exactly 1, the conversion join is safe to apply even to a single-denomination scope
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   20090   1.00000   1.00000
SELECT count(*) AS rows, min("Exchange") AS min_rate, max("Exchange") AS max_rate FROM contoso_served.v_contoso_fx_rate_day WHERE "FromCurrency" = "ToCurrency";

-- ================================================================================================
-- R1 · the reverse end of every fact edge: how many lines one dimension row can carry. A '0..N' promises nothing, but the number is what tells a reader whether a join is wide
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   93470   7   468   93550   28   408
SELECT (SELECT count(DISTINCT "OrderKey") FROM contoso_served.v_contoso_order_line) AS orders, (SELECT max(n) FROM (SELECT "OrderKey", count(*) n FROM contoso_served.v_contoso_order_line GROUP BY 1)) AS max_lines_per_order, (SELECT max(n) FROM (SELECT "ProductKey", count(*) n FROM contoso_served.v_contoso_order_line GROUP BY 1)) AS max_lines_per_product, (SELECT max(n) FROM (SELECT "StoreKey", count(*) n FROM contoso_served.v_contoso_order_line GROUP BY 1)) AS max_lines_per_store, (SELECT max(n) FROM (SELECT "CustomerKey", count(*) n FROM contoso_served.v_contoso_order_line GROUP BY 1)) AS max_lines_per_customer, (SELECT max(n) FROM (SELECT "OrderDate", count(*) n FROM contoso_served.v_contoso_order_line GROUP BY 1)) AS max_lines_per_order_day;

-- ================================================================================================
-- R2 · are the five header attributes constant across an order's lines? This is what makes Order addressable through a carried column instead of a relation of its own
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   93470   0   0   0   0   0
SELECT count(*) AS orders, sum(CASE WHEN dc>1 THEN 1 ELSE 0 END) AS orders_with_two_customers, sum(CASE WHEN ds>1 THEN 1 ELSE 0 END) AS orders_with_two_stores, sum(CASE WHEN dd>1 THEN 1 ELSE 0 END) AS orders_with_two_order_dates, sum(CASE WHEN dv>1 THEN 1 ELSE 0 END) AS orders_with_two_delivery_dates, sum(CASE WHEN dcur>1 THEN 1 ELSE 0 END) AS orders_with_two_currencies FROM (SELECT "OrderKey", count(DISTINCT "CustomerKey") dc, count(DISTINCT "StoreKey") ds, count(DISTINCT "OrderDate") dd, count(DISTINCT "DeliveryDate") dv, count(DISTINCT "CurrencyCode") dcur FROM contoso_served.v_contoso_order_line GROUP BY 1);

-- ================================================================================================
-- T1 · all three declared period levels at once, plus the weekday. Every one a function of the day, or the roll-up is not a roll-up
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   4018   0   0   0   0
SELECT count(*) AS days, sum(CASE WHEN y>1 THEN 1 ELSE 0 END) AS days_in_two_years, sum(CASE WHEN q>1 THEN 1 ELSE 0 END) AS days_in_two_quarters, sum(CASE WHEN mo>1 THEN 1 ELSE 0 END) AS days_in_two_months, sum(CASE WHEN w>1 THEN 1 ELSE 0 END) AS days_in_two_weekdays FROM (SELECT "Date", count(DISTINCT "Year") y, count(DISTINCT "YearQuarter") q, count(DISTINCT "YearMonth") mo, count(DISTINCT "DayofWeek") w FROM contoso_served.dim_contoso_calendar_day GROUP BY 1);

-- ================================================================================================
-- N1 · the sentinel store row in full — the one row that joins like a store and is not a market
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   999999   -1   --   Online   Online   NULL   -1
SELECT "StoreKey","StoreCode","CountryCode","CountryName","State","Status","GeoAreaKey" FROM contoso_served.dim_contoso_store WHERE "StoreKey" = 999999;

-- ================================================================================================
-- N2 · the spans, side by side. The calendar and the grid are both WIDER than the fact, which is why every containment above is 100 % and why a 'latest period' read off the calendar is empty
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   2016-01-01 00:00:00   2026-12-31 00:00:00   2016-05-18 00:00:00   2025-12-31 00:00:00   2016-05-18 00:00:00   2026-01-06 00:00:00   2016-01-01 00:00:00   2026-12-31 00:00:00
SELECT (SELECT min("Date") FROM contoso_served.dim_contoso_calendar_day) AS calendar_first, (SELECT max("Date") FROM contoso_served.dim_contoso_calendar_day) AS calendar_last, (SELECT min("OrderDate") FROM contoso_served.v_contoso_order_line) AS first_order, (SELECT max("OrderDate") FROM contoso_served.v_contoso_order_line) AS last_order, (SELECT min("DeliveryDate") FROM contoso_served.v_contoso_order_line) AS first_delivery, (SELECT max("DeliveryDate") FROM contoso_served.v_contoso_order_line) AS last_delivery, (SELECT min("Date") FROM contoso_served.v_contoso_fx_rate_day) AS grid_first, (SELECT max("Date") FROM contoso_served.v_contoso_fx_rate_day) AS grid_last;

-- ================================================================================================
-- N3 · the from-end of every fact edge: how many dimension rows carry NO line at all. This is what makes '0..N' the measured reading rather than a hedge
-- ------------------------------------------------------------------------------------------------
-- ANSWER:
--   4018   3450   2517   2517   74   64   104990   52189
SELECT (SELECT count(*) FROM contoso_served.dim_contoso_calendar_day) AS calendar_days, (SELECT count(DISTINCT "OrderDate") FROM contoso_served.v_contoso_order_line) AS days_with_an_order, (SELECT count(*) FROM contoso_served.dim_contoso_product) AS products, (SELECT count(DISTINCT "ProductKey") FROM contoso_served.v_contoso_order_line) AS products_sold, (SELECT count(*) FROM contoso_served.dim_contoso_store) AS stores, (SELECT count(DISTINCT "StoreKey") FROM contoso_served.v_contoso_order_line) AS stores_selling, (SELECT count(*) FROM contoso_served.dim_contoso_customer) AS customers, (SELECT count(DISTINCT "CustomerKey") FROM contoso_served.v_contoso_order_line) AS customers_buying;
