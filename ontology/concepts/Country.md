# Country

The account of concept Country.

## What a country is here

A country the business sells in or sells to, plus the online sentinel. Read from the rows: `AU, Australia`. A QUESTION ABOUT COUNTRIES IS A QUESTION ABOUT THIS CONCEPT — "which countries", "list the countries", "how many countries", "by country". The country is not a property of the customer or of the store; both of them POINT at it. "Countries where we have customers" asks for THIS concept's members, restricted to the ones a customer references — the subject is Country and Customer is the restriction, never the other way round, which returns one row per customer. Customer, Store and Location all point at it, measured many:one. A customer cannot reach a location: the customer's own `GeoAreaKey` is a different code space from the location's, and joining on the country CODE is many:many, which multiplies every customer by the locations in its country. SO THE NAME HAS ONE HOME AND EVERY SIDE CAN REACH IT. `country_name` names `country_code` here, and Customer and Store reach it through an edge instead of carrying a copy; Location carries its own copy beside the code. `--` IS NOT A COUNTRY. The source wrote the online business as one row of the store table with `--` where a country code goes, and it is carried here for the reason `dim_location` carries it: dropping it would make the online store's code a reference to nothing. "In how many countries do we sell" counts real countries only, and this concept's own `real` population is what keeps the sentinel out of a geographic answer. That row stands for the online business, reachable by naming the `sentinel` population or the `online` one on [[Store]]. a question says "Australia" or "Italy", never `AU`.

## How identity is established

A `country_code` that IS the identity — ISO-3166 alpha-2, no surrogate behind it.

## The grain

one row per country code — the sentinel is stored but is not a country

## The sentinel row — a population, not an exclusion

`--` is the sentinel the source wrote where the online store's country goes. Counting it adds a country that is not one to "in how many countries do we sell", and it is the single largest "store" in the warehouse, so it dominates any list it is allowed into.

- **never** — count the sentinel as a country

THE SAME MECHANISM AS Store's, on this concept's OWN rows. Not a duplicate of it: the sentinel is written into THREE relations, each with its own column and its own row — `dim_store.store_code = -1`, `dim_location.location_code = -1`, and here `dim_country.country_code = '--'`. One fact, three populations, because a population selects the rows of the relation it is declared on and nothing else. `dim_country` holds one sentinel row; every other row is a real country.

the countries Contoso actually sells in.

the sentinel row, asked for by name or not at all.

## Whose country a sales question means

A sale has no country of its own to point at: it reaches one only through something else that carries a country code, and three relations here do — the store it was rung up at, the customer who bought it, and the store's site. The readings are far apart. Germany's growth reads very differently through the customer and through the store, because the store path drops the online channel, a large share of net revenue. A reader given a bare number cannot tell which they got. Naming the value is not naming the reading: "Germany" settles the code, `DE`, and says nothing about which of the three joins to put it on.

**A sale is attributed by its channel — operator ruling.** A shop sale is trade in the country the shop stands in; a web sale is trade in the country the customer lives in. That is the reading an unqualified country question means — the default (`territory`) of rule Country.whose — and it is a column on the sales line, `sale_country_code`, so it needs no join. The store's, the customer's and the site's own country stay askable by name through their own relations.

Every line is attributed to one real country, so the countries sum to the whole fact — nothing double counted and nothing lost. The `--` sentinel carries no lines on this axis, because a web sale is attributed to a person and a person has a real country; the store route puts every online line on it.

**This reading is not the customer's country under another name**, though here it is row-for-row identical to it: no physical sale in this warehouse crosses a border, so the two agree by an accident of the data. A German tourist buying in Paris would part them and would be French trade.

the prohibition: never pick between the store and the customer silently, and never average the two. The attribution above picks neither.

## Cites

- `dataset:dim_country.country_code`
- `dataset:dim_country.country_name`
- `dataset:dim_country.is_placeholder`
- `rule:Country.rows`
- `rule:Country.where_we_have_customers`
- `rule:Country.whose`

## grounding.note

one code per country as meant; a source spelling that duplicates another country is folded in the transform, and the placeholder `--` is not a country
