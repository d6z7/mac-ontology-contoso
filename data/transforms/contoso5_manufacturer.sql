-- contoso5_manufacturer — the distinct values of dim_product.manufacturer: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_manufacturer.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_manufacturer AS
SELECT DISTINCT manufacturer AS code
FROM contoso_served.dim_product
WHERE manufacturer IS NOT NULL;
