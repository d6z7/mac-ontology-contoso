# ask(1) — Contoso demo ontology

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

{{meta}}

## Concepts

The objects you can ask about. Each has one canonical definition and binds to real columns.

{{concepts}}

## Measures — the contested total, made explicit

"Total sales" is not one number. The ontology names each defensible reading as a **derived measure**
with its exact formula and the guardrails that keep it meaningful, so the choice is inspectable
rather than guessed:

{{measures}}

The rule that matters most is **convert-before-sum**: a raw `SUM(NetPrice)` across mixed currencies
adds incompatible units and is meaningless; multiplying each line by its `ExchangeRate` first makes
the total comparable.

## Synopsis

The compact grammar — how the model is invoked. Every flag here is optional with a disclosed default,
because this model declares no mandatory dimension and no mutually-exclusive choices; a richer model
would also carry required and alternative-group flags. The allowed values and the full property list
are in the whitelist below.

```text
{{synopsis}}
```

## What a question can contain — the whitelist

Beyond the measure and its reading, a question may name any of these dimensions and properties to slice
or group the total. This is the model's **question grammar** — an explicit whitelist, generated from
the join graph and the registers, not hand-listed. Every property is either **closed** (its allowed
values named below, straight from the register that pins it) or **open** (any value of the given type):

{{ask_grammar}}

Only two properties are closed — **Brand** and **Currency**, because a register pins their values;
everything else, including **period** (grounded on the order date, grain day → month → quarter → year),
is open. Because the whitelist is generated from the model, it is always exactly as wide as the
ontology: the `period.window` gate in the options below now has a matching axis to act on. Add a
concept and its properties appear here — which is precisely how the model grows.

## Decision lanes

Every rule carries a **kind** that sorts it into a lane — this is how the model decides whether to
answer, ask, or refuse:

{{decision_lanes}}

## Options — what a question may leave open

For each choice a question can leave open, the policy says whether the model may assume a default,
must ask, or must refuse. Worst-wins: a **REFUSE** gate overrides an assumable default on the same
question.

{{options}}

## Limitations — what it will not do

The model answers only from what it carries, and it says so plainly rather than approximating:

{{limitations}}

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

{{see_also}}
