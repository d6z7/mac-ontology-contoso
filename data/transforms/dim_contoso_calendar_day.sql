-- data/transforms/dim_contoso_calendar_day.sql — realizes data/transforms/dim_contoso_calendar_day.yaml.
-- The served relation contoso_served.dim_contoso_calendar_day: one statement, one served relation.
-- AUTHORED, NOT DEPLOYED: connection.yaml declares read_only: true, so this view does
-- not exist in the warehouse yet and every rule's status in the descriptor is
-- `authored`. The SELECT body below was executed read-only and is recorded with its
-- answers in queries/p4_transformation_authoring.sql (T1/T2).
-- PRECONDITION: the schema contoso_served must exist and must not hold the 15 leftover views
-- of the deleted run (RUN.md Q2/Q15, register NS-SERVING-01).
-- INPUTS   main.date
-- BAKES OUT  nothing. This is a declared PASSTHROUGH: 17 columns, 4 018 rows, no rule applied.
--   The transform exists so that the next upstream schema change is visible instead of fatal.
-- CASTS   Date: TIMESTAMP -> DATE. OPERATOR RULING 2026-09-19 ("change the dates from sources to
--   datasets ... all time fields are anyway 00000"), which answers the `needs_ruling` this
--   descriptor's open item `varchar-datekey` and its sibling `boolean-as-integer` both defer to —
--   "should a served column's type be corrected when the landing's type is wrong?" — for the
--   TEMPORAL case only. The cast is LOSSLESS and that was MEASURED, not assumed: over all 19
--   date/timestamp columns of this warehouse, 1 816 902 non-null values,
--   `sum(CASE WHEN col <> date_trunc('day', col) THEN 1 ELSE 0 END)` = 0 — and 4 018 of 4 018 on
--   this column. The cast is applied HERE, in the transform, and the landing `main.date` keeps
--   its TIMESTAMP: the sources->datasets seam is where a served type is decided.
--   THE JOIN MOVES WITH IT. The fact's OrderDate/DeliveryDate join this column by EXACT EQUALITY;
--   both sides are cast in the same change (v_contoso_order_line.sql), so the equality still
--   compares like with like. Re-measured after the cast: 3 450 of 4 018 ordered days, 3 498 of
--   4 018 delivered days, inclusion 1.0 over 223 974 rows, 0 orphans — identical to before.
-- CARRIES UNFIXED: DateKey is a varchar YYYYMMDD, WorkingDay is an integer used as a boolean, and
--   the calendar covers 359 days beyond the last fact. Those two type mismatches are NOT swept in
--   with the temporal one: the ruling above was asked and given about dates, and the open items
--   record that each of the other two turns on a question nobody has answered (which column the
--   calendar keys on; whether a flag should be served boolean). The calendar must not be trimmed
--   to the fact's span — a calendar exists to carry days nothing happened on.
-- GRAIN    one row per Date — 4 018 rows / 4 018 distinct / 0 duplicates (T2e).
CREATE OR REPLACE VIEW contoso_served.dim_contoso_calendar_day AS
SELECT CAST(d."Date" AS DATE) AS "Date",
       d."DateKey",
       d."Year",
       d."YearQuarter",
       d."YearQuarterNumber",
       d."Quarter",
       d."YearMonth",
       d."YearMonthShort",
       d."YearMonthNumber",
       d."Month",
       d."MonthShort",
       d."MonthNumber",
       d."DayofWeek",
       d."DayofWeekShort",
       d."DayofWeekNumber",
       d."WorkingDay",
       d."WorkingDayNumber"
FROM main.date d;
