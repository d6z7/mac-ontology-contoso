# Currency.whose

The account of rule Currency.whose.

## Cites

- `concept:Currency`
- `concept:Order`
- `concept:Store`
- `concept:Location`
- `concept:ExchangeRate`
- `edge:order__paid_in__currency`
- `edge:exchange_rate__quotes_from__currency`
- `edge:exchange_rate__quotes_to__currency`

## Why it is a choice

Currency is reached by three last hops (the build's L7 route check lists the pairs): the sale's own currency
(`order__paid_in__currency`) and the two currencies of an exchange rate (`exchange_rate__quotes_from__currency`,
`exchange_rate__quotes_to__currency`). An exchange rate reaches Currency by the two rate hops directly; a sale, a store
or a site by all three, the rate ones through `order__converts_at__exchange_rate`. L3: a route choice lists the only
routes, an unlisted route is refused, and its default applies when the question names none.

## One choice, not two

The rate's two sides and the sale's currency are one choice because they share the target. A route choice that listed
only the two rate hops would also lie on the sale's routes into Currency and, by L3, refuse the sale's own currency as
unlisted. Measured 2026-11-17 on the runtime's generated questions: with such a choice beside this one, "net amount by
currency" was asked back (default `ask`) or routed through the rate's source currency (default `source`). Listing all
three hops here keeps "by currency" on the sale's currency.

## The default

`paid_in`, proposed 2026-11-17: the currency the sale was transacted in. It applies and is disclosed as proposed
(GRAMMAR_v3 L3, Y-6). The rate's target is the sale's currency on every line (the edge joins `currency_code` to
`to_currency`), so `rate_target` gives a sale the same currency as `paid_in`; the rate's source is the amounts' unit,
USD on every line, so `rate_source` puts every sale in USD. An exchange-rate question that names no side reaches the
sale currency of the orders that used the rate; naming from or to picks that side. RC13 follows the default;
`acceptance/tools/rule_switch_test.py` shows `rate_source` changes its answer and `rate_target` does not.
