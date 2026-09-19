---
type: Doc
title: SME questions — ontology
description: 29 questions and 45 sign-off requests the model and its tests put to an SME
tags:
- CONTOSO
- sme-questions
---

What the model and its tests ask a subject-matter expert: **29 question(s)** and **45 sign-off request(s)**, 74 row(s) in all. Consolidated from the register (model conditions and change-record `sme` blocks), concept open-question fields and test oracles flagged needs-SME; projected from ontology_quality.json and acceptance/sme_needs.json, so it stays in sync.

Conversation status is not part of this projection; it lives in the bundle's SME question ledger.

Rows by origin: concept-field 29 · register 45

## Questions — 29

### `concept:age_band#open_questions[AB-Q1]`

- origin: concept-field · owner role: operator · concept: [age_band](concepts/age_band.md)
- declared by the artifact: status NEEDS_SME_CONFIRMATION
- source: `ontology/concepts/customer/age_band.yaml` → `open_questions[id=AB-Q1]`

> Is 2025-12-31 the as-of date this delivery wants pinned, and who re-derives the band when the fact horizon moves past it? The date is a constant in three places that must agree — the transform rule, the .sql literal, and the descriptor note — and nothing compares it to max(order date).

### `concept:age_band#open_questions[AB-Q2]`

- origin: concept-field · owner role: operator · concept: [age_band](concepts/age_band.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/customer/age_band.yaml` → `open_questions[id=AB-Q2]`

> Are the partial bottom band (20-24, which the floor leaves short of five full years of intake) and the open-topped 90+ band the intended shape, or should the range be declared with explicit edges?

### `concept:age_band#open_questions[AB-Q3]`

- origin: concept-field · owner role: operator · concept: [age_band](concepts/age_band.md)
- declared by the artifact: status NEEDS_SME_CONFIRMATION
- source: `ontology/concepts/customer/age_band.yaml` → `open_questions[id=AB-Q3]`

> Can a human confirm the 15 bands as the whole value set, raising the members to confidence C and the closure to `closed`? The set is measured complete and is closed by construction; only the confirmation is missing, because a machine may not stamp C. Until then the set is declared `open` and a sixteenth band would be accepted silently rather than flagged.

### `concept:brand#open_questions[BRD-Q1]`

- origin: concept-field · owner role: operator · concept: [brand](concepts/brand.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/catalog/brand.yaml` → `open_questions[id=BRD-Q1]`

> Is Brand 1:1 with Manufacturer by law, or by coincidence in this snapshot? Measured 1:1 over all 11 brands today. If it is law, one of the two is redundant; if it is not, a manufacturer axis may eventually be wanted and this concept does not provide one.

### `concept:calendar_day#open_questions[CAL-Q1]`

- origin: concept-field · owner role: operator · concept: [calendar_day](concepts/calendar_day.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/time/calendar_day.yaml` → `open_questions[id=CAL-Q1]`

> Should the calendar key on `Date` or on `DateKey`? The two are bijective over all 4 018 rows; this concept keys on Date because the facts carry timestamps, but a delivery whose facts carry YYYYMMDD strings would want the other, and only one of the two can be the declared key.

### `concept:calendar_day#open_questions[CAL-Q2]`

- origin: concept-field · owner role: operator · concept: [calendar_day](concepts/calendar_day.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/time/calendar_day.yaml` → `open_questions[id=CAL-Q2]`

> Is the calendar year the reporting year? Only Gregorian periods are served — there is no fiscal-period column anywhere in the delivery — so a fiscal question cannot be answered and would need a new column rather than a new concept.

### `concept:continent#open_questions[CON-Q1]`

- origin: concept-field · owner role: operator · concept: [continent](concepts/continent.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/geography/continent.yaml` → `open_questions[id=CON-Q1]`

> Where do the 93 550 online lines belong in a continent total? They have a customer (and so a customer continent) but no store geography, so a store-side view has to put them somewhere or outside everything. Tied to CTY-Q1 on the Country concept.

### `concept:country#open_questions[CTY-Q1]`

- origin: concept-field · owner role: operator · concept: [country](concepts/country.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/geography/country.yaml` → `open_questions[id=CTY-Q1]`

> Does store CountryCode '--' mean "no geography" or "global"? The register records the question and the data cannot settle it; the answer decides whether an online line belongs in a continent total or outside every one of them.

### `concept:currency#open_questions[CUR-Q1]`

- origin: concept-field · owner role: operator · concept: [currency](concepts/currency.md)
- declared by the artifact: status NEEDS_SME_CONFIRMATION
- source: `ontology/concepts/finance/currency.yaml` → `open_questions[id=CUR-Q1]`

> What are the five currencies called? The delivery states no name anywhere, so every label is empty and a question phrased in words ('in euros') can only be resolved by convention, which this bundle declines to invent. A human supplies the five names.

### `concept:currency#open_questions[CUR-Q2]`

- origin: concept-field · owner role: operator · concept: [currency](concepts/currency.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/finance/currency.yaml` → `open_questions[id=CUR-Q2]`

> Should this bundle declare a reporting currency, so that a cross-currency total has a default answer instead of a per-currency breakdown?

### `concept:currency#open_questions[CUR-Q3]`

- origin: concept-field · owner role: operator · concept: [currency](concepts/currency.md)
- declared by the artifact: status NEEDS_SME_CONFIRMATION
- source: `ontology/concepts/finance/currency.yaml` → `open_questions[id=CUR-Q3]`

> The closed claim currently rests on the register-delegation route, which `check_enumeration_closure` accepts without per-member confirmation. Can a human also confirm the five codes as the whole domain, so the claim holds on its own evidence rather than on a delegation?

### `concept:customer#open_questions[CUS-Q1]`

- origin: concept-field · owner role: operator · concept: [customer](concepts/customer.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/customer/customer.yaml` → `open_questions[id=CUS-Q1]`

> Can a customer be restated — a second row for one CustomerKey with a new validity window? No customer is restated today (1 row each, measured), so this concept declares no snapshot collapse; if restatement is possible the concept needs one before the first duplicate lands.

### `concept:customer#open_questions[CUS-Q2]`

- origin: concept-field · owner role: operator · concept: [customer](concepts/customer.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/customer/customer.yaml` → `open_questions[id=CUS-Q2]`

> When a question says "by region" without saying whose, is the customer's geography or the store's intended? This concept defaults to the customer's because the store dimension has no continent and 41.8 % of lines sit at the 'Online' sentinel, but that is a modelling choice and not a measurement.

### `concept:exchange_rate#open_questions[FX-Q1]`

- origin: concept-field · owner role: operator · concept: [exchange_rate](concepts/exchange_rate.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/finance/exchange_rate.yaml` → `open_questions[id=FX-Q1]`

> Should the line-to-quote join be as-of (latest quote on or before the order date) instead of exact date equality? Equality works only because the grid is gapless and runs a year past the newest order; an order dated off the grid yields a silent NULL rather than a refusal.

### `concept:geo_area#open_questions[GA-Q1]`

- origin: concept-field · owner role: operator · concept: [geo_area](concepts/geo_area.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/geography/geo_area.yaml` → `open_questions[id=GA-Q1]`

> Should data/lookups/contoso_geo_area.lookup.csv be re-cut as the UNION of the customer and store region sets, so the three store-only regions resolve through the register like every other? That is a P6 change, not a concept change, and it would retire the declared-gap rule above.

### `concept:geo_area#open_questions[GA-Q2]`

- origin: concept-field · owner role: operator · concept: [geo_area](concepts/geo_area.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/geography/geo_area.yaml` → `open_questions[id=GA-Q2]`

> The 608 keys mix states, provinces, territories and counties across 8 countries. Is "region" one axis, or does a comparison across countries need a level that does not exist here?

### `concept:gross_sales_amount#open_questions[GSA-Q1]`

- origin: concept-field · owner role: operator · concept: [gross_sales_amount](concepts/gross_sales_amount.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/finance/gross_sales_amount.yaml` → `open_questions[id=GSA-Q1]`

> Is there a reporting currency this bundle should convert to by default, or must every multi-currency figure name its own? No default is declared, so today a cross-currency total has to state its conversion.

### `concept:net_sales_amount#open_questions[NSA-Q1]`

- origin: concept-field · owner role: operator · concept: [net_sales_amount](concepts/net_sales_amount.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/finance/net_sales_amount.yaml` → `open_questions[id=NSA-Q1]`

> Should a margin measure be declared over the served UnitCost? Cost is on the row and nothing reads it, so "profit" currently gets no answer and no refusal.

### `concept:net_sales_amount#open_questions[NSA-Q2]`

- origin: concept-field · owner role: operator · concept: [net_sales_amount](concepts/net_sales_amount.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/finance/net_sales_amount.yaml` → `open_questions[id=NSA-Q2]`

> Is OrderDate the right default period axis for a sales figure, or should a delivered-basis reading exist alongside it? Both roles are served and 130 424 of 223 974 lines carry the same date, so the choice is invisible on more than half the fact.

### `concept:order_line#open_questions[OL-Q1]`

- origin: concept-field · owner role: operator · concept: [order_line](concepts/order_line.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/order/order_line.yaml` → `open_questions[id=OL-Q1]`

> Is an order-level measure (freight, an order total, a header discount) expected in this delivery? A line relation can repeat a header column but never hold one, so the day such a figure arrives a second served relation at order grain becomes the right answer immediately.

### `concept:order_line#open_questions[OL-Q2]`

- origin: concept-field · owner role: operator · concept: [order_line](concepts/order_line.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/order/order_line.yaml` → `open_questions[id=OL-Q2]`

> Should the rate be matched as-of (latest quote on or before the order date) rather than on exact date equality? Equality works only because the quote grid is gapless and runs a year past the newest order; an order dated off the grid yields a silent NULL.

### `concept:product#open_questions[PRD-Q1]`

- origin: concept-field · owner role: operator · concept: [product](concepts/product.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/catalog/product.yaml` → `open_questions[id=PRD-Q1]`

> Is ProductCode the product's business identity, or an internal label? Both it and ProductName are measured unique over all 2 517 rows today, which is almost certainly convention rather than law; the answer decides whether a code arriving twice is a duplicate or a legitimate restatement.

### `concept:product#open_questions[PRD-Q2]`

- origin: concept-field · owner role: operator · concept: [product](concepts/product.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/catalog/product.yaml` → `open_questions[id=PRD-Q2]`

> Does a missing Weight mean "not recorded" or "not applicable"? 284 of 2 517 rows have no weight and 62 name a unit without one, so the two readings give different denominators for every weight figure.

### `concept:product_category#open_questions[PCT-Q1]`

- origin: concept-field · owner role: operator · concept: [product_category](concepts/product_category.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/catalog/product_category.yaml` → `open_questions[id=PCT-Q1]`

> Should CategoryKey and SubCategoryKey get relations of their own? They have no table in this delivery, so a category attribute other than its name has nowhere to live — the same shape NS-ORDERS-02 records for the order header.

### `concept:product_subcategory#open_questions[PSC-Q1]`

- origin: concept-field · owner role: operator · concept: [product_subcategory](concepts/product_subcategory.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/catalog/product_subcategory.yaml` → `open_questions[id=PSC-Q1]`

> Is the SubCategoryKey-to-CategoryKey digit encoding (101 under 1, 201 under 2) a delivery contract or a coincidence? This concept refuses to rely on it either way; a ruling would let a consumer use it, or retire the question.

### `concept:store#open_questions[STR-Q1]`

- origin: concept-field · owner role: operator · concept: [store](concepts/store.md)
- declared by the artifact: status NEEDS_SME_CONFIRMATION
- source: `ontology/concepts/store/store.yaml` → `open_questions[id=STR-Q1]`

> Is the business entity the store CODE (67) or the store VERSION (74)? This concept answers "code, collapsed to the latest version" and keys on the version because the fact does. The descriptor recorded the question as unruled and a human still owns it — the answer changes every store count in the bundle.

### `concept:store#open_questions[STR-Q2]`

- origin: concept-field · owner role: operator · concept: [store](concepts/store.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/store/store.yaml` → `open_questions[id=STR-Q2]`

> Should the online channel be modelled as a store at all, or as a separate channel axis? Keeping it here puts 41.8 % of the fact in a row whose country, region and state are all sentinels, so every store-geography figure carries a residual that is not a place.

### `concept:store_status#open_questions[SST-Q1]`

- origin: concept-field · owner role: operator · concept: [store_status](concepts/store_status.md)
- declared by the artifact: status NEEDS_SME_CONFIRMATION
- source: `ontology/concepts/store/store_status.yaml` → `open_questions[id=SST-Q1]`

> Did the landing's '' on 58 store rows mean 'operating', or 'not recorded'? The transform conformed it to NULL alongside the one genuine NULL, so the two are no longer distinguishable in the served plane. If it meant 'operating', a third member is legitimate and this concept's absence reading is over-cautious.

### `concept:store_status#open_questions[SST-Q2]`

- origin: concept-field · owner role: operator · concept: [store_status](concepts/store_status.md)
- declared by the artifact: status OPEN
- source: `ontology/concepts/store/store_status.yaml` → `open_questions[id=SST-Q2]`

> Should 'Restructured' roll up under 'Closed' for reporting? Both always carry a CloseDate, so structurally they are the same event with different causes; whether a business report wants them separate is not something the data can say.

## Sign-offs — 45

### `concept:age_band#confidence`

- origin: register · owner role: not declared · concept: [age_band](concepts/age_band.md)
- source: `ontology/concepts/customer/age_band.yaml` → `metadata.confidence`

> Is the concept “Age Band” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:brand#confidence`

- origin: register · owner role: not declared · concept: [brand](concepts/brand.md)
- source: `ontology/concepts/catalog/brand.yaml` → `metadata.confidence`

> Is the concept “Brand” (grouping) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:calendar_day#confidence`

- origin: register · owner role: not declared · concept: [calendar_day](concepts/calendar_day.md)
- source: `ontology/concepts/time/calendar_day.yaml` → `metadata.confidence`

> Is the concept “Calendar Day” (reference) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:continent#confidence`

- origin: register · owner role: not declared · concept: [continent](concepts/continent.md)
- source: `ontology/concepts/geography/continent.yaml` → `metadata.confidence`

> Is the concept “Continent” (grouping) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:country#confidence`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/concepts/geography/country.yaml` → `metadata.confidence`

> Is the concept “Country” (reference) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:currency#confidence`

- origin: register · owner role: not declared · concept: [currency](concepts/currency.md)
- source: `ontology/concepts/finance/currency.yaml` → `metadata.confidence`

> Is the concept “Currency” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:customer#confidence`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md)
- source: `ontology/concepts/customer/customer.yaml` → `metadata.confidence`

> Is the concept “Customer” (entity) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:exchange_rate#confidence`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/concepts/finance/exchange_rate.yaml` → `metadata.confidence`

> Is the concept “Exchange Rate” (measure) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:geo_area#confidence`

- origin: register · owner role: not declared · concept: [geo_area](concepts/geo_area.md)
- source: `ontology/concepts/geography/geo_area.yaml` → `metadata.confidence`

> Is the concept “Region” (reference) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:gross_sales_amount#confidence`

- origin: register · owner role: not declared · concept: [gross_sales_amount](concepts/gross_sales_amount.md)
- source: `ontology/concepts/finance/gross_sales_amount.yaml` → `metadata.confidence`

> Is the concept “Gross Sales Amount” (measure) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:net_sales_amount#confidence`

- origin: register · owner role: not declared · concept: [net_sales_amount](concepts/net_sales_amount.md)
- source: `ontology/concepts/finance/net_sales_amount.yaml` → `metadata.confidence`

> Is the concept “Net Sales Amount” (measure) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:order_line#confidence`

- origin: register · owner role: not declared · concept: [order_line](concepts/order_line.md)
- source: `ontology/concepts/order/order_line.yaml` → `metadata.confidence`

> Is the concept “Order Line” (event) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:product#confidence`

- origin: register · owner role: not declared · concept: [product](concepts/product.md)
- source: `ontology/concepts/catalog/product.yaml` → `metadata.confidence`

> Is the concept “Product” (reference) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:product_category#confidence`

- origin: register · owner role: not declared · concept: [product_category](concepts/product_category.md)
- source: `ontology/concepts/catalog/product_category.yaml` → `metadata.confidence`

> Is the concept “Product Category” (grouping) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:product_subcategory#confidence`

- origin: register · owner role: not declared · concept: [product_subcategory](concepts/product_subcategory.md)
- source: `ontology/concepts/catalog/product_subcategory.yaml` → `metadata.confidence`

> Is the concept “Product Subcategory” (grouping) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:store#confidence`

- origin: register · owner role: not declared · concept: [store](concepts/store.md)
- source: `ontology/concepts/store/store.yaml` → `metadata.confidence`

> Is the concept “Store” (reference) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `concept:store_status#confidence`

- origin: register · owner role: not declared · concept: [store_status](concepts/store_status.md)
- source: `ontology/concepts/store/store_status.yaml` → `metadata.confidence`

> Is the concept “Store Status” (enumeration) defined correctly? It is recorded at confidence I (inferred), not confirmed.

### `rule:age_band.as_of.date_travels_with_the_figure#confidence`

- origin: register · owner role: not declared · concept: [age_band](concepts/age_band.md)
- source: `ontology/concepts/customer/age_band.yaml` → `contract.rules[id=age_band.as_of.date_travels_with_the_figure]`

> Is the rule “The band is as-of 2025-12-31 and says so in the answer” on “Age Band” correct? It is recorded as proposed, not confirmed.

### `rule:age_band.precision.single_year_refused#confidence`

- origin: register · owner role: not declared · concept: [age_band](concepts/age_band.md)
- source: `ontology/concepts/customer/age_band.yaml` → `contract.rules[id=age_band.precision.single_year_refused]`

> Is the rule “Single-year age is not served — the answer is a refusal naming the ruling” on “Age Band” correct? It is recorded as proposed, not confirmed.

### `rule:brand.axis.orthogonal_to_category#confidence`

- origin: register · owner role: not declared · concept: [brand](concepts/brand.md)
- source: `ontology/concepts/catalog/brand.yaml` → `contract.rules[id=brand.axis.orthogonal_to_category]`

> Is the rule “Brand and category are two axes — neither rolls up into the other” on “Brand” correct? It is recorded as proposed, not confirmed.

### `rule:calendar_day.extent.latest_comes_from_the_fact#confidence`

- origin: register · owner role: not declared · concept: [calendar_day](concepts/calendar_day.md)
- source: `ontology/concepts/time/calendar_day.yaml` → `contract.rules[id=calendar_day.extent.latest_comes_from_the_fact]`

> Is the rule “The calendar is wider than the data — never take "latest" from this dimension” on “Calendar Day” correct? It is recorded as proposed, not confirmed.

### `rule:calendar_day.working_day.flag_not_quantity#confidence`

- origin: register · owner role: not declared · concept: [calendar_day](concepts/calendar_day.md)
- source: `ontology/concepts/time/calendar_day.yaml` → `contract.rules[id=calendar_day.working_day.flag_not_quantity]`

> Is the rule “WorkingDay is a 0/1 flag — filter or group on it, never sum it” on “Calendar Day” correct? It is recorded as proposed, not confirmed.

### `rule:continent.side.customer_only#confidence`

- origin: register · owner role: not declared · concept: [continent](concepts/continent.md)
- source: `ontology/concepts/geography/continent.yaml` → `contract.rules[id=continent.side.customer_only]`

> Is the rule “There is no store-side continent — the roll-up exists on one side only” on “Continent” correct? It is recorded as proposed, not confirmed.

### `rule:country.roles.customer_or_store_never_both#confidence`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/concepts/geography/country.yaml` → `contract.rules[id=country.roles.customer_or_store_never_both]`

> Is the rule “Country is carried in two roles that do not agree — name the one you mean” on “Country” correct? It is recorded as proposed, not confirmed.

### `rule:country.sentinel.online_is_a_member#confidence`

- origin: register · owner role: not declared · concept: [country](concepts/country.md)
- source: `ontology/concepts/geography/country.yaml` → `contract.rules[id=country.sentinel.online_is_a_member]`

> Is the rule “The '--' store country is a channel, not missing geography” on “Country” correct? It is recorded as proposed, not confirmed.

### `rule:currency.labels.codes_only#confidence`

- origin: register · owner role: not declared · concept: [currency](concepts/currency.md)
- source: `ontology/concepts/finance/currency.yaml` → `contract.rules[id=currency.labels.codes_only]`

> Is the rule “A currency NAME does not resolve here — the delivery holds no names” on “Currency” correct? It is recorded as proposed, not confirmed.

### `rule:customer.geography.rollup_only#confidence`

- origin: register · owner role: not declared · concept: [customer](concepts/customer.md)
- source: `ontology/concepts/customer/customer.yaml` → `contract.rules[id=customer.geography.rollup_only]`

> Is the rule “Geography rolls up — the point location is not served and not derivable” on “Customer” correct? It is recorded as proposed, not confirmed.

### `rule:exchange_rate.direction.usd_base_as_of_order_date#confidence`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/concepts/finance/exchange_rate.yaml` → `contract.rules[id=exchange_rate.direction.usd_base_as_of_order_date]`

> Is the rule “The direction is USD to the order's currency, on the order's day — measured, not inferred” on “Exchange Rate” correct? It is recorded as proposed, not confirmed.

### `rule:exchange_rate.pair.never_half_a_pair#confidence`

- origin: register · owner role: not declared · concept: [exchange_rate](concepts/exchange_rate.md)
- source: `ontology/concepts/finance/exchange_rate.yaml` → `contract.rules[id=exchange_rate.pair.never_half_a_pair]`

> Is the rule “A quote is keyed by an ordered pair and a day — all three, or none” on “Exchange Rate” correct? It is recorded as proposed, not confirmed.

### `rule:geo_area.register.declared_gap_on_the_store_side#confidence`

- origin: register · owner role: not declared · concept: [geo_area](concepts/geo_area.md)
- source: `ontology/concepts/geography/geo_area.yaml` → `contract.rules[id=geo_area.register.declared_gap_on_the_store_side]`

> Is the rule “Three store regions have no register row — say so rather than return nothing” on “Region” correct? It is recorded as proposed, not confirmed.

### `rule:geo_area.sentinel.online_has_no_region#confidence`

- origin: register · owner role: not declared · concept: [geo_area](concepts/geo_area.md)
- source: `ontology/concepts/geography/geo_area.yaml` → `contract.rules[id=geo_area.sentinel.online_has_no_region]`

> Is the rule “Store GeoAreaKey -1 is the online channel, and it is a member” on “Region” correct? It is recorded as proposed, not confirmed.

### `rule:gross_sales_amount.derivation.quantity_times_unit_price#confidence`

- origin: register · owner role: not declared · concept: [gross_sales_amount](concepts/gross_sales_amount.md)
- source: `ontology/concepts/finance/gross_sales_amount.yaml` → `contract.rules[id=gross_sales_amount.derivation.quantity_times_unit_price]`

> Is the rule “Gross is quantity times LIST price, per line, then summed” on “Gross Sales Amount” correct? It is recorded as proposed, not confirmed.

### `rule:gross_sales_amount.evidence.no_line_is_not_a_zero#confidence`

- origin: register · owner role: not declared · concept: [gross_sales_amount](concepts/gross_sales_amount.md)
- source: `ontology/concepts/finance/gross_sales_amount.yaml` → `contract.rules[id=gross_sales_amount.evidence.no_line_is_not_a_zero]`

> Is the rule “A scope with no line has no gross figure — refuse, never report a zero” on “Gross Sales Amount” correct? It is recorded as proposed, not confirmed.

### `rule:net_sales_amount.ambiguity.gross_or_net#confidence`

- origin: register · owner role: not declared · concept: [net_sales_amount](concepts/net_sales_amount.md)
- source: `ontology/concepts/finance/net_sales_amount.yaml` → `contract.rules[id=net_sales_amount.ambiguity.gross_or_net]`

> Is the rule “A bare total is net, and the reading is disclosed rather than silent” on “Net Sales Amount” correct? It is recorded as proposed, not confirmed.

### `rule:net_sales_amount.derivation.quantity_times_net_price#confidence`

- origin: register · owner role: not declared · concept: [net_sales_amount](concepts/net_sales_amount.md)
- source: `ontology/concepts/finance/net_sales_amount.yaml` → `contract.rules[id=net_sales_amount.derivation.quantity_times_net_price]`

> Is the rule “Net is quantity times DISCOUNTED price, per line, then summed” on “Net Sales Amount” correct? It is recorded as proposed, not confirmed.

### `rule:net_sales_amount.evidence.no_line_is_not_a_zero#confidence`

- origin: register · owner role: not declared · concept: [net_sales_amount](concepts/net_sales_amount.md)
- source: `ontology/concepts/finance/net_sales_amount.yaml` → `contract.rules[id=net_sales_amount.evidence.no_line_is_not_a_zero]`

> Is the rule “A scope with no line has no net figure — refuse, never report a zero” on “Net Sales Amount” correct? It is recorded as proposed, not confirmed.

### `rule:order_line.currency.no_bare_cross_currency_sum#confidence`

- origin: register · owner role: not declared · concept: [order_line](concepts/order_line.md)
- source: `ontology/concepts/order/order_line.yaml` → `contract.rules[id=order_line.currency.no_bare_cross_currency_sum]`

> Is the rule “Amounts are store-local — a multi-currency sum needs a stated conversion” on “Order Line” correct? It is recorded as proposed, not confirmed.

### `rule:order_line.grain.no_header_relation#confidence`

- origin: register · owner role: not declared · concept: [order_line](concepts/order_line.md)
- source: `ontology/concepts/order/order_line.yaml` → `contract.rules[id=order_line.grain.no_header_relation]`

> Is the rule “An order-grain figure comes from the line, because no header relation is served” on “Order Line” correct? It is recorded as proposed, not confirmed.

### `rule:product.price.catalogue_is_not_the_sale#confidence`

- origin: register · owner role: not declared · concept: [product](concepts/product.md)
- source: `ontology/concepts/catalog/product.yaml` → `contract.rules[id=product.price.catalogue_is_not_the_sale]`

> Is the rule “The catalogue price is not the sold price — sales figures come from the line” on “Product” correct? It is recorded as proposed, not confirmed.

### `rule:product.weight.unit_and_weight_are_independent#confidence`

- origin: register · owner role: not declared · concept: [product](concepts/product.md)
- source: `ontology/concepts/catalog/product.yaml` → `contract.rules[id=product.weight.unit_and_weight_are_independent]`

> Is the rule “A weight unit does not imply a weight, and neither absence is a zero” on “Product” correct? It is recorded as proposed, not confirmed.

### `rule:product_category.level.category_is_not_subcategory#confidence`

- origin: register · owner role: not declared · concept: [product_category](concepts/product_category.md)
- source: `ontology/concepts/catalog/product_category.yaml` → `contract.rules[id=product_category.level.category_is_not_subcategory]`

> Is the rule “Two levels are both called "category" — resolve to the one asked for and say which” on “Product Category” correct? It is recorded as proposed, not confirmed.

### `rule:product_subcategory.parent.read_the_column_not_the_key#confidence`

- origin: register · owner role: not declared · concept: [product_subcategory](concepts/product_subcategory.md)
- source: `ontology/concepts/catalog/product_subcategory.yaml` → `contract.rules[id=product_subcategory.parent.read_the_column_not_the_key]`

> Is the rule “A subcategory's parent is read from the row, never parsed out of its key” on “Product Subcategory” correct? It is recorded as proposed, not confirmed.

### `rule:store.sentinel.online_is_served#confidence`

- origin: register · owner role: not declared · concept: [store](concepts/store.md)
- source: `ontology/concepts/store/store.yaml` → `contract.rules[id=store.sentinel.online_is_served]`

> Is the rule “The online sentinel is a real member carrying 41.8 % of the fact” on “Store” correct? It is recorded as proposed, not confirmed.

### `rule:store.versions.entity_count_is_the_code#confidence`

- origin: register · owner role: not declared · concept: [store](concepts/store.md)
- source: `ontology/concepts/store/store.yaml` → `contract.rules[id=store.versions.entity_count_is_the_code]`

> Is the rule “Counting stores counts codes, not rows — 67, never 74” on “Store” correct? It is recorded as proposed, not confirmed.

### `rule:store_status.absence.operating_has_no_code#confidence`

- origin: register · owner role: not declared · concept: [store_status](concepts/store_status.md)
- source: `ontology/concepts/store/store_status.yaml` → `contract.rules[id=store_status.absence.operating_has_no_code]`

> Is the rule “"Operating" is an absence here, not a code — read it from the dates” on “Store Status” correct? It is recorded as proposed, not confirmed.

## Findings — 1 (not questions)

- **sme-value-unasked** (low) · `age_band` — 15 value(s) not confirmed and no question recorded

  > Values at confidence I or Q with no `open_question`: 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90.

## Operator items — 0 (not SME questions)

None.
