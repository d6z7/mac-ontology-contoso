---
type: DQ Issue
title: served relation `contoso5_channel` is claimed by no concept
description: served relation `contoso5_channel` is claimed by no concept
tags:
- Contoso 5
- severity:medium
- disposition:accepted
---

`DQ-UNCLAIMED-CONTOSO5_CHANNEL` · severity **medium** · disposition **accepted · said by ontology-developer** · filed under [contoso5_channel](../datasets/contoso5_channel.md)

## Finding

served relation `contoso5_channel` is claimed by no concept

## About

- `dataset:contoso5_channel`

## Needs

**Needs** — Which is it? ANSWER ONE OF: model_a_concept | stop_serving_it | backs_no_notion. A decline is a legitimate answer and the reason is the deliverable — `backs_no_notion` with no reason leaves the next reader exactly where this finding found them.

**Remedies**

- model_a_concept: a concept grounds on it and the relation becomes answerable
- stop_serving_it: it leaves the served plane — which on a 1:1 passthrough means authoring a transform, because a passthrough serves everything by construction
- backs_no_notion: it stays served and is recorded as deliberately unmodelled, so the next reader finds the decision instead of the gap

## Disposition

**accepted**.
- said by **mac_dq_findings.py/1**
- said by **ontology-developer**: “RULED BY ROLE ontology-developer UNDER EXPLICIT TASK DIRECTION (2026-10-23, the operator's ruling that the KPI channel split belongs in the transformation layer), NOT A STANDING OPERATOR SIGN-OFF ON THIS BUNDLE'S MODEL — flagged here for operator review/override. MEASURED, and the answer is `backs_no_notion` rather than `model_a_concept`: THE CHANNEL IS ALREADY MODELLED, AS A READING AND NOT AS AN ENTITY. `Store.channel` declares it as a POPULATION AXIS on Store with two named populations (`physical`, `online`), and `v_contoso5_sales_line.channel` now carries the same split as a column on the FACT so that no question has to reach the store dimension to learn it. A `Channel` CONCEPT existed and was DELIBERATELY DELETED — acceptance/prompts/*.txt still carry it as history — because a channel is not a thing you can count, it is which rows a question is about. This relation is the closed DOMAIN that column draws from (`references: contoso5_channel.code`), never a second ground: binding a concept to it would make a THIRD home for one fact, beside the population rule and the fact column, which is the defect the 2026-10-15 register fold exists to prevent. AND IT IS CLOSED BY CONSTRUCTION, unlike its twelve siblings: the values come from a CASE expression with exactly two branches, so no delivery can add a third without editing the transform — the others are cut from a stored column and are closed only as far as today's rows go.”

## Repaired by

_No transform's `repairs` names this finding._

## Blocks and waives

_It blocks and waives nothing._

## Evidence

- 22 relation(s) are served and 8 are claimed by at least one of 11 concept(s); `contoso5_channel` is claimed by none. A served relation is one a question can read, so an unclaimed one is either a notion nobody modelled or a relation that should not be served — and the delivered artifacts do not say which.
