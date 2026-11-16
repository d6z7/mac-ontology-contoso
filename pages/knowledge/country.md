# Country

> The human account. The declaration is `ontology/concepts/country.yaml`; read this first, whole, then compare it against that
> file. Every ruling below is dated and every figure measured.

## What a country is here

A country the business sells in or sells to: eight of them, plus the online sentinel. Read from
the rows: `AU, Australia`. A QUESTION ABOUT COUNTRIES IS A QUESTION ABOUT THIS CONCEPT — "which
countries", "list the countries", "how many countries", "by country". The country is not a
property of the customer or of the store any more; both of them POINT at it. "Countries where we
have customers" asks for THIS concept's members, restricted to the ones a customer references —
the subject is Country and Customer is the restriction, never the other way round, which returns
one row per customer. A2: a keyed dimension that other rows point at → `reference`. Customer,
Store and Location all point at it, measured many:one. IT WAS A COLUMN ON THREE RELATIONS AND A
REFERENCE TO NOTHING. `dim_customer.country_code`, `dim_store.country_code` and
`dim_location.country_code` each carried the code, and the NAME was carried on exactly one of them
— `dim_location.country_name`, ruled `label_of: country_code`. So a question about customers could
not reach the name: dim_location is the STORE's geography, keyed on location_code, and nothing
joins a customer to it. Measured 2026-09-30, the two candidate paths both fail: the customer's own
`GeoAreaKey` is a different code space (608 values over 1..616 against the location's 67; 69,902
customers have no location; where they collide the country agrees on 14,989 of 35,088), and
joining on the country CODE is many:many — 9 codes over 67 location rows, US alone 24 — which
turns 104,990 customers into 1,462,707 rows. SO THE NAME HAS ONE HOME AND EVERY SIDE CAN REACH IT.
`country_name` is ruled `label_of: country_code` with `register: long` here, once, and Customer,
Store and Location reach it through an edge instead of each carrying a copy. Operator ruling,
2026-09-30. `--` IS NOT A COUNTRY. The source wrote the online business as one row of the store
table with `--` where a country code goes, and it is carried here for the reason `dim_location`
carries it: dropping it would make the online store's code a reference to nothing. "In how many
countries do we sell" is EIGHT, not nine, and this concept's own `real` population is what keeps
the sentinel out of a geographic answer — executably, since 2026-10-01. That row carries 93,550 of
223,974 sales and $86.8M, reachable by naming the `sentinel` population or the `online` one on
[[Store]]. NAMES RESOLVE THROUGH `data/lookups/contoso5_country_code.lookup.yaml` — a question
says "Australia" or "Italy", never `AU`.

## How identity is established

The canonical key is a COLUMN fact and is not repeated here; this says only HOW identity is
established. A `country_code` that IS the identity — ISO-3166 alpha-2, nine codes, no surrogate
behind it.

## The grain

one row per country code — nine as stored, eight as meant

## The sentinel row — a population, not an exclusion

`--` is the sentinel the source wrote where the online store's country goes. Counting it answers 9
to "in how many countries do we sell" when the truth is 8, and it is the single largest "store" in
the warehouse, so it dominates any list it is allowed into.

The declaration states this executably as well, because this rule has no body yet:

- **never** — report nine countries

NO `when:`/`then:`, 2026-10-01 — the body below states both. The `then` read "exclude `--`, and
say so", which is exactly what `default: real` does, disclosed on every answer. `never: report
nine countries` is KEPT: it is the measured consequence in the bundle's own words, it is what the
model is shown, and no predicate says it.

THE SAME MECHANISM AS Store's, on this concept's OWN rows. Not a duplicate of it: the sentinel is
written into THREE relations, each with its own column and its own row — `dim_store.store_code
= -1`, `dim_location.location_code = -1`, and here `dim_country.country_code = '--'`. One fact,
three populations, because a population selects the rows of the relation it is declared on and
nothing else. MEASURED on `dim_country`: 9 rows, 1 sentinel, 8 real.

the 8 countries Contoso actually sells in.

the 1 sentinel row, asked for by name or not at all.

## Whose country a sales question means

A sale has no country of its own to point at: it reaches one only through something else that
carries a country code, and three relations here do — the store it was rung up at, the customer who
bought it, and the store's site. The readings are far apart. Germany's 2025 growth is +18.07%
through the customer and +49.65% through the store, because the store path drops the online channel
and the online channel is 40% of net revenue. A reader given a bare number cannot tell which they
got. Naming the value is not naming the reading: "Germany" settles the code, `DE`, and says nothing
about which of the three joins to put it on.

**A sale is attributed by its channel — operator ruling, 2026-10-25.** A shop sale is trade in the
country the shop stands in; a web sale is trade in the country the customer lives in. That is the
reading an unqualified country question means, and it is a column on the sales line,
`sale_country_code`, so it needs no join and no choice. The store's, the customer's and the site's
own country stay askable by name through their own relations.

Measured over all 223,974 lines: eight countries, every line attributed, Germany 24,638,830.18, the
eight summing to 218,814,471.66 — the whole fact, nothing double counted and nothing lost. The `--`
sentinel carries ZERO lines on this axis, because a web sale is attributed to a person and a person
has a real country; the store route put 93,550 lines on it.

**This reading is not the customer's country under another name**, though here it is row-for-row
identical to it: no physical sale in this warehouse crosses a border, 0 of 130,424, so the two agree
by an accident of the data. A German tourist buying in Paris would part them and would be French
trade. The operator was offered `default: customer` on 2026-10-22 and refused it for that reason.

Two earlier rulings on this question are superseded and are recorded where they were made.
2026-09-30 named the STORE as the unqualified reading; 2026-10-22 removed every default and made the
unqualified case ASK ("THERE IS NO DEFAULT ... DEFAULT IS ASK"), which held until today. What
survives from both, unchanged, is the prohibition: never pick between the store and the customer
silently, and never average the two. The attribution above picks neither.
