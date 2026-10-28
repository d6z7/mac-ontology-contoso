# CLONED on 2026-09-29 from mac-ontology-contoso@e7465b1 acceptance/tools/generate_shape_oracles.py; ROOT is the bundle this file sits in
"""Derive shape+outcome oracles from the QUESTION TEXT, mechanically.

AUTHORITY. Everything asserted here comes from the question's own words, resolved through the
same registers the interpreter resolves them through. Nothing is read from the planner, nothing
is read from a previous run, and no expected VALUE is ever written. That is what keeps these
oracles independent of the engine they grade.
"""
from __future__ import annotations
import os
import pathlib
import json, re, sys, yaml
from pathlib import Path
from intent_killtest import build

ROOT = pathlib.Path(os.environ.get("MAC_BUNDLE_ROOT") or pathlib.Path(__file__).resolve().parents[2])  # the bundle this tool sits in


def _outcome_classes() -> tuple[set[str], set[str]]:
    """(canonical outcome classes, the gate subset) READ from mac_vocabulary.yaml#outcome_class.

    THE LAW IS READ, NEVER RESTATED. The first bundle's copy of this tool wrote `ANSWER` — a
    spelling the closed vocabulary does not declare (its member is `COMMIT`) — and a gate set of
    six tokens of which three (`DECLINE`, `CLARIFY`, `REJECT`) are deprecated or unknown to it.
    check_outcome_class_closure measured the cost on this bundle: 302 of 308 outcome declarations
    non-canonical, all of them this tool's. The framework is found through MAC_FRAMEWORK_ROOT or
    as the sibling checkout; without it the four canonical members stand as the fallback, said so.
    """
    root = os.environ.get("MAC_FRAMEWORK_ROOT")
    candidates = [pathlib.Path(root)] if root else []
    candidates += [ROOT.parents[2] / "meaning-as-code", pathlib.Path.home() / "dev" / "meaning-as-code"]
    for c in candidates:
        vocab = c / "mac_vocabulary.yaml"
        if vocab.is_file():
            terms = (yaml.safe_load(vocab.read_text(encoding="utf-8")) or {}).get("outcome_class", {}).get("terms") or {}
            canonical = {t for t, m in terms.items() if isinstance(m, dict) and m.get("status") == "canonical"}
            if canonical:
                return canonical, canonical - {"COMMIT"}
    print("  (framework vocabulary not located; the four canonical outcome classes stand as the fallback)", file=sys.stderr)
    return {"COMMIT", "ASK", "REFUSE", "BLOCK"}, {"ASK", "REFUSE", "BLOCK"}


CANONICAL, GATE = _outcome_classes()
ACTIVITY_RE = re.compile(
    r"\b(sold|sell|sells|bought|buy|buys|placed|order|orders|ordered|revenue|sales|quantity|"
    r"spent|purchase[ds]?|trend|growth|value)\b", re.I)
WHEN_RE = re.compile(r"^\s*when\b", re.I)
PERIOD_RE = re.compile(r"\b(20\d\d|q[1-4]\s*20\d\d|last \d+ years?|january|february|march|april|"
                       r"may|june|july|august|september|october|november|december|monthly|"
                       r"year-over-year|quarter)\b", re.I)


def _canonical(outcome: str) -> str:
    """An outcome this tool emits must be a canonical member of the closed vocabulary — refused
    here, loudly, rather than written and found by the gate."""
    if outcome not in CANONICAL:
        raise SystemExit(f"outcome {outcome!r} is not a canonical outcome class ({sorted(CANONICAL)})")
    return outcome


def value_index(registers) -> dict[str, list[tuple[str, str]]]:
    """search term -> [(concept, column)] from the DECLARED SEARCH COLUMNS only.

    NOT EVERY CELL, and the difference is a false assertion. The first version indexed every
    column of every register row, so a three-digit numeral in a question matched a SURROGATE
    KEY: "Countries where average order value exceeds 500" resolved `500` to StoreKey 500
    (Contoso Store Kansas) and asserted the SQL must constrain a store. A correct answer would
    have failed the pin.

    A register DECLARES which of its columns a word is looked up through — `search`, with
    `display_label` as what a reader is shown — and those are the only columns a question can
    legitimately be matched against. The surrogate, `source_view`, `confidence` and `note` are
    provenance: nobody names a store by its surrogate, and no question resolves through them.
    Reading the declaration instead of every cell is the same discipline `period_column` and
    `pin_column` below already follow.
    """
    out: dict[str, list[tuple[str, str]]] = {}
    for reg in registers.loaded:
        decl = reg.declaration
        lookupable = {c.lower() for c in (*decl.search, *decl.display_label)}
        for row in reg.rows:
            for col, cell in row.cells.items():
                if cell and len(cell) > 2 and col.lower() in lookupable:
                    out.setdefault(cell.strip().lower(), []).append((decl.concept, col))
    return out


def period_column(idx) -> str | None:
    """The column a bundle declares as its reporting period — from the `period` field role.

    NOT A LITERAL. The first draft typed a column name here, which is the hardcoding this estate
    keeps re-finding: the oracle would have been about one bundle and silently wrong on any other.
    """
    for c in idx.concepts.values():
        for col, role in (c.grounding.field_roles or {}).items():
            if role.rsplit(".", 1)[-1] == "period":
                return col.lower()
    return None


def pin_column(concept_name: str, idx) -> str | None:
    """The column a filter on this concept constrains — its identity column, from grounding."""
    c = idx.concepts.get(concept_name)
    if not c:
        return None
    key = c.identity.canonical_key
    fr = c.grounding.field_roles or {}
    if key and key in fr:
        return key
    return next((col for col, role in fr.items()
                 if role.rsplit(".", 1)[-1] == "dimension"), None)


def _default_reading_owner(text: str, idx) -> str | None:
    """A concept the question's words reach whose contract DECLARES how to read it."""
    low = text.lower()
    hits: list[tuple[int, str]] = []
    for name, c in idx.concepts.items():
        reading = getattr(getattr(c, "contract", None), "default_reading", None)
        if not reading:
            continue
        words = {name.lower()} | {w for w in re.findall(r"[a-z]+", (c.label or "").lower())}
        # the declared reading names the words it claims: "an unqualified 'sales', 'revenue' ..."
        words |= {w.strip("'\"") for w in re.findall(r"[\'\"]([a-z ]{3,20})[\'\"]", reading.lower())}
        if any(re.search(rf"\b{re.escape(w)}\b", low) for w in words if w):
            # TWO CONCEPTS CAN CLAIM THE SAME WORD — this bundle's gross and net measures both
            # answer to "sales". The tie is broken by the declarations themselves: one of them
            # says "THIS IS THE DEFAULT" in as many words, and the other says to report it only
            # when the question asks for it. Reading that is not a preference, it is the rule.
            hits.append((0 if "this is the default" in reading.lower() else 1, name))
    return min(hits)[1] if hits else None


def derive(q: dict, idx, registers, vidx) -> dict:
    text = q["question"]
    low = text.lower()
    pins: list[str] = []
    why: list[str] = []
    review: list[str] = []

    # 1. a VALUE named in the question that a declared register resolves
    dim_words = {c.lower() for c in idx.concepts}
    for term, hits in vidx.items():
        m = re.search(rf"\b{re.escape(term)}\b(\s+(\w+))?", low)
        if not m:
            continue
        concept = hits[0][0]
        follower = (m.group(2) or "").rstrip("s")
        # "the ONLINE STORE" — 'online' is a value in the Country register (a sentinel), and the
        # question means a store. A register hit qualified by ANOTHER concept's name is not a safe
        # assertion, so it is reported for review instead of pinned. An oracle that asserts
        # something false is worse than one that asserts less.
        if follower and follower in dim_words and follower != concept.lower():
            review.append(f"{term!r} resolves through the {concept} register but is followed by "
                          f"{follower!r} — ambiguous, so no pin was asserted")
            continue
        # "WHEN was the first store CLOSED" — the state word names the EVENT BEING DATED, not a
        # filter on it. A correct answer reads the date column (min of the closure date) and
        # carries no status predicate at all, so a pin here would fail a right answer. Same
        # principle as the guard above, applied to the question's tense rather than its nouns.
        if WHEN_RE.match(low):
            review.append(f"{term!r} resolves through the {concept} register, but the question "
                          f"asks WHEN — the word names the event being dated, not a filter on it, "
                          f"so no pin was asserted")
            continue
        col = pin_column(concept, idx)
        if col and col.lower() not in pins:
            pins.append(col.lower())
            why.append(f"the question names {term!r}, which the {concept} register resolves, "
                       f"so {col} must be constrained")

    # 2. a PERIOD named in the question
    # THE PERIOD BELONGS TO THE FACT. "Which stores closed after 2020" names a year and reaches no
    # fact — the date it means is the store's own, not the reporting period — so pinning the
    # fact's period column there would be a false assertion. The pin is made only where the
    # question also uses an activity word, which is what puts the fact in scope.
    if (m := PERIOD_RE.search(text)) and (pc := period_column(idx)):
        if ACTIVITY_RE.search(low):
            pins.append(pc)
            why.append(f"the question names the period {m.group(0)!r} AND an activity word, so the "
                       f"reporting-period column {pc} must be constrained")
        else:
            review.append(f"names the period {m.group(0)!r} but no activity word — the date may be "
                          f"the subject's own, not the reporting period; no pin asserted")

    # 3. outcome — from the corpus's OWN tag, and then from the ONTOLOGY, which overrules it
    reg = (q.get("regression") or "")
    tags = {str(t).strip().lower() for t in (q.get("tags") or [])}
    surface: list[str] = []
    # `tags` WAS DECLARED AND UNREAD, and it cost a false expectation. This block read only
    # `regression`, so ADV-23 "Sales in Turkey" — tagged `nonexistent-value` AND `refusal`, on a
    # bundle whose data contains no Turkey at all — was given `expected.outcome: ANSWER`. A
    # correct refusal would have been graded a failure. The tags say exactly what is needed and
    # nothing looked at them; this estate is named after that defect.
    #: A THING THE BUNDLE DOES NOT HOLD IS ANSWERED, NOT WITHHELD — operator ruling 2026-10-24.
    #:
    #: Verbatim: "refusal here would not be the right answer ... the answe would be no/none/NA ...
    #: or anything that describes that this is out of boundaries of the systme like : no evidence
    #: for ... such and such". And on ADV-23 first: "refusal is not the answer anymore. the answer
    #: is that there is no sales i turkey".
    #:
    #: THIS REVERSES "3 refusals correct" of 2026-10-19 for the whole class — ADV-23 (Turkey),
    #: MQ-13 (Hungary) and ADV-14 (an Electronics category this taxonomy does not have). I had
    #: argued ADV-14 might be different, a missing CATEGORY rather than a missing COUNTRY with no
    #: population to report as empty; the operator ruled it the same.
    #:
    #: `there is none` IS NOW SAYABLE, which it was not when the old mapping was written: stage 2's
    #: shape vocabulary had four terms and none of them was a proposition or an absence until the
    #: two vocabularies were unified on 2026-10-24.
    #:
    #: AND IT IS STILL NOT A FIGURE. A zero would assert a population that holds nothing; "no
    #: evidence for Hungary" asserts there is no such population here. The references' own 2026-10-19
    #: argument against a zero is kept and still stands.
    #:
    #: `unanswerable` KEEPS ITS GATE. A question this bundle cannot answer at all is not the same as
    #: a question whose answer is "none" — the ruling was about things that are absent, not about
    #: questions that cannot be put.
    if tags & {"refusal", "nonexistent-value"}:
        named = ", ".join(sorted(tags & {"refusal", "nonexistent-value"}))
        outcome, o_why = "COMMIT", (
            f"the corpus TAGS this {named}, and by the operator's ruling of 2026-10-24 a thing the "
            f"bundle does not hold is ANSWERED with a statement of absence that NAMES it — "
            f"'no evidence for ...' — never withheld")
    elif "unanswerable" in tags or "unanswerable" in reg:
        outcome, o_why = "REFUSE", (f"the corpus tags this {reg!r} unanswerable — not an absence to "
                                    f"report but a question that cannot be put")
    elif "ambiguity" in reg:
        # A TAG SAYS THE QUESTION IS AMBIGUOUS. IT DOES NOT SAY THE ONTOLOGY IS.
        # The first draft asserted ASK here and was WRONG on 4 of 5: this bundle declares
        # `contract.default_reading` for exactly this case — "an unqualified 'sales', 'revenue' or
        # 'total' means NetSalesAmount ... disclose the currency with the figure". A question the
        # ontology has already ruled on must be ANSWERED, with the reading disclosed; asking would
        # be the engine ignoring a declaration, which is the defect this estate is named after.
        owner = _default_reading_owner(text, idx)
        if owner:
            outcome = "COMMIT"
            o_why = (f"the corpus tags this {reg!r}, but {owner} declares a "
                     f"contract.default_reading that resolves it — the declaration overrules the tag")
            surface.append("which reading was used, and the unit or currency of the figure")
        else:
            outcome = "COMMIT"
            o_why = (f"the corpus tags this {reg!r} and NO concept declares a default_reading that "
                     f"resolves it — flagged for review rather than ruled from the question text")
            review.append(f"tagged {reg!r} with no declared default_reading found; whether the "
                          f"engine should answer, refuse or ask is an SME ruling, not a derivation")
    else:
        outcome, o_why = "COMMIT", "a well-formed request for data, with no tag saying otherwise"

    # 4. shape — from the question's own grammar
    must_not, shape_why = [], []
    if re.search(r"\b(top|highest|lowest|most|least)\s+\d+", low) or re.search(r"\btop \d+", low):
        n = int(re.search(r"\b(?:top|highest|lowest|most|least)\s+(\d+)", low).group(1))
        must_not.append(f"return a single scalar; the question asks for the top {n}, which is {n} rows")
        shape_why.append(f"'top {n}' in the question text")
    elif re.match(r"^(what|which|list|show)\b", low) and not re.match(r"^what is the\b", low) \
            and "how many" not in low:
        must_not.append("return a single scalar count; the question asks which members, not how many")
        shape_why.append("the question opens with a which/list form, not 'how many'")
    if "how many" in low:
        must_not.append("return a list of members instead of a count")
        shape_why.append("'how many' in the question text")

    return {
        "question": {"id": q["id"], "text": text, "class": "SHAPE",
                     "expected_outcome": _canonical(outcome)},
        "kind": "shape",
        "authority": "derived",
        "authority_note": (
            "DERIVED FROM THE QUESTION TEXT by genoracles.py, and from nothing else. The outcome "
            "comes from the corpus's own regression tag; the pinned columns from values the "
            "question names that a DECLARED register resolves, plus the reporting period when the "
            "question names one; the shape prohibitions from the question's own grammar "
            "(how-many vs which, and an explicit top-N). "
            "NO EXPECTED VALUE IS ASSERTED and none may be added here: this bundle has no second "
            "source of truth for what a measure means, so a value written from the ontology would "
            "test the planner against the ontology and not against the world. "
            "NOTHING WAS READ FROM A RUN. These assertions were not observed, so a capture that "
            "disagrees is evidence about the engine, not about this file."
        ),
        "expected": {"outcome": _canonical(outcome),
                     **({"shape": "refusal"} if outcome in GATE else {}),
                     #: THE ABSENCE ANSWER'S OWN SHAPE, from the one closed list both stages share
                     #: (`canonize.ANSWER_SHAPES`). Without it the oracle would assert COMMIT and
                     #: say nothing about what a correct commit looks like here.
                     **({"shape": "there is none"}
                        if outcome not in GATE
                        and tags & {"refusal", "nonexistent-value"} else {}),
                     **({"must_surface_any": surface} if surface else {}),
                     **({"must_pin": pins} if pins else {}),
                     **({"must_not": must_not} if must_not else {})},
        "derivation": {"outcome_basis": o_why, "pins": why, "shape": shape_why,
                       **({"not_asserted": review} if review else {})},
        "about": [],
        "stable": True,
    }


if __name__ == "__main__":
    idx, _ = build()
    from mac_console.ask_engine import load_bundle
    registers = load_bundle("example", ROOT.name, ROOT).registers
    vidx = value_index(registers)
    qs = yaml.safe_load(open(ROOT / "acceptance/questions.yaml"))
    out_dir = ROOT / "acceptance/oracle"
    n_pin = n_shape = 0
    for q in qs:
        o = derive(q, idx, registers, vidx)
        (out_dir / f"{q['id']}.yaml").write_text(
            yaml.safe_dump(o, sort_keys=False, width=100, allow_unicode=True))
        n_pin += len(o["expected"].get("must_pin", []))
        n_shape += len(o["expected"].get("must_not", []))
    print(f"{len(qs)} oracles written · {n_pin} pin assertions · {n_shape} shape prohibitions")
