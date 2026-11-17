# Customer.per_customer

The account of rule Customer.per_customer.

## Cites

- `concept:Customer`
- `concept:Order`
- `rule:Customer.active_on_the_reference_date.active`
- `rule:Customer.active_on_the_reference_date.registered`

## Why it is a choice (2026-11-17)

"Revenue per customer" divides by a count of customers, and the register holds three different counts: the customers
who bought (the distinct `customer_key` on the sales lines), the customers active on the reference date (rule
Customer.active_on_the_reference_date, `active`), and every customer on the register (`registered`). Half the register
has never ordered, so the three give different figures. Before this rule no declaration said which one a per-customer
figure divides by, and the corpus answered it three ways.

## The default and what decided it

`buyers`, proposed on 2026-11-17 when the contoso acceptance forks were turned into rules (operator 2026-11-17: "the
answer depends on the rule you set. you can set i one way or another way. the ruling must be transparent and must be
changeable"). It is `proposed`: it applies and is disclosed as proposed (GRAMMAR_v3 L3, Y-6).

What the operator said earlier, recorded here so the choice can be set against it:

- 2026-10-23, on the question that became MQ-23: "try adding a question: revenue per actvie cutsomer - (who placed
  order in the past) ... and see what happens then." This reads an active customer as one who has ordered: the
  `buyers` option.
- 2026-10-24, on ADV-03: "adv03 accept", approving revenue per customer by country divided by every customer on file:
  the `registered` option. That signed figure is kept in ADV-03's reference as the answer under `registered`.

Setting the default to `registered` or `active` switches ADV-03 and MQ-23 to the answers their references hold under
that option; `acceptance/tools/rule_switch_test.py` proves the figures differ.

## Not enforced by the runtime yet

`ratio.denominator_count` is unimplemented in the runtime (its key reader table: "L2 ratio legs"), so the engine does
not yet read this choice; the references follow it, and the switch test shows its effect on them.
