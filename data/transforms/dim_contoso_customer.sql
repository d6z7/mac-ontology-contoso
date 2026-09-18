-- data/transforms/dim_contoso_customer.sql — realizes data/transforms/dim_contoso_customer.yaml.
-- The served relation contoso_served.dim_contoso_customer: one statement, one served relation.
-- AUTHORED, NOT DEPLOYED: connection.yaml declares read_only: true, so this view does
-- not exist in the warehouse yet and every rule's status in the descriptor is
-- `authored`. The SELECT body below was executed read-only and is recorded with its
-- answers in queries/p4_transformation_authoring.sql (T1/T2).
-- PRECONDITION: the schema contoso_served must exist and must not hold the 15 leftover views
-- of the deleted run (RUN.md Q2/Q15, register NS-SERVING-01).
-- INPUTS   main.customer
-- BAKES OUT
--   · a PADDED region label: 4 rows carry a trailing space in State and StateFull ('Birmingham '
--     x3, 'Bradford ' x1) whose trimmed form already exists as its own value, so the landing
--     spells two regions two ways — 565 State spellings fold to 563, 610 StateFull to 608, and
--     13 order lines belong to those customers (T13a/T13c). Measured in P4: the P1 anomaly pass
--     did not sweep for padding.
--   · the STALE derived attribute: Age is as-of 2020/2021 (year(Birthday) + Age is 2020 or 2021
--     on every one of the 104 990 rows, T11e) while the facts run to 2025-12-31 — it is not
--     projected, and neither are the 11 other columns the question scope does not name
--     (register NS-CUSTOMER-01: 12 of 24 columns served).
-- CARRIES UNFIXED: the one customer whose validity window has zero length (StartDT = EndDT), and
--   GeoAreaKey, which joins to nothing in this delivery.
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
       c."Gender"
FROM main.customer c;
