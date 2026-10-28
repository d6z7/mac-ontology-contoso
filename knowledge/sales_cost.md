# SalesCost

> The human account. The declaration is `ontology/concepts/sales_cost.yaml`; read this first,
> whole, then compare it against that file.

## Overview

What the goods on a sale cost Contoso: quantity times unit cost, per sale, summed. MARGIN IS NOT
STORED. It is [[NetRevenue]] minus this, computed at whatever grain the question asks for — never
a per-sale margin averaged, which weights a one-unit sale the same as a fifty-unit one.

## Grain

one row per sale (order_key, line_number)
