# Business case: Vehicle identification by VIN

All figures in EUR, undiscounted, computed by `prodoffs.py case` from `business_case.yaml`.

| Alternative | One-off | Year 1 net | Year 2 net | Year 3 net | 3-year net | Payback | Monthly net at end |
|---|---|---|---|---|---|---|---|
| Buy: vendor API | 36,000 | 270,619 | 310,703 | 294,557 | **839,880** | month 4 | 24,546 |
| Build: own decoder | 198,000 | -32,127 | 132,397 | 170,564 | **72,834** | month 31 | 14,214 |
| Hybrid: vendor behind own layer | 108,000 | 176,057 | 256,343 | 256,343 | **580,744** | month 9 | 21,362 |
| Hybrid layer: vendor behind own layer, no own decoding | 108,000 | 216,557 | 274,703 | 258,557 | **641,818** | month 8 | 21,546 |
| Hybrid layer, VIN first, holdout, price cap, landing pages | 126,000 | 216,557 | 284,063 | 279,149 | **653,770** | month 9 | 23,262 |

## Assumptions

- 600,000 part-search sessions a month; vehicle known today in 35% of them.
- If VIN entry is offered, 25% of the other sessions use it: about 97,500 lookups a month.
- Search-to-order conversion 4.8% with a known vehicle versus 3.8% without.
- Checkout completion uplift 2% on orders from VIN-identified sessions.
- Return rate 17%, of which 45% fitment-related; VIN identification removes 60% of those, scaled by precision. Cost per return 21.
- Average order value 118, gross margin 28%, team-week 9,000.
- Undiscounted; strategic effects (marketplace, new markets) are not priced in and are argued by the roles.
- Return-rate and fitment-share figures follow public industry reports for auto parts e-commerce; all other numbers are illustrative.
- hybrid_layer corrects hybrid: vendor_share flat at 1.0 because the 12 team-weeks fund the layer, vendor adapter and S-009 migration but no own decoder (all five critiques).
- hybrid_layer run_cost_monthly 4,500 instead of 9,000: no decoder data licences; about 0.3 FTE layer upkeep (1 FTE about 10,000 a month, from build's 21,000 minus 6,000 licences for 1.5 FTE) plus buy's 1,500 vendor management.
- hybrid_layer_measured adds 2 team-weeks for VIN landing pages (CMO), fee_growth_per_year 0.05 for a contract price cap (CEO), VIN-entry-first sequencing (CPO) and a 10 per cent holdout for 8 weeks (CDO); the holdout's small value loss is not modelled.
- Own home-market decoding is not priced in any hybrid_layer version; it should come back as a separate candidate with its own effort, licences and owner.
