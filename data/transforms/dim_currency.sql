-- dim_currency — the CURRENCY DIMENSION.
--
-- GRAIN: one row per ISO currency code.   KEY: `currency_code`.
--
-- ITS OWN RELATION, not a register, because it is JOINED TO by a fact and a bridge. A register is a
-- value set that resolves a name; a dimension is a thing a fact points at. CurrencyCode is both, and
-- the register stays for name resolution.
CREATE OR REPLACE VIEW contoso_served.dim_currency AS
SELECT DISTINCT s."CurrencyCode" AS currency_code   -- PK
FROM main.sales s
WHERE s."CurrencyCode" IS NOT NULL;
