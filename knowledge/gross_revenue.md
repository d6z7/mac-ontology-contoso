# GrossRevenue

> The human account. The declaration is `ontology/concepts/gross_revenue.yaml`; read this first,
> whole, then compare it against that file.

## Overview

What Contoso would have charged at list: quantity times the undiscounted price, per sale, summed.
IT IS NOT WHAT WAS RECEIVED — [[NetRevenue]] is. This exists so the discount can be measured,
gross minus net; presented as revenue it overstates by exactly that amount.

## Grain

one row per sale (order_key, line_number)
