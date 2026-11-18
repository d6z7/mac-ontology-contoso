# Customer

The account of concept Customer.

## Overview

A person on Contoso's customer register: 104,990 of them, each with a name, a birth date and a place — continent, country, state, city. HALF OF THEM HAVE NEVER BOUGHT ANYTHING. 52,189 of the 104,990 appear on a sale; 52,801 appear on none, so "a customer" and "a buyer" are two populations and the register is the wider one. THIS IS BY DESIGN, NOT A DEFECT: the upstream generator splits CustomerWeight from OrderWeight precisely so a large register carries a small order volume (`references/upstream_semantics.md`). A bare customer count must say which population it counted. Read from the rows: Jamie Hetherington, Tasmania, born 1946. THE PLACE IS SERVED AS A CODE, AND THE COLUMN SAYS SO. `country_code` carries `AU`, `CA`, `DE` — ISO-3166 alpha-2, the same spelling `dim_location` and `dim_store` use. The landing also carries the long name — `customer.CountryFull`, Australia, Canada, measured one-to-one over all eight — and the operator ruled NOT to serve it yet: the code is named honestly first. Until it is served there is nothing here to rule `label_of`, so a question asking for countries is answered in codes. IT IS A VERSION OF A PERSON. `valid_from` and `valid_to` are on every row, so this dimension keeps HISTORY. "Customers as they are today" and "the customer a 2017 sale was made to" are different rows, and reading one as the other re-attributes old sales to new addresses.

## Identity

A surrogate `customer_key` annotated by `customer_name`, which is 99,200 distinct over 104,990 rows — near-unique and NOT unique, so it identifies nothing on its own.

## Grain

one row per customer version (customer_key)

## Customer.as_of_now_or_sale

they return DIFFERENT rows, and the difference is every customer who moved

- **when** — customers are joined to sales over a period
- **then** — say whether it means the customer as they are now or as they were at the time of sale
- **never** — ignore the validity window because both readings return rows

## Cites

- `dataset:dim_customer.customer_key`
- `dataset:dim_customer.customer_name`
- `dataset:dim_customer.continent`
- `dataset:dim_customer.country_code`
- `dataset:dim_customer.state`
- `dataset:dim_customer.city`
- `dataset:dim_customer.gender`
- `dataset:dim_customer.birth_date`
- `dataset:dim_customer.valid_from`
- `dataset:dim_customer.valid_to`
- `dataset:dim_customer.valid_end`
- `rule:Customer.active_on_the_reference_date`
- `rule:Customer.age`
- `rule:Customer.as_of_now_or_sale`
- `rule:Customer.per_customer`
- `rule:Customer.register_not_buyers`
