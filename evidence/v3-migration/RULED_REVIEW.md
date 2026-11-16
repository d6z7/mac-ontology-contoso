# RULED_REVIEW

Every rule that was `ruled` in the 0.4.0 bundle `mac-ontology-contoso`, as `mac_migrate_v3` wrote it (Y-7, conservative: words are accepted only from (a) a quote attributed to the operator, (b) in a RULED- / RULING- / PROTOCOL- record, (c) that names the rule or a former id).

**19 ruled in 0.4.0: 13 kept `ruled`, 6 dropped to `proposed`.**

| rule | v3 state | words (first 160 chars) | record | why accepted / why dropped |
|---|---|---|---|---|
| Color.one_spelling | ruled | the word is fold | data/transforms/dim_product.sql | 0.4.0 said entry carried verbatim (the bundle's own claim); its record is not a RULED-/RULING-/PROTOCOL- record |
| Country.where_we_have_customers | ruled | this question must be answerable: where we have customers. it can be usnerstood by you and can be understood by 2nd generation of LLM. i dont accept bullshit th… | meaning-as-code#decisions/FINDINGS-2026-10-19_slots-versus-object-sets-operator-rulings.md | 0.4.0 said entry carried verbatim (the bundle's own claim); its record is not a RULED-/RULING-/PROTOCOL- record |
| Country.whose | ruled | ok go B1 now | meaning-as-code#decisions/RULED-2026-10-25_a-sale-is-attributed-by-its-channel.md | 0.4.0 said entry carried verbatim (the bundle's own claim) |
| Customer.active_on_the_reference_date | ruled | it is differentitaion between active custoomers and registered customers | (none) | 0.4.0 said entry carried verbatim (the bundle's own claim); its record is not a RULED-/RULING-/PROTOCOL- record |
| Location.site | ruled | dont call it site code ... just site, location, city | data/datasets/dim_location.yaml | 0.4.0 said entry carried verbatim (the bundle's own claim); its record is not a RULED-/RULING-/PROTOCOL- record |
| Order.cost_is_procurement | ruled | from the shop perspective cost is procurement cost. The rest is revenue or income. | ontology/MODELLING-LOG.md | 0.4.0 said entry carried verbatim (the bundle's own claim); its record is not a RULED-/RULING-/PROTOCOL- record |
| Order.discount_percent_is_over_gross | proposed | — | - | RULED-2026-10-29_column-facts-on-the-relation-concept-facts-on-the-concept.md names the rule, but no operator quote stands in the section that names it (a + c) |
| Order.discount_total_is_money | ruled | if i ask what is a total discount then i would expect to get THE DISCOUNTED AMOUNT OF MONEY and not %. total discount in 2024 should be refused to answer to the… | meaning-as-code#decisions/RULED-2026-10-13_what-a-total-discount-means.md | 0.4.0 said entry carried verbatim (the bundle's own claim) |
| Order.is_the_purchase | proposed | — | - | no RULED-/RULING-/PROTOCOL- record names the rule or a former id |
| Order.margin_ratio_is_named | proposed | — | - | RULED-2026-10-29_column-facts-on-the-relation-concept-facts-on-the-concept.md names the rule, but no operator quote stands in the section that names it (a + c) |
| Order.now_is_the_newest_order | ruled | but as the time move on ... we need to specify the sampling date lets say on 31.12.2025 | meaning-as-code#decisions/RULED-2026-10-23_the-sampling-date-is-the-newest-order.md | 0.4.0 said entry carried verbatim (the bundle's own claim) |
| Order.period | proposed | — | - | no RULED-/RULING-/PROTOCOL- record names the rule or a former id |
| Order.price_is_per_article | proposed | — | - | RULED-2026-10-29_column-facts-on-the-relation-concept-facts-on-the-concept.md names the rule, but no operator quote stands in the section that names it (a + c) |
| Order.price_terms | ruled | UnitPrice = regular/list price per unit | meaning-as-code#decisions/HANDOVER-2026-10-26_retire-product-prices.md | 0.4.0 said entry carried verbatim (the bundle's own claim); its record is not a RULED-/RULING-/PROTOCOL- record |
| Order.revenue_means_net | ruled | Keep net + disclose | meaning-as-code#decisions/RULING-2026-11-16_grammar-v3.md#b-4-orderrevenue_means_net | operator-confirmed mapping (--words-from) |
| Product.price_is_dated | proposed | — | - | cited HANDOVER-2026-10-26_retire-product-prices.md is not a RULED-/RULING-/PROTOCOL- record (b) |
| Store.channel | ruled | now i am for correctnes and correct is that both internet and physical shops combined make revenue. | meaning-as-code#decisions/RULED-2026-10-18_both-channels-make-revenue.md | 0.4.0 said entry carried verbatim (the bundle's own claim) |
| Store.premises_not_place | ruled | a Store is a PLACE on one location you can shop at ... store is part of location | ontology/concepts/store.yaml | 0.4.0 said entry carried verbatim (the bundle's own claim); its record is not a RULED-/RULING-/PROTOCOL- record |
| Store.trading | ruled | stores that are closed, restructured have close date and are not active anymore; other stores without status do not have close date are ONLY stores currently ac… | knowledge/store.md | 0.4.0 said entry carried verbatim (the bundle's own claim); its record is not a RULED-/RULING-/PROTOCOL- record |
