# Manual value check — the 38 executed answers, 2026-10-08

## Why this file exists

All 83 oracles in this corpus are `authority: derived` and **none asserts a value**, by their own
standing note: this bundle has no second source of truth for what a measure means, so a value written
from the ontology would test the planner against the ontology and not against the world. That leaves
38 answers carrying an executed figure that nothing has ever checked.

**Method.** For each of the 38 I wrote my own query against the RAW `main` tables — `sales`, `store`,
`customer`, `product`, `currencyexchange` — never by re-running the captured SQL and never through
`contoso_served`. Re-running the plan would test the plan against itself; reading through the served
views would test a view against itself. Where a reading was contestable (which country, which store
population, which age boundary) I computed every candidate so the choice is visible, not assumed.

## Verdict

* **Arithmetic: 38 of 38 reproduce exactly.** No figure in this corpus is a miscalculation.
* **Answers the question asked: 35 of 38.** Three are listed under DEFECTS.
* **Produced by the current ontology: 0 of 38.** See STALENESS.

## STALENESS — the standing caveat on every row below

The 38 were captured on 2026-10-02 (7 answers, ontology `3c0afde850b2d121`) and 2026-10-04 (31
answers, ontology `ab8e044ecebec2ca`). Both fingerprints predate the fifth-revision column standard
and today's rule commit. Nothing recorded here was produced by the bundle as it now stands, so
"the value is correct" is a statement about the world, not a licence to approve the run.

## KILLED — two things I suspected and the data refuted

Recorded because a wrong suspicion left unrecorded gets re-suspected.

1. **"`unit: USD` is a lie over a mixed-currency sum" — FALSE.** `net_amount = Quantity * NetPrice`
   and the lines carry five `CurrencyCode` values, which looks like a five-currency sum labelled USD.
   It is not. **52,972 non-USD lines carry `UnitPrice` EXACTLY equal to the USD catalogue price**
   `product.Price` (AUD 7,390 · CAD 12,230 · EUR 24,991 · GBP 8,361), and `UnitPrice/Price` sits at
   1.12–1.16 uniformly across all five currencies while `UnitPrice/(Price*Rate)` scatters 0.77–1.48.
   The stored amounts are USD on every line. `sales.ExchangeRate` is the **USD→local** rate — it
   equals `currencyexchange` at `FromCurrency='USD', ToCurrency=<line currency>` on 100% of rows.
   `currency.ambiguity.code_is_not_the_unit_of_the_amounts` is accurate when it says "the amounts
   are USD", and `CurrencyCode` is the currency transacted in, not the unit of the figure.
2. **"AGG-14 answered `converted to USD` without converting" — CORRECT ANYWAY.** The conversion is a
   no-op because the amounts are already USD. The only gap is that nothing in the answer SAYS so;
   see DEFECT 4.

## DEFECTS

### 1. STORE-06 is the wrong answer — "How many store versions are recorded?" → 57

Truth: **73** versions excluding the online sentinel (74 rows in `main.store`, over 66 real
`StoreCode` values; 58 current + 16 ended). The run returned 57 — the count of OPEN distinct location
codes — on SQL byte-identical to RC05, STORE-01 and STORE-02.

The question asks for the pre-collapse row count and `grounding.snapshot_rule` collapsed exactly that
before reading. **The answer's own disclosure states the right number**: "The relation holds 74 rows
over 67 codes because it also records ENDED stores". The declaration knew; the plan discarded it.

### 2. MQ-01 answers a different kind of question — "What is the definition of Customer?" → 104990

The count is right (104,990 distinct `CustomerKey`), and it is RC04's answer on RC04's SQL. A
definitional question was routed to a count. No value error; a question-type error.

### 3. STORE-09 bypasses the Store population its siblings apply — "revenue of all Contoso stores"

218,814,471.66 is the grand total with **no join to `dim_store` at all**, so neither
`store.resolution.the_channel_is_the_location_sentinel` (`physical`) nor
`store.resolution.active_is_the_absent_close_date` (`active`) was applied or disclosed. Every sibling
applies both and says so — STORE-08 (Armagh), STORE-11 (closed stores), MQ-07 (online), RC05, MQ-06.

Under the siblings' population the answer is **128,818,965.21** — 41% lower. Decomposition:
physical 132,024,417.53 + online 86,790,054.13 = 218,814,471.66, and 0 sales rows lack a store.
Whether "all Contoso stores" includes the online channel is the operator's call; the defect is that
this one question never consulted the concept whose population the other five disclose.

### 4. `answer_parts.reading` is stamped from `default_reading` regardless of which rule fired

**21 answers across the corpus** carry `net_revenue.contract.default_reading` verbatim: "An
unqualified price means WHAT THE CUSTOMER PAID PER ARTICLE: `{net_amount}` summed and divided by
UnitsSold, 310.98 USD." That is the ruling for `net_revenue.default.a_price_is_revenue_per_article`,
and **ADV-25 is the only one of the 21 it actually governs**.

Thirteen of the 21 carry an executed value: ADV-22, ADV-25, AGG-01, AGG-05, AGG-06, AGG-07, AGG-12,
AGG-14, MQ-07, MQ-12, STORE-08, STORE-09, STORE-11. The other eight (ADV-03, ADV-04, ADV-08, AGG-03,
AGG-04, AGG-10, AGG-15, MQ-11) carry it with no value at all.

So `default_reading` is being stamped on every answer that touches the concept, whatever was asked
and whatever fired. Twelve total-revenue answers state a reason belonging to a per-unit question.
Values unaffected; the stated reason is somebody else's, and a reader has no way to tell.

### 5. Four answers cite retired vocabulary

MQ-01, MQ-02, RC05 and STORE-06 disclose "counted by … (`identity.canonical_key` of X)" and
"(`identity.counts_as` of Store)". `identity` was retired from the column standard; the relation key
is `key`. Stale because the recordings predate the conversion — but it is the prose a reader sees.

## The ledger — all 38

Every row reproduced from raw `main` tables. `=` means my independent figure matched to the last digit.

| ID | Question | Executed | Independent check | |
|---|---|---|---|---|
| ADV-22 | Revenue | 218814471.65866 USD | `SUM(Quantity*NetPrice)` = | ✓ |
| ADV-25 | Average price | 310.98342951483824 USD/unit | `SUM(Qty*NetPrice)/SUM(Qty)` = | ✓ |
| AGG-01 | total net revenue | 218814471.65866 USD | = | ✓ |
| AGG-02 | total quantity sold | 703621 units | `SUM(Quantity)` = | ✓ |
| AGG-05 | net revenue in Germany | 24638830.1795 USD | `customer.Country='DE'` = (store reading would be 14,382,768.44) | ✓ |
| AGG-06 | net revenue, Contoso brand | 38431107.31785 USD | `product.Brand='Contoso'` = | ✓ |
| AGG-07 | net revenue Q1 2024 | 9494485.56976 USD | `OrderDate ∈ [2024-01-01, 2024-04-01)` = | ✓ |
| AGG-12 | Germany share of total | 0.11260146549143872 | DE/total = | ✓ |
| AGG-13 | gross/net ratio | 1.063008040065774 | `SUM(Qty*UnitPrice)/SUM(Qty*NetPrice)` = | ✓ |
| AGG-14 | total net revenue **converted to USD** | 218814471.65866 USD | = ; conversion is a no-op, amounts already USD | ✓ʰ |
| MQ-01 | **definition** of Customer | 104990 | count is right, question is not a count | ✗ |
| MQ-02 | concepts in the ontology | 17 | 17 `meta_concept` rows, 17 concept files = | ✓ |
| MQ-06 | average store size | 1511.7543859649122 m2 | `AVG(SquareMeters)` over 57 open physical = (all 74 → 1494.79) | ✓ |
| MQ-07 | revenue, online store | 86790054.12699 USD | `StoreCode=-1` = | ✓ |
| MQ-12 | Total sales in dollars | 218814471.65866 USD | = ; and the dollars are real | ✓ |
| RC04 | how many customers | 104990 | `COUNT(DISTINCT CustomerKey)` = | ✓ |
| RC05 | how many stores | 57 | open distinct `StoreCode`, excl. sentinel = | ✓ |
| RC06 | products in catalog | 2517 | `COUNT(DISTINCT ProductKey)` = | ✓ |
| RC07 | customers in Germany | 9981 | `Country='DE'` = | ✓ |
| RC08 | stores closed | 14 | closed distinct codes = (16 rows; 5 codes are both open and closed) | ✓ |
| RC09 | Contoso products | 710 | = | ✓ |
| RC10 | orders in 2024 | 15899 | `DISTINCT OrderKey` from `sales` = , and from `orders.DT` = | ✓✓ |
| RC11 | distinct products sold 2023 | 2485 | = | ✓ |
| RC12 | female customers in Europe | 19564 | `Gender='female' AND Continent='Europe'` = | ✓ |
| RC13 | orders in euros, Q1 2024 | 1099 | = ; a COUNT may filter on currency, no amount presented | ✓ |
| RC14 | aged 25–44 on 2022-12-10 | 31586 | bound window `[1977-12-11, 1997-12-11)` = , **and** an independent age-at-date computation = | ✓✓ |
| RC15 | products bought by FR customers, Q1 2024 | 359 | = | ✓ |
| STORE-01 | stores still open | 57 | = | ✓ |
| STORE-02 | stores not closed | 57 | = | ✓ |
| STORE-03 | stores restructured | 6 | codes with a closed version then a later open one = ; `Status='Restructured'` holds 7 rows over 6 codes | ✓ |
| STORE-04 | first store closure | 2013-12-05 | `MIN(CloseDate)` = (same with and without the sentinel) | ✓ |
| STORE-06 | store **versions** recorded | 57 | truth is **73** (74 rows, 66 real codes, 58 current + 16 ended) | ✗ |
| STORE-07 | stores that have closed | 14 | = | ✓ |
| STORE-08 | revenue, Contoso Store Armagh | 2282987.23662 USD | `StoreKey=360` = | ✓ |
| STORE-09 | revenue, all Contoso stores | 218814471.65866 USD | = for "all sales"; siblings' population gives 128,818,965.21 | ✗ |
| STORE-10 | stores in Germany | 8 | open `CountryCode='DE'` = (all versions → 9) | ✓ |
| STORE-11 | revenue, all closed stores | 3205452.32521 USD | = | ✓ |
| STORE-14 | stores in Germany closed | 2 | = | ✓ |

ʰ right figure, missing disclosure — see DEFECT 4 and KILLED 2.

### Internal consistency, checked as a cross-foot

* 57 open codes + 14 closed codes − 5 codes in both states = 66 real codes = 67 − the sentinel. ✓
* physical 132,024,417.53 + online 86,790,054.13 = 218,814,471.66 grand total, 0 orphan sales rows. ✓
* RC10 agrees computed two ways, from `sales.OrderDate` and from `orders.DT`. ✓
* RC14 agrees computed two ways, from the bound birth window and from age-at-date. ✓

## Not approved by this file

This is a measurement of 38 figures against the warehouse. It approves nothing: the recordings are
stale against the current ontology, three answers do not answer their question, and approval is the
operator's. What it does establish is that **no figure here is an arithmetic error** — the three
defects are all about which question was answered, and that is a planner matter, not a maths one.
