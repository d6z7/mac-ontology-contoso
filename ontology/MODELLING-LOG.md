# contoso5 — the modelling log

The line of thought behind this ontology, kept as it happened. Operator, 2026-09-29: *"lets try to
build new one and keep the log what your line of thought were."*

**Why a log exists at all.** The first draft was dropped. It passed every gate — schema, grain,
not-per-table, 12 of 12 suite cases against the warehouse — and was still wrong: 6 of 15 classes,
43 edges where far fewer were right, and edges named for their join columns rather than for
anything they meant. Asked what the strategy had been, the honest answer was *none*: read the
schema, make a concept per relation, run gates until green. A method nobody can see cannot be
corrected, so this time the reasoning is written before the YAML is.

**The ruling that shapes this attempt.** *"we have to start building ontology around one central
concept ... concept subject is always originating from the data from the physical layer not from
the structure of the data model."* So the first question is not "what relations are there" but
"what is this data ABOUT" — and the way to answer it is to read rows, not the ER diagram.

---

## Entry 1 — what NOT to do, before doing anything

The first draft's central mistake was structural: it treated the schema as the model. Eight
relations → eight-ish concepts, foreign keys → edges, done. That produces a schema with new
filenames, which `check_concepts_not_per_table` exists to refuse — and it did not refuse the draft
only because two relations happened to back several concepts by accident of the measure-split rule.

The correction is a change of INPUT, not of effort: read the data.

## Entry 2 — reading the rows

Rows, not columns. One of each served relation, then a handful of distributions.

**`v_contoso5_sales_line`, a row:** on 2016-05-18, customer 1293529 at store 430 bought 2 of
product 153 for 751.95 USD. The next line, same order: 8 of product 1621 for 62.35. Then a
different customer at store 410, in GBP, net 681.72 against gross 717.60 — so there was a
discount. Each row is *one product sold to one person, at one place, on one day, for one amount*.

**`dim_customer`:** Jamie Hetherington, Australia, Tasmania, male, born 1946, valid 1983–2033. A
person — and a *version* of a person, because the validity window is on every row.

**`dim_product`:** "Contoso 4G MP3 Player E400 Green" and "... E400 Orange" are two product keys.
The name encodes brand + capacity + type + model + colour, and colour alone makes a new row. So a
"product" here is a SKU — a colour variant — not a model.

**`dim_store`:** "Contoso Store Yukon", CA, opened 2009, closed 2015, 1210 m². Physical shops
named for where they are.

**The shape of the business, from distributions.** Ten years, 2016-05 to 2025-12. Consumer
electronics — Computers alone are 43 % of net revenue. Nine store countries. Five currencies, USD
just over half. Orders are small baskets: one to seven lines, median two.

**And one thing the schema does not say.** `dim_store` has 74 rows. One of them is
`store_key 999999, "Online store", country --, state Online, no floor area`. That single row
carries **93,550 of 223,974 lines and $86.8M of $218.8M — 40 % of revenue** — and customers from
every country buy through it, which is why "do people buy abroad" returns tens of thousands of
US customers at a `--` store. There is no channel column in any landing. The source encoded a
CHANNEL as a fake store, and a model built from the structure inherits the disguise: the first
draft had `Store` with 74 members and never noticed one of them was not a store.

That is the whole argument for reading rows first. The structure says "eight relations, one of
them stores". The data says "this business is two-fifths online and the schema hid it".

## Entry 3 — the central concept

What is this data ABOUT? Every dimension exists to describe one thing: a product being sold.
Customer says to whom, product says what, store says where, date says when, currency and rate say
in what money. None of them means anything on its own here — a customer with no purchases is not
in this data's interest. So the centre is **the sale**.

Not "SalesLine". That is the structure's name for it — a line of an order, a row of a view. What
happens in the world is that somebody buys something; the landing table is already called
`sales`, and each row is one product sold. **`Sale`** is the concept, and the row is its grain.

Two alternatives considered and set aside:

- *The order as the centre.* An order is a basket of one to seven sales. But every measure —
  quantity, the three amounts — sits on the line, and the order carries none of its own. The
  order is a grouping of the atom, not the atom.
- *The customer as the centre.* Tempting because it is the largest dimension. But 104,990 people
  described by where they live and when they were born is a directory, not a business. The
  business is what they bought.

A2 on `Sale`: does it HAPPEN and move through phases? Yes — ordered on one day, delivered on
another. `class: event`.

## Entry 4 — what a Sale needs, in the order the data raised them

Building outward from the centre. Each question is one the rows forced:

1. **Through which channel?** — raised FIRST, before any dimension, because 40 % of sales have no
   physical store and the schema hides that. A `Channel` with two members, online and store,
   resolved from `store.location_code = -1`. Nothing stores it; it must be computed.
2. **What was sold?** — `Product`, a SKU.
3. **To whom?** — `Customer`, a versioned person.
4. **Where, if physically?** — `Store`, and only the 73 that are stores.
5. **When?** — `CalendarDay`, two of them per sale.
6. **In what money?** — `Currency`, and `ExchangeRate` to get the line's USD into it.

Grouped by A2 as I go. The first draft's mistake was answering "what relations exist" instead of
"what does the centre need"; the difference shows immediately at step 1, which the first draft
did not have at all.

## Entry 5 — the first two concepts, and what the gates said

Written: `sale.yaml` (the centre) and `channel.yaml` (the first thing the data raised).

Before writing either, an audit of the dropped draft that changes how the rules are written:
**it invented five rule kinds.** The closed vocabulary is `aggregation, ambiguity, default,
exclusion, guarantee, resolution`; the draft used `disambiguation`, `grain`, `grouping`,
`temporal`, `unit` on 12 of its 21 rules. `validate_schema` let them through because `kind` has no
enum in the schema — only the vocabulary gate sees it, and nothing had run that gate on a concept
file. So `sale.yaml`'s "revenue means net" is `ambiguity`, not `disambiguation`, and every rule id
now carries its kind in its name where a reader will see it: `sale.ambiguity.revenue_means_net…`.

**Gates, over two concepts:**

```
validate_schema              86 of 86 clean
concepts_not_per_table       OK — M:N
concept_columns_exist        every column of 2 concepts exists
grain_declaration            complete
answerability                2 of 2 derive
no_shadow_ontology           clean
datasets_are_grounded        FAIL — 6 of 8 ungrounded
```

The last line is correct and stays red on purpose. It is the denominator for building outward:
two of eight served relations are reached by a concept, and the number should fall to zero as
the centre's needs are answered — not be made green by writing a concept per relation, which is
the draft's mistake with a different justification.

**One tool defect found on the way.** `check_guardrails --propose` refused `sale.yaml` with
INVENTED-COLUMN-ROLE: the enforcer for a *data-plane* refusal matched the *ontology's* column
roles (`key`, `dimension`, `attribute`) against the data plane's closed set. Scoped to `data/`,
proven both ways, committed to the framework. It would have refused every concept ever written.

## Entry 6 — running A2 on what a Sale needs, before writing any of it

The draft chose `entity` six times by reflex. This time each class is decided top-to-bottom on
A2's six lines, and the branch taken is recorded so a wrong answer is visible here rather than in
a graph later.

| concept | A2 branch | class | why that branch and not the one above it |
|---|---|---|---|
| Product | *keyed dimension that facts point at* | **reference** | 2,517 keyed rows with their own columns; a sale points at it. Not entity — "check reference first". |
| Customer | *structured thing with identity, none of the above* | **entity** | A2's own worked example. Facts point at it, but it is a person with a life of its own, not a lookup. |
| Store | *keyed dimension that facts point at* | **reference** | 73 shops a sale points at. The 74th row is the online sentinel and belongs to Channel, not here. |
| CalendarDay | *keyed dimension that facts point at* | **reference** | 4,018 keyed days; every date in the bundle points at it. |
| Currency | *controlled set of coded values* | **enumeration** | five ISO codes, one column, no attributes of its own — "if it's a code list, enumeration". |
| ExchangeRate | *a number you sum/average (has unit)* | **measure** | a rate is a quantity with a unit, aggregated by rule (per-day, never averaged). The draft said `event`; nothing about it moves through phases. |
| Order | *does it HAPPEN and move through phases?* | **event** | placed on a day, delivered on another; a container of sales. Not `grouping` — that branch is for dimensional roll-ups like Category over Product, not for a basket of events. |

Deliberately not yet: the four measures (UnitsSold, NetRevenue, GrossRevenue, SalesCost), and the
lifted dimensions (Brand, ProductCategory, Color — `grouping`, `grouping`, `enumeration`). They
come after the centre's six direct needs are grounded and `datasets_are_grounded` reads 8 of 8.

Two things noted for the data plane rather than solved here:
- Store's `close_date`/`status_annotation`: 59 of 74 rows carry no status. "How many stores"
  has two honest answers and the concept must say so.
- The online sentinel deserves a real column on the served store relation. That is a transform
  change — phase 2, a finding, a person's ruling — and the ontology should not make it from here.

## Entry 7 — the resolve step, and a disagreement with the neighbour

After the seven direct-need concepts, `datasets_are_grounded` fell to 1 of 8 ungrounded (only
`dim_location`, deliberately last) and every gate passed except one: **answerability** said
`Product`, `Store` and `CalendarDay` have no `resolve` step, while `Customer` passes.

The difference is the class A2 gave them. `entity` is not a lookup; `reference` is — "a keyed
dimension that facts point at" — and a lookup has to say how a WORD reaches its KEY. The draft
hid this by calling all four `entity`. A2 was right and the gate is right; the mechanism, read
from `check_answerability.resolvers`: a reference concept's resolve step is supplied by a
register it cites, by a `values` block, or — derived, not listed — by another reference/enumeration
concept whose canonical key is one of its grounding columns.

Per concept, honestly:

- **Store** — 67 store names were cut into `contoso5_store_name.lookup.csv`. "Contoso Store
  Yukon" resolves through it. Cited. True.
- **CalendarDay** — a date is self-resolving under ISO, and the gate has no notion of that (it
  models exactly one resolve mechanism: a register; its own mutant is "take the register away").
  But a question does not say "2016-01-15"; it says "January 2016" or "Q1 2016", and THOSE resolved
  through `contoso5_year_month` and `contoso5_year_quarter`. Cited. Also true at the time —
  **and OVERTURNED on 2026-09-30.** It was the right observation with the wrong conclusion: the
  question's words do need reading, but a register reads them by MATCHING A NAME, and a day is not a
  name. Both halves of that cost were then measured. The lookups: eight registers on this one
  concept, 350 rows — `year_month` and its short form 132 each, `year_quarter` 44, the month names
  12 and 12, the weekdays 7 and 7, the quarters 4 — re-cut every delivery for facts the Gregorian
  calendar states. The answers: asked "which stores closed after 2020" the resolver matched the term
  `close_date` to the register value `Closed` at ratio 0.75, reported it RESOLVED, and then refused
  the date as "no known Store matches the value '2020-12-31'"; one more resolving rung and a question
  about dates is answered by filtering on status. Operator: *"the mechanism for days should be
  default built in and NOT rely in any moment on lookups"*, then *"remove time related lookups
  datasets"*. The eight registers are deleted, the words and shapes are declared once in the
  framework (`mac_vocabulary.yaml#calendar_vocabulary`) and read by the runtime's built-in calendar,
  and the cutter now REFUSES to make them again
  (`guardrails/data/sources.yaml#TEMPORAL-AS-LOOKUP`). This concept declares its columns; the
  calendar reads the words.
- **Product** — no register exists and none can: 2,517 SKU names, refused at cut time and marked
  `searchable: like`. The gate is right that a SKU's name does not resolve offline. It never needs
  to: nobody asks for "Contoso 4G MP3 Player E400 Green" — they ask for green MP3 players, or
  Contoso audio. **A product is reached through its attributes.** So Product cites nothing, and
  its resolve step must become derivable the moment Brand, Colour and Category exist as concepts
  with registers. That is a prediction, tested below.

**Lifting the attributes, and where I part from the leaner bundle.** Brand, ProductCategory and
Color become concepts. A2 run top to bottom — event? no; measure? no; *a controlled set of
allowed coded values?* yes — gives **`enumeration`** for all three, and A2 says take the first
branch that fits. The neighbouring bundle calls Brand and Category `grouping`, and A2 does list
"Category over Product" under that branch — but `grouping` comes AFTER `enumeration` in the
order, and A2's own tie-breaker ("a small fixed code set with no attributes of its own →
enumeration") decides it. Recorded, not copied. It also has a practical consequence: `resolvers()`
only registers reference/enumeration concepts, so as enumerations they can supply Product's
resolve step; as groupings they could not.

**Two data-plane findings the lifting surfaced**, noted for phase 2 rather than fixed here:
- `color` has seventeen members and one is `blue` beside `Blue`. One colour stored two ways.
  Kept as a member because the register is what the warehouse holds; folding it is a ruling.
- `Location` row -1 is the online sentinel mirrored from the store table; excluded by rule, as
  on Store.

## Entry 8 — the prediction failed, and what that was worth

Entry 7 predicted that Product's resolve step would become derivable the moment Brand, Colour and
Category existed as concepts with registers. Written, gated: `datasets_are_grounded` 8 of 8, every
other gate green — and Product still read *"no declaration supplies the `resolve` step"*.

**Wrong about the wiring, not the idea.** In-process: `resolvers(Product)` returned exactly Brand,
ProductCategory and Color, each with its register. The gate computed the path and then never
credited it — `resolvers()` fed the guarantee's prose and nothing else. The `resolve` step for a
`reference` knew three mechanisms only: a register cited in the file, a register on the
descriptor's canonical column, a `values` block.

That is a real tension inside the framework, and the log is where it gets said: A2 names Product
as THE example of `reference`, and this gate made a large surrogate-keyed dimension unable to ever
be one. One of them had to give. The gate did — a reference now resolves through the concepts it
grounds when nothing more direct exists — and the change is held by a mutant: a reference whose
only resolving attribute is demoted to `entity` must read None again. Proven, committed.

**A latent defect the patch tripped.** The script's entry point sat mid-file, above the definition
it now needed; an import never sees that, a script run does. Every fixture and mutant crashed
with a NameError the harness could only call "rejection unattributed". Moved to the end. Worth
recording because the shape recurs: a proof that passes in one execution mode and not another is
telling you about the mode, not the proof.

Result: **13 of 13 concepts derive every answer-path step**, and Product does so the way a
product is actually found — by what it is, not what it is called.

## Entry 9 — the measures

Entry 6 deferred them until the centre's direct needs were grounded; they are. Four concepts,
because `semantics.unit` is singular and a Sale has four things worth summing. A2: *a number you
sum, with a unit* → `measure`, all four. Each grounds the sale relation and is sliced by the same
six dimensions Sale is — so "revenue by brand" is NetRevenue → Product → Brand, one hop each.

| concept | column | type | why not the others |
|---|---|---|---|
| UnitsSold | quantity | flow, units | not a count of sales — most lines carry more than one |
| NetRevenue | net_amount | flow, USD | the default reading of "revenue": after discount |
| GrossRevenue | gross_amount | flow, USD | before discount; exists so the discount can be measured |
| SalesCost | cost_amount | flow, USD | margin is not stored; it is net minus this, at query grain |

The per-unit prices stay on Sale as attributes. They are `intensive` — meaningful as an average,
never a total — and a measure concept over one of them would invite exactly the sum that rule
`sale.aggregation.amounts_not_prices` forbids.

## Entry 10 — the edges, decided before they are written

The draft had 43 edges named `SalesLine__product_key__to__Product` — the join column, restated.
The guardrail now rules an edge id is `{subject}__{verb}__{object}` and that ONE-RELATIONSHIP is
ONE-EDGE. So the questions are: what are the relationships, who owns each, and what is the verb.

**The verbs come from the row's own story.** "Customer 1293529 bought 2 of product 153 at store
430 on 2016-05-18, delivered the same day, in USD." Read out loud, that sentence IS the edge list:

| edge | why this verb |
|---|---|
| `sale__bought_by__customer` | the row says who bought |
| `sale__of__product` | what was bought |
| `sale__at__store` | where — and for the online row, Store's own rule excludes it |
| `sale__ordered_on__calendar_day` / `sale__delivered_on__calendar_day` | two dates, two edges, same target — a sale has both |
| `sale__paid_in__currency` | the customer's money |
| `sale__through__channel` | the first thing the data raised; computed, so a business edge |
| `sale__converts_at__exchange_rate` | the one many:many, declared as what it is |

**Sale owns the dimension edges, and Order owns exactly one.** Order grounds the same relation
and the same columns — customer, store, dates, currency — and ONE-RELATIONSHIP-ONE-EDGE says two
concepts sharing a relation and a target through the same column are one relationship seen
twice. So `order__comprises__sale` is Order's only edge: everything an order has, it has through
its sales. The draft emitted five Order edges duplicating Sale's; they were the same five facts.

**The measures declare no edges at all.** UnitsSold, NetRevenue, GrossRevenue and SalesCost ground
the sale relation with `product_key`, `store_key`, `customer_key` as reference keys; that grounding
is how they reach a dimension. The draft's 24 measure edges were the cartesian product the refusal
names. If a planner needs them spelled out, the suite or a question will say so — that is a test
to run, not an edge to pre-emptively write.

**Product owns three business edges to the concepts lifted from its columns** —
`product__sold_under__brand`, `product__belongs_to__product_category`, `product__comes_in__color`
— each `shared_attribute`, each anchored by a resolution rule on the target, because a business
edge without one is an unexplained claim. Store owns `store__sited_in__location`. ExchangeRate owns
its three: `exchange_rate__quoted_on__calendar_day`, `__quotes_from__currency`,
`__quotes_to__currency`.

**Sixteen edges.** Ten physical, with the cardinality READ from `data/references_served`
including participation — `1..N` on a from-end means the measurement found every parent has at
least one child; the draft's neighbour writes `0..N` on both ends of everything, which is the
unmeasured default. Six business. `verified_by` is added after they are measured, not before.

## Entry 11 — what the measurer said about the edges

Sixteen declared, fourteen measured on the first pass, every measured predicate resolving at
100% with fanout 1 — the cardinalities read from the data plane hold. Two could not be measured,
and each said something worth keeping:

- **`sale__converts_at__exchange_rate`** — *"binds 2 columns … the shared column cannot be
  derived unless exactly one is."* Expected: the rate's key is a triple, the relation is
  many:many on any one column, and the edge says so in its own note. Unprovable by this tool,
  declared as what it is.
- **`order__comprises__sale`** — *"cardinality '1..N' constrains nothing — a shared column value
  cannot contradict it."* Entry 10 said Order owns exactly one edge, and I wrote it from Order's
  side. The measurer is right that "an order comprises 1..N sales" is a claim nothing can
  falsify. The same fact from the sale's side — `sale__belongs_to__order`, to-end `'1'` — CAN be:
  fanout from a sale to its order is either 1 or the claim is wrong. Flipped. Order still has one
  edge; it is stated so it can be measured, which is the whole point of stating it.

One mechanical defect too: a bare `1` in YAML is an integer, the schema wants the string `'1'`,
and my helper quoted only the to-end. Fixed for both ends. Fifteen measurable, one declared
unmeasurable with its reason.

## Entry 12 — a correction: the standard already rules the edge count, and I ruled against it

Asked whether I had observed the vocabulary and grammar rules in mac, I checked, and the answer
about edges was no. CONFORMANCE §2.3, "AN EDGE IS A PROPERTY OF THE CONCEPT, NOT OF A FOREIGN
KEY", has been in the estate since before contoso5 existed:

> *"One foreign key fans out to many edges. Where OrderLine, Order and SalesAmount all declare
> `CustomerKey: identity: reference`, all three reference Customer and all three are edges.
> Refusing that as 'ambiguous' took a reference bundle from 3 wrong edges to 0."*

Entry 10 refused exactly that. "Sale owns the dimension edges; the measures reach through their
grounding; Order owns one" was my rule, and this morning I wrote it into the guardrail as
`ONE-RELATIONSHIP-ONE-EDGE` — from the dropped draft's symptom (43 edges that looked like a
cartesian product) without reading the standard that decides it. The draft's defects were the
column-named ids and the self-join predicates. Its count was closer to right than my 16.

§2.3 also names the case I did get right: *"a shared relation carries no foreign key at all. An
inline dimension — Brand on the product row, Location on the store row — relates to its host
with nothing to lift, which is why a reference bundle with 19 concepts carried 8 edges and owed
12 more."* Those six business edges stand.

**So the edge set is derived, as §2.3 prescribes:** from every `identity: reference` a concept
declares, to the one concept whose canonical key is that column. Order owes five (customer,
store, both dates, currency). Each measure owes six. The verbs stay the row's story — an order is
`placed_by` a customer, a measure is `by` a dimension because that is what a question says:
"revenue by brand". Forty-five edges, of which twenty-nine are the fan-out §2.3 describes. The
guardrail refusal is rewritten to what the standard says — `ENDPOINT-GUESSED` — and records what
it replaced.

Two things I take from this beyond the edges. The guardrail tree can carry a wrong rule as easily
as a right one, and it will be enforced either way; a rule written from a symptom needs the
standard read first. And the operator's question was the check — the same shape as this
morning's cookbook.

## Entry 13 — where the second attempt stands

**17 concepts, 45 edges, one log.** I wrote "every gate green" here, and it was false: I had read the last two lines of `check_rule_reference_basis` and missed 24 witnesses above them. Entry 14 records what they were and what reading the standard properly then changed. The numbers below stood at the time for the gates I had actually read:

```
validate_schema              103 of 103 clean
concepts_not_per_table       OK — M:N (dim_product backs 4, v_contoso5_sales_line backs 7)
datasets_are_grounded        8 of 8
answerability                17 of 17 derive — Product through Brand, Colour, Category
ontology suite               13 of 13 against the warehouse; 4 computed concepts skipped by name
edge_definition              90 of 90 endpoints
er_projection                45 of 45 realized and grounded
edge_joins_measured          39 of 39 predicates
edge_claims_proved           44 of 45 — the fx conversion is many:many by construction
edges.json                   measured 44 · total 45 · unproved 1
```

**What is different from the dropped draft, and why it is not taste.** The centre was found by
reading rows and everything else was built outward from what it needs. Every class was decided on
A2 and the branch is logged. Every rule kind is one of the closed six. Every edge id is a verb
from the row's own story, and every physical cardinality was read from the measured references
with participation kept. Channel exists because the data raised it and the schema hid it.

**What I got wrong along the way, kept here because the log is for that:** a prediction about
how Product would resolve (entry 8 — right idea, wrong wiring, and a latent entry-point defect in
the gate); an unfalsifiable edge direction the measurer refused (entry 11); and a guardrail rule I
wrote this morning that contradicted CONFORMANCE §2.3, caught by the operator's question and
replaced (entry 12). Four framework fixes came out of this attempt, each held by a mutant.

**What remains provisional, stated so nobody has to discover it:**
- three served shapes are `driven_by: proposed` against unruled findings (DQ-DUP-ORDERROWS-SALES,
  DQ-DANGLINGKEY-CATEGORYKEY, DQ-STORE-TWO-GRAINS); Sale, Product and ProductCategory rest on them
- every rule is `confidence: P` — a provisional reading, none ratified by a person
- `Color` carries `blue` beside `Blue`; `Channel` deserves a real column on the served store
  relation; both are phase-2 findings, noted, not fixed from here
- the `resolved_axis` identity kind exists in the parser's message and not in the vocabulary — a
  framework discrepancy, recorded, not a bundle's to settle

**What has not been done:** no business question has been asked of it. The suite proves keys and
grain; it does not ask "revenue by brand" and check the number. That is the next rung, and it is
the one that will show which of the seven open findings actually matter.

## Entry 14 — the standard I had not read, and what it changed

Operator: *"did you also observe new rules in mac about vocabulary and grammar for ontology?"* —
then, when I moved on without answering: *"you did not answer my question"*, and *"in mac
standards"*.

**The honest answer was no.** The closed vocabularies I had taken from `mac.schema.json`; the
grammar lives in `mac_rules.yaml#mac.authoring.reference_markup` and in
`reference_manual/column_specification.md`, `column_rulings.md`, `identity_and_rules.md`, and I had
opened none of them. Three consequences, each found by being caught rather than by reading:

1. **Reference markup.** A column or relation named in a rule's `when/then/never` is written
   `` `{name}` ``, and `binds:` must agree both ways. 24 witnesses in 11 of 17 files — after I had
   written "every gate green" in entry 13. Fixed: braced where the identifier resolves in the
   concept's own scope, said in English where it does not (the rule forbids marking a token that
   resolves to nothing), `store_key` added to Channel's binds.
2. **`role: attribute` does not exist.** 20 of my columns carried it. Where it came from, exactly:
   the schema's enum still listed it — closed on 2026-09-27 *from contoso4's 142 declarations
   (attribute 45)* so that bundle would stay valid; `sdk/authoring/authoring.py` showed
   `Surname: {role: attribute}` as its example; contoso4 next door uses it 44 times;
   `validate_schema` accepted all 20; `check_vocabulary_parity` had reported the disagreement since
   09-27 inside the framework gate run and nobody stopped. Operator ruling: it is deprecated; the
   vocabulary's five terms win. Schema enum, authoring example and guidance corrected; contoso4's
   44 become invalid, which is the honest consequence (operator: *"attribute does not exist
   anymore"*).
3. **Rulings are grammar, not prose.** The column standard has `rulings: {label_of, finer_than,
   scoped_by, never_axis}`; I had written several of them as rules. Measured before ruled, on the
   served plane, read-only:

   | ruling | holds | fails |
   |---|---|---|
   | `label_of` (distinct = distinct = pairs) | manufacturer→brand (11/11/11), product_name→product_key, product_code→product_key (2,517), country_name→country_code (9) | store_name→store_key (67 names, 74 keys), customer_name→customer_key (99,200 / 104,990) |
   | `finer_than` (pairs = distinct finer) | sub_category→category (32), year_month→year_quarter (132), year_quarter→year (44), year_month→month_name (132), country→continent (8), state→country_code on location (67) | customer state→country (610 pairs over 565 states — a child with two parents) |
   | `scoped_by` (reused across, none within) | customer state: 40 of 565 codes carried by more than one country; the within-test needs a state name the served row does not carry — declared on the across half, said here | — |
   | `never_axis: privacy` | customer_name 94,488 of 99,200 values held by one row; city 21,317 of 34,581 | birth_date 1,476 of 24,147; state 16 of 565 |

   Declared on the owning concept only (one home): Product, ProductCategory, CalendarDay, Customer,
   Location. `never_axis` needed evidence the register could not give — the profiler did not measure
   "held by exactly one row" — so the chain was built rather than the result copied: `mac_profile.py/6`
   measures it in one GROUPING SETS scan for near-unique non-key columns, `mac_dq_findings.py` raises
   `DQ-IDENTIFYING-<relation>-<column>` (a column 1:1 with the row is excluded — that is a name for
   the key, the `label_of` constellation), and Customer cites the two ids. Operator: *"must have"*.

**What else the standard changed.** Sale's seven amounts moved to the four measure concepts as
compositions (`net_amount` with `net_price`, and so on; `semantics.unit: USD` — the schema's own
`Quantity x NetPrice` example); `order_date` is `period` on Sale, Order and the measures, and the
ordered-or-delivered ambiguity became `sale.default.period_is_order_date`, consistent with the
`axis_kinds` I had already declared; `weight` left Product — three units and a blank in one column
is a transform's job, not a concept's; `valid_from`/`valid_to`/`date_key` are `housekeeping`;
every rule's `never` is the prohibition and its `why` the reason (23 split); "not served" was a
retired term. Product carries `list_price`/`list_cost` as `intensive` USD measures.

**What the run of all 78 framework gates then said.** 48 green. Mine, fixed: reference markup,
retired term, a `note` key on a vocabulary block. Not mine, recorded: `rule_coverage` 0 of 27 (no
question corpus exists yet), `vacuous_assertions` (generated sanity lineage), the artifact
registry's 27 kinds with no declared shape, `has_producer`, `seam_contract`, `protocol`; the parity
gate's last slot (`TableFile.columns.role`: audit/delivery_axis/unknown) is a human's call.
Channel fails KEY-BACKED and MEMBER-GRAIN because it is computed over its host's rows — the
phase-2 transform its definition already owes. The public-token gate found "2005 Volkswagen
Sharan" in the customer source sample (2,991 of 104,990 source rows carry the make); operator:
*known, accepted — the name of the product*; the rule was narrowed to exclude a model year before
the make, with a witness, so the gate's self-test now holds that decision (67 rules proven).

**The one that blocks.** The platform's runtime refuses `rulings` on a column ("TODAY'S FLAGS ARE
role, identity, measure") and refuses two measure columns — both admitted by mac on 09-27/28 and
never taught to the reader. A bundle on the column standard cannot load there; six gates that use
that loader could not run. The change (typed `rulings` with two readers — `label_of` as the display
column, `never_axis` and `housekeeping` as refusals where `attribute` is refused today; several
measure columns when the concept states the composed unit) was read to the point of writing and is
owed; nothing in the platform was changed. Runtime baseline: 958 passed.

## Entry 15 — the KPI specification, and the average that was never an average

**The operator specified the sales measures, 2026-09-30.** Four base columns — Quantity, UnitPrice,
NetPrice, UnitCost — and eight derived measures: gross sales, revenue, discount amount, discount %,
COGS, margin, margin %, markup %. Three amounts were already served (`gross_amount`, `net_amount`,
`cost_amount`). Two were not, and were added to the sales-line transform as `discount_amount`
(Quantity × (UnitPrice − NetPrice)) and `margin_amount` (Quantity × (NetPrice − UnitCost)). Both
identities hold to the cent against the base columns: 13,787,071.00 and 122,332,211.24.

**The three percentages are not columns and must not be.** A per-row ratio cannot be folded back to
the right figure, so they are ratios of sums taken at aggregate time through `Intent.denominator`.
The interpreter chose the denominators unprompted — gross for discount, revenue for margin, cost for
markup — and the two new concepts declare them, because discount over net gives 6.30 % where over
gross it gives 5.93 %, and markup and margin differ by more than a factor of two on one profit.

**The average price dissolved a framework limit instead of needing one.** "Average price" had
answered 976.96, the mean value of a sale LINE, because a flow concept folds only its flow column and
the per-unit column is unreachable from it. A runtime change was drafted and proposed. It was not
needed: the operator ruled the average is what the customer paid per article, which is total paid over
total articles — a ratio of two existing measures, 218,814,471.66 / 703,621 = 310.98. Revenue over
UnitsSold. Declared as a default on NetRevenue; no new column, no new concept, no runtime change. The
unweighted mean of `net_price` (309.87) answers a different question and the rule now forbids it.

**Two findings recorded, not worked around.** `check_rule_reference_basis` warns that the new rule
names UnitsSold with "no edge, units differ (usd vs units), no shared surface term" — but a per-unit
price is exactly a ratio across units, and `mac.aggregate.unit_algebra` sanctions unit(a)/unit(b). The
checker treats differing units as evidence of an unmodelled relationship; for a ratio it is evidence
of a correct one. Second: three concepts invented earlier this session to route around framework
limits (StoreClosure, Discount-as-workaround, NetUnitPrice) were withdrawn on the operator's ruling
that a framework limit is to be reported, never modelled around. "How many stores have closed" stays
unanswerable, by decision: the grammar's `not_expressible.null_test` already names that question as
its own example.

## Entry 16 — Sale deleted: a line is not an event

**The operator saw it in the columns and I argued the wrong side twice.** Order's six columns are a
strict subset of Sale's eight. I defended both concepts on the grounds that they carry different
counts, 93,470 orders against 223,974 sales, and that deleting either loses one. That defended a
number, not a meaning.

**The rows settle it.** An event needs a when, a who and a where. Measured across all 93,470 orders,
the number that differ across their own lines is ZERO for `order_date`, `delivery_date`,
`customer_key`, `store_key` and `currency_code`. Only product, quantity and price vary — 61,042,
55,704 and 61,045 orders respectively. So a line owns nothing that makes it an occurrence. It borrows
the when, the who and the where from the order and adds which product and how many. The ontology had
already written the fact down, in `order.resolution.by_grouping_sales`: "the header attributes are
constant within each". Nobody drew the implication.

**So Sale was the Order repeated once per product with the header copied onto every copy.** Its 223,974
is not a business quantity; it is how the storage holds 93,470 purchases. The three real volume
questions already had homes: purchases 93,470 (Order), items 703,621 (UnitsSold), rows 223,974 (none,
and that is correct). The line grain was never homeless either — all six measures are keyed on
`order_key` + `line_number` and ARE the line.

**What moved.** Sale's `contract.default_reading` and its three rules went to Order, renamed:
`rate_on_order_date`, `period_is_order_date`, `an_unscoped_question_covers_all_time` — the last being
the operator's all-time ruling, which would have been lost with the file. Of Sale's nine edges, seven
were duplicates already reached by Order or the measures; `sale__through__channel` and
`sale__converts_at__exchange_rate` were the only inbound edges Channel and ExchangeRate had, and both
are order-level facts (the channel derives from the store, the rate from the order date and currency,
all constant within an order), so they moved to Order. 60 edges became 53.

**One gate earned its place.** `check_references` refused the bundle: the moved exchange-rate edge's
`resolved_by` still pointed at `sale.yaml#contract.rules.sale.resolution.rate_on_order_date`, an
address that no longer existed. A rename leaving a consumer on a dead pointer is the estate's recorded
failure mode and this is the first time a gate caught it in the act.

**Verified after.** 19 concepts, 53 edges, compiles clean, 24 of 24 checkers pass. "Revenue" 218,814,471.66
all periods; "how many orders" 93,470; "revenue in 2024" 31,639,690.92 bound to `order_date`; "average
order value" 2,341.0129 as revenue over Order. Each figure re-derived against the warehouse and equal.


## Entry 17 — Product keeps identity, sales keep price

**Operator ruling, 2026-10-26:** Product serves no price and no cost. `main.product` does carry
`Price` and `Cost`, and they do match the source; they are withheld deliberately, not absent. The
served question space reads dated sales-line factors (`unit_price`, `net_price`, `unit_cost`) and
derived amounts (`gross_amount`, `net_amount`, `cost_amount`, `margin_amount`, `discount_amount`).

**Why this was ruled:** a product-level standing price is undated and misleads historical reads.
Measured before 2024, line price differs from list on 122,953 of 223,974 lines (55%). From 2024
onward the price factor is 1.0, so the line price equals the source list level for current sales.

**What moved:** `list_price` / `list_cost` were removed from `dim_product` (SQL, dataset,
relation, concept binding). Their naming surfaces moved to `unit_price` / `unit_cost` on the sales
line. The Product price-resolution rule over catalogue columns was retired and recorded in
`tombstones` with its replacement reading: latest line unit price, date-carried.

## Entry 18 — the measures fold into Order: one fact node per grain (ontology 1.1)

**Operator ruling, 2026-10-26:** "i rule to move it in", and "make it version of ontology 1.1".
Every concept file now carries `metadata.version: '1.1'`; the MAC stamp stays `0.3.0-develop`.

**What was wrong.** Six measure concepts — NetRevenue, GrossRevenue, SalesCost, Margin, Discount,
UnitsSold — each served one column of `v_contoso5_sales_line`, at the grain Order already reads,
and each declared the line's foreign keys. CONFORMANCE §2.3 (entry 12) derives an edge from every
such declaration, so every join existed once per measure: 45 edges over 15 distinct joins. The
cost was measured on 2026-10-25: the territory default named ONE copy of the attribution edge, so
it reached revenue questions and not margin, cost, discount or units questions.

**What moved.** The six concepts are gone and their columns are served by Order, which is now the
fact node: 11 concepts, 15 edges. §2.3 is unchanged and still obeyed — one concept declares each
key, so it derives one edge per key. The three ratio rules moved to Order with their ids unchanged;
their denominators are now the columns the retired concepts measured (`quantity`,
`gross_amount`, `net_amount`, `cost_amount`). NetRevenue's 2026-09-30 price reading moved onto
`net_amount`'s description. `country.yaml`'s territory reading now names
`order__attributed_to__country`. Every retired concept and edge is tombstoned with its successor.

**How.** An experimental copy built for the measurement (`arm/`, by another agent) was NOT copied
in: it had been written through a YAML round-trip that stripped every comment, including recorded
rulings, and it dropped NetRevenue's `default_reading`. The fold was re-applied to the live files
as text edits instead, merging the surface work landed earlier the same day.

## Entry 19 — `dim_store.location_code` renamed to `store_code` (mechanical, no semantic change)

**Operator order, 2026-10-26:** rename `dim_store.location_code` to `store_code` and propagate to
ontology and approved references.

**What changed.** The served alias in `data/transforms/dim_store.sql` is now `store_code`; every
ontology declaration that served or bound that column was rewritten to the new name; the
`store__sited_in__location` edge now joins `dim_store.store_code = dim_location.location_code`.
`dim_location` keeps `location_code` as its own key.

**What did NOT change.** Meaning, values and predicates. The column is still cut from
`main.store.StoreCode`; `store_code = -1` is still the online sentinel; Store's channel rule and the
24 approved reference SQLs were rewritten mechanically and re-run to the same expected values.

**Governance move.** `contoso5:column/dim_store.location_code` is tombstoned with successor
`contoso5:column/dim_store.store_code`, and retired-forms now refuses new authored uses of the old
name on `dim_store`.


## Entry 19 — the pricing rulebook, and one home for every price and cost word

**Operator ruling, 2026-10-26 (the "rulebook"), confirmed 2026-10-28 as the valid one.** The four
source fields carry everything: `UnitPrice` = the regular/list price per unit, `NetPrice` = the
actual selling price per unit after discount, `UnitCost` = the cost per unit, `Quantity` = units.
The amounts derive from them: gross = quantity × unit_price, net = quantity × net_price,
cost = quantity × unit_cost, discount = quantity × (unit_price − net_price), margin = net − cost,
and gross − discount = net, net − cost = margin. Measured on all 223,974 lines: 0 violations.

**And, 2026-10-28: "from the shop perspective cost is procurement cost. The rest is revenue or
income."** So `cost` names only what the goods cost Contoso to buy.

**What moved, word by word:**
- `unit price` left the price ratio and joined `unit_price`: under the rulebook it is the
  REGULAR price, not what was paid.
- `price`, `average price`, `price per unit`, `price per article` stay on the ratio
  revenue ÷ units (310.98, the 2026-09-30 reading). That is the quantity-weighted average of the
  actual selling price, which the rulebook names `NetPrice`, so the two rulings agree.
- `net_price` gained `selling price`, `actual price` and `price paid`, and lost `what one costs`:
  "cost" is procurement only.
- `cost_amount` gained the bare `cost`, `procurement cost`, `purchase cost` and `cost of sales`;
  `unit_cost` gained `procurement cost per unit`.
- `net_amount` gained `income`.
