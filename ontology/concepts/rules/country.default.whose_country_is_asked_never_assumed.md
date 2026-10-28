---
type: Rule
title: country.default.whose_country_is_asked_never_assumed
description: default rule · binds country_code
tags:
- CONTOSO5
- mac.concept.rule.default
- confidence:C
applies_to: ../country.md
---

## Rule

- **Kind** — `default`
- **Confidence** — C (confirmed)
- **Scope** — CONTOSO5
- **Binds** — `country_code`
- **Rule id** — `country.default.whose_country_is_asked_never_assumed`
- **Decided in** — `meaning-as-code#decisions/RULED-2026-10-25_a-sale-is-attributed-by-its-channel.md`

> The clauses below are PROJECTED from `mac.canon.path_select` — the canon this rule binds. They are not authored here and must not be edited: change the declaration.

### When

a measure is grouped by or filtered on this concept and the question does not say through what

### Then — do (then)

4 named reading(s): `customer` (also called customer country; where our customers are; customer countries); `location` (also called site country; location country); `store` (also called store country; where we trade; trading country); `territory` (also called country of the sale; where the sale was made; trade in; business in; market). `customer` arrives by `customer__based_in__country`; `location` arrives by `location__in__country`; `store` arrives by `store__trades_in__country`; `territory` arrives by `order__attributed_to__country`. a question naming none of them takes `territory`, and the answer DISCLOSES that it did

### Never — don't (never)

averaging two readings, which are answers to different questions; picking between them silently

Applies to [Country](../country.md).