---
type: DQ Issue
title: data-sanity case G-contoso5_manufacturer-KEY did not pass
description: data-sanity case G-contoso5_manufacturer-KEY did not pass
tags:
- Contoso 5
- severity:high
- disposition:open
---

`DQ-CASE-G-contoso5_manufacturer-KEY` · severity **high** · disposition **open — nobody has ruled** · filed under [contoso5_manufacturer](../datasets/contoso5_manufacturer.md)

## Finding

data-sanity case G-contoso5_manufacturer-KEY did not pass

## About

- `dataset:contoso5_manufacturer`

## Needs

**Needs** — a disposition: fix the data, or accept the reading with a reason.

## Disposition

**open**.
- said by **mac_dq_findings.py/1**

## Repaired by

_No transform's `repairs` names this finding._

## Blocks and waives

_It blocks and waives nothing._

## Evidence

- Prove the declared key of contoso5_manufacturer is still unique QUESTION. Can two rows now share code? ANSWER. 1 column(s) are declared as the key of this relation. RISK. A duplicated key multiplies e
