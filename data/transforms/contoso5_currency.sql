-- contoso5_currency — the distinct values of dim_currency.currency_code: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_currency.lookup.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_currency AS
SELECT DISTINCT currency_code AS code
FROM contoso_served.dim_currency
WHERE currency_code IS NOT NULL;
