---
type: Rule
title: sales.ask_currency_when_ambiguous
description: ambiguity rule
tags:
- mac.rule_kind.ambiguity
applies_to: ../sales.md
---

## Rule

- **Kind** — `ambiguity`
- **Rule id** — `sales.ask_currency_when_ambiguous`

### When

a question implies a single-currency total but names no reporting currency and the rows span several

### Then — do (then)

either ASK which reporting currency, or COMMIT to the disclosed base currency as the default

### Never — don't (never)

silently picking one currency's rows and calling it the total

Applies to [Sales (net revenue)](../sales.md).