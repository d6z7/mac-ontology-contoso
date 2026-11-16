# MIGRATION_NEEDS

What grammar v3 needs that the 0.4.0 bundle `mac-ontology-contoso` does not have, written by `mac_migrate_v3` instead of being invented. Each item: the file, what is missing, the decision that requires it, and what the bundle owner must add.

**21 items** — confirm 8, join 3, layout 2, ledger 1, value 1, words 6

| # | kind | file | what is missing | required by | the owner adds |
|---|---|---|---|---|---|
| 1 | value | `mac.project.yaml` | connector 'mac.connector.duckdb' is not pinned to a major version | GRAMMAR_v3 §2.7 connector `<namespace>.connector.<name>/<major>`; L15 (not answerable until pinned) | append the connector's major version, e.g. `/1` |
| 2 | confirm | `ontology/rules/Color.one_spelling.yaml` | rule Color.one_spelling is `ruled` on 0.4.0 words whose record (data/transforms/dim_product.sql) is not a ruling record; carried as the bundle states it | Y-7; GRAMMAR_v3 §2.4 | operator to confirm the words rule this rule |
| 3 | confirm | `ontology/rules/Country.where_we_have_customers.yaml` | rule Country.where_we_have_customers is `ruled` on 0.4.0 words whose record (meaning-as-code#decisions/FINDINGS-2026-10-19_slots-versus-object-sets-operator-rulings.md) is not a ruling record; carried as the bundle states it | Y-7; GRAMMAR_v3 §2.4 | operator to confirm the words rule this rule |
| 4 | confirm | `ontology/rules/Customer.active_on_the_reference_date.yaml` | rule Customer.active_on_the_reference_date is `ruled` on 0.4.0 words whose record (none) is not a ruling record; carried as the bundle states it | Y-7; GRAMMAR_v3 §2.4 | operator to confirm the words rule this rule |
| 5 | confirm | `ontology/rules/Location.site.yaml` | rule Location.site is `ruled` on 0.4.0 words whose record (data/datasets/dim_location.yaml) is not a ruling record; carried as the bundle states it | Y-7; GRAMMAR_v3 §2.4 | operator to confirm the words rule this rule |
| 6 | confirm | `ontology/rules/Order.cost_is_procurement.yaml` | rule Order.cost_is_procurement is `ruled` on 0.4.0 words whose record (ontology/MODELLING-LOG.md) is not a ruling record; carried as the bundle states it | Y-7; GRAMMAR_v3 §2.4 | operator to confirm the words rule this rule |
| 7 | words | `ontology/rules/Order.discount_percent_is_over_gross.yaml` | rule Order.discount_percent_is_over_gross: ruled in 0.4.0, no operator words found — operator to confirm (written `state: proposed`; RULED-2026-10-29_column-facts-on-the-relation-concept-facts-on-the-concept.md names the rule, but no operator quote stands in the section that names it (a + c)) | Y-7; GRAMMAR_v3 §2.4 (`ruled` needs a person's verbatim words) | operator to confirm: add the ruling's said entry (by, date, words, in) and set state: ruled |
| 8 | words | `ontology/rules/Order.is_the_purchase.yaml` | rule Order.is_the_purchase: ruled in 0.4.0, no operator words found — operator to confirm (written `state: proposed`; no RULED-/RULING-/PROTOCOL- record names the rule or a former id) | Y-7; GRAMMAR_v3 §2.4 (`ruled` needs a person's verbatim words) | operator to confirm: add the ruling's said entry (by, date, words, in) and set state: ruled |
| 9 | words | `ontology/rules/Order.margin_ratio_is_named.yaml` | rule Order.margin_ratio_is_named: ruled in 0.4.0, no operator words found — operator to confirm (written `state: proposed`; RULED-2026-10-29_column-facts-on-the-relation-concept-facts-on-the-concept.md names the rule, but no operator quote stands in the section that names it (a + c)) | Y-7; GRAMMAR_v3 §2.4 (`ruled` needs a person's verbatim words) | operator to confirm: add the ruling's said entry (by, date, words, in) and set state: ruled |
| 10 | words | `ontology/rules/Order.period.yaml` | rule Order.period: ruled in 0.4.0, no operator words found — operator to confirm (written `state: proposed`; no RULED-/RULING-/PROTOCOL- record names the rule or a former id) | Y-7; GRAMMAR_v3 §2.4 (`ruled` needs a person's verbatim words) | operator to confirm: add the ruling's said entry (by, date, words, in) and set state: ruled |
| 11 | words | `ontology/rules/Order.price_is_per_article.yaml` | rule Order.price_is_per_article: ruled in 0.4.0, no operator words found — operator to confirm (written `state: proposed`; RULED-2026-10-29_column-facts-on-the-relation-concept-facts-on-the-concept.md names the rule, but no operator quote stands in the section that names it (a + c)) | Y-7; GRAMMAR_v3 §2.4 (`ruled` needs a person's verbatim words) | operator to confirm: add the ruling's said entry (by, date, words, in) and set state: ruled |
| 12 | confirm | `ontology/rules/Order.price_terms.yaml` | rule Order.price_terms is `ruled` on 0.4.0 words whose record (meaning-as-code#decisions/HANDOVER-2026-10-26_retire-product-prices.md) is not a ruling record; carried as the bundle states it | Y-7; GRAMMAR_v3 §2.4 | operator to confirm the words rule this rule |
| 13 | words | `ontology/rules/Product.price_is_dated.yaml` | rule Product.price_is_dated: ruled in 0.4.0, no operator words found — operator to confirm (written `state: proposed`; cited HANDOVER-2026-10-26_retire-product-prices.md is not a RULED-/RULING-/PROTOCOL- record (b)) | Y-7; GRAMMAR_v3 §2.4 (`ruled` needs a person's verbatim words) | operator to confirm: add the ruling's said entry (by, date, words, in) and set state: ruled |
| 14 | confirm | `ontology/rules/Store.premises_not_place.yaml` | rule Store.premises_not_place is `ruled` on 0.4.0 words whose record (ontology/concepts/store.yaml) is not a ruling record; carried as the bundle states it | Y-7; GRAMMAR_v3 §2.4 | operator to confirm the words rule this rule |
| 15 | confirm | `ontology/rules/Store.trading.yaml` | rule Store.trading is `ruled` on 0.4.0 words whose record (knowledge/store.md) is not a ruling record; carried as the bundle states it | Y-7; GRAMMAR_v3 §2.4 | operator to confirm the words rule this rule |
| 16 | join | `data/datasets/dim_country.yaml` | column `country_code` references contoso5_country_code.code but no edge joins it: no concept takes contoso5_country_code (a value set no concept takes cannot be an edge's end) | U-2 (edges are the only joins); L7 | put a concept on the target (or a unique key) and add the edge, or drop the reference |
| 17 | join | `data/datasets/dim_currency.yaml` | column `currency_code` references contoso5_currency.code but no edge joins it: no concept takes contoso5_currency (a value set no concept takes cannot be an edge's end) | U-2 (edges are the only joins); L7 | put a concept on the target (or a unique key) and add the edge, or drop the reference |
| 18 | join | `data/datasets/dim_product.yaml` | column `category_name` references contoso5_category_name.code but no edge joins it: no concept takes contoso5_category_name (a value set no concept takes cannot be an edge's end) | U-2 (edges are the only joins); L7 | put a concept on the target (or a unique key) and add the edge, or drop the reference |
| 19 | ledger | `governance/sme-questions.yaml` | 18 findings carry SME fields (sme_owner, current_handling, residual_risk, ruling question/because/established/for_the_human) whose home is a ledger entry; they are seeded in governance/sme-history/migrated-finding-fields.yaml | brief 2026-11-16 (SME fields -> the SME ledger, linked by asked_in) | create the ledger entries from the seed and set each finding's `asked_in` |
| 20 | layout | `governance/tombstones.yaml` | cited by 1 declaration(s) (e.g. data/datasets/v_contoso5_sales_line.yaml) but outside the v3 layout and the tool-read planes; carried as it is so the citation resolves | GRAMMAR_v3 §1 (tool-read planes: decisions/, evidence/) | move it into decisions/ (or evidence/) and repoint the citations |
| 21 | layout | `ontology/MODELLING-LOG.md` | cited by 2 declaration(s) (e.g. data/datasets/dim_product.yaml) but outside the v3 layout and the tool-read planes; carried as it is so the citation resolves | GRAMMAR_v3 §1 (tool-read planes: decisions/, evidence/) | move it into decisions/ (or evidence/) and repoint the citations |

## Decisions the migration took (no owner action needed)

- data/datasets/v_contoso5_sales_line.yaml: offers.aggregate.default `net_amount` -> proposed rule Order.default_measure (measure choice; Y-6 applies it, disclosed)
- project as_of: {anchor: v_contoso5_sales_line.order_date} — the one column declaring offers.anchor: latest (Y-2)
- data/datasets/dim_customer.yaml: `valid: {start: valid_from, end: valid_end}` from rule Customer.active_on_the_reference_date — the reading set declares unstated as_of anchor / nothing (a validity window); mac_vocabulary.yaml#reading_input.as_of
- reading set name `population` (ontology/concepts/customer.yaml) differs from rule Customer.active_on_the_reference_date's last segment; v3 has no home for a set name (the compile derives it from the rule id)
- reading set name `price` (data/datasets/v_contoso5_sales_line.yaml) differs from rule Order.price_is_per_article's last segment; v3 has no home for a set name (the compile derives it from the rule id)
- reading set name `percent` (data/datasets/v_contoso5_sales_line.yaml) differs from rule Order.discount_percent_is_over_gross's last segment; v3 has no home for a set name (the compile derives it from the rule id)
- data/datasets/v_contoso5_sales_line.yaml: reading set `ratio` (rule Order.margin_ratio_is_named) has no default; written `default: ask` (the 0.4.0 meaning of an absent default; B-1)
- reading set name `ratio` (data/datasets/v_contoso5_sales_line.yaml) differs from rule Order.margin_ratio_is_named's last segment; v3 has no home for a set name (the compile derives it from the rule id)
- edge product__sold_under__brand (Product -> Brand): both concepts on dim_product; no v3 edge (L7), recorded in ontology/concepts/Brand.md
- edge product__belongs_to__product_category (Product -> ProductCategory): both concepts on dim_product; no v3 edge (L7), recorded in ontology/concepts/ProductCategory.md
- edge product__comes_in__color (Product -> Color): both concepts on dim_product; no v3 edge (L7), recorded in ontology/concepts/Color.md
- ontology/concepts/exchange_rate.yaml: label 'Exchange Rate' equals the spaced name; not written (GRAMMAR_v3 §3), kept as a word
- ontology/concepts/product_category.yaml: label 'Product Category' equals the spaced name; not written (GRAMMAR_v3 §3), kept as a word
- ontology/rules/Brand.not_manufacturer.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/Country.whose_is_the_store.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/Currency.code_is_not_the_unit.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/Customer.as_of_now_or_sale.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/Customer.register_not_buyers.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/ExchangeRate.convert_per_day.yaml: canon additivity_guard -> implemented_by {'law.L2': 'dataset:v_contoso5_fx_rate', 'dataset:v_contoso5_fx_rate.rate': 'measure'} (R-2; params ['axis_effects', 'measure_column'] are not kept)
- ontology/rules/Order.how_many.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/Order.is_the_purchase.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/Order.no_lifecycle_state.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/Order.rate_on_order_date.yaml: canon composite_key_guard -> implemented_by {'law.L0': 'dataset:v_contoso5_fx_rate', 'dataset:v_contoso5_fx_rate.to_currency': 'dimension', 'dataset:v_contoso5_fx_rate.date_day': 'date', 'dataset:v_contoso5_fx_rate.from_currency': 'dimension'} (R-2; params ['code_column', 'scope_columns'] are not kept)
- ontology/rules/Order.revenue_means_net.yaml: said from the operator-confirmed mapping meaning-as-code#decisions/RULING-2026-11-16_grammar-v3.md#b-4-orderrevenue_means_net (--words-from)
- ontology/rules/Product.price_is_dated.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/Store.counted_by_site.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- ontology/rules/Store.record_questions.yaml: prose rule with no owner; owner assigned to the operator (Y-7)
- data/datasets/dim_country.yaml: `members: {}` — its key `country_code` takes its values from the register contoso5_country_code.code (the rows are members of a value set)
- data/datasets/dim_currency.yaml: `members: {}` — its key `currency_code` takes its values from the register contoso5_currency.code (the rows are members of a value set)
- data/datasets/dim_product.yaml: column `product_key` reference to concept 'Product' (no join columns) dropped (U-1: a dataset never points at a concept)
- data/datasets/dim_store.yaml: column `store_key` was `identifier` and declares a hierarchy ruling; written `is: dimension` (GRAMMAR_v3 §2.1: parent / within only on a dimension or name)
- data/sources/currencyexchange.yaml: the connection has no source map; address carries the schema 'main'
- data/sources/customer.yaml: the connection has no source map; address carries the schema 'main'
- data/sources/date.yaml: the connection has no source map; address carries the schema 'main'
- data/sources/orderrows.yaml: the connection has no source map; address carries the schema 'main'
- data/sources/orders.yaml: the connection has no source map; address carries the schema 'main'
- data/sources/product.yaml: the connection has no source map; address carries the schema 'main'
- data/sources/sales.yaml: the connection has no source map; address carries the schema 'main'
- data/sources/store.yaml: the connection has no source map; address carries the schema 'main'
- finding DQ-AMBIGREF-CURRENCYCODE: `about` source:currencyexchange taken from its text
- finding DQ-DANGLINGKEY-CATEGORYKEY: `about` source:product taken from its text
- finding DQ-DANGLINGKEY-GEOAREAKEY: `about` source:customer taken from its text
- finding DQ-DANGLINGKEY-SUBCATEGORYKEY: `about` source:product taken from its text

## Files not carried (outside the v3 layout and not a tool-read plane or a generated page)

- `README.md` — outside the v3 layout (UNCLASSIFIED)
- `build.sh` — outside the v3 layout (script.bundle_shell)
- `contoso5.mac` — outside the v3 layout (declaration.resource_description)
- `tools_trace_extract.py` — outside the v3 layout (script.bundle_local)

## Status after the in-place migration (2026-11-17, branch 0.4.1-develop)

**10 closed, 11 open.** Validator (v3work/v3schema/validate_v3.py): 3 errors, all LAYOUT on kept bundle files
the v3 layout has no home for (`README.md`, `build.sh` = this bundle's deploy, `tools_trace_extract.py`).
Compile-back (mac_compile_v3 -> 0.4.0 compiler): COMPILES, 0 errors.

| # | status | how |
|---|---|---|
| 1 | closed | `connector: mac.connector.duckdb/1` — the major the connection file declares (`spec_version: mac.connector/1`) |
| 2 | OPEN — operator | Color.one_spelling dropped to `proposed` (Y-7): its words stand only in dim_product.sql comments |
| 3 | closed | Country.where_we_have_customers stays `ruled`: the words stand verbatim in the decision record it cites (FINDINGS-2026-10-19 …operator-rulings) |
| 4 | OPEN — operator | Customer.active_on_the_reference_date dropped to `proposed`: its three sayings cite no record |
| 5 | OPEN — operator | Location.site dropped to `proposed`: its words stand only in data/datasets/dim_location.yaml |
| 6 | closed | Order.cost_is_procurement stays `ruled`: the words stand verbatim in MODELLING-LOG Entry 19 (now evidence/MODELLING-LOG.md), the record it cites |
| 7–11, 13 | OPEN — operator | already `proposed`; no record carries operator words for Order.discount_percent_is_over_gross, Order.is_the_purchase, Order.margin_ratio_is_named, Order.period, Order.price_is_per_article, Product.price_is_dated (HANDOVER-2026-10-26 gives the reasons "verbatim in substance", not verbatim) |
| 12 | closed | Order.price_terms stays `ruled`: "UnitPrice = regular/list price per unit" stands verbatim in HANDOVER-2026-10-26, the record it cites |
| 14 | OPEN — operator | Store.premises_not_place dropped to `proposed`: its words were in the replaced 0.4.0 concept file only |
| 15 | closed | Store.trading stays `ruled`: DNA-2026-09-25 quotes the 2026-09-30 ruling verbatim; added as the first `said` entry |
| 16–18 | closed | the three references were circular: contoso5_country_code / contoso5_currency / contoso5_category_name are each cut FROM the column that referenced them (their .sql: `SELECT DISTINCT … FROM` dim_country / dim_currency / dim_product). Dropping them loses no fact; data/lineage/*.transform.yaml records the derivation |
| 19 | OPEN — operator | the SME ledger (format mac.sme-questions/1) is dialogue written through the console's ledger store, with participants, owner and status; this public bundle has no ledger and no SME participants. The 18 findings' SME fields stay in governance/sme-history/migrated-finding-fields.yaml until the operator decides whether contoso gets a ledger |
| 20 | closed | governance/tombstones.yaml -> evidence/tombstones.yaml, declared out of scope (project.out_of_scope.evidence_tombstones_yaml); no v3 declaration cites it |
| 21 | closed | ontology/MODELLING-LOG.md -> evidence/MODELLING-LOG.md; citations repointed. (evidence/, not decisions/: a root decisions/ makes the 0.4.0 reference checker resolve every `meaning-as-code#decisions/…` citation inside the bundle) |
