-- dim_product — the PRODUCT DIMENSION.
--
-- mac.transform.driven_by: proposed
-- mac.transform.because: DQ-DANGLINGKEY-CATEGORYKEY
--
-- ONE DECISION HERE IS RULED, NOT PROPOSED: the colour case fold below (operator, 2026-09-30). The
-- driver above stays `proposed` because it describes the relation's SHAPE, which still rests on an
-- open finding; a per-column ruling has no slot of its own and is recorded at the column.
--
-- READ, NOT DECORATION. `mac_transforms` lifts these onto the descriptor, so a reader
-- learns WHO decided this shape without opening the SQL. `proposed` because the
-- decision below was made from a MEASUREMENT this bundle already holds, and the
-- finding it names is still open — a person has not yet ruled on it.
--
-- GRAIN: one row per ProductKey.   KEY: `product_key`.   2 517 rows, 2 517 distinct keys.
--
-- CATEGORY AND SUBCATEGORY ARE LEVELS ON THIS DIMENSION, not dimensions of their own. They are
-- functionally dependent on the product and no fact points at them: measured, CategoryKey and
-- SubCategoryKey are key-shaped and NO relation in scope carries either as a key
-- (DQ-DANGLINGKEY-CATEGORYKEY, -SUBCATEGORYKEY). Promoting them would manufacture two boxes nothing
-- can join to; as levels, the hierarchy is stated where it lives.
--
-- COST AND PRICE ARE IN THE SOURCE (`main.product.Cost` / `main.product.Price`) and are
-- DELIBERATELY NOT PROMOTED into the served Product view (operator ruling, 2026-10-26). The
-- source columns are an undated standing snapshot, while the served question space reads dated
-- sales-line prices (`unit_price`, `net_price`, `unit_cost`) and composes amounts from them.
CREATE OR REPLACE VIEW contoso_served.dim_product AS
SELECT
  p."ProductKey"      AS product_key,        -- PK
  p."ProductCode"     AS product_code,
  p."ProductName"     AS product_name,
  p."Manufacturer"    AS manufacturer,
  p."Brand"           AS brand,
  -- ONE COLOUR, ONE SPELLING (operator ruling, 2026-09-30: "the word is fold"). The landing holds
  -- `Blue` on 197 products and `blue` on 3 — one colour spelled twice, measured 17 distinct values
  -- over 16 case-folded ones. The ontology said so and could not act on it: Color declared the
  -- lowercase spelling as a 17th MEMBER "awaiting a ruling", and RC03 answered 17 where the
  -- approved answer is 16. Folding here, not at read time, is what the concept itself asked for —
  -- "folding it is a ruling for a person and a transform, not a silent edit in the ontology".
  --
  -- THE RULE IS THE FIRST LETTER, NOT THE ONE BAD VALUE (operator, 2026-09-30). This was a
  -- `CASE WHEN "Color" = 'blue'` — a fix for the typo that is in the data TODAY, which says nothing
  -- about the next one and would let `red` through in silence. A colour name is capitalised: that is
  -- the rule, it holds for every member, and it is idempotent on the 16 that already comply.
  --
  -- NOT `initcap`, deliberately: it lowercases the remainder of every word, so `Silver Grey` would
  -- come back `Silver grey` and a compliant member would be rewritten. Only the first character is
  -- touched; the rest is the delivery's. `main.product` keeps both spellings, so the defect stays
  -- visible where it is real.
  upper(substr(p."Color", 1, 1)) || substr(p."Color", 2)   AS color,
  p."CategoryName"    AS category_name,      -- level 1
  p."SubCategoryName" AS sub_category_name,  -- level 2, finer_than category_name
  p."Weight"          AS weight,             -- unit: see weight_unit; never summed across products
  p."WeightUnit"      AS weight_unit
FROM main.product p;
