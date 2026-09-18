-- data/transforms/dim_contoso_customer.sql — realizes data/transforms/dim_contoso_customer.yaml.
-- The served relation contoso_served.dim_contoso_customer: one statement, one served relation.
-- MATERIALISED 2026-09-18 into contoso_served, on the operator's authorisation to open the
-- connection for writing ("i am fine with read write for connection"); connection.yaml now declares
-- read_only: false and the pipeline materialises its own declared views into its own view_schema.
-- The rules' statuses stay `authored`: that word describes who wrote them, and nothing here ratified.
-- Verified after creation against the grain the descriptor declares: 104 990 rows / 104 990 distinct
-- CustomerKey. The SELECT body was previously executed read-only and is recorded with its answers in
-- queries/p4_transformation_authoring.sql (T1/T2), at 12 columns; age_band_5y is the thirteenth.
-- PRECONDITION: the schema contoso_served must exist. The 15 leftover views of the deleted run are
--   gone — the operator dropped both schemas 2026-09-18 (register NS-SERVING-01, now `accepted`).
-- INPUTS   main.customer
-- BAKES OUT
--   · a PADDED region label: 4 rows carry a trailing space in State and StateFull ('Birmingham '
--     x3, 'Bradford ' x1) whose trimmed form already exists as its own value, so the landing
--     spells two regions two ways — 565 State spellings fold to 563, 610 StateFull to 608, and
--     13 order lines belong to those customers (T13a/T13c). Measured in P4: the P1 anomaly pass
--     did not sweep for padding.
--   · the STALE derived attribute: Age is as-of 2020/2021 (year(Birthday) + Age is 2020 on 94 990
--     rows and 2021 on 10 000, ZERO rows consistent with 2024/2025/2026) while the facts run to
--     2025-12-31, and it is not banded either (67 distinct values 19..85, only 21 833 of 104 990
--     rows a multiple of 5). It is not projected. Neither are the 11 other columns the question
--     scope does not name (register NS-CUSTOMER-01: 12 of 24 landing columns refused).
-- DERIVES
--   · age_band_5y — the 5-year age band, AS OF 2025-12-31. Rules exclude-stale-derived-age and
--     derive-age-band-as-of, both resolving DQ-CUSTOMER-01.
--
--     THE AS-OF DATE IS THE DELIVERY'S FACT HORIZON (the newest order date, 2025-12-31) AND IT IS A
--     CONSTANT IN THIS FILE. An age without an as-of date is exactly the defect being baked out, so
--     this one is declared in three places that must agree: the rule in the .yaml, the literal
--     below, and the served column's notes in data/datasets/dim_contoso_customer.yaml.
--     CONSEQUENCE, and it is not policed by anything: WHEN THE FACT HORIZON MOVES, THIS BAND MUST BE
--     RE-DERIVED. A delivery that gains 2026 facts serves a band as-of a year in the past — the same
--     defect class, one iteration on — and it will do so silently. DQ-CUSTOMER-01 residual risk 1
--     names the acceptance property that would catch it as a follow-up; it does not exist yet.
--
--     THE MONTH-DAY CORRECTION IS A NO-OP TODAY AND IS WRITTEN ANYWAY. date_diff('year', ...) counts
--     year boundaries crossed, which equals true age only when the as-of date falls on or after the
--     birthday in that year. 31 December always does. A re-derivation to a mid-year horizon would
--     silently over-count every customer whose birthday had not yet passed, so the term is here
--     while it is provably inert rather than after it has become a defect.
--
--     MEASURED over main.customer, read-only, with this exact expression: 15 bands (20, 25, … 90),
--     0 nulls over 104 990 rows, smallest cell 1 396, no customer alone in a band.
--   · NEITHER INPUT IS SERVED. Birthday is CONSUMED and NOT PROJECTED: it is the exact date of birth,
--     i.e. the identifier the band exists to generalise. A consumer cannot recover it, or a
--     single-year age, from the served row.
-- CARRIES UNFIXED: the one customer whose validity window has zero length (StartDT = EndDT);
--   GeoAreaKey, which joins to nothing in this delivery; and the QUASI-IDENTIFIER shape of the
--   served row — ZipCode alone singles out 29 193 of 104 990 customers, and adding age_band_5y to
--   ZipCode + Gender takes that from 35 894 to 74 617 (DQ-CUSTOMER-02, `coverage: gap` — measured,
--   registered, deliberately untreated, and a pattern record rather than an exposure because this is
--   MIT-licensed synthetic data).
-- GRAIN    one row per CustomerKey — 104 990 rows / 104 990 distinct / 0 duplicates (T2d). Nothing
--          is filtered: the dimension over-covers its fact (52 189 of 104 990 appear on an order)
--          and that is disclosed on the descriptor, not trimmed here.
CREATE OR REPLACE VIEW contoso_served.dim_contoso_customer AS
SELECT c."CustomerKey",
       c."GeoAreaKey",
       c."StartDT",
       c."EndDT",
       c."Continent",
       c."CountryFull",
       c."Country",
       trim(c."StateFull") AS StateFull,
       trim(c."State") AS State,
       c."City",
       c."ZipCode",
       c."Gender",
       CAST(floor((date_diff('year', c."Birthday", DATE '2025-12-31')
                   - CASE WHEN strftime(DATE '2025-12-31', '%m%d') < strftime(c."Birthday", '%m%d')
                          THEN 1 ELSE 0 END) / 5) * 5 AS INTEGER) AS age_band_5y
FROM main.customer c;
