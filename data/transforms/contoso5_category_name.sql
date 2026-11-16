-- contoso5_category_name — the distinct values of dim_product.category_name: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_category_name.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_category_name AS
SELECT DISTINCT category_name AS code
FROM contoso_served.dim_product
WHERE category_name IS NOT NULL;
