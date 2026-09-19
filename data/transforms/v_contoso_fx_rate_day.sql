-- data/transforms/v_contoso_fx_rate_day.sql — realizes data/transforms/v_contoso_fx_rate_day.yaml.
-- The served relation contoso_served.v_contoso_fx_rate_day: one statement, one served relation.
-- AUTHORED, NOT DEPLOYED: connection.yaml declares read_only: true, so this view does
-- not exist in the warehouse yet and every rule's status in the descriptor is
-- `authored`. The SELECT body below was executed read-only and is recorded with its
-- answers in queries/p4_transformation_authoring.sql (T1/T2).
-- PRECONDITION: the schema contoso_served must exist and must not hold the 15 leftover views
-- of the deleted run (RUN.md Q2/Q15, register NS-SERVING-01).
-- INPUTS   main.currencyexchange
-- BAKES OUT  nothing. Declared PASSTHROUGH: 4 columns, 100 450 rows, no rule applied — no defect
--   was measured in this relation (complete grid, self-rate exactly 1, every rate > 0; T12).
-- CASTS   Date: TIMESTAMP -> DATE. OPERATOR RULING 2026-09-19 ("change the dates from sources to
--   datasets ... all time fields are anyway 00000"). LOSSLESS, measured not assumed: 0 non-midnight
--   values over 100 450 of 100 450 rows. The landing `main.currencyexchange` keeps TIMESTAMP.
--   THIS COLUMN IS ONE SIDE OF THE CONVERSION JOIN and must not be cast alone. The other side is
--   v_contoso_order_line.OrderDate, and the rule `ontology/rules.yaml#order_line_usd_conversion`
--   matches them on EXACT DATE EQUALITY (`x."Date" = f."OrderDate"`, plus the pinned USD base and
--   the line's own ToCurrency). Both sides are cast in the same change; the join stays an equality
--   between two DATEs rather than becoming a DATE-to-TIMESTAMP comparison. RE-MEASURED after the
--   cast, identical to before: 223 974 join rows over 223 974 lines, 0 lines without a quote,
--   min 1 / max 1 quotes per line, and sum(Quantity * NetPrice * Exchange) = 223 597 710.61 to the
--   cent. decisions/0001-order-line-fact-of-record.md rests on that figure.
-- GRAIN    one row per (Date, FromCurrency, ToCurrency) — 100 450 rows / 100 450 distinct /
--          0 duplicates (T2f). Exchange is a RATE: join and multiply, never sum.
CREATE OR REPLACE VIEW contoso_served.v_contoso_fx_rate_day AS
SELECT CAST(x."Date" AS DATE) AS "Date",
       x."FromCurrency",
       x."ToCurrency",
       x."Exchange"
FROM main.currencyexchange x;
