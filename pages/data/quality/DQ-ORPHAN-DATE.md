---
type: DQ Issue
title: raw landing `date` is consumed by no transformation
description: raw landing `date` is consumed by no transformation
tags:
- Contoso 5
- severity:medium
- disposition:open
---

`DQ-ORPHAN-DATE` · severity **medium** · disposition **open — nobody has ruled** · filed under [v_contoso5_sales_line](../datasets/v_contoso5_sales_line.md)

## Finding

raw landing `date` is consumed by no transformation

## About

- `source:date`

## Needs

**Needs** — a ruling: is this relation OUT OF SCOPE for this bundle, or is a served relation missing?

## Disposition

**open**.
- said by **mac_dq_findings.py/1**

## Repaired by

_No transform's `repairs` names this finding._

## Blocks and waives

_It blocks and waives nothing._

## Evidence

- 4,018 rows harvested and never curated; no data/transforms/*.yaml declares it as an input
- Filed under v_contoso5_sales_line: `date` feeds no dataset; the dates it would describe are this dataset's order and delivery dates, read through the built-in calendar (S-3).
