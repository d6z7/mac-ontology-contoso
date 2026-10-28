-- dim_customer — the CUSTOMER DIMENSION.
--
-- GRAIN: one row per CustomerKey.   KEY: `customer_key`.
--
-- NOT SLOWLY-CHANGING, and that is measured rather than assumed: the landing holds 104 990 rows over
-- 104 990 distinct CustomerKey, so there is exactly one row per customer and no history to keep. A
-- Type-2 treatment here would invent versions that do not exist.
--
-- StartDT/EndDT ARE BUSINESS CONTENT, NOT HOUSEKEEPING. The first cut of this scaffold dropped them
-- as an SCD-2 validity window, which was a guess and was wrong. Measured: EndDT is NEVER null (an
-- open-ended SCD-2 row would be), 75 275 of 104 990 end AFTER the last order in the warehouse, 5 637
-- sit at a 2045 sentinel meaning "no end", and NO customer's window closes before their own last
-- order. That is a relationship window somebody can ask about, so it is carried and named for what it
-- is.
--
-- ONE ROW IS INVERTED — EndDT <= StartDT — and it is carried rather than filtered. Dropping a row to
-- make a window tidy hides the only evidence that the window is not.
--
-- BIRTHDAY IS CARRIED, `Age` IS NOT. Age is derived from Birthday and goes stale the moment it is
-- stored; the landing's value is a snapshot as of a load nobody recorded. The fact is the birth date,
-- and an age is computed against the period a question asks about. (contoso2 banded age as-of a chosen
-- horizon and the operator identified that as one person's curation leaking into the data.)
--
-- THE COUNTRY COLUMN IS NAMED FOR WHAT IT HOLDS (operator ruling, 2026-09-30). It was `country`
-- and it carries `AU`, `CA`, `DE` — a code, and every other relation in this bundle already spells a
-- code column `country_code` (dim_location, dim_store). The rename is not cosmetic: a question asking
-- to LIST countries got eight two-letter codes back and nothing in the bundle said they were codes,
-- because the name claimed they were countries. `main.customer` also carries `CountryFull`
-- (Australia, Canada, ... — measured one-to-one over all eight), and the operator ruled NOT to serve
-- it yet: the code is named honestly first, the long name is a separate decision.
--
-- THE NAME IS FOR DISPLAY, NEVER AN AXIS. GivenName/Surname identify a person: legitimate to show on
-- a row, never something to GROUP BY. Street address and postcode are not carried at all — no
-- question in this warehouse is asked at that grain, and they are the most identifying columns here.
-- A DAY IS A DATE, NOT A TIMESTAMP (operator ruling, 2026-09-30). The landing delivers these as
-- TIMESTAMP and every value measured is midnight — 0 rows of any of the nine date columns in this
-- warehouse carry a time — so the time component is a type artefact that carries no fact. It is
-- cast away here: a reader comparing a day to a day should not have to know that one side is
-- 2019-11-03 00:00:00, and a question about a date should not have to spell one.
--
CREATE OR REPLACE VIEW contoso_served.dim_customer AS
SELECT
  c."CustomerKey"                                     AS customer_key,     -- PK
  c."GivenName" || ' ' || c."Surname"                 AS customer_name,    -- display only: never_axis
  c."Continent"                                       AS continent,        -- geography, coarsest
  c."Country"                                         AS country_code,   -- ISO-3166 alpha-2, not a name
  c."State"                                           AS state,
  c."City"                                            AS city,             -- geography, finest
  c."Gender"                                          AS gender,
  CAST(c."Birthday" AS DATE)                          AS birth_date,       -- the FACT; age is derived
  CAST(c."StartDT" AS DATE)                           AS valid_from,
  CAST(c."EndDT" AS DATE)                             AS valid_to          -- 2045 = no end declared
FROM main.customer c;
