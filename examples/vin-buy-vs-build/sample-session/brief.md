# Decision brief: Vehicle identification by VIN: buy a vendor API, build our own decoder, or a hybrid?

Decision owner: Head of Product. Roles: Executive, Product, Engineering, Marketing, Data, Legal. Round 1.

No agreement. Closest option: **hybrid_terms_conditional**. Head of Product decides.

**Decision:** pending. The agents recommend; Head of Product decides.

## Option

| Initiative | Version |
|---|---|
| Vehicle identification by VIN | Hybrid, phased: vendor behind own vehicle-ID layer, on 24 November vendor terms |

Capacity: 14 of 24 team-weeks.

## Cost per role

| Role | Deviation | Tolerance | Mood |
|---|---|---|---|
| Executive | 30% | 20% | angry |
| Product | 26% | 19% | angry |
| Engineering | 14% | 18% | neutral |
| Marketing | 0% | 20% | pleased |
| Data | 19% | 14% | angry |
| Legal | 12% | 20% | neutral |

## Strategy check

- **Revenue +20% this year:** this option adds about 1,078,111 revenue in year 1, 9% of the growth target.
- **One-off investment:** 126,000 against a limit of 150,000: within.
- **Added run cost per month once live:** 17,775 against a limit of 15,000: BREACH.
- **Payback, months:** 10 against a limit of 12: within.

## Future-proof check

- **Two new EU markets, H2:** on track
- **Marketplace, year end:** on track
- **Wrong-fitment returns down by a third:** on track

## Shortcuts this plan creates

- **S-042** Long-tail and foreign VINs stay dependent on the vendor. Cost later: Per-lookup fees stay for the long tail; renegotiation needed at volume.

## Shortcuts this plan pays down

- S-009

## Business case

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

## Positions

| Role | Stance | Preferred | Key idea | Top risk |
|---|---|---|---|---|
| Data | Hybrid: own vehicle ID, vendor only as decoder | vehicle-id: hybrid | Abstain below a confidence threshold: wrong match costs more than no match | Vendor reply on data-use conditions is open; if it keeps the 24-month retention and reuse with no storage right for us, hybrid loses its compounding benefit and drifts toward buy |
| Engineering | Own vehicle-ID layer, vendor behind it | vehicle-id: hybrid | Hybrid in two phases: phase 1 (about 8 weeks) ships the layer, vendor adapter and our own IDs for spring; phase 2 (about 4 weeks) adds cache, fallback and the S-009 migration | Run-cost guardrail breach in Hybrid (16,800 vs 15,000) if cache and negotiation do not close the gap |
| Executive | Hybrid, but only with run cost under 15k | vehicle-id: hybrid | Thin abstraction variant: buy now, own vehicle-ID mapping layer from week 1, only 6 to 8 weeks, a possible new option between buy and hybrid | Run cost: hybrid is 1,800 a month over the guardrail unless levers 1, 2 or 6 land; a breach is a red line for me |
| Legal | Hybrid, only on a processor-only vendor contract | vehicle-id: hybrid | Hybrid with a pilot: sign a 6-month pilot with ramp-up minimum fee, a DPA and a price cap; convert to 36 months only if measured precision is at least the stated level | Signing the offer as drafted: vendor retains and reuses VINs for 24 months; breach of Art 28 and possible fines of up to 10 million EUR or 2% of turnover for processor-related violations (Art 83(4)), and customer trust loss [lawyer] |
| Marketing | Hybrid, ship early, claim only measured fit | vehicle-id: hybrid | Staged option: buy first (4 weeks) behind a thin own vehicle-ID layer, so the first release is vendor-only and the layer grows later; ask the facilitator to add it as a version of hybrid. | Public promise we cannot keep: a fit or precision claim made from the vendor's 98.5% before we measure it on our catalog |
| Product | Hybrid, but VIN entry live in weeks | vehicle-id: hybrid | Phased hybrid: ship VIN entry on the vendor in weeks 5 to 6 behind a thin mapping, then complete the vehicle-ID layer in weeks 7 to 14. Customer sees value in January, we avoid S-040. | Vendor reply on VIN data use is outstanding; 24-month retention and reuse may be a Legal red line, which would delay any option that depends on the vendor (Buy and Hybrid). |

## Pros and cons by alternative

### buy

**Pros**

- Fastest to a measurable result: 4 team-weeks, value from month 2, so we get a baseline-vs-treatment readout before spring (Data)
- Best three-year net in the case (839,880) and inside all guardrails (Data)
- Highest day-one coverage (95% claimed) means the least no-result noise in the experiment (Data)
- 4 weeks (range 3 to 6), smallest capacity draw (17% of 24), live well before spring (Engineering)
- Payback month 4 and best 3-year net in the case (839,880) (Engineering)
- Within every guardrail on paper (Engineering)
- Termination for convenience after month 12 gives a legal exit (Engineering)
- Inside every guardrail: one-off 36k vs 150k limit, payback month 4, run cost within 15k (Executive)
- Best 3-year net 839,880; year 1 net 270,619; 10% of the growth goal (Executive)
- 4 team-weeks, leaves 20 of 24 weeks for other bets before spring (Executive)
- Fastest to live; easiest to hit the spring season (Executive)
- Fastest to market; vendor carries registry and manufacturer data licensing risk (Legal)
- Termination for convenience exists (after month 12), so it is not a contract without an exit (Legal)
- Fastest: 4 team-weeks, so VIN entry can be live well before the spring season and campaign planning can start now (Marketing)
- Best year 1 revenue (1,197,901) and payback in month 4; the earliest campaign proof points (Marketing)
- Within every guardrail, so no budget fight that delays the launch date (Marketing)
- Smallest effort: 4 team-weeks, so VIN entry can be live around mid January, well before spring. (Product)
- Best numbers in the case: 839,880 3-year net, payback month 4, all guardrails within. (Product)
- Leaves 20 of 24 capacity weeks for fixing search UX and fallbacks. (Product)

**Cons**

- Breaks own_core_data: search, cart and returns keyed to the vendor's vehicle IDs (S-040); mapping to catalog standards costs extra (Data)
- Vendor may retain VINs 24 months and use them to improve its product: our customer and vehicle data trains their asset (Data)
- No own VIN-to-vehicle table accumulates, so every future lookup is rented and exit means 8 to 10 weeks of remap (Data)
- Marketplace third-party listings cannot be matched to our own vehicle keys; the data model for sellers is hostage to the vendor (Data)
- Creates S-040 on top of open S-009: search, cart and returns keyed to proprietary vendor IDs. Blocks marketplace. Breaks my red line no_strategic_blocker (Engineering)
- Vendor IDs returned as proprietary; mapping to catalog standards costs extra, so lock-in is priced by the vendor (Engineering)
- Annual price review up to 15%, 36-month term, SLA credits capped at 10% of the fee, which is no remedy for an outage on the search path (Engineering)
- Vendor may retain VINs for 24 months and reuse them; needs Legal, and a vendor outage degrades search with no fallback (Engineering)
- Remap later costs 8 to 10 weeks, more than the 8 weeks it saves, and S-009 stays open (Engineering)
- S-040 blocks the marketplace bet; 8 to 10 team-weeks (about 72-90k at 9k) to remap later (Executive)
- Lock-in: 36-month term, proprietary IDs, up to +15% a year, no leverage once everything is keyed to vendor IDs (Executive)
- Vendor data clause (24-month retention, reuse to improve the service) is unresolved and may be a Legal red line (Executive)
- Returns-down bet depends on a vendor precision figure we have not verified (Executive)
- As drafted it fails my red line: vendor may keep VINs 24 months and use them to improve its service, which makes it a controller for that purpose or an unauthorised use beyond our instructions (GDPR Art 28(3)(a), 28(10)) [lawyer] (Legal)
- Sub-processors only 'on request': we need a list and prior notice and objection right (GDPR Art 28(2), 28(4)) (Legal)
- Vendor's proprietary IDs: no exit in practice, because search, cart and returns would be keyed to IDs we cannot keep (S-040) (Legal)
- Price review up to 15% a year, uncapped by index; minimum fee 6,000 EUR whether or not volume arrives (Legal)
- SLA credits capped at 10% of the monthly fee: a VIN outage in season costs us far more than that (Legal)
- Accuracy claims (95% coverage, 98.5% precision) are the vendor's own test set; we cannot pass them on to customers (Legal)
- Vendor 24-month VIN retention and reuse clause may contradict what we tell customers about their data (needs legal review before any privacy-related copy) (Marketing)
- Blocks the marketplace bet (S-040): third-party sellers could not be matched, so the 'works for every seller' claim is off the table (Marketing)
- No differentiation: any competitor can license the same decoder; the claim 'enter your VIN' is parity, not advantage (Marketing)
- Price review up to 15% a year pushes cost per lookup, and so cost per acquired order, upward (Marketing)
- S-040: search, cart and returns keyed to vendor IDs; 8 to 10 weeks to remap, blocks the marketplace bet (third-party listings need our own vehicle matching). (Product)
- Vendor IDs are proprietary; mapping to catalog standards costs extra. Any later vendor switch is a customer-visible migration (garage profiles with saved VINs). (Product)
- Vendor may keep VINs 24 months and reuse them: a trust and legal question that can surface in customer-facing copy. (Product)
- Wrong-fitment bet depends entirely on an unverified 98.5% precision. (Product)

### build

**Pros**

- Cleanest data ownership: own decoder, own IDs, own VIN table; fixes S-009 (Data)
- Full control over precision and coverage rules, and per-decision explainability (Data)
- Full control of data, no per-lookup fee, no vendor dependency (Engineering)
- Fixes S-009 and gives the marketplace a proper vehicle-ID layer (Engineering)
- Owns the data asset; no per-lookup fee at scale; fixes S-009 (Executive)
- Best long-run unit cost if volume grows (Executive)
- No third-party processor for the lookup itself: simplest GDPR picture (we stay sole controller) (Legal)
- No vendor price or retention terms to negotiate (Legal)
- Own data asset and a story we fully control (no vendor dependency in the claim) (Marketing)
- Strongest long-run differentiation if coverage became excellent (Marketing)
- Own data and IDs, fixes S-009, no per-lookup fee. (Product)
- Strongest long-run control of fitment quality and of the marketplace matching. (Product)

**Cons**

- Month 8 to value: no spring measurement window, and the readout lands after the season we are optimising for (Data)
- Hit rate starts at 72% and precision at 95%; wrong data in year 1 means more wrong-fit returns, not fewer (Data)
- Breaches three guardrails (198k one-off, 21k run, 31 months payback); home markets only, blocks eu-markets (S-041) (Data)
- 22 weeks (range 20 to 30) of 24 available: 9% buffer at best, probable overrun. Blocks other catalog work for two quarters (Engineering)
- Creates S-041: home markets only, 6 to 8 weeks per new country. Blocks eu-markets (two launches in H2). Breaks no_strategic_blocker (Engineering)
- Breaches all three guardrails: 198,000 one-off, 21,000 a month run cost, payback month 31 (Engineering)
- Needs registry and manufacturer data contracts and an owner for data freshness; no team is named today, which risks no_orphan_service (Engineering)
- Misses the spring season if the range runs long (Engineering)
- Breaches three guardrails: 198k one-off, 21k/month run cost, payback month 31 (Executive)
- Year 1 net is negative (-32,127); only 3% of growth goal (Executive)
- 22 of 24 team-weeks, nothing left for eu-markets or marketplace (Executive)
- S-041 blocks eu-markets: 6 to 8 weeks per new country (Executive)
- Misses the spring season risk (Executive)
- Data licensing is the legal weak point: registry access differs by country, and manufacturer data is accessible under the EU rules on repair and maintenance information (Regulation (EU) 2018/858, Chapter XV) only for defined purposes and on defined terms; database rights (Directive 96/9/EC) may apply [lawyer, per country] (Legal)
- Each new country (eu-markets bet) means a new data source and a new licence review, 6 to 8 weeks each per S-041 (Legal)
- We then own accuracy: any 'fits your car' claim rests on our own data and our own liability (Legal)
- 22 team-weeks of 24 and a launch very likely after the spring season starts: we lose a selling season while a competitor campaign runs (Marketing)
- Home markets only (S-041): cannot say 'across Europe' and blocks the two new EU markets bet; launch campaigns there would have no VIN story (Marketing)
- Year 1 net negative (-32,127) and three guardrail breaches (Marketing)
- 22 team-weeks of 24; from a 4 Dec decision it ships around May, after the spring season starts. Breaks my market_window red line. (Product)
- Home markets only (S-041): blocks the two new EU markets bet; 6 to 8 weeks per new country. (Product)
- Breaches three guardrails: one-off 198,000 vs 150,000, run cost 21,000 vs 15,000, payback month 31 vs 12. (Product)
- Risk of a half-finished decoder: customers whose VIN is not covered hit a dead end on day one. (Product)

### hybrid

**Pros**

- Meets own_core_data: our own vehicle-ID layer is the key in search, cart, garage and returns; vendor IDs live only in a mapping table (Data)
- Every vendor lookup is written to our own VIN-to-vehicle store, so the asset compounds and vendor_share falls to 0.55 then 0.35 (Data)
- Live in month 3 (12 team-weeks), early enough for a holdout readout before spring (Data)
- Same ID layer can accept third-party marketplace items, protecting that bet (Data)
- Fixes S-009 and supports the returns-down bet by logging fitment outcome per resolved vehicle (Data)
- Own vehicle-ID layer (catalog-owned interface) with the vendor as one replaceable provider behind it. Fixes S-009 (Engineering)
- 12 weeks (range 10 to 16) is 50% of capacity, 8 to 12 weeks of buffer (Engineering)
- S-042 blocks nothing; keeps marketplace and eu-markets open. Third-party sellers can be matched to our IDs, not the vendor's (Engineering)
- Reversible: vendor can be swapped, or own decoding added per country, without remapping search, cart or returns (Engineering)
- Payback month 9 and 3-year net 580,744, inside the 12-month payback guardrail (Engineering)
- Keeps marketplace and eu-markets open: S-042 blocks nothing, own vehicle-ID layer fixes S-009 (Executive)
- Year 1 net 176,057, 3-year net 580,744, payback month 9, 9% of growth goal (Executive)
- 12 of 24 team-weeks; capacity left for the other bets (Executive)
- Vendor becomes replaceable behind our layer, which is our lever on price (Executive)
- Own vehicle-ID layer means vendor IDs are mapped to ours, so exit is a technical task, not a rewrite (Legal)
- Lets us put the vendor behind a clean DPA and swap it if terms are breached or prices rise (Legal)
- Keeps the VIN stored on our side under our own retention rule (my garage), not the vendor's (Legal)
- Vendor behind our own vehicle-ID layer: 12 team-weeks, still plausible before spring if started in January and a thin first release ships on the vendor (Marketing)
- Keeps marketplace and new-market stories open (S-042 blocks nothing), so one message can run across home markets, new EU markets and third-party sellers (Marketing)
- Own IDs make 'my garage' with a stored VIN, repeat-order reminders and CRM campaigns possible: a retention channel that gets cheaper with use (Marketing)
- Year 1 revenue 1,078,111, only about 10% below buy, payback month 9 (Marketing)
- Own vehicle-ID layer (12 team-weeks) means saved garages, search, cart and returns key to our IDs, so vendor swap or own decoding later is invisible to customers. (Product)
- Protects both the marketplace and the new-markets bets (blocks: none). Fixes S-009. (Product)
- 3-year net 580,744, payback month 9, year 1 revenue 1,078,111 (9% of growth goal), nearly equal to Buy in year 1. (Product)

**Cons**

- Breaches the monthly run-cost guardrail (16,800 vs 15,000); a cost question for Executive, not a data red line (Data)
- Long-tail and foreign VINs stay on vendor (S-042); fee per lookup stays until own decoding matures (Data)
- Needs a contract that lets us store and reuse results. Vendor reply on our data-use conditions is still open (Data)
- Breaches run-cost guardrail: 16,800 a month vs 15,000 (1,800 over) (Engineering)
- S-042: long-tail and foreign VINs stay on vendor fees; renegotiation needed at volume (Engineering)
- 3-year net about 259,000 lower than buy, and 8 weeks more engineering than buy (Engineering)
- Still a vendor dependency during the 36-month term unless the contract is changed; own layer needs a named operating team (Engineering)
- As drafted breaches the run cost guardrail: 16,800 vs 15,000 per month (+1,800) (Executive)
- Costs about 259k less than buy over 3 years (839,880 vs 580,744), the price of optionality (Executive)
- Payback month 9 is thin if adoption or conversion is 30% worse (Executive)
- Long-tail and foreign VINs stay on per-lookup fees; renegotiation needed at volume (Executive)
- Two data flows to document (us and vendor); more contract work up front (about 2 to 3 weeks of legal time) (Legal)
- Still depends on vendor for long-tail and foreign VINs (S-042), so price protection still matters (Legal)
- Breaches the run-cost guardrail (16,800 vs 15,000 a month); needs an owner decision or a price renegotiation (Marketing)
- Longest wait for a full launch story if the layer slips; risk of announcing before it works (Marketing)
- Long-tail and foreign VINs still depend on the vendor, so coverage claims must stay at the vendor-measured level (Marketing)
- Run cost 16,800 a month vs 15,000 guardrail: a breach to be fixed by cache, volume tiers or minimum fee, not ignored. (Product)
- 12 weeks is the wrong schedule if done as one big release; a naive plan lands in March, tight for spring. (Product)
- Long-tail and foreign VINs stay on the vendor (S-042) and fees continue. (Product)


## Trade-offs

What each role gave up in this option:

- **Executive:** 30% away from its opening position (tolerance 20%).
- **Product:** 26% away from its opening position (tolerance 19%).
- **Engineering:** 14% away from its opening position (tolerance 18%).
- **Data:** 19% away from its opening position (tolerance 14%).
- **Legal:** 12% away from its opening position (tolerance 20%).

Why the other options were not recommended:

- **hybrid_phased_draft** (Hybrid: vendor behind own vehicle-ID layer, own decoding later): red lines: broken_promise, guardrail_breach, lawful_basis; guardrails: added run cost per month once live; outside tolerance: executive 24% > 20%, data 27% > 14%, legal 47% > 20%.
- **buy_reference** (Buy: vendor API, direct integration, on 24 November vendor terms): red lines: no_strategic_blocker, own_core_data; new risk to Marketplace, year end; outside tolerance: executive 26% > 20%, engineering 66% > 18%, data 53% > 14%, legal 23% > 20%.

## Owner's answers to the roles' questions

- **Is the marketplace bet firm for year end?** Yes, firm. Do not trade it away for a cheaper integration.
- **Is the 15,000 run-cost guardrail a hard limit?** Hard limit for launch. A breach is not acceptable. Bring the run cost under it with volume tiers, a ramped minimum or caching.
- **Spring start date and soft launch?** First sales week is mid-March. Soft launch to 10% of traffic is acceptable and is the plan.
- **Who owns the vehicle-ID layer after launch?** A named owning team inside Engineering. The name is set before signature.
- **Term: 24 months, 36 months or a stage gate?** Sign 24 months to get the 5% price cap. Add a 12-month review.
- **Holdout: 10% without VIN entry for about 8 weeks, or 20% A/B?** 10% holdout for 8 weeks. Keep a 5% control until the mid-May returns readout.
- **Any fit guarantee or return promise in first-release scope?** No guarantee in the first release. Claims only after our own measurement.
- **VIN storage in 'my garage' in the first release?** No. First release keeps VINs only for the single lookup. Garage storage comes later with a DPIA.
- **May we negotiate volume tiers, a minimum-fee ramp and a 99.9% SLA?** Yes. Those are the levers for the run-cost gap.

## Disagreements

- None
