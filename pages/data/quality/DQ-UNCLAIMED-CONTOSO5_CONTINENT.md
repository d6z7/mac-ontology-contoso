---
type: DQ Issue
title: served relation `contoso5_continent` is claimed by no concept
description: served relation `contoso5_continent` is claimed by no concept
tags:
- Contoso 5
- severity:medium
- disposition:accepted
---

`DQ-UNCLAIMED-CONTOSO5_CONTINENT` · severity **medium** · disposition **accepted · said by ontology-developer** · filed under [contoso5_continent](../datasets/contoso5_continent.md)

## Finding

served relation `contoso5_continent` is claimed by no concept

## About

- `dataset:contoso5_continent`

## Needs

**Needs** — Which is it? ANSWER ONE OF: model_a_concept | stop_serving_it | backs_no_notion. A decline is a legitimate answer and the reason is the deliverable — `backs_no_notion` with no reason leaves the next reader exactly where this finding found them.

**Remedies**

- model_a_concept: a concept grounds on it and the relation becomes answerable
- stop_serving_it: it leaves the served plane — which on a 1:1 passthrough means authoring a transform, because a passthrough serves everything by construction
- backs_no_notion: it stays served and is recorded as deliberately unmodelled, so the next reader finds the decision instead of the gap

## Disposition

**accepted**.
- said by **mac_dq_findings.py/1**
- said by **ontology-developer**: “RULED BY ROLE ontology-developer UNDER EXPLICIT TASK DIRECTION (2026-10-16 register->relation fold completion), NOT A STANDING OPERATOR SIGN-OFF ON THIS BUNDLE'S MODEL — flagged here for operator review/override. MEASURED, not the three stock answers: `Customer` already serves this exact value (`dim_customer.continent`, in `Customer`'s own grounding), so this is neither an unmodelled notion (`model_a_concept`) nor a notion with none (`backs_no_notion`) — it is ALREADY modelled, one relation over. The register is the FK domain `dim_customer.continent` draws from (and, where shared, what other relations' own `continent`-shaped columns draw from too), not a second ground for `Customer`. Declining to bind it as a second `grounding.bindings[]` entry: `check_delivery_consistency._effective_source` reads only a concept's FIRST binding, so a second entry would not even register as 'claimed' by this gate, and restructuring `Customer`'s primary binding onto this narrower, differently-named register would drop columns and rules bound to the richer relation's own column names for no gain.”

## Repaired by

_No transform's `repairs` names this finding._

## Blocks and waives

_It blocks and waives nothing._

## Evidence

- 22 relation(s) are served and 8 are claimed by at least one of 11 concept(s); `contoso5_continent` is claimed by none. A served relation is one a question can read, so an unclaimed one is either a notion nobody modelled or a relation that should not be served — and the delivered artifacts do not say which.
