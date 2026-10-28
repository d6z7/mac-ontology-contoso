# NetRevenue

> The human account. The declaration is `ontology/concepts/net_revenue.yaml`; read this first,
> whole, then compare it against that file.

## Overview

What Contoso actually charged: quantity times the discounted price, per sale, summed. Read from
the rows: 681.72 net against 717.60 gross on one sale — the gap is the discount. THE DEFAULT
READING OF "REVENUE", and it is after discount. [[GrossRevenue]] is the same figure before it.
Answering one when a question meant the other moves every derived figure — margin most of all — in
a direction somebody will like. IT IS IN USD. The sale's `currency_code` names what the customer
paid in, not what this is stated in; conversion goes through [[ExchangeRate]] at the sale's own
order date.

## Grain

one row per sale (order_key, line_number)

## default.revenue_means_net

the gap between net and gross is the discount, so the wrong choice moves every derived figure by
exactly the amount somebody wanted to see

The declaration states this executably as well, because this rule has no body yet:

- **when** — a question says "revenue" or "sales" without saying net or gross
- **then** — answer with `{net_amount}` and say NET — it is after discount; the figure before discount is [[GrossRevenue]]
- **never** — pick one silently

## default.a_price_is_revenue_per_article

the operator ruled the average is what the customer paid per article, so the denominator is
articles sold and not sale lines. All three readings look like a unit price and only one answers
the question.

THREE READINGS LOOK LIKE A UNIT PRICE AND ONE ANSWERS THE QUESTION, and the figures are why the
choice is not presentational:

| reading | arithmetic | figure |
|---|---|---|
| **price per article** — what this rule declares | `SUM(net_amount) / SUM(quantity)` | **310,98** |
| averaging `net_price` | weights a one-unit sale like a fifty-unit one | 309,87 |
| averaging `net_amount` | the value of a LINE, not of an article | 976,96 |

The pre-discount figure is [[GrossRevenue]] over the same denominator, 330,58, reached by naming
gross — a different axis, held by `revenue_means_net`.

DECLARED EXECUTABLY as `mac.canon.ratio_select`, bound 2026-10-05, so the reading is the runtime's
and no longer a model's guess. `default: price_per_article` carries the operator's ruling: a question
naming no reading commits to this one and discloses that it did. The surfaces a person may say are
declared — price, average price, unit price, price per unit, per unit, price per article, per
article — and matched exactly, case/space/underscore folded.

`net_price` LEFT `binds`, which is the part worth noticing. A ratio rule's `binds` IS its numerator,
so naming the column the rule FORBIDS would have declared it as part of the figure being divided.
Nothing is lost by its leaving: `net_price` carries `measure.type: intensive`, which is what forbids
averaging it, and `net_amount` carries `canonical: true` against a grain of one row per sale line,
which is what makes 976,96 a per-line figure. The prohibitions are declarations, not sentences.
