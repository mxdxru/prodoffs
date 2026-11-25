# Business case: Vehicle identification by VIN

All figures in EUR, undiscounted, computed by `prodoffs.py case` from `business_case.yaml`.

| Alternative | One-off | Year 1 net | Year 2 net | Year 3 net | 3-year net | Payback | Monthly net at end |
|---|---|---|---|---|---|---|---|
| Buy: vendor API | 36,000 | 270,619 | 310,703 | 294,557 | **839,880** | month 4 | 24,546 |
| Build: own decoder | 198,000 | -32,127 | 132,397 | 170,564 | **72,834** | month 31 | 14,214 |
| Hybrid: vendor behind own layer | 108,000 | 176,057 | 256,343 | 256,343 | **580,744** | month 9 | 21,362 |
| Buy: vendor API, on 24 November vendor terms | 36,000 | 260,869 | 307,778 | 302,250 | **834,898** | month 4 | 25,188 |
| Hybrid, phased: vendor behind own layer, on 24 November vendor terms | 126,000 | 167,282 | 256,343 | 256,343 | **553,969** | month 10 | 21,362 |

## Against the strategy

| Alternative | Revenue added, year 1 | Share of growth goal | Guardrails |
|---|---|---|---|
| Buy: vendor API | 1,197,901 | 10% | within |
| Build: own decoder | 363,153 | 3% | breach: One-off investment 198,000 > 150,000; Added run cost per month once live 21,000 > 15,000; Payback, months 31 > 12 |
| Hybrid: vendor behind own layer | 1,078,111 | 9% | breach: Added run cost per month once live 16,800 > 15,000 |
| Buy: vendor API, on 24 November vendor terms | 1,197,901 | 10% | within |
| Hybrid, phased: vendor behind own layer, on 24 November vendor terms | 1,078,111 | 9% | breach: Added run cost per month once live 17,775 > 15,000 |

Goals: Revenue +20% this year (baseline 60,000,000, target +20%); Workshops 40% of revenue by year end.
Guardrails: max one off investment 150,000, max added run cost monthly 15,000, max payback months 12.

## Assumptions

- 600,000 part-search sessions a month; vehicle known today in 35% of them.
- If VIN entry is offered, 25% of the other sessions use it: about 97,500 lookups a month.
- Search-to-order conversion 4.8% with a known vehicle versus 3.8% without.
- Checkout completion uplift 2% on orders from VIN-identified sessions.
- Return rate 17%, of which 45% fitment-related; VIN identification removes 60% of those, scaled by precision. Cost per return 21.
- Average order value 118, gross margin 28%, team-week 9,000.
- Undiscounted; strategic effects (marketplace, new markets) are not priced in and are argued by the roles.
- Return-rate and fitment-share figures follow public industry reports for auto parts e-commerce; all other numbers are illustrative.
- SESSION CHANGE 1: added alternative buy_terms (copy of buy) with fee_per_lookup 0.09 (was 0.08) and fee_growth_per_year 0.05 (was 0.15). Source: evidence/vendor-reply.md, dated 24 November (assembly.md says 1 December; the file says 24 November). Price cap of 5% a year applies only if we sign for 24 months, which the owner has chosen (answers.yaml). The reply gives no cap after 24 months; this copy assumes the 5% rate holds for all three years of the horizon.
- SESSION CHANGE 2: added alternative hybrid_terms (copy of hybrid) with fee_per_lookup 0.09, fee_growth_per_year 0.05 (same source and assumption as change 1) and one_off_team_weeks 14 (was 12). Source: Engineering round 1 amended point estimate, range 12 to 18, confidence medium-low. Phase 1 about 8 weeks, phase 2 about 6 weeks. Engineering's figure, not verified against the S-009 register.
- SESSION CHANGE 3: no volume tier, minimum-fee ramp or SLA change is modelled. None is in the vendor reply. The executive's figures (0.06 above 60,000 lookups; a lower minimum) are not in this file; the script models a flat fee only.
- UNSOURCED, NOT CHANGED: run_cost_monthly 9000 for hybrid and hybrid_terms (own layer) and 1500 for buy and buy_terms. Engineering has not verified the 9,000 build-up and says a thin owned layer would carry the same owned-service cost. Engineering must supply the build-up before the rerun. Values kept as in baseline.
- NOT CHANGED: baseline, and the buy, build and hybrid alternatives as sent with the offer (fee 0.08, growth 0.15). Baseline is correct for the offer that was sent.
