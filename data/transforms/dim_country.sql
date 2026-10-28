-- dim_country — the COUNTRY.
--
-- mac.transform.driven_by: ruled
-- mac.transform.because: operator ruling 2026-09-30 (no finding; a shape a person asked for)
--
-- GRAIN: one row per country code.   KEY: `country_code`.
--
-- WHY IT EXISTS. The country was a COLUMN on three relations and a REFERENCE to nothing:
-- `dim_customer.country_code`, `dim_store.country_code`, `dim_location.country_code`. The name was
-- carried on ONE of them (`dim_location.country_name`, ruled `label_of: country_code`), so a
-- question about CUSTOMERS could never reach it: dim_location is the STORE's geography, keyed on
-- location_code, and there is no path from a customer to it. Measured 2026-09-30: the customer's
-- own `GeoAreaKey` is a different code space (608 values over 1..616 against the location's 67),
-- 69,902 customer rows have no location at all, and where the two do collide the country agrees on
-- 14,989 of 35,088 rows. Joining them would attach the wrong country to more than half the estate.
-- Joining the customer to dim_location on the country CODE instead is many:many — 9 codes over 67
-- rows, US alone 24 — and turns 104,990 customers into 1,462,707 rows.
--
-- So the country becomes what it always was: a dimension of its own, one row per code, referenced
-- by all three. That is a measurable foreign key rather than a value-set overlap.
--
-- THE SOURCE IS THE STORE, NOT THE CUSTOMER, and both were measured: `main.store` carries all NINE
-- codes with their names and `main.customer` carries EIGHT — the same eight, name for name, with no
-- disagreement (measured 2026-09-30, a full outer join over (code, name) differs on one row only,
-- and that row is the sentinel below). The store side is therefore the total one and is read here;
-- the customer side is a subset and needs no union.
--
-- `--`/Online IS CARRIED, AND IT IS NOT A COUNTRY. The source wrote the online business as one row
-- of the store table with `--` where a country code goes (see [[Store]]'s channel axis), and `dim_location`
-- already carries that sentinel. Dropping it here would make the online store's country code a
-- reference to nothing — a BROKEN foreign key standing in for a sentinel a person already ruled on
-- — so the row is carried and the concept says what it means. "In how many countries do we sell"
-- is 8, not 9, and Country's own `real` population is what keeps the sentinel out of a geographic
-- answer. The dimension holds what the warehouse holds; the ontology says what it means.
CREATE OR REPLACE VIEW contoso_served.dim_country AS
SELECT
  s."CountryCode"              AS country_code,   -- PK, ISO-3166 alpha-2 ('--' = the online sentinel)
  any_value(s."CountryName")   AS country_name    -- the long name: 'Australia' for 'AU'
FROM main.store s
GROUP BY s."CountryCode";
