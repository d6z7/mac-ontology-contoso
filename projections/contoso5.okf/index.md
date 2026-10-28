---
type: Index
title: CONTOSO5 knowledge bundle
description: OKF bundle projected from the CONTOSO5 MAC ontology.
---


# CONTOSO5 knowledge bundle

Projected from the **CONTOSO5** MAC ontology by `mac_to_okf.py`. 11 concepts.

| concept | type | description |
|---|---|---|
| [Brand](/Brand.md) | Enumeration | Whose name a product is sold under: eleven names, carried as a column on the product row with no table and no key of their own. |
| [Category](/ProductCategory.md) | Enumeration | How Contoso groups what it sells: eight categories, each over several of thirty-two sub-categories, both carried as names on the product row. |
| [Colour](/Color.md) | Enumeration | The colour a product comes in: sixteen values on the served row, and the one attribute that on its own makes a new SKU — "E400 Green" and "E400 Orange" are two products. |
| [Country](/Country.md) | Enumeration | A country Contoso sells in — 8 of them, plus one `--` sentinel that is not a place. |
| [Currency](/Currency.md) | Enumeration | The money a sale is denominated in: five ISO codes, pointed at by every sale and by both ends of every exchange rate. |
| [Customer](/Customer.md) | Entity | A person on Contoso's customer register: 104,990 of them, each with a name, a birth date and a place — continent, country, state, city. |
| [Exchange Rate](/ExchangeRate.md) | Metric | What one currency was worth in another on one day: 100,450 quoted rates over a date and an ordered pair of currencies. |
| [Location](/Location.md) | Entity | THE PLACE a store stands on — a country and a state, and nothing that belongs to the shop itself. |
| [Order](/Order.md) | Event | One customer's purchase on one date, counted by distinct `order_key` over the line relation. |
| [Product](/Product.md) | Entity | A thing Contoso sells, at the level the shelf knows it: a SKU. |
| [Store](/Store.md) | Entity | THE PREMISES Contoso sells from — a shop that stood on one place for one trading period, with its own name, floor area, opening date and closing date. |
