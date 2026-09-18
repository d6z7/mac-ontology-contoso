-- data/transforms/v_contoso_order_line.sql — realizes data/transforms/v_contoso_order_line.yaml.
-- The served relation contoso_served.v_contoso_order_line: one statement, one served relation.
-- AUTHORED, NOT DEPLOYED: connection.yaml declares read_only: true, so this view does
-- not exist in the warehouse yet and every rule's status in the descriptor is
-- `authored`. The SELECT body below was executed read-only and is recorded with its
-- answers in queries/p4_transformation_authoring.sql (T1/T2).
-- PRECONDITION: the schema contoso_served must exist and must not hold the 15 leftover views
-- of the deleted run (RUN.md Q2/Q15, register NS-SERVING-01).
-- INPUTS   main.orderrows (the line, and the grain)  x  main.orders (the header)
-- BAKES OUT
--   · the DOUBLE DELIVERY: main.sales repeats these 223 974 lines with 0 differences over 10
--     columns (T5) and is deliberately not read — register NS-ORDERS-01. One figure, one home.
--   · the landing's abbreviation: orders.DT is served as OrderDate, the name the same value
--     carries in the sales delivery (identical on 223 974/223 974 rows, T4).
-- CARRIES UNFIXED (see the descriptor's open_transforms[]): the 1 448 orders with RowNumber gaps,
--   the 8 indistinguishable line pairs, and the 93 550 lines pointing at the sentinel store.
-- GRAIN    one row per (OrderKey, RowNumber) — 223 974 rows / 223 974 distinct / 0 duplicates (T2a).
--          The join cannot fan out or lose a line: orders.OrderKey is unique and 0 lines are
--          orphaned (T3). orders.OrderKey is read as the JOIN PREDICATE only; the served OrderKey
--          is projected from the detail side.
CREATE OR REPLACE VIEW contoso_served.v_contoso_order_line AS
SELECT r."OrderKey",
       r."RowNumber",
       o."DT" AS OrderDate,
       o."DeliveryDate",
       o."CustomerKey",
       o."StoreKey",
       r."ProductKey",
       o."CurrencyCode",
       r."Quantity",
       r."UnitPrice",
       r."NetPrice",
       r."UnitCost"
FROM main.orderrows r
JOIN main.orders o ON o."OrderKey" = r."OrderKey";
