-- contoso5_status — the distinct values of dim_store.status_annotation: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_status.lookup.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_status AS
SELECT DISTINCT status_annotation AS code
FROM contoso_served.dim_store
WHERE status_annotation IS NOT NULL;
