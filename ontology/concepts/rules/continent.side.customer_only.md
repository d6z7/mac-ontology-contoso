---
type: Rule
title: There is no store-side continent — the roll-up exists on one side only
description: exclusion rule · binds Continent, Country
tags:
- mac.rule_kind.exclusion
- confidence:P
applies_to: ../continent.md
---

## Rule

- **Kind** — `exclusion`
- **Confidence** — P (proposed)
- **Binds** — `Continent`, `Country`
- **Rule id** — `continent.side.customer_only`

### When

a question asks for a continent figure about STORES, or about where sales were made

### Then — do (then)

REFUSE the store-side continent and say why — `{dim_contoso_store}` carries no continent column — then offer the customer-side continent figure, or the store-side figure at `{CountryCode}` level, which is as far as that relation reaches

### Never — don't (never)

deriving a store continent by mapping `{CountryCode}` through the customer dimension: that silently attributes the 93 550 online lines to nothing and asserts a roll-up the store relation does not carry

Applies to [Continent](../continent.md).