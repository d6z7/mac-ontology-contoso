---
type: DQ Issue
title: 15 leftover views in the warehouse, measured, neither treated as sources nor
  served
description: 'Measured 2026-09-18 from information_schema, BEFORE THE DROP recorded
  above: the warehouse held 8 BASE TABLEs in `main` (what setup.sh builds from data/*.parquet)
  plus 15 VIEWs left by a deleted run —'
tags:
- CONTOSO
- severity:medium
- confidence:I
- lifecycle:draft
---

`NS-SERVING-01` · severity **medium** · confidence **I** · disposition **accepted · ruled by operator**

## Finding
Measured 2026-09-18 from information_schema, BEFORE THE DROP recorded above: the warehouse held 8 BASE TABLEs in `main` (what setup.sh builds from data/*.parquet) plus 15 VIEWs left by a deleted run — 8 in `contoso_raw` and 7 in `contoso_served` (S20). The 8 `contoso_raw` views were measured row-for-row and column-for-column identical to the `main` base tables before being set aside (P1). The 7 `contoso_served` views were deliberately NOT read: their names and renamed columns ARE the deleted run's modelling decisions, and reading them would smuggle a deleted result into this one. None of them carries a name this promotion coins (0 collisions over the 6 served names, S21).


## Current handling
NOT treated as sources (no raw descriptor, no profile) and NOT served. This bundle's own serving schema is declared in connection.yaml#view_schema as `contoso_served`, so the 6 relations promoted here will be created alongside those 7 leftovers unless they are dropped first.


## Residual risk
A reader of `contoso_served` would see 7 relations from a deleted run beside 6 from this one and could not tell which is a result. DROP cannot be done from here: the declared connection is read-only and dropping is destructive. REVERSED/CLOSED WHEN: the operator drops `contoso_raw` and `contoso_served` before the transform step materialises (run record Q2, Q15), or rules that a different serving schema should be declared instead.


## Sign-off required
The operator of this checkout — it is their warehouse file and their console mount; no modelling ruling is involved.


## Disposition

**accepted** — ruled by **operator**.

The leftovers were a second vocabulary for one warehouse, not a second body of data. Dropped on the operator's explicit instruction 2026-09-18 (`DROP SCHEMA contoso_served CASCADE; DROP SCHEMA contoso_raw CASCADE`), after measuring that every row in them is reachable from `main` or from the parquet files behind it. Verified after: `information_schema` holds 8 BASE TABLEs in `main` and no views at all; main.orderrows still 223 974 rows and main.customer still 104 990, matching the pre-drop measurements. The risk this entry existed to record — a reader of `contoso_served` seeing 7 relations from a deleted run beside 6 from this one, unable to tell which is a result — cannot arise, because this run's 6 views will be the only relations in that schema.