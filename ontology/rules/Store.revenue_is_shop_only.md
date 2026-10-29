---
type: Rule
title: Store.revenue_is_shop_only
state: superseded
---

# Store.revenue_is_shop_only

> PROJECTED from `ontology/rules/Store.revenue_is_shop_only.yaml` by tools/mac_rules.py — do not edit; change the yaml.

If revenue is asked without naming a channel, only shop revenue is assumed.

- **State** — superseded · wording proposed, awaiting acceptance
- **Concepts** — Store, Order
- **Formal** — **Prose** — no symbolic form yet; handed to the model as text (formalisation debt)
- **Keywords** — revenue, shop, channel, online
- **Superseded by** — `Store.channel`

## How and where it is implemented

```
  declared at   (nowhere — prose, stated in words only)
  tested by     (nothing names a question)
```

## What was said

> *"then it was aimed at simplicity ... now i am for correctnes and correct is that both internet and physical shops combined make revenue."* — operator, 2026-10-18 (`ontology/concepts/store.yaml (comment, v0.3.0)`)

> *"if the revenue is asked without specifying a channel then only shop is assumed"* — operator, 2026-10-10 (`meaning-as-code#decisions/RULED-2026-10-18_both-channels-make-revenue.md`)
