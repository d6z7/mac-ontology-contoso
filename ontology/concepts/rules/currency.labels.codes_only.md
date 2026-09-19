---
type: Rule
title: A currency NAME does not resolve here — the delivery holds no names
description: ambiguity rule · binds CurrencyCode
tags:
- mac.rule_kind.ambiguity
- confidence:P
applies_to: ../currency.md
---

## Rule

- **Kind** — `ambiguity`
- **Confidence** — P (proposed)
- **Binds** — `CurrencyCode`
- **Rule id** — `currency.labels.codes_only`

### When

a question names a currency in words — dollars, euros, pounds, sterling

### Then — do (then)

for a word that maps unambiguously to one of the 5 codes, resolve it and say which code was used; for an ambiguous word ask which is meant, naming the candidate codes

### Never — don't (never)

picking one of `{CurrencyCode}`'s dollar codes for a bare 'dollars' — USD, CAD and AUD are all dollars, and the delivery states no name for any of them to arbitrate with

Applies to [Currency](../currency.md).