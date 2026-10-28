---
type: DQ Issue
title: served relation `contoso5_brand` is claimed by no concept
description: '22 relation(s) are served and 8 are claimed by at least one of 11 concept(s);
  `contoso5_brand` is claimed by none. A served relation is one a question can read,
  so an unclaimed one is either a notion '
tags:
- CONTOSO5
- severity:medium
- confidence:?
- lifecycle:draft
---

`DQ-UNCLAIMED-CONTOSO5_BRAND` · severity **medium** · confidence **?** · disposition **accepted · ruled by ontology-developer**

## Finding
22 relation(s) are served and 8 are claimed by at least one of 11 concept(s); `contoso5_brand` is claimed by none. A served relation is one a question can read, so an unclaimed one is either a notion nobody modelled or a relation that should not be served — and the delivered artifacts do not say which.

## Current handling
—

## Residual risk
—

## Sign-off required
—

## Disposition

**accepted** — ruled by **ontology-developer**.

RULED BY ROLE ontology-developer UNDER EXPLICIT TASK DIRECTION (2026-10-16 register->relation fold completion), NOT A STANDING OPERATOR SIGN-OFF ON THIS BUNDLE'S MODEL — flagged here for operator review/override. MEASURED, not the three stock answers: `Brand` already serves this exact value (`dim_product.brand`, in `Brand`'s own grounding), so this is neither an unmodelled notion (`model_a_concept`) nor a notion with none (`backs_no_notion`) — it is ALREADY modelled, one relation over. The register is the FK domain `dim_product.brand` draws from (and, where shared, what other relations' own `brand`-shaped columns draw from too), not a second ground for `Brand`. Declining to bind it as a second `grounding.bindings[]` entry: `check_delivery_consistency._effective_source` reads only a concept's FIRST binding, so a second entry would not even register as 'claimed' by this gate, and restructuring `Brand`'s primary binding onto this narrower, differently-named register would drop columns and rules bound to the richer relation's own column names for no gain. `Brand` also carries `counts: brand` — 11 distinct values over 2517 product rows, exactly this register's 11 rows.

## Table
- [product](../sources/product.md)