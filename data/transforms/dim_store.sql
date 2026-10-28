-- dim_store — the TRADING UNIT.
--
-- GRAIN: one row per StoreKey.   KEY: `store_key`.   REFERENCES: dim_location.
--
-- A UNIT IS NOT A SITE. 74 units over 67 sites; `sales` references StoreKey, so every revenue figure
-- is attributed to the unit that earned it, which is correct and must not be rolled up to the site
-- silently. `store_code` is the declared FK to dim_location, which is what makes the roll-up
-- expressible rather than accidental.
--
-- ACTIVE IS `close_date IS NULL`, 58 of 74. NOT `Status`: measured on contoso4, Status disagrees on
-- StoreKey 630, which carries a CloseDate and an EMPTY Status — counting by Status returns 59 and
-- includes a unit that stopped trading in 2019. Status is carried as an annotation, not a lifecycle.
-- A DAY IS A DATE, NOT A TIMESTAMP (operator ruling, 2026-09-30). The landing delivers these as
-- TIMESTAMP and every value measured is midnight — 0 rows of any of the nine date columns in this
-- warehouse carry a time — so the time component is a type artefact that carries no fact. It is
-- cast away here: a reader comparing a day to a day should not have to know that one side is
-- 2019-11-03 00:00:00, and a question about a date should not have to spell one.
--
CREATE OR REPLACE VIEW contoso_served.dim_store AS
SELECT
  s."StoreKey"     AS store_key,          -- PK
  s."StoreCode"    AS store_code,      -- FK -> dim_location
  s."Description"  AS store_name,
  s."CountryCode"  AS country_code,
  s."State"        AS state,
  CAST(s."OpenDate"  AS DATE) AS open_date,
  CAST(s."CloseDate" AS DATE) AS close_date,        -- NULL means trading: the whole lifecycle test
  -- THE ONE EMPTY STATUS IS FILLED, DERIVABLY. Operator ruling, 2026-10-01: "this is data impurity
  -- ... we can fix in transformation ... but the business side is correct". A store is inactive when it
  -- carries a close date AND a status of Closed or Restructured, and one row broke that: StoreKey 630,
  -- Contoso Store Utah, shut 2019-11-03 with an empty Status.
  --
  -- THE FILL IS MEASURED, NOT GUESSED. The two statuses mean different things and the rows say which:
  -- a RESTRUCTURED location always has a later row at the same StoreCode (6 of 6 locations), and a
  -- CLOSED one never does (0 of 8). Utah has a single row and no successor, so it is Closed by the
  -- data's own rule. The rule reproduces all 15 stated values exactly and fills only the 16th, so the
  -- landing's own values are never overwritten.
  CASE
    WHEN s."CloseDate" IS NULL THEN s."Status"
    WHEN nullif(trim(s."Status"), '') IS NOT NULL THEN s."Status"
    WHEN EXISTS (SELECT 1 FROM main.store l
                 WHERE l."StoreCode" = s."StoreCode" AND l."OpenDate" > s."CloseDate")
      THEN 'Restructured'
    ELSE 'Closed'
  END              AS status_annotation,  -- the landing's value where stated; derived where blank
  s."SquareMeters" AS square_metres       -- owned by the UNIT, not the site
FROM main.store s;
