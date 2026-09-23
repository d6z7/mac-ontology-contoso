-- data/transforms/dim_contoso_product.sql — realizes data/transforms/dim_contoso_product.yaml.
-- The served relation contoso_served.dim_contoso_product: one statement, one served relation.
-- AUTHORED, NOT DEPLOYED: connection.yaml declares read_only: true, so this view does
-- not exist in the warehouse yet and every rule's status in the descriptor is
-- `authored`. The SELECT body below was executed read-only and is recorded with its
-- answers in queries/p4_transformation_authoring.sql (T1/T2).
-- PRECONDITION: the schema contoso_served must exist and must not hold the 15 leftover views
-- of the deleted run (RUN.md Q2/Q15, register NS-SERVING-01).
-- INPUTS   main.product
-- BAKES OUT
--   · a closed vocabulary drifting by CASE: 17 spellings of Color over 16 colours, the one split
--     group being Blue (197 rows) / blue (3) (T6a, T6b). The canonical spelling is MEASURED from the
--     data — the most-used spelling in each case-insensitive group — not transcribed by hand.
--   · '' as a second spelling of MISSING in WeightUnit (222 rows, exactly the rows whose Weight
--     is null) -> NULL (T7).
-- CARRIES UNFIXED: the 62 rows that name a unit for a weight that is not there (missing vs
--   not-applicable is a ruling, not a rule).
-- GRAIN    one row per ProductKey — 2 517 rows / 2 517 distinct / 0 duplicates (T2b). The colour
--          join cannot fan out: color_canon holds one row per case-insensitive colour (T6c).
CREATE OR REPLACE VIEW contoso_served.dim_contoso_product AS
WITH color_spelling AS (                 -- how often each SPELLING of a colour is used
    SELECT "Color" AS color_raw, count(*) AS rows_with_spelling
    FROM main.product
    WHERE "Color" IS NOT NULL
    GROUP BY 1
),
color_canon AS (                         -- one canonical spelling per case-insensitive colour
    SELECT lower(color_raw) AS color_lc, color_raw AS color_canonical
    FROM (SELECT color_raw,
                 row_number() OVER (PARTITION BY lower(color_raw)
                                    ORDER BY rows_with_spelling DESC, color_raw) AS rn
          FROM color_spelling)
    WHERE rn = 1
)
SELECT p."ProductKey",
       p."ProductCode",
       p."ProductName",
       p."Manufacturer",
       p."Brand",
       coalesce(cc.color_canonical, p."Color") AS Color,
       nullif(p."WeightUnit", '') AS WeightUnit,
       p."Weight",
       p."Cost",
       p."Price",
       p."CategoryKey",
       p."CategoryName",
       p."SubCategoryKey",
       p."SubCategoryName"
FROM main.product p
LEFT JOIN color_canon cc ON cc.color_lc = lower(p."Color");
