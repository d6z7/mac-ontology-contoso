# Customer

> The human account. The declaration is `ontology/concepts/customer.yaml`; read this first,
> whole, then compare it against that file.

## Overview

A person on Contoso's customer register: 104,990 of them, each with a name, a birth date and a
place — continent, country, state, city. HALF OF THEM HAVE NEVER BOUGHT ANYTHING. 52,189 of the
104,990 appear on a sale; 52,801 appear on none, so "a customer" and "a buyer" are two populations
and the register is the wider one. THIS IS BY DESIGN, NOT A DEFECT: the upstream generator splits
CustomerWeight from OrderWeight precisely so a large register carries a small order volume
(`references/upstream_semantics.md`). A bare customer count must say which population it counted. Read from the rows: Jamie Hetherington, Tasmania, born 1946. THE
PLACE IS SERVED AS A CODE, AND THE COLUMN SAYS SO. `country_code` carries `AU`, `CA`, `DE` —
ISO-3166 alpha-2, the same spelling `dim_location` and `dim_store` use, and it was called
`country` until 2026-09-30. A list of countries came back as eight two-letter codes and nothing in
the bundle said they were codes, because the name claimed they were countries (RC02). The landing
also carries the long name — `customer.CountryFull`, Australia, Canada, measured one-to-one over
all eight — and the operator ruled NOT to serve it yet: the code is named honestly first. Until it
is served there is nothing here to rule `label_of`, so a question asking for countries is answered
in codes. A2: a structured thing with identity, none of the other five → `entity`. A2's own worked
example, and the one place the residual class is right: a person is not a lookup. IT IS A VERSION
OF A PERSON. `valid_from` and `valid_to` are on every row, so this dimension keeps HISTORY.
"Customers as they are today" and "the customer a 2017 sale was made to" are different rows, and
reading one as the other re-attributes old sales to new addresses.

## Identity

Established as `fk_name`.

The canonical key is a COLUMN fact and is not repeated here; this says only HOW identity is
established. A surrogate `customer_key` annotated by `customer_name`, which is 99,200 distinct
over 104,990 rows — near-unique and NOT unique, so it identifies nothing on its own.

## Grain

one row per customer version (customer_key)

## ambiguity.as_of_now_or_as_of_sale

they return DIFFERENT rows, and the difference is every customer who moved

The declaration states this executably as well, because this rule has no body yet:

- **when** — customers are joined to sales over a period
- **then** — say whether it means the customer as they are now or as they were at the time of sale
- **never** — ignore the validity window because both readings return rows
