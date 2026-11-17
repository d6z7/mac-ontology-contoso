# TODO — what this bundle still needs

Each item states what is open in the bundle as it stands, what is needed, and who acts. An item leaves this file when
it is done; its history is git's.

## For the operator

1. **Four rules quote the operator, but no ruling record holds the words.** Each is `state: proposed`:
   `Color.one_spelling` (its words stand in `data/transforms/dim_product.sql`), `Customer.active_on_the_reference_date`
   (three sayings, no record), `Location.site` (its words stand in `data/datasets/dim_location.yaml`),
   `Store.premises_not_place` (no record). Needed: the operator confirms that the quoted words rule each rule (then
   `state: ruled`, with the record in `said[].in`), or the rule stays proposed. GRAMMAR_v3 §2.4: `ruled` needs a person's
   verbatim words.

2. **Six rules carry no operator words.** Each is `state: proposed`: `Order.discount_percent_is_over_gross`,
   `Order.is_the_purchase`, `Order.margin_ratio_is_named`, `Order.period`, `Order.price_is_per_article`,
   `Product.price_is_dated`. Needed: a `said` entry (by, date, words, in) and `state: ruled`, or the rule stays proposed.

3. **No SME ledger.** The bundle has no `governance/sme-questions.yaml`. The SME fields of 18 findings (`ruling.question`,
   `ruling.because`, `ruling.established`, `ruling.for_the_human`) sit in
   `governance/sme-history/migrated-finding-fields.yaml`, and no finding carries `asked_in`. Needed: the operator decides
   whether this bundle gets a ledger (format mac.sme-questions/1: participants, owner, status). If it does, the entries are
   created from that file and each finding's `asked_in` is set; if not, the file leaves the bundle.

4. **L15 is NOT ANSWERABLE on three project keys** (`tools/mac_compile.py`):
   - `interpreter` and `model_catalog`: the operator approved dropping both keys from the grammar (grammar-fixes ruling,
     Z-1 and Z-2). Needed: the grammar unlock that drops them; nothing is added to this bundle.
   - `data_signoff`: no rule signs the data, and the operator defers signing (Z-3). Needed: `data_signoff: rule:<id>`
     when the operator signs.

## For the tools

5. **Eight profiles are older than their dataset or transform** (L15): `dim_country`, `dim_currency`, `dim_customer`,
   `dim_location`, `dim_product`, `dim_store`, `v_contoso5_fx_rate`, `v_contoso5_sales_line`. Needed: a profiler run over
   the warehouse (`data/profiles/` is tools only).

6. **Two build warnings (MAC011).** 13 lookup datasets (`contoso5_*`) are taken by no concept and read by no transform;
   `contoso5_country_code.label` is read by nothing and not hidden. Needed: a reader for each, or each hidden.

## With the translation layer (plan W6: the 0.4.0 compile-back and the runtime's 0.4.0 view deleted)

7. **`## migrated from` in `ontology/rules/Order.default_measure.md`.** The compile-back (`tools/mac_compile_v3.py`,
   M-MEASURE) and the runtime's 0.4.0 view (`ontology/v3/view.py`) read it to fold the default-measure rule; removing it
   now moves plans. Needed: the section leaves when those readers are deleted.

8. **Nine prose rules name their owner through a placeholder `said` entry**,
   `in: 'migration to grammar v3: owner assigned (Y-7)'`: `Brand.not_manufacturer`, `Currency.code_is_not_the_unit`,
   `Customer.as_of_now_or_sale`, `Customer.register_not_buyers`, `Order.how_many`, `Order.is_the_purchase`,
   `Order.no_lifecycle_state`, `Product.price_is_dated`, `Store.record_questions`. The schema requires `said[0].by` on
   `implemented: prose`, and the compile-back (R-SAID) and the runtime's 0.4.0 view drop exactly these entries by that
   `in`. Needed: each entry restated as the owner alone (`by`) when those readers are deleted.
