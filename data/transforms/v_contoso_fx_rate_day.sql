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
-- GRAIN    one row per (Date, FromCurrency, ToCurrency) — 100 450 rows / 100 450 distinct /
--          0 duplicates (T2f). Exchange is a RATE: join and multiply, never sum.
CREATE OR REPLACE VIEW contoso_served.v_contoso_fx_rate_day AS
SELECT x."Date",
       x."FromCurrency",
       x."ToCurrency",
       x."Exchange"
FROM main.currencyexchange x;
