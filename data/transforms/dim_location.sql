-- dim_location — the PHYSICAL SITE.
--
-- mac.transform.driven_by: proposed
-- mac.transform.because: DQ-STORE-TWO-GRAINS
--
-- READ, NOT DECORATION. `mac_transforms` lifts these onto the descriptor, so a reader
-- learns WHO decided this shape without opening the SQL. `proposed` because the
-- decision below was made from a MEASUREMENT this bundle already holds, and the
-- finding it names is still open — a person has not yet ruled on it.
--
-- GRAIN: one row per StoreCode.   KEY: `location_code`.
--
-- THIS RELATION EXISTS TO SPLIT A GRAIN THAT WAS CONFLATED. `store` carries TWO populations — 74
-- trading UNITS and 67 physical SITES — and the passthrough model declared only one, raised as
-- DQ-STORE-TWO-GRAINS. A location can hold a SUCCESSION of units, so summing a per-unit measure such
-- as SquareMeters over all 74 triple-counts New Brunswick, which has held three.
--
-- SquareMeters is therefore NOT here: it is owned by the UNIT and changes between successors. What a
-- site owns is its place.
CREATE OR REPLACE VIEW contoso_served.dim_location AS
SELECT
  s."StoreCode"    AS location_code,      -- PK
  any_value(s."CountryCode") AS country_code,
  any_value(s."CountryName") AS country_name,
  any_value(s."State")       AS state,
  count(*)                   AS units_ever_here
FROM main.store s
GROUP BY s."StoreCode";
