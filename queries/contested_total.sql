-- The demo: "What were our total sales?" — one question, several defensible answers.
--
-- Run against the warehouse built by setup.sh:
--     duckdb contoso.duckdb < queries/contested_total.sql
--
-- Numbers in the comments are from the 100k-order sample; they scale with the size
-- you built. The point is not the figure — it's that a naive text-to-SQL bot silently
-- picks ONE of these and reports it as "the" answer.

-- 1) The naive answer: sum NetPrice x Quantity.
--    But the fact table holds FIVE currencies (AUD, CAD, EUR, GBP, USD). This adds
--    them as if they were one unit. Meaningless — the "never sum a global total
--    across incompatible markets/units" trap.
SELECT round(sum(Quantity * NetPrice), 0) AS net_local_MIXED_currency   -- ~218,814,472  <- do not trust
FROM sales;

-- 2) Same measure, honestly converted to one base currency via the per-row rate.
SELECT round(sum(Quantity * NetPrice * ExchangeRate), 0) AS net_base_currency  -- ~223,597,711
FROM sales;

-- 3) Gross vs net: with or without discount (UnitPrice = list, NetPrice = after discount).
SELECT round(sum(Quantity * UnitPrice * ExchangeRate), 0) AS gross_base_currency,
       round(sum(Quantity * NetPrice  * ExchangeRate), 0) AS net_base_currency
FROM sales;

-- 4) The double-count trap: `sales` is the SAME facts as `orders` x `orderrows`
--    (identical grain, same row count). Summing both doubles revenue.
SELECT (SELECT round(sum(Quantity*NetPrice),0) FROM sales)     AS via_sales,
       (SELECT round(sum(Quantity*NetPrice),0) FROM orderrows) AS via_orderrows;   -- equal!

-- 5) The honest breakdown the ontology DISCLOSES instead of silently picking one number.
SELECT CurrencyCode,
       count(*)                                      AS lines,
       round(sum(Quantity*NetPrice), 0)              AS net_local,
       round(sum(Quantity*NetPrice*ExchangeRate), 0) AS net_base
FROM sales
GROUP BY 1 ORDER BY net_base DESC;

-- Bonus data-quirk: "Online" shows up as a store COUNTRY next to real countries —
-- a channel masquerading as a market. Good material for a quarantine/disclose rule.
SELECT DISTINCT CountryName FROM store ORDER BY 1;
