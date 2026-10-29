---
type: Rule
title: Store.channel
state: ruled
---

# Store.channel

> PROJECTED from `ontology/rules/Store.channel.yaml` by tools/mac_rules.py — do not edit; change the yaml.

A store is a shop you can walk into. The online channel is recorded as a store, but a question about stores — how many there are, which ones — covers physical shops only unless it names the online channel. That default holds only when the question is about stores: revenue and every other figure of the sale includes both channels, even when the question's route passes through stores.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Store, Order
- **Formal** — **Symbolic** — declared at `ontology/concepts/store.yaml#readings.channel`
- **Keywords** — store, shop, online, physical, channel, web, internet, revenue, both channels
- **Decided in** — `meaning-as-code#decisions/RULED-2026-10-18_both-channels-make-revenue.md`
- **Supersedes** — `Store.revenue_is_shop_only`
- **Formerly** — `store.resolution.the_channel_is_the_location_sentinel`

## What was said

> *"now i am for correctnes and correct is that both internet and physical shops combined make revenue."* — operator, 2026-10-18 (`meaning-as-code#decisions/RULED-2026-10-18_both-channels-make-revenue.md`)

> *"i would like to revert my ruling from before. then it was aimed at simplicity ... now i am for correctnes and correct is that both internet and physical shops combined make revenue."* — operator, 2026-10-18 (`meaning-as-code#decisions/RULED-2026-10-18_both-channels-make-revenue.md`)


## Examples

| Question | Reading |
|---|---|
| how many stores do we have | physical shops only |
| what is our revenue | both channels |
