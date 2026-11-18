# Customer

The account of concept Customer.

## Overview

A person on Contoso's customer register, each with a name, a birth date and a place — continent, country, state, city. MANY OF THEM HAVE NEVER BOUGHT ANYTHING: a large share of the register appears on no sale, so "a customer" and "a buyer" are two populations and the register is the wider one. THIS IS BY DESIGN, NOT A DEFECT: the upstream generator splits CustomerWeight from OrderWeight precisely so a large register carries a small order volume (the generator's published configuration, https://docs.sqlbi.com/contoso-data-generator/config-data). A bare customer count must say which population it counted. THE PLACE IS SERVED AS A CODE, AND THE COLUMN SAYS SO. `country_code` carries `AU`, `CA`, `DE` — ISO-3166 alpha-2, the same spelling `dim_location` and `dim_store` use. The landing also carries the long name — `customer.CountryFull`, Australia, Canada, measured one-to-one with the code — and the operator ruled NOT to serve it: the code is named honestly first. A question asking for countries is answered with their names through Country, which this concept reaches by `country_code` (edge customer__based_in__country). IT IS A VERSION OF A PERSON. `valid_from` and `valid_to` are on every row, so this dimension keeps HISTORY. "Customers as they are today" and "the customer a past sale was made to" can be different rows, and reading one as the other re-attributes old sales to new addresses.

## Identity

A surrogate `customer_key` annotated by `customer_name`, which is near-unique and NOT unique, so it identifies nothing on its own.

## Grain

one row per customer version (customer_key)

## Customer.as_of_now_or_sale

they can return different rows, and the difference is every customer who moved

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
