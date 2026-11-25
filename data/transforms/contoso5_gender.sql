-- contoso5_gender — the distinct values of dim_customer.gender: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_gender.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_gender AS
SELECT DISTINCT gender AS code
FROM contoso_served.dim_customer
WHERE gender IS NOT NULL;
