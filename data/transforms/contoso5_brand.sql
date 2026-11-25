-- contoso5_brand — the distinct values of dim_product.brand: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_brand.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_brand AS
SELECT DISTINCT brand AS code
FROM contoso_served.dim_product
WHERE brand IS NOT NULL;
