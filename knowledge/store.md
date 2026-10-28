# Store

> The human account. The declaration is `ontology/concepts/store.yaml`; read this first, whole,
> then compare it against that file. Every ruling below is dated and every figure measured.

## What a store is

A shop Contoso sells from: 73 of them, each with a name, a country, a state, an opening date and a
floor area. Read from the rows: "Contoso Store Yukon", CA, opened 2009, closed 2015, 1210 m². A2:
a keyed dimension that facts point at → `reference`. 73, NOT 74. The relation has 74 rows and one
of them — store_key 999999, "Online store", country `--`, no floor — is not a shop. It is the
online channel written as a store, and it carries 40% of revenue. It is held out of every count
and every geography by the `physical` population declared below — the default — and a question
reaches it by naming `online`. A `Channel` concept carried this fact until 2026-10-01 and was
removed: it grounded on this same relation, its two members existed only as prose, and the
predicate belongs where the column is. A STORE IS A SHOP YOU CAN WALK INTO — 57 of them, and this
is an OPERATOR RULING of 2026-09-30 that settles what was carried as an open ambiguity until then:
"stores that are closed, restructured have close date and are not active anymore; other stores
without status do not have close date are ONLY stores currently active and this is the scope of
our interest in most questions." SO THE POPULATIONS ARE DECLARED, NOT DESCRIBED, and there are TWO
ORTHOGONAL SETS of them — one per state this relation's rows carry. How the store is TRADING
(`active` by default, or `ended`, `closed`, `restructured`) is stated by `close_date` and
`status_annotation`; which CHANNEL it is (`physical` by default, or `online`) is stated by
`store_code`. Each is a contract rule with an executable body, each names a default, and the
runtime discloses on every answer which it applied and which the question displaced. NEITHER IS A
`value_filter`, and this concept no longer declares one. That slot held `close_date IS NULL AND
store_code <> -1` until 2026-10-01 and applied it inviolably, which made "how many stores are
closed?" answer 0 — the question's own `status_annotation = 'Closed'` ANDed with `close_date IS
NULL` can never be true. A predicate a question may legitimately ask the other side of is a
DEFAULT READING, not a domain, and both of these are: 16 rows ended, and the one `store_code =
-1` row carries 86 790 054.13 of revenue. THE CLOSE DATE AND THE STATUS NOW AGREE, and until
2026-10-01 they did not. Contoso Store Utah (location 63) carried a close date of 2019-11-03 and
an EMPTY status, so counting by status said it was open while the date said it shut — the whole of
the 58-versus-59 disagreement the corpus records between "how many are still open" and "how many
are not closed". The operator ruled that impurity fixed in the transform, and it was filled
DERIVABLY rather than by hand: a restructured location always has a later row at the same code (6
of 6) and a closed one never does (0 of 8), and Utah has no successor, so it is Closed. Every one
of the 16 rows with a close date now carries Closed or Restructured, 9 and 7. SO THE TWO TESTS ARE
NOW EQUIVALENT, and the close date remains the one this concept uses because it is the simpler of
two statements of one fact: `close_date IS NOT NULL` selects exactly the rows `status IN
('Closed','Restructured')` selects. The status says WHY a store ended; the date says THAT it did.
WHAT ENDED IS A DIFFERENT NOTION. 16 rows carry a close date: 9 labelled Closed and 7 Restructured
(the store was rebuilt and a successor row exists at the same location — New Brunswick went 1 105
to 1 500 to 3 500 m²). Those are store CLOSURES and they are still answerable from this concept's
own columns — `close_date` says which rows ended and when, and `status_annotation` says why — and
they are reached by NAMING the population they belong to (`ended`, `closed`, `restructured`). They
are not what "a store" means unqualified, which is why `active` is the declared default rather
than the only reading. NAMES RESOLVE THROUGH `data/lookups/contoso5_store_name.lookup.yaml` — the
67 store names, cut from the landing's Description column and attached to store_name here.

## How identity is established

The canonical key is a COLUMN fact and is not repeated here; this says only HOW identity is
established. A surrogate `store_key` annotated by `store_name` — 67 distinct names over 74 rows,
so the name is not the key. A STORE IS ITS CODE; A ROW IS A TRADING PERIOD. `dim_store` is served
one row per `store_key`, and 74 keys stand over 67 codes: seven codes carry two or three rows each
— the same name, one row closed `Restructured` and the next opened months later (StoreCode 7,
"Contoso Store New Brunswick": keys 70, 72, 74; 2007-2014, 2015-2018, 2018-open). Those are one
shop restructured, not three shops. So `store_key` stays the canonical key — it is what `sales`
joins on, and every revenue figure belongs to the period that earned it — and `counts_as` names
the column one STORE is counted by (mac.schema.json#ConceptFile.concept.identity.counts_as — a
schema slot the vocabulary and the manual do not yet describe): COUNT(DISTINCT store_code) =
67, where COUNT(DISTINCT store_key) = 74 counted periods and called them stores (RC05,
2026-09-29). The approved answer is 67. THE COLUMN IS StoreCode UNDER THIS BUNDLE'S NAME. contoso5
served `StoreCode` as `store_code`, the FK to dim_location, reading the code as a SITE; the
rows say it is the store's own identity across restructurings. Serving it a second time as
`store_code` is a data-plane change for a person to rule on; until then the count is declared on
the column that carries the code.

## What the rows are, and why nothing is collapsed

ONE ROW PER STORE ALREADY, once the `active` population has selected the trading ones: 57 rows
over 57 location codes, because a location has at most one store with no close date. The relation
holds 74 rows over 67 codes because it also records ENDED stores — 7 of them restructured into a
successor at the same location — and the online sentinel. Those rows are selected out by the two
declared default populations rather than removed from the relation, and a question that names
`ended`, `closed`, `restructured` or `online` reaches them. SO NOTHING IS COLLAPSED HERE, and that
is a correction of 2026-09-30. This slot previously read "a store named without a date means its
LATEST period — the row with no close_date, else the latest open_date, per store_code", and a
collapse was written to realise it. The else-clause is what made it wrong: it represents a
location whose store has SHUT by that shut store, so an average over stores included nine shops
that no longer exist (1 504,55 m² against the 57 active ones' own figure). A collapse that keeps a
closed row is not a reading of "a store". A count of stores is a count of the active rows;
`identity.counts_as: store_code` still names what one store is, and over the filtered
population the two agree by construction.

## Why there is no `value_filter`, and two axes instead

THE PREDICATE THAT SELECTS THIS CONCEPT'S ROWS, read by planner/sql.py and disclosed on every
answer. Operator ruling, 2026-09-30: an active store has no close date, and the online sentinel is
not a store at all. NO `value_filter`, and that is the second correction of 2026-10-01. It read
`close_date IS NULL AND store_code <> -1`, applied inviolably. The first fix moved `close_date
IS NULL` out as a default reading and left `store_code <> -1` here as "the unaskable domain".
That was still wrong, and the operator caught it: the same predicate was ALSO declared as the
then-Channel concept's `physical` population — doppeltgemoppelt, one predicate in two homes — and
a predicate that a question can legitimately ask the other side of ("what is the revenue from the
online store?", 86 790 054.13, 40% of this bundle) is a DEFAULT READING, not a domain. So this
concept has NO unaskable rows and TWO orthogonal state axes, each a population rule below: how the
store is TRADING, and which CHANNEL it is. They are independent — the online store is also an
active store — which is why they are two rules and not one list.

## The channel axis — `physical` by default, `online` when asked

the sentinel row has no country and no floor, and as the single largest "store" it sits at the top
of every list it is allowed into — so `physical` is the default and a question must ask for
`online` to get it. It is one row of 74 and 40% of revenue, which is why neither including it
silently nor excluding it silently is acceptable.

RENAMED from `store.exclusion.the_online_row_is_not_a_store` on 2026-10-01. It was an exclusion —
"exclude `{store_code}` = -1, that row is the online channel, not a shop" — and an exclusion is
unaskable. This is not: "what is the revenue from the online store?" asks for exactly those rows,
and they carry 86 790 054.13, 40% of this bundle's revenue. A default reading, then, and the same
shape as the trading axis above. AND IT ABSORBED WHAT `Channel` DECLARED, before that concept was
removed on 2026-10-01: it grounded on this same relation and stated the same predicate on the same
column — one fact, two homes. The predicate lives where the column lives.

the 73 shops that have a country and a floor.

## The trading axis — `active` by default

two columns state one thing. Until the operator's impurity fix of 2026-10-01 they DISAGREED on one
row — Contoso Store Utah carried a close date and an empty status — and the corpus recorded that
as two honest answers to one question (58 "still open" against 59 "not closed"). The fill made
them equivalent: `close_date IS NOT NULL` now selects exactly the rows `status_annotation IN
('Closed','Restructured')` selects, 16 of them. So BOTH are legitimate ways to ask about the
state, which is why both are bound below and why a question using either displaces the default.
The confidence is C because a PERSON ruled it, not because a measurement implied it.

## Why these rules carry a body and no `when`/`then`/`never`

1 row, 86 790 054.13 of revenue — the online business written as a store.

NO `when:`, NO `then:`, NO `never:` — operator ruling, 2026-10-01: "i believe there is no reason
anymore for when then never". There is not, for a rule that HAS A BODY. The body below states the
condition (`binds`) and the action (`populations`, `default`) executably; prose beside it is a
second home for the same fact, and the prose home is the one that rots without anything noticing.
MEASURED, on this very rule. Its `never` read "read `{status_annotation}` as the state. It is
empty on all 58 rows that never closed" — true when written, FALSE after the operator's impurity
fix of 2026-10-01 filled the Utah row, and no gate caught it. It was corrected by hand hours
later, only because a human happened to re-read it. `why:` STAYS, and is not redundant: no
structure encodes "a person ruled this, on this date, against this measurement". That is the one
thing prose carries that a predicate cannot.

THE BODY OF THE RULE, not a description of one. Operator ruling, 2026-10-01: "i will want to have
rule act like DB trigger. if the condition is met ... then something should happen". The condition
is `about`; the action is the selected population. Every predicate is STRUCTURE, never SQL text,
for a measured reason: `assert_bound_params_only` refuses any raw string literal, so
`status_annotation IN ('Closed','Restructured')` written as text is UNEXECUTABLE — it plans
cleanly and dies at the adapter. Structured, its values are bound and it runs.

## One predicate, and its complement derived

THE CONDITION IS THIS RULE'S `binds:` ABOVE — no second list. A question constraining `close_date`
or `status_annotation` is making its own statement about the state, so the default steps aside.
Those two columns are two statements of ONE fact, which is why EITHER displaces it and why no
reader could have derived the condition from column names alone — the attempt that compared column
names saw no overlap and did nothing.

ONE PREDICATE, AND ITS COMPLEMENT DERIVED — operator design, 2026-10-01: "we should define that
closed stores have only close date is not null, then the active stores will be the negation of it
... this should be able to avoid the problem by design." It does, and that is the whole reason for
this shape. `closed` and `active` partition all 74 rows BY CONSTRUCTION — 16 + 58 — so there is
nothing to verify and no way to author an overlap or a gap. Two independently declared halves
needed a GATE to measure what this makes impossible. AND IT IS WHAT MAKES A NEGATION ANSWERABLE.
"not closed" is `active`, read off the lattice: each is the other's only sibling. No word list, no
string distance, no language.

"closed" NAMES THESE 16 ROWS in the operator's own usage — STORE-02 "how many stores are not
closed?" is approved at 57, this population's complement under the physical default. The 9 rows
whose `status_annotation` reads 'Closed' are a SUBDIVISION of it, named `shut` below, because one
word cannot denote two sets: RC08 "how many stores are closed?" is approved against those 9, and
until these were named apart the same word answered 16 in one approved question and 9 in another,
with nothing able to see the collision.

THE COMPLEMENT, declared as one rather than written out. "not closed" is a SURFACE of this
population, not a negation the engine must interpret — which is the point: a person's phrasing is
declared, matched exactly, and needs no instruction in any prompt.

THE SUBDIVISION of `closed`: WHY a store ended, not whether it did. 9 + 7 = 16 by construction,
because both are declared `of: closed`.

NAMED `shut`, NOT `closed` — the collision the lattice forces into the open. Derived from the rows
rather than chosen: a shut location never has a later row at the same code (0 of 8) and a
restructured one always does (6 of 6). This is the half that was not replaced.

7 rows over 6 locations: New Brunswick was restructured twice. A COUNT is 6 (identity.counts_as:
store_code) and a LIST shows 7 trading periods — both right, and the declaration is why.

## Where each fact is declared

| in this page | declared at |
|---|---|
| what a store is | `concept.definition`, one sentence |
| the count key | `concept.identity.counts_as: store_code` |
| nothing is collapsed | `grounding.snapshot_rule`, one sentence — quoted verbatim into every answer's disclosure |
| the two axes | `contract.rules[]`, two `mac.canon.population_select` bindings |
| each ruling's date and measurement | this page, and each rule's `why` |
