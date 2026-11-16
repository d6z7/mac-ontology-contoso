# UnitsSold

> The human account. The declaration is `ontology/concepts/units_sold.yaml`; read this first,
> whole, then compare it against that file.

## Overview

How many items went out: the quantity on a sale, summed. A2: a number you sum, with a unit →
`measure`. IT IS NOT A COUNT OF SALES OR ORDERS. 223,974 sales carry a quantity each and most
carry more than one — so "how many did we sell" and "how many times did we sell" are different
questions with different answers, and this concept answers the first.

## Grain

one row per sale (order_key, line_number)
