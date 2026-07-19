# ask(1) — Contoso demo ontology

> Generated from the ontology by `mac_to_manual.py` — do not edit by hand. Author the prose in `docs/manual.template.md`; the tables and lists below are filled from the concept, rule and policy files, so this page can never drift from the model.

A public, MIT-licensed demonstration of a **meaning-as-code** ontology over the SQLBI Contoso V2
dataset (running in local DuckDB). It shows how a semantic layer turns a **contested** business
question into one disclosed, correct answer — and lets you drill from the answer down to the
physical column it came from.

This page is the ontology read as a command-line tool: what you can ask, what it commits to, what it
asks you about, and what it refuses. The prose is written by hand; every table and list below is
generated straight from the concept, rule and policy files.

## The question the demo is built around

> **"What were our total sales?"**

Under-specified on purpose. A naive text-to-SQL bot silently picks one interpretation and hands you a
number. The ontology does not — it fixes one reading and **discloses the choice**:

- **COMMIT** — net revenue (`Quantity * NetPrice`), each line converted to one reporting base
  currency via its own `ExchangeRate`, then summed.
- **ASK** — if the rows span several currencies and no reporting currency is named, ask which — or
  commit to the disclosed base currency as the default.
- **REFUSE** — never sum `NetPrice` across the five currencies as if they were one unit; never add
  `sales` and `orders * orderrows` together (the same order lines, counted twice).

That single question exercises three traps at once — currency basis, gross-vs-net, and a
header/detail double-count — which is why it is the demo's centrepiece.

## At a glance

- **Source** — `CONTOSO`
- **Concepts** — 8
- **Rules** — 13  (COMMIT 8 · ASK 2 · REFUSE 3)
- **Derived readings** — 3
- **Joins** — 2

## Concepts

The objects you can ask about. Each has one canonical definition and binds to real columns.

| Concept | Kind | What it is |
| --- | --- | --- |
| **Brand** | enumeration | The set of 11 Contoso house brands a product belongs to (product.Brand). |
| **Product** | reference | A sellable item in the Contoso catalogue, identified by ProductKey (ProductCode is the business code). |
| **Currency** | enumeration | The transaction/reporting currencies present in the sales facts. |
| **Gross profit (gross margin)** | measure | GROSS PROFIT: net revenue minus cost of goods, per order line, converted to the reporting base currency and summed — Quantity x (NetPrice - UnitCost) x ExchangeRate. |
| **Store** | reference | A point of sale, identified by StoreKey, located in a CountryName. |
| **Order** | entity | An order header (one row per OrderKey in `orders`), whose detail lines live in `orderrows`. |
| **Sales (net revenue)** | measure | The monetary value of sales order lines. |
| **Period** | reference | The WHEN axis of a sale: the order date carried on each `sales` line (OrderDate), with DeliveryDate as a secondary date. |

## Measures — the contested total, made explicit

"Total sales" is not one number. The ontology names each defensible reading as a **derived measure**
with its exact formula and the guardrails that keep it meaningful, so the choice is inspectable
rather than guessed:

| Reading | Produces | Formula | Guardrails |
| --- | --- | --- | --- |
| `net_sales_base_currency` | Sales | `SUM(Quantity * NetPrice * ExchangeRate)` | Convert each line to base currency BEFORE summing — never SUM(NetPrice) across mixed CurrencyCode; Sum `sales` OR orders x orderrows, never both (same facts, two shapes) |
| `gross_sales_base_currency` | Sales | `SUM(Quantity * UnitPrice * ExchangeRate)` | — |
| `gross_profit_base_currency` | Margin | `SUM(Quantity * (NetPrice - UnitCost) * ExchangeRate)` | Revenue side is NET (NetPrice), consistent with Sales > net_sales_base_currency — do not mix gross revenue with cost; Convert each line to base currency BEFORE summing — never SUM across mixed CurrencyCode; Cost basis is UnitCost only (cost of goods). This is GROSS profit; operating/overhead costs are out of scope and undisclosed in the data |

The rule that matters most is **convert-before-sum**: a raw `SUM(NetPrice)` across mixed currencies
adds incompatible units and is meaningless; multiplying each line by its `ExchangeRate` first makes
the total comparable.

## Synopsis

The compact grammar — how the model is invoked. Every flag here is optional with a disclosed default,
because this model declares no mandatory dimension and no mutually-exclusive choices; a richer model
would also carry required and alternative-group flags. The allowed values and the full property list
are in the whitelist below.

```text
# Gross profit (gross margin)
ask <MEASURE> [--currency usd|eur|gbp|cad|aud] [--period <PERIOD>]

MEASURE := net_sales_base_currency | gross_sales_base_currency | gross_profit_base_currency      # Gross profit (gross margin)

[]  optional (has a disclosed default)     |  alternatives

# Sales (net revenue)
ask <MEASURE> [--product <PRODUCT>] [--store <STORE>] [--brand <BRAND>]
              [--currency usd|eur|gbp|cad|aud] [--period <PERIOD>]

MEASURE := net_sales_base_currency | gross_sales_base_currency | gross_profit_base_currency      # Sales (net revenue)

[]  optional (has a disclosed default)     |  alternatives
```

## What a question can contain — the whitelist

Beyond the measure and its reading, a question may name any of these dimensions and properties to slice
or group the total. This is the model's **question grammar** — an explicit whitelist, generated from
the join graph and the registers, not hand-listed. Every property is either **closed** (its allowed
values named below, straight from the register that pins it) or **open** (any value of the given type):

**Gross profit (gross margin)**

| Dimension | Property | Values you can name |
| --- | --- | --- |
| **Currency** | `CurrencyCode` | **closed** · USD, EUR, GBP, CAD, AUD |
| **Period** | `OrderDate` | open (timestamp) |
|  | `DeliveryDate` | open (timestamp) |

**Sales (net revenue)**

| Dimension | Property | Values you can name |
| --- | --- | --- |
| **Product** | `ProductCode` | open (string) |
|  | `ProductName` | open (string) |
|  | `Brand` | **closed** · Contoso, Fabrikam, Litware, Proseware, Southridge Video, Adventure Works, Wide World Importers, The Phone Company, Tailspin Toys, A. Datum, Northwind Traders |
|  | `CategoryName` | open (string) |
|  | `SubCategoryName` | open (string) |
|  | `Price` | open (decimal) |
| **Store** | `CountryName` | open (string) |
|  | `State` | open (string) |
| **Currency** | `CurrencyCode` | **closed** · USD, EUR, GBP, CAD, AUD |
| **Period** | `OrderDate` | open (timestamp) |
|  | `DeliveryDate` | open (timestamp) |

Only two properties are closed — **Brand** and **Currency**, because a register pins their values;
everything else, including **period** (grounded on the order date, grain day → month → quarter → year),
is open. Because the whitelist is generated from the model, it is always exactly as wide as the
ontology: the `period.window` gate in the options below now has a matching axis to act on. Add a
concept and its properties appear here — which is precisely how the model grows.

## Decision lanes

Every rule carries a **kind** that sorts it into a lane — this is how the model decides whether to
answer, ask, or refuse:

COMMIT · resolve and answer (disclosing any assumed default)

- `margin.gross_basis_disclosed` — computing profit or margin
- `margin.net_revenue_side` — taking the revenue side of profit
- `margin.single_currency_basis` — aggregating profit across rows that may span more than one CurrencyCode
- `sales.net_of_discount` — computing sales value from order lines
- `sales.single_currency_basis` — aggregating sales across rows that may span more than one CurrencyCode
- `resolve.never_fabricate` — Resolve only from the ontology; abstain and flag a gap, never invent
- `assumption.disclose_defaults` — Disclose every assumed default in the answer
- `measure.period_resolution` — Resolve an unspecified period to the full available range, disclosed

ASK · a required choice is open with no safe default — ask

- `sales.ask_currency_when_ambiguous` — a question implies a single-currency total but names no reporting currency and the rows span several
- `ambiguity.ask_dont_guess` — Ask with candidates when a required dimension is underspecified

REFUSE · the question asks for something the model must not answer that way

- `store.online_is_not_a_market` — producing a sales-by-country / by-market breakdown
- `sales.no_double_count_header_detail` — choosing a table to sum sales from
- `capability.refuse_missing_dimension` — Refuse to slice by a dimension the data does not carry

## Options — what a question may leave open

For each choice a question can leave open, the policy says whether the model may assume a default,
must ask, or must refuse. Worst-wins: a **REFUSE** gate overrides an assumable default on the same
question.

REFUSE · hard gates — worst-wins, these override any default on the same question

- `source.double_count` — sum EITHER `sales` OR orders x orderrows, never both — a query that sums both is REFUSED (doubles revenue).
- `market.online_channel` — in a by-country breakdown, 'Online' is a CHANNEL not a market — segregate and disclose, or exclude with a note.
- `capability.missing_dimension` — REFUSE dimensions the data does not carry (salesperson, supplier, promotion); name what it does carry.

COMMIT · safe defaults — assumed and disclosed

- `currency.basis` — no reporting currency named and rows span several -> convert each line to the disclosed base currency (Quantity x NetPrice x ExchangeRate) BEFORE summing; or ASK via sales.ask_currency_when_ambiguous.
- `measure.gross_vs_net` — unqualified 'sales' -> NET (Quantity x NetPrice); report GROSS only when explicitly asked, disclosed.
- `period.window` — no time window -> the full available range, disclosed; ASK if a specific window is implied.

## Limitations — what it will not do

The model answers only from what it carries, and it says so plainly rather than approximating:

- `store.online_is_not_a_market` — treat CountryName='Online' as a CHANNEL, not a country: separate it out and disclose, or exclude with a note
- `sales.no_double_count_header_detail` — sum EITHER the denormalized `sales` table OR orders x orderrows — never both; they are the same order lines in two shapes
- `capability.refuse_missing_dimension` — REFUSE and name what the model DOES carry: brand, product, category, store/country, currency, date
- `source.double_count` — sum EITHER `sales` OR orders x orderrows, never both — a query that sums both is REFUSED (doubles revenue).
- `market.online_channel` — in a by-country breakdown, 'Online' is a CHANNEL not a market — segregate and disclose, or exclude with a note.
- `capability.missing_dimension` — REFUSE dimensions the data does not carry (salesperson, supplier, promotion); name what it does carry.

## Examples

A committed answer, with its disclosure:

```text
ask "what were our total sales?"
```

> COMMIT — net revenue, each line converted to the base currency and summed; the answer discloses
> "net of discount · base currency USD · all channels · full available period."

An answer that asks first:

```text
ask "total sales in a single currency"
```

> ASK — the rows span AUD, CAD, EUR, GBP and USD and no reporting currency was named; the model
> offers the five and the disclosed default rather than silently picking one.

A refusal, with what the model **does** carry:

```text
ask "sales by salesperson"
```

> REFUSE — the model carries no salesperson dimension; it names what it can slice by instead
> (brand, product, category, store/country, currency, date).

## See also

Concepts —
- `ontology/concepts/catalog/brand.yaml`
- `ontology/concepts/catalog/product.yaml`
- `ontology/concepts/finance/currency.yaml`
- `ontology/concepts/finance/margin.yaml`
- `ontology/concepts/geography/store.yaml`
- `ontology/concepts/order/order.yaml`
- `ontology/concepts/sales/sales.yaml`
- `ontology/concepts/time/period.yaml`

Rules & policy —
- `ontology/rules.yaml`, `ontology/query_rules.yaml`, `ontology/edges.yaml`

Joins —
- Sales → Product (`sales.ProductKey = product.ProductKey`)
- Sales → Store (`sales.StoreKey = store.StoreKey`)
