---
type: Rule
title: Country is carried in two roles that do not agree — name the one you mean
description: ambiguity rule · binds Country, CountryCode
tags:
- mac.rule_kind.ambiguity
- confidence:P
applies_to: ../country.md
---

## Rule

- **Kind** — `ambiguity`
- **Confidence** — P (proposed)
- **Binds** — `Country`, `CountryCode`
- **Rule id** — `country.roles.customer_or_store_never_both`

### When

a question breaks a figure down by country without saying whose

### Then — do (then)

use the CUSTOMER role (`{Country}` on `{dim_contoso_customer}`) and say so; offer the STORE role (`{CountryCode}` on `{dim_contoso_store}`) when the question is about where the sale was made rather than who bought

### Never — don't (never)

mixing the two in one breakdown, or silently substituting one for the other: the store side carries the '--' sentinel on 93 550 of 223 974 lines and has no continent column, so the two roles give different rows and different totals

Applies to [Country](../country.md).