-- contoso5_channel — the distinct values of v_contoso5_sales_line.channel: this relation's rows (its descriptor's derived_from).
-- The rows of data/lookups/contoso5_channel.lookup.csv are this SELECT's output.
CREATE OR REPLACE VIEW contoso_served.contoso5_channel AS
SELECT DISTINCT channel AS code
FROM contoso_served.v_contoso5_sales_line
WHERE channel IS NOT NULL;
