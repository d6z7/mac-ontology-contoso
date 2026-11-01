-- contoso5_continent — the distinct values of dim_customer.continent: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_continent.lookup.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_continent AS
SELECT DISTINCT continent AS code
FROM contoso_served.dim_customer
WHERE continent IS NOT NULL;
