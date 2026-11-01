-- contoso5_store_name — the distinct values of dim_store.store_name: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_store_name.lookup.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_store_name AS
SELECT DISTINCT store_name AS code
FROM contoso_served.dim_store
WHERE store_name IS NOT NULL;
