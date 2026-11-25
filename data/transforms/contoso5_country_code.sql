-- contoso5_country_code — the distinct values of dim_country.country_code: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_country_code.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_country_code AS
SELECT DISTINCT country_code AS code, country_name AS label
FROM contoso_served.dim_country
WHERE country_code IS NOT NULL;
