---
name: edges-and-rules
description: Wire concepts together and state what must hold, using the framework's 22-pattern index rather than guessing joins. Use as step P9.
---

# P9 · EDGES AND RULES — how concepts relate, and what must hold

An edge says a fact can be joined to a dimension, and how. A rule says something that must be true
of the data or of any query over it. Together they are what lets an engine traverse from a question
to a defensible number without guessing a join — which is the whole point of having an ontology
rather than a schema.

This step was measured as the kit's worst: three operators holding an **identical** concept and
dataset inventory produced 5 edges, 12 edges, and 16 that were never written down. Two operators
*without* the kit produced 8 and 8, by the same route, because they used an instrument the kit had
not told them about. Read the next section before anything else.

## When

After P7 (concepts) and P8 (measures). You need the concept inventory settled, because an edge's
endpoints are **concepts, not tables**, and you need the datasets' declared foreign keys.

## First: use the framework's pattern index — the kit does not replace it

`reference_manual/patterns/` holds **22 named modeling patterns**, and `MODELLERS_COOKBOOK.md`
holds the anti-patterns that `check_cookbook_smells` enforces. They are the framework's own
modeling instrument and they are better than any summary this skill could give.

Go and read the pattern that matches your shape **before** you author edges. The ones that decide
edge structure most often:

- `role_playing_dimension` — one calendar joined three times as order date, ship date, due date.
  The commonest cause of an edge count being wrong in either direction.
- `degenerate_dimension` — an identifier on the fact with no dimension behind it. Not an edge.
- `multivalued_bridge`, `associative_entity` — many-to-many, which is never a single edge.
- `recursive_hierarchy`, `supertype_subtype` — self-reference and specialization.
- `scd_type_2`, `bitemporal` — a join that is only correct with a validity predicate.

**The kit routes; the framework instructs.** If a skill here and the pattern index disagree, the
pattern index is right and this skill has a bug worth reporting.

## Do

1. **Enumerate the candidate joins from the DECLARED foreign keys**, not from column-name
   similarity. Two columns called `customer_id` are a hypothesis; a declared foreign key is a fact
   you recorded in P5.
2. **Decide what is an edge.** An edge is a **fact ↔ dimension** join. Keep the file thin:
   - an attribute of a dimension is a **column on that dimension**, not an edge
   - a rollup derivable from a column (country → region) is **concept structure**, not an edge
   - a join you cannot confirm is **not wired** — record it as planned, not as fact
3. **Name the endpoints as concepts.** `from` and `to` each carry `concept`, with `role` and
   `cardinality`. The schema requires `concept` on every endpoint. An edge between tables is a
   schema fact; an edge between concepts is a meaning fact, and only the second survives the table
   being renamed.
4. **Carry the physical realization in `join_rule`** — the SQL predicate, on the real foreign-key
   columns, using the **dataset file stems** as relation names (the canonical name from
   the `ontology-shared-facts` skill), never the physical view names.
5. **Give every edge a stable `edge_id`** and a `level` and `type`. An edge that changes id when it
   is re-authored cannot be referred to by a rule, a test, or a decision record.
6. **Apply the role-playing pattern explicitly** when one dimension is joined more than once. Each
   role is a separate edge with its own `role` on the endpoint — not one edge used three ways, and
   not three copies of the dimension.
7. **Author the rules.** A rule states what must hold. Keep each one about *one* thing, bind it to
   the columns it constrains, and do not restate a law the framework already states — a concept
   repeating a universal law has written a copy, not a contract.
8. **Record what you deliberately did not wire**, with the reason. A join you rejected for a good
   reason is knowledge; absent, the next operator re-derives it and may decide differently. This is
   the single cheapest defense against the 5-versus-12 spread this step is known for.

## Produces

- `ontology/edges.yaml` — `metadata` plus `edges[]`, each with `edge_id`, `level`, `type`,
  `endpoints.from/to` (concept-named), and `join_rule`. `planned_edges[]` for the confirmed-later.
- `ontology/rules.yaml` — the typed rules.
- **Write the file.** One measured walk authored sixteen edges and shipped none of them, because
  the work lived in its notes and never reached `ontology/`. An edge you reasoned about is not an
  edge.

## Accepted by

- **`check_references`** — every concept, relation and column an edge or rule names must resolve.
  Dangling references are how an ontology passes review and fails at answer time.
- **`check_rule_reference_basis`** — a rule that names another concept must have a reason to. A
  cross-concept reference without a basis is usually a modeling error wearing a rule's clothes.
- **`check_canon_binding`** — a bound rule's prose must still say what its canon renders. The prose
  and the machine form must not drift apart; the prose is what a human reviews.
- **`check_enumeration_closure`** — a closed value set may not contain a member you admit you
  guessed. If you inferred it, it is not closed.
- **`check_common_rules`** — a concept restating a law MAC already states is a copy, not a contract.
- **`check_cookbook_smells`** — the cookbook's anti-patterns, enforced rather than described.

## Getting it right first time

- **Edge count is a symptom, not a target.** Do not aim for a number. Aim for: every measure can
  reach every dimension a question will slice it by, in one hop, without a probe. Then count.
- **The role-playing miss is the classic.** A single `date` dimension joined by three different
  date columns is three edges, each with its own role. Missing it silently answers "revenue by
  month" against the wrong date and no gate can catch it.
- **A degenerate dimension is not an edge.** An order number on the fact, with no order dimension,
  is a column. Wiring it as an edge invents a table.
- **Many-to-many is never one edge.** Reach for `multivalued_bridge` or `associative_entity`; a
  direct edge across a many-to-many silently multiplies every measure you aggregate through it.
- **If a rule needs a paragraph to justify, it is probably two rules.**

## What stays your judgment

- **Which joins a question will actually need.** The gates check that the edges you wrote are
  valid; nothing checks that the set is *sufficient*. Only the question scope tells you that, and
  if no question scope exists, say so rather than guessing — every measured operator invented one
  silently and they invented different ones.
- **Where a rollup is concept structure versus an edge.** Both can be made to work; they are not
  equally maintainable.
- **Whether a rule expresses what the business means.** A rule can be well-formed, bound, green,
  and wrong. No gate will tell you. This is the SME's to confirm, and it must be asked rather than
  assumed.
