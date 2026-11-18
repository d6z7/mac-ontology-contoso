# Color

The account of concept Color.

## Overview

The colour a product comes in: sixteen values on the served row, and the one attribute that on its own makes a new SKU — "E400 Green" and "E400 Orange" are two products. WHY IT IS A CONCEPT. "Green MP3 players" is how a question reaches a product. Nobody says a SKU's name. SIXTEEN, AND THE FOLD HAPPENS UPSTREAM. The landing row carried both `Blue` (197) and `blue` (3); `data/transforms/dim_product.sql` capitalises the first letter, so the served `color` holds `Blue` 200 and sixteen members in total — operator's ruling of 2026-09-30, taken as a rule about capitalisation rather than a patch naming one value. Measured on the served plane 2026-10-02: 16 distinct, 0 case variants, and `color = 'blue'` returns 0 rows. Nothing is folded at read time, and these rules must not ask for it.

## Identity

Sixteen colour NAMES used as their own key.

## Grain

one member per colour name — sixteen, stored and meant

## How the set of products carrying a colour is resolved

By the column declaration, and by nothing else.

The colour fold itself is the transform's guarantee and lives in its lineage; what a reader needs to know about it is the section below.

## Color.one_spelling

the landing row spells it two ways and the transform folds it; a breakdown that lists both is off by a line, which is what RC03 measured at 17 against an approved 16

- **when** — a question asks about blue products, or breaks products down by colour
- **then** — answer over the served `color`, where the two spellings are already one member
- **never** — report `Blue` and `blue` as two colours

## Cites

- `dataset:dim_product.color`
- `dataset:dim_product.product_key`
- `rule:Color.one_spelling`

## edge product__comes_in__color, from Product

(no notes)
