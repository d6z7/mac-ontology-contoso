<!--
Article 2 — "Meaning as Code" (v2, hardened after a 3-lens fidelity critique: thesis-fidelity=FAITHFUL,
confidentiality=PASS, register/flow=pass-with-edits; KR-balance lens crashed and was re-run separately).
Deck-grounded (operator's XO deck), conceptual (no GUI), Contoso-only, "promising / in development" register.
Places 4 visuals: 02-human-machine-bridge · 02-building-blocks · 02-semantic-spectrum · 02-determinism-dial.
-->

# Meaning as Code

*What the ontology actually is — and why writing it like software is the point.*

## The home, opened up

Part one argued that when you point an LLM straight at your database and delete the application, the *meaning* of your data is left homeless — and that its new home is an ontology, a semantic layer. This piece opens that home up: what's inside it, and why we treat it like code rather than documentation.

## The file is the bridge

Start with the smallest unit. Meaning lives in one file per concept — `sales.yaml`, `brand.yaml`, `currency.yaml` — and each file is a single source of truth with two audiences.

On the human side, the person who owns the meaning, the domain expert, authors and edits the file as a pull request. They approve changes with a formal sign-off, read it back as plain prose, and review it for one thing: is this semantically correct? On the machine side, the AI agent and CI/CD parse the same file, validate its structure, generate SQL from it, and execute it into an answer.

Same file, two audiences. That is the whole idea of *meaning as code*: the file is the bridge. And because it's a file in git, meaning inherits software's habits for free — versioned, diffed, reviewed in a pull request, audited over time. A change to what "revenue" means becomes a reviewable commit, not a Slack message someone half-remembers six months later.

It's worth being exact about that word, because it can mislead. **"Code" here is not a language — it's a discipline.** Just as *infrastructure as code* never meant writing servers in a programming language, *meaning as code* does not mean writing meaning in a formal logic like RDF or OWL. The meaning stays plain prose the domain expert can read; what makes it *code* is how it is **kept** — named files, versioned, diffed, reviewed, tested, checked. That is the whole trade this series argues for: drop the heavy formal languages, keep the engineering habits.

> **[visual — the file is the bridge]**

## Four building blocks

Inside, a concept's meaning is four kinds of statement, and each kind lives in exactly one place and points at the others by name.

- **Concept** — what it *means*: the definition, the class, the identity.
- **Rules** — what is *computed*: how a measure is derived, what belongs to a group.
- **Edges** — how concepts *connect*: the typed relationships between them.
- **Physical** — the *table descriptors*: columns, types, foreign keys, the seam where meaning meets data.

They cross-reference by name: a Rule declares the Concept it derives `over` and the Physical layer it is `validated_against`; an Edge names its `endpoints` and the foreign key that `realized_by` it; a Concept declares its `grounding`, the table it binds to. No box copies another. Every fact lives in exactly one layer.

Both payoffs come from that one rule. Because every reference is a named pointer and nothing is duplicated, a validator can check that they all resolve — the model is **checkable**. And because Physical is just one named layer among four, it is a single swappable seam: re-point it at another platform and nothing about what things *mean* has to change — the model is **projectable**. One discipline, two dividends.

> **[visual — four building blocks]**

None of this is a convention you enforce by hand. Meaning as code is a **framework** — MAC, for short — and, like any framework, its real work is the machinery beneath the format. Its job is to define these four blocks, ground them to the data, and give you the checks that keep them honest: referential-integrity validation, so every named pointer is proven to resolve; structural and syntactic checking; a linter; and the tooling around all of it. A format is a nice idea. A framework is what a team can actually build on — the compiler, the type-checker and the linter of *meaning*.

## Where this sits — the semantic spectrum

Isn't this just an ontology? Haven't people built semantic layers for decades? Yes — and it helps to see exactly where this sits.

There is a spectrum of how richly you can express meaning. A **controlled vocabulary** is terms with agreed definitions. A **taxonomy** adds hierarchy, so things roll up. A **thesaurus** adds synonyms and related terms. An **ontology** adds typed relations and constraints — formal semantics, meaning expressed as axioms a reasoner can traverse. Classical knowledge representation climbs those four rungs, and it climbs them well.

Meaning as code adds one more rung: **computation** — executable metric derivation. The distinction is precise. Classical KR *reasons*: it draws logical conclusions from axioms. This *computes*: it derives numbers. "Net revenue, converted to one reporting currency, then summed" is a calculation, not a logical entailment. A query layer can of course aggregate; the difference is that here the derivation is a first-class, versioned, governed part of the meaning itself — the rung the classical stack was never built around.

Grounding — binding meaning to physical data — is a *separate, orthogonal axis*. Classical KR has it too: an ABox in the graph, or OBDA mapping a query onto a relational store. Here we bind a text model to external tables. Any rung on the spectrum can be grounded; *how richly you express meaning* and *how you bind it to data* are two different questions.

And there is a plainer, practical point. RDF and OWL were built for formal, cross-organization knowledge — biomedical ontologies, data reconciled across institutions — where heavyweight logical inference earns its keep. Aimed at a single business's own data and metrics, that same machinery is heavy artillery: you take on a formal reasoner's cost, and its distance from the people who actually own the meaning, to buy inference you will rarely fire. That job wants a lighter layer — one a domain expert can read, and one that can compute.

> **[visual — the semantic spectrum]**

## What makes this different

If you take one thing from this piece, take this — and it is not a feature, it is the *goal*.

A classical ontology is built to be **reasoned over**: you model what is true, and a reasoner infers more of it. It is excellent at that, and at sharing that truth across systems and organizations. MAC is built to be **answered from**: the goal is not to infer new truths but to take a business's own question, in plain language, and return the correct number with its assumptions disclosed.

Change that one goal, and the rest is forced:

- it must be **legible**, because a person has to write and check the meaning — so it is prose, not formal triples;
- it must **compute**, because a business answer is usually a number — so it derives metrics, not just entailments;
- it must be **grounded and engineered like code**, because the answer has to be real and stay honest — so it binds to live data, and it is versioned, tested, and linted.

Other ontologies describe a domain. **MAC answers questions about it.**

## Playable, not executable

Here is the objection every engineer raises: an LLM is non-deterministic, so how can a file of meaning ever produce a trustworthy answer?

The file is a **score, not the sound**. You can't run a YAML; it is inert. But a competent player reads a score and performs it, and here the player is the AI agent and the performance is runnable SQL.

That performance has two kinds of step. Interpreting the question — mapping "how did we do last quarter?" onto a measure, a period, a filter — is a judgment call, and yes, it is probabilistic. But once the intent is resolved, the **rules render deterministically**: a SQL template with bound parameters produces the same SQL every time.

Which hands you a lever most discussions miss. The probabilistic part is the *interpretation*, and interpretation gets more determined the more complete the model is. A model that names every measure, every synonym, every default leaves the interpreter almost nothing to guess. **Model completeness and output determinism are two ends of one axis.** You don't abolish the probabilistic step; you shrink it, by filling in the meaning.

> **[visual — playable, not executable / the determinism dial]**

## Prove it, run it anywhere

This is where the model earns its keep. The model is the asset, and the AI is its **test harness** — an adversarial one. Point the agent at a question whose answer you already know; when it gets that answer wrong, the wrong answer is a signal about the *model*, not the SQL — a missing measure, an unnamed synonym, a default no one wrote down. You fix the meaning, not the query. Prove enough questions this way and you have a model you can trust.

And because the meaning is kept separate and every pointer is checkable, a proven model is not wedded to where it runs. It is designed to project onto the runtime you already have — a property graph, an RDF store, an object layer, a lakehouse. The model is the asset; the platform is just the runtime. (*How* you prove it at scale — the test corpus, and the governance that keeps a trusted model from silently drifting — is the next piece.)

> **[visual — one model, many projections]**

## The north star

Stripped to one sentence:

> Your business's meaning, authored once as code — one file per concept, owned by the people who own the meaning, in git. A human reads it; a machine executes it. Prove it with AI, and project it onto the platform you already run: the model is the asset, the AI is the test harness, the platform is just the runtime.

This is promising, and in development — not a finished product. But the shape is simple, and it is the shape of everything durable we have ever built in software: put the thing that matters in a file, give it a name, version it, test it, and let both people and machines read it. We are just doing it, at last, for meaning.
