---
type: Enum
title: Currency
description: The denomination an order's amounts are stated in, and the two ends of an exchange quote.
tags:
- CONTOSO
- enumeration
- confidence:I
resource: table://v_contoso_order_line
rule_pages:
- rules/currency.labels.codes_only.md
---

The denomination an order's amounts are stated in, and the two ends of an exchange quote. Five codes, measured identical across the three columns that carry them: the fact's CurrencyCode (USD 113 614, EUR 49 203, CAD 24 250, GBP 22 829, AUD 14 078 lines) and the fx grid's FromCurrency and ToCurrency (5 distinct each).
IT IS NOT A REPORTING CURRENCY. There is no declared currency this bundle reports in; every served amount is the order's own local money, and an order is measured to carry exactly one currency (0 of 93 470 orders carry two).
AND IT CARRIES NO NAMES. The delivery states no currency name anywhere, so this concept has codes and no labels. "Dollars" does not resolve here — USD, CAD and AUD are all dollars — and that unresolvable word is a refusal, not a near miss to be picked.

## Details

- **Identity** — iso
- **Version** — 1.0
- **Schema version** — 0.1.14
- **Status** — draft
- **Owner** — operator
- **Governance owner** — operator
- **Last reviewed** — 2026-09-18

## How to answer

*What an agent needs ONLY, to answer with this concept — no data probing.*

```text
The five members are in data/lookups/contoso_currency.lookup.csv, cut from the served plane and bound as this concept's value domain, so a currency word is resolved offline and an unresolvable word (a currency NAME, or a sixth code) is a refusal derived from a closed set rather than from an empty query. Conversion is the ExchangeRate concept's declared direction; nothing here needs a probe.
```

## Grounded in

- `v_contoso_order_line` — key `['OrderKey', 'RowNumber']`
- `v_contoso_fx_rate_day` — key `['Date', 'FromCurrency', 'ToCurrency']`

## Fields

| column | type | role | grounded in | description | joins → |
|---|---|---|---|---|---|
| `CurrencyCode` | varchar | dimension | `v_contoso_order_line` | the denomination of every amount on the row; 5 measured values. Joins to the fx grid as FromCurrency together with the day, not by itself. | — |
| `FromCurrency` | varchar | key | `v_contoso_fx_rate_day` | 5 measured values. | — |
| `ToCurrency` | varchar | key | `v_contoso_fx_rate_day` | 5 measured values. | — |

_Declared per column, over 3 columns: description 3 of 3 · type 3 of 3 · joins → 0 of 3. An em dash is a column for which nothing is declared._

## Relationships

*0 join(s) out · 3 in — click a concept to open it.*

**Referenced by** — these point at this concept:

- [Exchange Rate](exchange_rate.md) — on `FromCurrency`
- [Exchange Rate](exchange_rate.md) — on `ToCurrency`
- [Order Line](order_line.md) — on `CurrencyCode`

## Source of record
- Full MAC concept: `currency.yaml` — open the **YAML** tab for the complete typed definition.