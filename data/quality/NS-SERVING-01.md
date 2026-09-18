---
type: DQ Issue
title: 15 leftover views in the warehouse, measured, neither treated as sources nor
  served
description: 'Measured 2026-09-18 from information_schema: the warehouse holds 8 BASE
  TABLEs in `main` (what setup.sh builds from data/*.parquet) plus 15 VIEWs left by
  a deleted run — 8 in `contoso_raw` and 7 in `c'
tags:
- CONTOSO
- severity:medium
- confidence:I
- lifecycle:draft
---

`NS-SERVING-01` · severity **medium** · confidence **I**

## Finding
Measured 2026-09-18 from information_schema: the warehouse holds 8 BASE TABLEs in `main` (what setup.sh builds from data/*.parquet) plus 15 VIEWs left by a deleted run — 8 in `contoso_raw` and 7 in `contoso_served` (S20). The 8 `contoso_raw` views were measured row-for-row and column-for-column identical to the `main` base tables before being set aside (P1). The 7 `contoso_served` views were deliberately NOT read: their names and renamed columns ARE the deleted run's modelling decisions, and reading them would smuggle a deleted result into this one. None of them carries a name this promotion coins (0 collisions over the 6 served names, S21).


## Current handling
NOT treated as sources (no raw descriptor, no profile) and NOT served. This bundle's own serving schema is declared in connection.yaml#view_schema as `contoso_served`, so the 6 relations promoted here will be created alongside those 7 leftovers unless they are dropped first.


## Residual risk
A reader of `contoso_served` would see 7 relations from a deleted run beside 6 from this one and could not tell which is a result. DROP cannot be done from here: the declared connection is read-only and dropping is destructive. REVERSED/CLOSED WHEN: the operator drops `contoso_raw` and `contoso_served` before the transform step materialises (run record Q2, Q15), or rules that a different serving schema should be declared instead.


## Sign-off required
The operator of this checkout — it is their warehouse file and their console mount; no modelling ruling is involved.
