# data/lookups — the value registers of this bundle

The name-to-code registers an answering engine resolves a word against OFFLINE, so it
never probes the warehouse for a name and reads "no rows" as "no such thing". Every
register is cut from a SERVED relation (`data/datasets/`), carries its origin in a
`source_view` column on every row, and is a dated snapshot: re-cut it when the dataset
changes. Each `<x>.lookup.csv` has an `<x>.lookup.md` twin holding the exact query, the
row count and what is known to be wrong with the values — provenance never goes inside a
register, because a comment line above the header is read as the header.

This index is GENERATED from the registers themselves (scratchpad p6_lookups.py), so it
cannot drift from them; every number below is also in the twin beside the register.

| register | rows | code column | cut from | what it resolves |
| --- | --- | --- | --- | --- |
| `contoso_brand.lookup.csv` | 11 | `Brand` | `dim_contoso_product` | Resolve a brand word ("by brand" is one of the question scope's axes) to the spelling the served product dimension stores. |
| `contoso_calendar_month.lookup.csv` | 12 | `MonthNumber` | `dim_contoso_calendar_day` | Resolve a month word ("March", "Mar") to the MonthNumber the served calendar carries, and its quarter. |
| `contoso_calendar_quarter.lookup.csv` | 4 | `Quarter` | `dim_contoso_calendar_day` | Resolve a quarter word ("Q3") to the label the served calendar carries. |
| `contoso_calendar_weekday.lookup.csv` | 7 | `DayofWeekNumber` | `dim_contoso_calendar_day` | Resolve a weekday word ("Monday", "Mon") to the DayofWeekNumber the served calendar carries. |
| `contoso_color.lookup.csv` | 16 | `Color` | `dim_contoso_product` | Resolve a colour word to the one spelling the served product dimension carries. |
| `contoso_country.lookup.csv` | 9 | `Country` | `dim_contoso_customer` | Resolve a country word to the 2-letter code both the customer and the store dimension carry, and carry the continent so the scope's country -> continent roll-up resolves offline. |
| `contoso_currency.lookup.csv` | 5 | `CurrencyCode` | `v_contoso_order_line` | Resolve a currency to the code the fact carries — and refuse the words this delivery cannot resolve. |
| `contoso_gender.lookup.csv` | 2 | `Gender` | `dim_contoso_customer` | Resolve a gender word to the spelling the served customer dimension carries. |
| `contoso_geo_area.lookup.csv` | 608 | `GeoAreaKey` | `dim_contoso_customer` | Resolve a region word ("Bavaria", "Ohio") to the GeoAreaKey the served customer dimension carries — the delivery's only region key. |
| `contoso_product_category.lookup.csv` | 8 | `CategoryKey` | `dim_contoso_product` | Resolve a category word ("Home Appliances") to the CategoryKey the served product dimension carries. |
| `contoso_product_subcategory.lookup.csv` | 32 | `SubCategoryKey` | `dim_contoso_product` | Resolve a subcategory word ("Cell phones Accessories") to its SubCategoryKey, and carry the parent category so the two-level hierarchy resolves offline. |
| `contoso_store_status.lookup.csv` | 2 | `Status` | `dim_contoso_store` | Resolve a store-status word ("closed stores") to the spelling the served store dimension carries — and make visible that there is no code for the opposite. |
| `contoso_weight_unit.lookup.csv` | 3 | `WeightUnit` | `dim_contoso_product` | Resolve a unit word ("pounds") to the spelling the served product dimension carries. |
| `contoso_working_day.lookup.csv` | 2 | `WorkingDay` | `dim_contoso_calendar_day` | Resolve "working day" / "non-working day" to the WorkingDay flag the served calendar carries. |
| `dim_contoso_product.lookup.csv` | 2517 | `ProductKey` | `dim_contoso_product` | Resolve a product word (a name or a product code) to the ProductKey the fact carries. |
| `dim_contoso_store.lookup.csv` | 74 | `StoreKey` | `dim_contoso_store` | Resolve a store word (its description, or its store code) to the StoreKey the fact carries. |

**16 registers, 3312 rows**, observed 2026-09-18. Not registered, and why, is in the run record: City, ZipCode, customer identity, the
period labels, and a measure registry (that one is the measure step's, not this one's).
