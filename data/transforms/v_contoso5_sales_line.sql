-- v_contoso5_sales_line — THE FACT. One fact, served once.
--
-- mac.transform.driven_by: proposed
-- mac.transform.because: DQ-DUP-ORDERROWS-SALES
--
-- READ, NOT DECORATION. `mac_transforms` lifts these onto the descriptor, so a reader
-- learns WHO decided this shape without opening the SQL. `proposed` because the
-- decision below was made from a MEASUREMENT this bundle already holds, and the
-- finding it names is still open — a person has not yet ruled on it.
--
-- GRAIN: one row per (order_key, line_number) — an order LINE.   KEY: both.
--
-- ONE FACT, NOT TWO. The passthrough model served `sales` (13 cols) AND `orderrows` (7 cols), both
-- 223 974 rows, with sales a strict superset — raised as DQ-DUP-ORDERROWS-SALES at severity HIGH.
-- Two defensible answers to every question is not a richer model, it is an unresolved one.
-- `orderrows` is NOT promoted here; `sales` is the canonical line.
--
-- THE ORDER HEADER IS A DEGENERATE DIMENSION, not a second fact. `orders` (93 470 rows) carries
-- CustomerKey, StoreKey, CurrencyCode and two dates — every one of them repeated on the line, and no
-- measure of its own. A header with no measure is an attribute of its lines: `order_key` travels on
-- the fact and the header relation is not served at all.
--
-- NO ROW MAY BE ADDED BY A JOIN. This view reads ONE relation for exactly that reason: measured on
-- contoso3, v_container_move_line LEFT JOINed its voyage on a composite key that is not unique and
-- turned 20 000 rows into 20 199 — a 1 % overstatement of every measure summed over it, invisible
-- because the view still looked like a fact. Enrichment belongs on the dimension, never on the fact.
--
-- THE AMOUNTS ARE COMPOSED HERE AND CARRY THEIR UNIT. `Quantity x NetPrice` is USD though its factors
-- are `units` and `USD`; the unit is the discriminator and it is stated, not inferred.
CREATE OR REPLACE VIEW contoso_served.v_contoso5_sales_line AS
SELECT
  s."OrderKey"      AS order_key,         -- PK1, degenerate dimension (the order header)
  s."LineNumber"    AS line_number,       -- PK2
  CAST(s."OrderDate" AS DATE)    AS order_date,    -- a DATE, the REPORTING date; no calendar dimension
  CAST(s."DeliveryDate" AS DATE) AS delivery_date, -- a DATE; the calendar is built in
  s."CustomerKey"   AS customer_key,      -- FK -> dim_customer
  s."StoreKey"      AS store_key,         -- FK -> dim_store  (the UNIT, never the site)
  s."ProductKey"    AS product_key,       -- FK -> dim_product
  -- THE CHANNEL, ON THE FACT. ADDED 2026-10-23 on the operator's ruling: "these KPI s are the
  -- backbone so we should also look into transformation layer to maybe simplfy it".
  --
  -- WHY IT BELONGS HERE AND NOT ON A DIMENSION. A sale's channel is a property of the SALE. Until
  -- today it could only be read by routing to `dim_store` and inspecting `store_code = -1`, so
  -- the channel a question got depended on whether the join path happened to cross the store
  -- dimension. Measured 2026-10-10, that produced ONE QUESTION WITH THREE ANSWERS:
  --     total revenue      218,814,471.53   online included -- dim_store never joined
  --     revenue by product 218,814,471.53   online included
  --     revenue by country 128,818,965.21   online EXCLUDED -- the route to Country crossed dim_store
  -- `applies: subject` on the population rule guards that symptom. This column removes the cause:
  -- the channel is now reachable from every question regardless of route.
  --
  -- NO JOIN, SO THE VIEW'S OWN INVARIANT HOLDS. The sentinel is a KEY on this fact, not an
  -- attribute of a dimension, so no row can be added. MEASURED EQUIVALENT over all 223,974 lines
  -- on 2026-10-23: `store_key = 999999` and `store_code = -1` each select 93,550 lines with
  -- ZERO disagreements, 0 orphan lines, and one dim_store row carries the key. If that ever
  -- parts, the two spellings have drifted and a gate must say so -- which it can now, because the
  -- fact is stated here instead of being the ABSENCE of a predicate.
  --
  -- THE VALUE NAMES ARE THE DECLARED POPULATION NAMES, not new words:
  -- `store.resolution.the_channel_is_the_location_sentinel` names them `physical` and `online`.
  -- One axis, one vocabulary.
  --
  -- WHAT THIS DOES NOT CHANGE. `dim_store.store_code` and that population rule stay exactly as
  -- they are, so a question whose SUBJECT is a store still defaults to physical shops and "how
  -- many stores do we have" is still 57.
  CASE WHEN s."StoreKey" = 999999 THEN 'online' ELSE 'physical' END AS channel,
  -- THE COUNTRY OF THE SALE, ON THE FACT. ADDED 2026-10-25 on the operator's ruling of the same
  -- day ("ok go B1 now"), recorded in
  -- meaning-as-code#decisions/RULED-2026-10-25_a-sale-is-attributed-by-its-channel.md.
  --
  -- WHAT IT IS. A shop sale is attributed to the country the SHOP stands in; a web sale is
  -- attributed to the country the CUSTOMER lives in. That is the operator's own sentence of
  -- 2026-10-22, verbatim: "revenue in germany is the revenue from stores in germany and from
  -- customers in germany who boguht internet. stores only is not enough".
  --
  -- WHY IT BELONGS ON THE FACT. The attribution is a property of the SALE and of nothing else, and
  -- the pattern page proves no dimension row can carry it: the ONE online store row serves
  -- customers in 8 countries, so a country written on `dim_store` would have to be eight values at
  -- once. Until today the only routes from a sale to a country were `dim_store.country_code` and
  -- `dim_customer.country_code`, and NEITHER answers "what is our business in Germany" -- the store
  -- route cannot see a single web sale, and the customer route re-attributes a foreigner's
  -- in-shop purchase to where they live. Measured on this warehouse, the store route puts 93,550
  -- lines on the '--' sentinel, which `dim_country` names "Online" and which the declarations say
  -- is not a place.
  --
  -- MEASURED, 2026-10-25, over all 223,974 lines:
  --     lines                   223,974   unchanged: no row added, no row lost
  --     non-null attribution    223,974   every line reaches a country
  --     distinct countries            8   the eight real ones
  --     '--' sentinel lines           0   the sentinel leaves the country axis of a SALE entirely
  --     physical lines          130,424   of which store country <> customer country: 0
  --     online lines             93,550   of which store country is the sentinel: 93,550
  -- THE ZERO IS THE FINDING. No physical sale in this warehouse crosses a border, so here this
  -- column is row-for-row identical to the customer's country. It is NOT declared as the
  -- customer's country, because the two mean different things and only the agreement is an
  -- accident of the data: a German tourist buying in Paris would be French trade under this
  -- column and German trade under `dim_customer`. The operator was offered `default: customer` on
  -- 2026-10-22 and refused it for exactly that reason. The declaration states the MEANING; the
  -- measurement states that the readings currently agree.
  --
  -- NO ROW MAY BE ADDED, AND THIS HONOURS THAT RULE RATHER THAN EXCEPTING IT. The view's invariant
  -- above forbids a JOIN on the fact, because on contoso3 a non-unique composite join turned
  -- 20,000 rows into 20,199 -- a 1% overstatement invisible to every reader. These are correlated
  -- SCALAR SUBQUERIES, which cannot add a row by construction: if either key were non-unique the
  -- query would ERROR rather than silently multiply. Measured the same day: dim_store 74 rows over
  -- 74 distinct keys, dim_customer 104,990 over 104,990, and 0 lines whose store or customer key
  -- fails to match. So the risk the invariant names is structurally absent, not merely unobserved.
  --
  -- THE CODE, NOT THE NAME. `country_name` has ONE home by the operator's ruling of 2026-09-30 and
  -- every side reaches it through an edge; this column carries the ISO code, like every other
  -- country column in the bundle.
  CASE
    WHEN s."StoreKey" = 999999
      THEN (SELECT c."Country"     FROM main.customer c WHERE c."CustomerKey" = s."CustomerKey")
      ELSE (SELECT st."CountryCode" FROM main.store   st WHERE st."StoreKey"   = s."StoreKey")
  END                                            AS sale_country_code,
  s."CurrencyCode"  AS currency_code,     -- FK -> dim_currency: the ORDER's currency, NOT the unit of
                                          -- the amounts below, which are USD
  s."Quantity"                                   AS quantity,      -- measure, unit: units
  s."NetPrice"                                   AS net_price,     -- measure, unit: USD (per unit)
  s."UnitPrice"                                  AS unit_price,    -- measure, unit: USD (per unit)
  s."UnitCost"                                   AS unit_cost,     -- measure, unit: USD (per unit)
  -- NOT ROUNDED, AND THAT IS THE POINT. The first cut of this scaffold wrote ROUND(..., 2) here, and
  -- it cost $1.46: rounded per line then summed gives 218 814 470.20, summed then rounded gives
  -- 218 814 471.66. A fact stores the number; ROUNDING IS A PRESENTATION DECISION and belongs at the
  -- edge, once, where somebody can see it. Baked in at line grain it is an error every aggregate
  -- above inherits and nobody can undo.
  s."Quantity" * s."NetPrice"                    AS net_amount,    -- measure, unit: USD
  s."Quantity" * s."UnitPrice"                   AS gross_amount,  -- measure, unit: USD
  s."Quantity" * s."UnitCost"                    AS cost_amount,   -- measure, unit: USD
  -- DERIVED, per the operator's KPI spec of 2026-09-30. Both are Σ-able at line grain; the
  -- three PERCENTAGE KPIs are ratios of these sums and are never stored per row.
  s."Quantity" * (s."UnitPrice" - s."NetPrice") AS discount_amount, -- measure, unit: USD
  s."Quantity" * (s."NetPrice" - s."UnitCost")  AS margin_amount    -- measure, unit: USD
FROM main.sales s;
