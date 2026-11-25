-- contoso5_color — the distinct values of dim_product.color: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_color.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_color AS
SELECT DISTINCT color AS code
FROM contoso_served.dim_product
WHERE color IS NOT NULL;
