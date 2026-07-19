<!--
Article 4 — "Meaning That Grows" (operator thesis, 2026-07-19). The ontology is EXTENDABLE; business
logic is a CONTINUOUS EVOLUTION of rules; stated in a HUMAN-UNDERSTANDABLE way; readable by BUSINESS
EXPERTS, not only data/software engineers. Worked on the live Contoso demo: the model REFUSES a profit
question (meaning gap), a person AUTHORS the Margin measure (a contested business judgment, in prose),
the same question COMMITS — and every answer shows the rules that FIRED and the shortcuts (DEAD ENDS)
they refused. Honest ending: meaning gaps you can close by authoring; data gaps (salesperson) you can't.
Visuals: ask-refuse-before · 04-margin-extension (definition+diff) · margin-commit-after · 04-trace-fired-deadends.
No "rot" (operator's word ban).
-->

# Meaning That Grows

*The best models tell you where they are thin. Then you teach them — and the teaching is prose a person can read, not code an engineer has to write.*

## The gap the model hands you

The last piece ended on the leftover: a model built this way will tell you, out loud, exactly where it is still thin. Here is what that looks like when you take it up on the offer.

Ask the Contoso model *"which category is the most profitable?"* and it does not answer. It **refuses** — and it tells you why, and how to fix it:

> *'profitable' is not defined in the model. The ontology defines Sales (net revenue), but not Profit or Margin. The data carries UnitCost, but no Profit concept composes it with revenue. To rank categories by profitability, define a Profit measure in the ontology's concepts layer first.*

That is not a breakdown. It is the model drawing you a map of its own edge. The cost was in the warehouse all along; what was missing was the *meaning* — a decision nobody had made yet.

> **[visual — the refusal: "'profitable' is not defined in the model" (ask · before)]**

## You author the meaning, not code

So you make the decision. And here is the thing worth sitting with: *what "profit" means is a business judgment, not a technical one.* Gross margin or net? Which costs count — only cost of goods, or freight and overhead too? Net of discount, or list price? The data cannot settle any of it. Someone who understands the business has to.

You write that decision down — in one small file, in plain sentences:

- **Margin** is a measure: net revenue minus cost of goods, per line, converted to one currency, then summed.
- **Gross, not net** — only cost of goods (`UnitCost`) is subtracted; the data holds no operating costs, so we don't pretend to a net-profit figure.
- **Revenue net of discount** — the same basis as Sales, so the two measures agree.
- **Convert before summing** — never add profit across five currencies raw.

Each of those is a rule shaped *when → then → never* — a sentence, not a function. The person who owns what "profit" means can read it, and argue with it, without opening the interpreter.

> **[visual — the edit: the Margin definition beside the two-file git diff]**

## It grows

Nothing else changed. Not the data, not the interpreter, not the model — one file of meaning.

Ask the same question again: **Computers, $53.7M** — a ranked, executed answer that discloses every judgment you just made. Refuse became commit, from a single edit that the framework's own checks — schema, references, shape — accept.

And something quieter grew with it. The system's generated manual — the list of exactly what you are allowed to ask — now reads `MEASURE := net sales | gross sales | gross profit`. You didn't only add a concept. **The set of questions the system can answer expanded** — and the proof of it regenerates itself, so it can't quietly disagree with what the model actually does.

> **[visual — the commit: "Computers $53.7M", assumptions disclosed (ask · after)]**

## Every answer keeps its work

Growth is only trustworthy if you can watch it work. So every answer carries its trace — the rules that **fired**, and the shortcuts they **refused**.

For the profit question, six rules fired — three of them the ones you had just written. And there were four dead ends. The model was *stopped* from reporting net profit (using costs it does not have), from taking cost off gross revenue (which overstates by the whole discount), from summing raw across currencies. You see not only what it did, but what it was prevented from doing — and which rule did the preventing.

> **[visual — the trace: rules that fired vs. dead ends]**

This is why the rules matter more than the code. They are the business logic, out in the open, accumulating one legible sentence at a time. A controller can read `margin.gross_basis_disclosed`, decide *"no — for us, freight belongs in cost of goods,"* and that is a one-line change to the **meaning** — not a ticket handed to engineering. The domain expert edits the domain.

## Meaning gaps and data gaps

There is an honest limit, and the model knows it.

Ask *"sales by salesperson"* and it refuses too — but that refusal will **never** become a commit, however much meaning you author. There is no salesperson in the data. That gap is in the warehouse, not the ontology.

This is the quiet strength of the whole approach: the model can tell you *which kind of gap you are looking at.* A missing **measure** — profit — is a gap in meaning, and you close it by writing the meaning down. A missing **dimension** — salesperson — is a gap in data, and no amount of authoring will conjure it. A refusal you can *act on* is worth more than a confident number you then have to go and check by hand.

## What this really is

Step back from the demo for a moment. Everything your business knows that the data does not say — what *profit* means for you, which sale counts, why "Online" is a channel and not a country — has always lived in people's heads, and in the application code that quietly hard-wired their decisions long after the people moved on. This is a way to write it down instead. Not as a diagram for architects, not in a formal notation for engineers — but as plain descriptions, in your own words, one idea at a time.

That is all the ontology is: a handful of small files — plain YAML you could read over a colleague's shoulder — each one a **unit of meaning**. A concept, a measure, a rule, stated the way you'd explain it to someone on their first day. You describe what things mean; the framework takes care of the rest — checking that every definition is well-formed and that every reference points at something real, so the meaning holds together as it grows. The person who understands the business writes down the meaning of the business, and keeps writing it, one plain sentence at a time, as the questions get harder.

And once it is written down, it is *yours*. The meaning is no longer trapped inside one application, one database, or one vendor's model — it is captured, checkable, and portable. You described it once, in language a person can read; now it can answer questions, explain how it reached them, refuse what it shouldn't, and run on whatever technology you already have.

That is the whole idea. **Capture the meaning — and everything else is just where you choose to point it.**
