---
type: Rule
title: Location.channel
state: proposed
---

# Location.channel

> PROJECTED from `ontology/rules/Location.channel.yaml` by tools/mac_rules.py — do not edit; change the yaml.

The online store is recorded as a location, but it is not a place. Questions about locations and places cover physical locations only, unless they name the online channel.

- **State** — proposed · wording proposed, awaiting acceptance
- **Concepts** — Location
- **Formal** — **Symbolic** — implemented by the declarations below
- **Keywords** — location, place, site, online, physical, channel
- **Formerly** — `location.exclusion.the_online_row_is_not_a_place`

## How and where it is implemented

```
  declared at   ontology/concepts/location.yaml#readings.channel
                ontology/relations/dim_location.yaml#columns.location_code.rules
  realized by   mac.canon.population_select  (kind resolution)   default: physical
                physical: location_code != -1
                online: location_code = -1
  executed by   planner/populations.py — WHICH ROWS a concept has. Named populations as structured predicates (planner/predicates.py), one marked `default`, and the rule's own 
  tested by     (nothing names a question)
```
