-- data/transforms/dim_contoso_store.sql — realizes data/transforms/dim_contoso_store.yaml.
-- The served relation contoso_served.dim_contoso_store: one statement, one served relation.
-- AUTHORED, NOT DEPLOYED: connection.yaml declares read_only: true, so this view does
-- not exist in the warehouse yet and every rule's status in the descriptor is
-- `authored`. The SELECT body below was executed read-only and is recorded with its
-- answers in queries/p4_transformation_authoring.sql (T1/T2).
-- PRECONDITION: the schema contoso_served must exist and must not hold the 15 leftover views
-- of the deleted run (RUN.md Q2/Q15, register NS-SERVING-01).
-- INPUTS   main.store
-- BAKES OUT
--   · '' as a second spelling of MISSING in Status: 58 rows carry '' and 1 carries NULL (T8);
--     the served column spells missing exactly one way, NULL on 59 of 74 rows. It does NOT
--     impute a meaning: whether '' meant 'operating' is an open ruling, and one of the 58 rows
--     carries a CloseDate, which is evidence against reading '' as 'operating' (T8).
-- CARRIES UNFIXED: the sentinel row (StoreKey 999999 / StoreCode -1 / GeoAreaKey -1 /
--   CountryCode '--' / CountryName+State 'Online'), the SCD-2 versioning (67 codes over 74 rows)
--   and GeoAreaKey, which joins to nothing in this delivery.
-- GRAIN    one row per StoreKey = one store VERSION — 74 rows / 74 distinct / 0 duplicates (T2c).
CREATE OR REPLACE VIEW contoso_served.dim_contoso_store AS
SELECT s."StoreKey",
       s."StoreCode",
       s."GeoAreaKey",
       s."CountryCode",
       s."CountryName",
       s."State",
       s."Description",
       s."OpenDate",
       s."CloseDate",
       s."SquareMeters",
       nullif(s."Status", '') AS Status
FROM main.store s;
