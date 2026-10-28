# ADV-01..25 — derived by hand, classified

Measured 2026-09-30 against `contoso5.duckdb` (`contoso_served`) and `ontology/concepts/*.yaml`.
Five parallel derivations, each blind to the engine's own answer. Board at time of writing:
77 rows — 27 proven / 24 routed / 15 unproven / 5 failed / 5 unrun / 1 error.

Classification is the operator's rule: **ONTOLOGY** = a declaration is missing and the shape to
hold it already exists and is read; **FRAMEWORK** = no shape exists to express the question;
**NEITHER** = already declared, the runtime must simply apply it; **RULING** = a person must
decide before any declaration can be written.

## Verdict per question

| id | question | class | state |
|---|---|---|---|
| ADV-01 | several measures over one row set | NEITHER | answers via `Intent.also` |
| ADV-02 | gross minus net by brand | RULING | contradicts `sales_cost.yaml` |
| ADV-03 | colour fold | NEITHER | answers |
| ADV-04 | biggest month-over-month drop | FRAMEWORK | no sortable month axis |
| ADV-05 | row-over-row arithmetic | FRAMEWORK | no expression over two rows |
| ADV-06 | year-over-year by country | FRAMEWORK + RULING | LAG built; country path undeclared |
| ADV-07 | Q1 2024 against Q1 2023 | FRAMEWORK | two disjoint period ranges |
| ADV-08 | average order value by country | RULING | ratio already expressible |
| ADV-09 | countries above a threshold | FRAMEWORK | `having` |
| ADV-10 | products in over 5 countries | FRAMEWORK | `having` |
| ADV-11 | nested over another result | FRAMEWORK | encapsulation |
| ADV-12 | price | RULING | which price |
| ADV-13 | nested over another result | FRAMEWORK | encapsulation |
| ADV-14 | category synonyms | ONTOLOGY | alias map |
| ADV-15 | structural zero | NEITHER | 0, store filter load-bearing |
| ADV-16 | relational divide | FRAMEWORK | test is vacuous, see below |
| ADV-17 | every country | FRAMEWORK | test is vacuous, see below |
| ADV-18 | relational divide | FRAMEWORK | encapsulation |
| ADV-19 | text over rule prose | FRAMEWORK | no string match |
| ADV-20 | open questions | ONTOLOGY | `open_questions` unpopulated |
| ADV-21 | lineage OrderLine to Continent | FRAMEWORK | lineage not addressable |
| ADV-22 | revenue | RULING | unscoped period |
| ADV-23 | sales in Turkey | NEITHER | refuse, register is closed |
| ADV-24 | how many stores are open | NEITHER | **57** |
| ADV-25 | average price | RULING | which price, over what |

## The four findings that outrank the table

### 1. `contract.default_reading` is empty on all 18 concepts

The key is fully alive: the parser reads it (`ontology/parser.py:624`), the prompt composer hands it
to the interpreter (`interpret/prompt.py:322`), the renderer discloses it (`renderer/render.py:76`),
the meaning plane projects it. Not one contoso5 concept declares it. Every question below that is
classed RULING is a question this key would answer, once a person fixes the value.

### 2. The geography path into Country is undeclared, and it is not a rounding difference

`Country` has three inbound edges — `customer__based_in__country`, `store__trades_in__country`,
`location__in__country`. Nothing declares which one a sales question means.

| reading | Germany 2025 growth |
|---|---|
| customer path | +18.07% |
| store path | +49.65% |

The store path drops the online channel, which is 40% of net revenue. Four of the twenty-five hang
on this one undeclared choice.

### 3. The generic fix for #2 is blocked in the schema, and the framework says so itself

`relationAliasBlock` is the declared mechanism for routing a surface token to an edge, realized by
`mac.canon.relation_alias_resolve`. It is in `mac.schema.json`, in `mac_vocabulary.yaml`, has a
reference-manual page, and is used on an edge in the framework's own `example_shop_ontology`.

It has no runtime reader, and `canon.py:144` records why:

> NOT IMPLEMENTABLE FROM ITS PAGE: `relationAliasBlock` carries only `realized_by` — no slot holds
> the surfaces the canon would match against. The grammar must declare the surfaces before a reader
> can exist.

Verified independently: `relationAliasBlock.properties` is exactly `{realized_by}`, while the canon's
own doc string says it matches against `relationAliasBlock.multilingual`. **The schema and the canon
contract disagree.** One additive slot unblocks the generic path for every "by X" routing question.

`parse_edges` also builds `Edge(...)` field by field and never passes `aliases`, and the `Edge` model
forbids extras — so an edge alias block declared in a bundle today is silently dropped.

### 4. The declared-but-unread gate cannot see this, by construction

`check_declarations_read.py` credits a reader by matching the **leaf** key name only.

| measure | count |
|---|---|
| schema declarations traced | 211 |
| distinct leaf names | 116 |
| leaf names serving more than one path | 34 |
| declarations riding a leaf shared with another path | 129 |

`edges[].aliases` is certified read by `parser.py:202`, a **docstring** about *concept value*
aliases. Its whole `realized_by` subtree rides on the concept-side readers: `applied_as` alone
serves 15 distinct declaration paths from one line. The gate proves "some declaration named X is
read", never "this declaration is read", so a dead shape sharing a leaf with a live one passes.

Separately, `strip_comments` blanks `tokenize.COMMENT` but not statement-position strings, so 18 of
384 declarations are certified by a docstring alone.

Both measurements are reproducible by importing the gate and re-running its own `audit()`:
for the leaf collision, group its schema rows by `row["key"]` and count the leaves serving more than
one `row["declaration"]`; for the docstring credit, monkey-patch `strip_comments` to also blank
statement-position STRING tokens (a token whose preceding significant token is NEWLINE, INDENT or
DEDENT) and diff the two reports. Blanking *every* STRING token overstates the count at 127, because
`values.get("aliases")` is itself a string literal and is genuine evidence.

## Two acceptance tests that cannot fail

- **ADV-09** — threshold is 500; the lowest country average order value is 2,204. All 8 countries
  return under the right computation and under the wrong one.
- **ADV-17** — all 11 brands return under every reading of "every country".

A green on either proves nothing. Both need a threshold inside the observed range.

## Figures derived by hand

| id | figure |
|---|---|
| ADV-06 | 80 rows; 2025 Germany +18.1%, US −21.5% |
| ADV-07 | Q1 2024 9,494,486 against Q1 2023 11,002,644, −13.7% |
| ADV-08 | Italy highest at 2,459.71 |
| ADV-09 | all 8 countries |
| ADV-10 | 2,207 of 2,517 products |
| ADV-15 | 0 — structural; without the store filter it becomes 16,584 |
| ADV-22 | net all time 218,814,471.66; gross 232,601,542.66; 2025 29,277,489.59 |
| ADV-24 | **57** active stores — US 21, DE 8, FR 7, GB 6, AU 5, CA 4, NL 4, IT 2 |
| ADV-25 | net per unit 310.98; gross per unit 330.58; catalogue mean 356.83; per order 2,341.01 |

`ADV-24` is worth keeping: 74 store rows, 67 location codes, 16 carry a close date, one of the
remaining 58 is the online sentinel. Counting by `status_annotation` instead gives 58, because
store 630 carries a close date with an empty status. That single row is the whole historic 58-vs-59
disagreement, and the close-date ruling settles it.

## Owed rulings

1. **Geography** — does "by country" mean the customer's country or the store's? (#2 above)
2. **ADV-02** — the question says margin is gross minus net; `sales_cost.yaml` says net minus cost.
3. **ADV-12 / ADV-25** — which column is "price", and what does averaging it mean?
4. **ADV-22** — what period does an unscoped measure question cover?
5. **STORE-07** — "how many stores have closed": 8 labelled, 9 final, or 16 with a close date?
6. **Schema slot** — may `relationAliasBlock` carry surfaces, so the canon becomes implementable?
7. **Gate precision** — fix leaf matching to full-path matching? It will turn a green gate red and
   the resulting UNREADs need owners.
