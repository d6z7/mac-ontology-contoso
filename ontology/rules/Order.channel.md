# Order.channel

The account of rule Order.channel.

## Cites

- `concept:Order`
- `dataset:v_contoso5_sales_line.is_web_sale`

## The choice

Which channels a figure of the sale covers: `both` (every sales line), `shops` (the lines sold in a shop,
`is_web_sale` false) or `online` (the web shop's lines, `is_web_sale` true). The transform derives `is_web_sale` on the sales
line from the web shop's store key, so the options read a column and never a stored value.

## The default

`both`, by the operator's ruling of 2026-10-18 ("both internet and physical shops combined make revenue",
RULED-2026-10-18_both-channels-make-revenue). The state is `proposed`, as every choice written on 2026-11-17 is; the
operator's words above are what would make it `ruled`. Rule Store.channel keeps its own default for questions whose
subject is a store (how many stores, which ones); this rule is about the sale. STORE-09 follows the default;
`acceptance/tools/rule_switch_test.py` shows `shops` and `online` change its answer.
