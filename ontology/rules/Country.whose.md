---
type: Rule
title: Country.whose
state: ruled
---

# Country.whose

> PROJECTED from `ontology/rules/Country.whose.yaml` by tools/mac_rules.py — do not edit; change the yaml.

When a question asks for figures by country without saying whose country, a sale is attributed to the country it was made in: a shop sale to the country the shop stands in, an online sale to the country the customer lives in. Every sale reaches exactly one country, so the parts add up to the whole. A question may instead ask by store country, customer country or site country and gets that reading. The answer says which country it used.

- **State** — ruled · wording proposed, awaiting acceptance
- **Concepts** — Country, Customer, Order, Store
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — country, whose country, attribution, territory, market, store country, customer country, by country
- **Decided in** — `meaning-as-code#decisions/RULED-2026-10-25_a-sale-is-attributed-by-its-channel.md`
- **Supersedes** — `Country.whose_is_asked`
- **Formerly** — `country.default.whose_country_is_asked_never_assumed`

## How and where it is implemented

```
  declared at   ontology/concepts/country.yaml#readings.whose
  realized by   mac.canon.path_select  (kind default)   default: territory
                territory: via: order__attributed_to__country
                store: via: store__trades_in__country
                customer: via: customer__based_in__country
                location: via: location__in__country
  executed by   canons/path_select.py + planner/paths.py, hooked at planner/joins.resolve_join — WHICH RELATION an answer is reached through. The fourth member of the family po
  tested by     AGG-05  'What is the net revenue in Germany?'  board: pass (stale)
  tested by     AGG-16  'What percentage of total net revenue comes from customers resident in Germany?'  board: pass (stale)
  tested by     AGG-17  'What percentage of total net revenue was rung up by shops sited in Germany?'  board: pass (stale)
```

## What was said

> *"ok go B1 now"* — operator, 2026-10-25 (`meaning-as-code#decisions/RULED-2026-10-25_a-sale-is-attributed-by-its-channel.md`)


## Examples

| Question | Reading |
|---|---|
| revenue by country | country of the sale: shop country for shop sales, customer country for online sales; disclosed |
