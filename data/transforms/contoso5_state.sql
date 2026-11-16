-- contoso5_state — the distinct values of dim_location.state: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_state.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_state AS
SELECT DISTINCT state AS code
FROM contoso_served.dim_location
WHERE state IS NOT NULL;
