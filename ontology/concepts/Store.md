# Store

The account of concept Store.

## What a store is

A shop Contoso sells from, each with a name, a country, a state, an opening date and a floor area. One row of the relation — store_key 999999, "Online store", country `--`, no floor — is not a shop. It is the online channel written as a store, and it carries a large share of revenue. It is held out of every question about stores by the `physical` default, and a question reaches it by naming `online`; revenue and every other figure of the sale includes both channels (rule Store.channel). A STORE IS A SHOP YOU CAN WALK INTO, and this is an OPERATOR RULING: "stores that are closed, restructured have close date and are not active anymore; other stores without status do not have close date are ONLY stores currently active and this is the scope of our interest in most questions." SO THE POPULATIONS ARE DECLARED, NOT DESCRIBED, and there are TWO ORTHOGONAL SETS of them — one per state this relation's rows carry. How the store is TRADING (`active` by default, or `closed`, `shut`, `restructured`) is stated by `close_date` and `status_annotation`; which CHANNEL it is (`physical` by default, or `online`) is stated by `store_code`. Each is a rule with a choice, each names a default, and the runtime discloses on every answer which it applied and which the question displaced. A predicate a question may legitimately ask the other side of is a DEFAULT READING, not a domain, and both of these are: the rows that ended, and the one `store_code = -1` row, which carries a large share of revenue. THE CLOSE DATE AND THE STATUS AGREE. The landing carries one store, Contoso Store Utah, with a close date and an EMPTY status; the operator ruled that impurity fixed in the transform, which fills it DERIVABLY rather than by hand: a restructured location always has a later row at the same code and a closed one never does, and Utah has no successor, so it is Closed. Every row with a close date carries Closed or Restructured. SO THE TWO TESTS ARE EQUIVALENT, and the close date remains the one this concept uses because it is the simpler of two statements of one fact: `close_date IS NOT NULL` selects exactly the rows `status IN ('Closed','Restructured')` selects. The status says WHY a store ended; the date says THAT it did. WHAT ENDED IS A DIFFERENT NOTION. The rows with a close date are labelled Closed or Restructured (the store was rebuilt and a successor row exists at the same location, as at New Brunswick). Those are store CLOSURES and they are still answerable from this concept's own columns — `close_date` says which rows ended and when, and `status_annotation` says why — and they are reached by NAMING the population they belong to (`closed`, `shut`, `restructured`). They are not what "a store" means unqualified, which is why `active` is the declared default rather than the only reading. The store names are cut from the landing's Description column and attached to store_name here.

## How identity is established

A surrogate `store_key` annotated by `store_name` — names repeat across rows, so the name is not the key. `dim_store` is served one row per `store_key`, and some codes carry two or three rows each — the same name, one row closed `Restructured` and the next opened months later (New Brunswick is one). So `store_key` is the key — it is what `sales` joins on, and every revenue figure belongs to the period that earned it. THE COLUMN IS StoreCode UNDER THIS BUNDLE'S NAME.

## What the rows are, and why nothing is collapsed

ONE ROW PER STORE ALREADY, once the `active` population has selected the trading ones: one row per location code, because a location has at most one store with no close date. The relation holds more rows than codes because it also records ENDED stores — the restructured ones, each with a successor at the same location — and the online sentinel. Those rows are selected out by the two declared default populations rather than removed from the relation, and a question that names `closed`, `shut`, `restructured` or `online` reaches them. SO NOTHING IS COLLAPSED HERE. A collapse that keeps a closed row is not a reading of "a store". A count of stores is a count of the active rows.

Operator ruling: an active store has no close date, and a question about stores covers physical shops only unless it names the online channel. So this concept has NO unaskable rows and TWO orthogonal state axes, each a population rule below: how the store is TRADING, and which CHANNEL it is. They are independent — the online store is also an active store — which is why they are two rules and not one list.

## The channel axis — `physical` by default, `online` when asked

the sentinel row has no country and no floor, and as the single largest "store" it sits at the top of every list it is allowed into — so `physical` is the default and a question must ask for `online` to get it. It is one row and a large share of revenue, which is why neither including it silently nor excluding it silently is acceptable.

"what is the revenue from the online store?" asks for exactly those rows. A default reading, then, and the same shape as the trading axis above. The predicate lives where the column lives.

the shops that have a country and a floor.

## The trading axis — `active` by default

two columns state one thing. The fill made them equivalent: `close_date IS NOT NULL` selects exactly the rows `status_annotation IN ('Closed','Restructured')` selects. So BOTH are legitimate ways to ask about the state, which is why both are bound below and why a question using either displaces the default. It is ruled because a PERSON ruled it, not because a measurement implied it.

One row, a large share of revenue — the online business written as a store.

## One predicate, and its complement derived

A question constraining `close_date` or `status_annotation` is making its own statement about the state, so the default steps aside. Those two columns are two statements of ONE fact, which is why EITHER displaces it and why no reader could have derived the condition from column names alone.

ONE PREDICATE, AND ITS COMPLEMENT DERIVED — operator design: "we should define that closed stores have only close date is not null, then the active stores will be the negation of it ... this should be able to avoid the problem by design." It does, and that is the whole reason for this shape. `closed` and `active` partition every row BY CONSTRUCTION, so there is nothing to verify and no way to author an overlap or a gap. Two independently declared halves needed a GATE to measure what this makes impossible. AND IT IS WHAT MAKES A NEGATION ANSWERABLE. "not closed" is `active`, read off the lattice: each is the other's only sibling. No word list, no string distance, no language.

"closed" NAMES THESE ROWS in the operator's own usage — STORE-02 "how many stores are not closed?" is approved as this population's complement under the physical default. The rows whose `status_annotation` reads 'Closed' are a SUBDIVISION of it, named `shut`, because one word cannot denote two sets: RC08 "how many stores are closed?" is approved against every row with a close date.

THE COMPLEMENT, declared as one rather than written out. "not closed" is a SURFACE of this population, not a negation the engine must interpret — which is the point: a person's phrasing is declared, matched exactly, and needs no instruction in any prompt.

THE SUBDIVISION of `closed`: WHY a store ended, not whether it did. Both are declared `of: closed`, and together they cover every closed row.

NAMED `shut`, NOT `closed` — the collision the lattice forces into the open. Derived from the rows rather than chosen: a shut location never has a later row at the same code and a restructured one always does.

A location can carry more than one restructured row: New Brunswick was restructured more than once.

## Cites

- `dataset:dim_store.store_key`
- `dataset:dim_store.store_code`
- `dataset:dim_store.store_name`
- `dataset:dim_store.country_code`
- `dataset:dim_store.state`
- `dataset:dim_store.open_date`
- `dataset:dim_store.close_date`
- `dataset:dim_store.status_annotation`
- `dataset:dim_store.square_metres`
- `dataset:dim_store.is_online`
- `dataset:dim_store.is_shut`
- `dataset:dim_store.is_restructured`
- `rule:Store.channel`
- `rule:Store.premises_not_place`
- `rule:Store.record_questions`
- `rule:Store.trading`

## grounding.note

Nothing is collapsed: once the `active` population has selected the trading rows there is one row per store already, one per location code, because a location has at most one store with no close date (the row count is measured in data/profiles). Why is in ontology/concepts/Store.md.
