-- v_contoso5_fx_rate — the FX BRIDGE. A BRIDGE, not a dimension.
--
-- GRAIN: one row per (date_day, from_currency, to_currency).   KEY: all three.
--
-- WHY IT IS NOT A DIMENSION. Nothing points AT it with a single key; it is entered from two
-- directions at once and its whole purpose is to carry a RATE between two members of dim_currency. A
-- dimension answers "which one"; a bridge answers "at what rate, on which day".
--
-- THE RATE IS `to_currency` UNITS PER ONE `from_currency` UNIT — measured, not assumed:
-- EUR->USD averages 1.11, USD->EUR 0.90, USD->USD is exactly 1.0 on all 4 018 days.
--
-- IT IS NOT NEEDED TO READ THE FACT. Measured on contoso4: NetPrice is stored in USD, not in the
-- order's currency — one product shows identical min 429.91 and max 1249.75 across CAD, EUR, GBP and
-- USD, which is impossible for local-currency storage. So this bridge is for RESTATING a USD figure
-- in another currency, never for making the fact comparable.
CREATE OR REPLACE VIEW contoso_served.v_contoso5_fx_rate AS
SELECT
  CAST(x."Date" AS DATE) AS date_day,     -- PK1, a DATE: the calendar is a function, not a dimension
  x."FromCurrency" AS from_currency,      -- PK2, FK -> dim_currency
  x."ToCurrency"   AS to_currency,        -- PK3, FK -> dim_currency
  x."Exchange"     AS rate                -- to_currency units per 1 from_currency unit
FROM main.currencyexchange x;
