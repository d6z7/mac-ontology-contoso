# Color

The account of concept Color.

## Overview

The colour a product comes in: the one attribute that on its own makes a new SKU — "E400 Green" and "E400 Orange" are two products. WHY IT IS A CONCEPT. "Green MP3 players" is how a question reaches a product. Nobody says a SKU's name. ONE SPELLING PER COLOUR, AND THE FOLD HAPPENS UPSTREAM. The landing carries both spellings, `Blue` and blue; `data/transforms/dim_product.sql` capitalises the first letter, so the served `color` holds one `Blue` — the operator's ruling, taken as a rule about capitalisation rather than a patch naming one value. On the served plane there are no case variants, and `color = 'blue'` returns no rows. Nothing is folded at read time, and these rules must not ask for it.

## Identity

Colour NAMES used as their own key.

## Grain

one member per colour name, stored and meant

## How the set of products carrying a colour is resolved

By the column declaration, and by nothing else.

The colour fold itself is the transform's guarantee and lives in its lineage; what a reader needs to know about it is the section below.

## Color.one_spelling

the landing row spells it two ways and the transform folds it; a breakdown that lists both is off by a line

- **when** — a question asks about blue products, or breaks products down by colour
- **then** — answer over the served `color`, where the two spellings are already one member
- **never** — report `Blue` and blue as two colours

## Cites

- `dataset:dim_product.color`
- `dataset:dim_product.product_key`
- `rule:Color.one_spelling`

## edge product__comes_in__color, from Product

(no notes)
