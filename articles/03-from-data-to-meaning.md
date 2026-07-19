<!--
Article 3 — "From Data to Meaning" (worked-example reframe, operator-directed). Gets hands dirty on the
Contoso sample: 3 ingredients (MAC · DATA · LLM) → the LLM PROBES the data (structure, cardinality,
keys, values) → PROPOSES a draft ontology → but structure isn't meaning, so a person authors the
contested rules (autodiscovery-vs-authoring) → then see / test / can't-drift. No "rot" (operator's word
choice). Contoso-only, "in development" register. Visuals TBD: probe→propose→author · structure-vs-meaning · see/test/drift.
-->

# From Data to Meaning

*Where does the ontology come from? You don't write it from a blank page — the LLM drafts it from your data, and you teach it the few things the data can't say.*

## Three ingredients

The first two pieces argued for meaning as code: prose a human owns and a machine runs. Fair question — who writes it? Hundreds of concepts, by hand, from an empty file? No. You start with three ingredients and let them do most of the work.

- **MAC** — the framework: the shape a concept takes (definition, rules, edges, grounding) and the checks that keep it honest.
- **The data** — your warehouse. Ours is the public Contoso demo: a catalogue retailer, with tables for sales, orders, products and stores, selling in five currencies.
- **The LLM** — the agent that reads both.

Point the agent at the data with MAC's shape in hand, and watch what it does.

## It probes; it doesn't guess

A blank-slate model told to "represent this domain" will hallucinate a plausible ontology. That is not what happens here. Given the warehouse, the agent **probes** it — the way a careful analyst would on their first day:

- **Structure.** It lists the tables and columns and reads their types: `sales`, `orders`, `orderrows`, `product`, `store`; `NetPrice`, `UnitPrice`, `Quantity` look like amounts, `ExchangeRate` like a factor, `OrderDate` like a date.
- **Cardinality.** It counts distinct values. `CurrencyCode` has **five** — a small, closed set. `Brand` has **eleven** — closed too. `ProductKey` has thousands — an identity key, not a category.
- **Keys and joins.** It finds the foreign keys — `sales.ProductKey → product`, `sales.StoreKey → store` — and reads them as the relationships between things.
- **The actual values.** It samples them, and notices what a schema alone would hide: `CountryName` holds `"Online"` sitting next to Germany and France — a channel wearing a country's clothes; and `sales` has the same row count as `orders` joined to `orderrows` — the same facts in two shapes.

The aim is that little here is invented — each observation is meant to trace back to something the data actually says.

## It proposes a draft

From that, the agent proposes a first ontology. Sales as a measure, grounded in the columns it found. Product, Store, Currency, Brand and Period as the axes you can slice by. The foreign keys become edges. The low-cardinality columns — currency, brand — become closed value-sets, their members pulled straight from the data. It even raises the two oddities as open questions: *is "Online" a market or a channel? Should `sales` and `orders × orderrows` ever be added together?*

**A surprising amount of the structure drafts itself.** On a warehouse this size the agent can cover much of a first draft in one pass — concepts, groundings, joins, value-sets. In our runs it did a lot of the lifting. This is the part everyone hopes for.

> **[visual — the agent probes the data (structure · cardinality · keys · values) and proposes a draft]**

## But structure is not meaning

Here is where the honesty comes in — and where the person is not optional.

The probe can see that `NetPrice` and `UnitPrice` both exist. It cannot know that *"revenue" means net, not gross* — that is a business decision, and the data holds both columns with no note saying which one you report. It can see five currencies and an exchange rate. It cannot know that *summing them raw is meaningless* and you must convert first — nothing in the data says so. It can flag that `"Online"` looks strange. It cannot decide *whether to exclude it or disclose it*. It can notice the duplicate facts. It cannot rule that *you must never add the two shapes together.*

These are the contested decisions — the ones a naive text-to-SQL bot gets silently wrong — and they are exactly what the data cannot tell you. So the division of labour is clear: **the machine proposes the structure; a person authors the meaning.** The agent can draft much of the *shape*; you write the handful of rules that make the answers *correct*. That handful is small, and it is the whole game.

> **[visual — structure vs meaning: what the probe can infer / what only a person can decide]**

## Then you make it trustworthy

A draft you refined by hand is still just prose you hope is right — until you can see it, test it, and keep it from drifting.

**See it.** The model is browsable. You can read every concept in plain language, see for each kind of question whether the model commits, asks, or refuses, and drill from an answer down to the exact column it came from. You can see what the AI is set up to do before it runs — and so can the analyst who owns the meaning, without reading a line of code.

**Test it.** Keep a corpus of questions whose answers you already know, and check the model on every change. In the Contoso demo, *"What were our total sales?" → $223.6M, net of discount, converted to one reporting currency.* When the SQL faithfully executes the model and the answer still comes out wrong, the query is rarely the culprit — far more often it is a gap in the meaning: a measure you never named, a default nobody wrote down. (Sometimes it is dirty data or a stale known-answer instead — which is why a failing test is worth *reading*, not just counting.) Your question corpus becomes a regression suite for meaning — as strong as its corpus and its known-good answers.

**It can't drift.** The browsable model, the manual, the list of exactly what you can and cannot ask — none of it is hand-written; all of it is generated from the one model, so it won't quietly disagree with what the AI actually does — as long as the gate runs on every build. And a definition you have stabilised stays that way until someone deliberately revisits it — not silently, behind your back. That it runs on ordinary version control is just the plumbing that makes it true.

> **[visual — see it · test it · it can't drift]**

## What you're left with

Put it together and the job is not "write an ontology." It is: **let the machine draft the structure from the data, author the meaning the data cannot hold, then see it, test it, and keep it honest.** The agent can take on much of the tedious drafting; you do the small part that decides whether the number is right.

This is promising, and in development — the tooling is young, the corpus small. But the shape is the ordinary shape of software, finally applied to meaning: draft, review, test, version.

And the best part is the leftover. A model built this way will tell you, out loud, exactly where it is still thin — a dimension it could not ground, a question it has to refuse. Making it *grow* from there — safely, and on purpose — is the last piece.
