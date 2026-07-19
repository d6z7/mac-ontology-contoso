<!--
Article 1 — VERSION 2 (hardened after a 3-lens adversarial critique: thesis-fidelity, RDF-balance, register/honesty/flow).
Changes vs v1: earned the "app = meaning" bridge via the operator's own "business process" wording; RDF section
now credits the crown jewels (shared identity, inference) + concedes RDF still wins cross-organization, targets
human-ILLEGIBILITY not formality, present-tense (not an obituary); number corrected to the reproducible $223.6M
(committed demo query); opening heading made concrete; two overclaims dialed back. Public/Contoso-only.
Number format: period-decimal ($223.6M) — deliberate for a public English/USD piece.
-->

# The Layer You Deleted

*An LLM can replace most of your application layer. The part it can't replace is the part that made the numbers mean anything.*

## Two layers, for forty years

Business software has had the same shape for four decades. A **database** to hold the data. An **application** on top of it to run the business process and put it in front of the user. ERP, CRM, the internal tool nobody likes — every one is a version of that two-layer stack.

It's easy to picture the application as "the screens." But the screens were the least of it. To run the business process, the application had to encode the **business logic** — and that logic was never separate from what the data *meant*. The database has a column called `NetPrice` and a column called `UnitPrice`; it was the application that knew *"revenue" means net, not gross*, that *a total must be converted to one currency before you add it up*, that *these two tables are the same sale recorded twice and must never be summed together*. The rules the application ran the business by **were the meaning of the data, in executable form.**

So the two-layer stack was really this: the database stored the facts, and the application held what the facts meant. Keep that split in mind — because an LLM is about to take over one half of it.

## Then the LLM arrived and took over half of it

An LLM can now do three things that used to require the application:

- it can **read the database** — the tables, the columns, the relationships;
- it can **understand a question** in plain language;
- it can **write the SQL** to answer it.

That's most of the *reporting* face of an application — the read side, where you ask the data a question and get it back on a screen. (The process side — the transactions, the writes — is a longer story; the same argument applies, but the read side is where LLM-on-the-database is most seductive and most silently wrong.) So the obvious move, the one nearly everyone is making, is to point the LLM straight at the database and delete the application. Why build screens and query logic when you can just *ask*?

And it works — right up until it doesn't.

## What you deleted was the meaning

Ask the LLM-on-the-database a simple question:

> "What were our total sales?"

You'll get a number, fast and confident. And it's very likely wrong — not because the SQL is broken (the SQL is perfect), but because *"total sales" was never a database question.* It's a business decision. Net or gross? Which currency, when the rows span five of them? Summed from which table, when the warehouse holds the same sale two ways? The application used to make those calls. You deleted it. So the LLM makes them instead — silently, invisibly, differently from one run to the next — and hands you a number with no asterisk.

Follow where each piece went. The data is still in the database. The language and the SQL moved to the LLM. But the **meaning** — the business logic the application was quietly carrying — is now homeless. It isn't in the database; it was never data. It isn't in the LLM; it's *your* company's private meaning, not general knowledge the model was trained on. And it isn't in the application, because you removed that.

That homeless meaning is the gap everyone is walking into. Something has to take over the application's old job of holding what the data means. **That something is an ontology — a semantic layer.** Not the screens; the meaning that used to sit behind them.

## We have tried to build this before — RDF and knowledge graphs

And here it pays to be fair, because giving meaning a home *outside* the application is not a new idea — it's exactly what the semantic web set out to do. RDF, OWL, and knowledge graphs have been building that layer for two decades, and much of what they get right still holds:

- meaning should be **explicit** — in its own layer, not buried in application code no one reads;
- the **relationships** between concepts are first-class, not an afterthought (what property-graph databases are genuinely great at);
- a concept can have one **shared, unambiguous identity** that many systems — even different organizations — point at;
- a machine can **derive and check** the consequences of the meaning, not just store it.

Those last two are real powers a layer of English prose does *not* replace. If your problem is meaning shared and resolved across organizational boundaries, RDF still wins.

So what actually changed? Not the value of an explicit, governed semantic layer — that's more relevant than ever. One *constraint* changed. RDF and OWL were built machine-first: until recently a machine couldn't read a sentence, so meaning had to be encoded in a form a reasoner could traverse — which the person who actually knows what "revenue" means, the finance analyst, can't read or write. The meaning got translated, by specialists, into an artifact the expert could no longer check. And meaning the business can't see is meaning that drifts.

The LLM lifts *that* constraint — the illegibility, not the formality. A machine can read prose now, so for a single business's internal meaning, the semantic layer can be disciplined English the domain expert writes and the AI reads. Keep the good part of the idea — explicit, shared, governed meaning. Drop the part that was there mainly to make it machine-consumable at the cost of being human-unreadable.

## "Just write it in English" is not the whole story

If it were, the replacement for the application would be a wiki — and wikis don't answer questions. What replaces it is a small, disciplined structure. The trick is a ladder: put each piece of meaning on the *lowest* rung that can carry it.

- **Schema** for what's structural — a column, a key, a join.
- **Data / lookups** for what's enumerable — the list of valid brands, the five currencies.
- **Decision tables** for what's mechanical — this policy tier, that default.
- **Prose** only for genuine judgment — what "total sales" *means*, when to refuse, what to disclose.

Most of what people call "business rules" is really structure or data in disguise, and belongs lower on the ladder where it's cheap and unambiguous. Prose is reserved for the small, contested set of decisions a bare LLM gets silently wrong — the exact decisions the application used to own. (This is still formalism, note — the point was never to abandon structure, only to stop making it unreadable.)

## What it looks like when it works

Point that semantic layer at the same question — *"what were our total sales?"* — and you don't just get a number. You get a number **with its reasoning disclosed**:

> **$223.6M** — net revenue, each line converted to USD before summing, all channels, full available period.
> *(Assumed: net, not gross; base currency USD. Say so if you meant otherwise.)*

Three things just happened that a bare LLM won't do:

- it **committed** to one reading — and told you which;
- it **disclosed** the assumptions it made to get there;
- and had you asked for something the data can't answer — "sales by salesperson," a dimension the model doesn't carry — it would **refuse and say so**, instead of inventing a plausible-looking column.

Commit, disclose, refuse. That's the difference between an answer you can **defend** and a number you have to go verify by hand. It's also, not by accident, what a well-built application used to guarantee — now stated as explicit meaning instead of buried in code.

## The honest part

This is promising, and in development — not a finished product with a checkmark. The demo runs on a public, openly-licensed dataset so it can be shown in the open, and the semantic layer driving it is a few dozen lines of readable definitions, not a research artifact.

There's a catch the next two articles take on. Meaning written in English is only trustworthy if it can't quietly drift — so the next piece is how you keep this layer honest: generated from a single source, tested against a known-answer corpus, and governed so it can't silently regress. The one after is how it grows — because a good semantic layer will tell you, out loud, where it's uncertain and what it doesn't yet cover.

But the core claim is simple. The application always did two jobs: it ran the business process, and it put it on a screen. The LLM can rebuild the screen and the queries. What it can't rebuild is the business logic those screens encoded — the meaning of your data. That still has to live somewhere. Give it a home you own, and make the AI answer from it.
