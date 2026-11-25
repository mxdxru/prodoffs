# Decision brief: vin-buy-vs-build

**Status:** Accepted. **Option:** H3. **Round:** 2.

## Roadmap

| Initiative | Version |
|---|---|
| Vehicle identification by VIN | Hybrid layer, VIN entry first, holdout, price-capped vendor, VIN landing pages |

Capacity: 14 of 24 team-weeks.

## Cost per role

| Role | Deviation | Tolerance | Mood |
|---|---|---|---|
| CEO | 0% | 20% | pleased |
| CPO | 0% | 19% | pleased |
| CTO | 5% | 18% | pleased |
| CMO | 0% | 20% | pleased |
| CDO | 2% | 14% | pleased |

## Future-proof check

- **Two new EU markets, H2:** on track
- **Marketplace, year end:** on track
- **Wrong-fitment returns down by a third:** on track

## Shortcuts this plan creates

- **S-042** All VIN decoding stays with the vendor; own decoding is a separate later decision. Cost later: Per-lookup fees for every VIN until own decoding is approved and built; growth capped by contract.

## Shortcuts this plan pays down

- S-009

## Business case

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

## Positions

| Role | Stance | Preferred | Key idea | Top risk |
|---|---|---|---|---|
| CDO | Our vehicle ID, vendor as one source | vehicle-id: hybrid | Shadow-decode: log both vendor result and our own decoder result for every home-market VIN; switch a market only when ours matches vendor precision on 30 days of data | Buy: S-040 plus S-009 means two systems on external IDs; marketplace launch at year end needs a remap nobody has planned |
| CEO | Hybrid: revenue by month 3, marketplace safe | vehicle-id: hybrid | Negotiate the vendor contract for hybrid with a 2-year price cap, a volume tier above 100k lookups a month and no exclusivity, using our own-decoding roadmap as leverage | Buy: the marketplace at year end inherits vendor IDs; the remap (8 to 10 weeks) lands exactly when marketplace engineering is needed, and the vendor can raise prices knowing we cannot leave |
| CMO | VIN live by month 3, full coverage | vehicle-id: hybrid | Soft launch on the vendor behind the thin first cut of the layer at week 6-8 for paid-search VIN landing pages only, measure entry share and conversion before the public claim | Build: launching a 'fit guaranteed' message on 72% coverage creates a promise we break in public, which would cross my broken_promise red line once announced |
| CPO | Hybrid, but VIN live before spring | vehicle-id: hybrid | Sequence hybrid customer-first: week 1 to 6 thin vehicle-ID mapping table plus VIN entry wired to the vendor; richer layer and own decoding after the season | Build ships after the spring season and with 28% dead ends; workshops try VIN once, fail, and go back to dropdowns for good |
| CTO | Own vehicle-ID layer, vendor behind it | vehicle-id: hybrid | Contract the vendor with our own vehicle IDs as the integration key and a 12-month exit clause, so switching is a config change | Buy: every sprint after launch adds systems on vendor IDs, so the S-040 remap grows past 10 weeks by marketplace launch at year end |

## Pros and cons by alternative

### buy

**Pros**

- Fastest path to a measured baseline: VIN-identified sessions visible within 2 months (CDO)
- Hit rate 0.95 from day one across all markets, including the two H2 countries (CDO)
- Claimed precision 0.985 is the best available on day one (CDO)
- Best 3-year net in the case (839,880) and payback in month 4 (CEO)
- Value in month 2, so conversion and returns move inside revenue_q1's two-quarter window (CEO)
- 4 team weeks leaves 20 of the 24-week budget for other revenue work (CEO)
- Fastest answer to competitors who already offer VIN search: live in about 2 months (CMO)
- 95% hit rate and 98.5% precision from day one, enough to say 'parts that fit' (CMO)
- VIN landing pages for paid search can go live with the launch (CMO)
- Fastest path: 4 team-weeks, value in month 2, VIN entry live well before the spring season (CPO)
- Hit rate 0.95 and precision 0.985 from day one, so workshops get few dead ends (CPO)
- Leaves 20 of 24 team-weeks for the season's other workshop features (CPO)
- 4 team-weeks, live in month 2; leaves 20 of 24 weeks for other work (CTO)
- 95% hit rate and 98.5% precision from day one, including foreign VINs for eu-markets (CTO)
- No new service to own beyond an integration (CTO)

**Cons**

- Breaks red line own_vehicle_id: S-040 keys search, cart and returns to the vendor's vehicle IDs (CDO)
- Repeats D-0018: a second system on external IDs on top of open S-009, making the marketplace remap 8 to 10 weeks (CDO)
- Marketplace sellers cannot be matched to an identity we do not own; every match runs through vendor IDs (CDO)
- Vendor match quality is a black box; no way to audit wrong matches against our own fitment data (CDO)
- S-040 keys search, cart and returns to vendor IDs and blocks the marketplace bet; block_on_strategy_risk makes it unacceptable as specified (CEO)
- Deepens S-009 instead of fixing it: two supplier ID schemes, no own layer (CEO)
- Margin leak: about 97,500 lookups a month at 0.08 plus 15% a year price growth and a 6,000 monthly minimum; no leverage at renewal (CEO)
- S-040 blocks the marketplace: third-party listings cannot carry the same fitment promise, so the story splits in two at year end (CMO)
- Fitment claim depends on a vendor we cannot control; a vendor outage or price hike hits a public promise (CMO)
- S-040 keys search, cart and returns to vendor IDs and blocks the marketplace; strategy-risk rule can veto it outright (CPO)
- Doubles down on S-009: a second supplier-ID dependency in the same flows customers touch (CPO)
- Vendor price increases (15% a year) arrive with no leverage and could force rationing VIN lookups later (CPO)
- Creates S-040: search, cart and returns keyed to vendor IDs, which blocks marketplace (breaks no_strategic_blocker) (CTO)
- Deepens S-009 instead of paying it down: a second supplier's IDs spread through core systems (CTO)
- Not reversible: 8 to 10 weeks to remap, no leverage on the 15% yearly fee growth (CTO)

### build

**Pros**

- Full data ownership: vehicle identity becomes our asset, reusable for marketplace sellers (CDO)
- Fixes S-009 (CDO)
- Every decoding rule is auditable, so wrong matches can be traced and corrected (CDO)
- No per-lookup fees, so best on margin once running; fixes S-009 (CEO)
- Full ownership of vehicle IDs for marketplace matching (CEO)
- Own fitment data could become a differentiator we can market as ours (CMO)
- No per-lookup fee eating into paid-search margin at scale (CMO)
- Fixes S-009 and owns the vehicle model for marketplace listings (CPO)
- No per-lookup fee pressure on how freely we offer VIN entry (CPO)
- Fixes S-009: we own the vehicle-ID layer and the decoder (CTO)
- No per-lookup fees; full control of mapping quality long term (CTO)

**Cons**

- Year-1 hit rate 0.72 and precision 0.95: one wrong match in twenty, and wrong matches cost more than no match (CDO)
- S-041 blocks eu-markets: 6 to 8 weeks of data sourcing per new country (CDO)
- Value lands only at month 8, so returns-down cannot be measured until late in the 12 months (CDO)
- 22 of 24 team weeks leaves almost nothing for instrumentation and data quality tooling (CDO)
- Year 1 net -32,127 and payback in month 31: no visible revenue within two quarters (CEO)
- 22 of 24 team weeks for one initiative; nothing else ships (CEO)
- S-041 covers home markets only and blocks the eu-markets H2 bet (6 to 8 weeks per country) (CEO)
- Hit rate starts at 72%: a worse customer experience than the vendor at launch, which can hurt conversion rather than lift it (CEO)
- Run cost 21,000 a month is a fixed cost that does not shrink if VIN adoption is lower than 25% (CEO)
- Month 8 time to value: competitors keep the VIN advantage for most of the year (CMO)
- 72% hit rate in year 1 means one in four VINs fails; cannot say 'guaranteed' with that (CMO)
- S-041 blocks the two new EU markets in H2: no VIN story at launch there, worst moment to lack it (CMO)
- Breaks red line season_window: value in month 8, i.e. mid-summer, after the spring repair season (CPO)
- Year-1 hit rate 0.72: more than one VIN in four is a dead end, which kills workshop adoption on first try (CPO)
- Precision 0.95 in year 1 risks wrong vehicles shown as certain, the opposite of what ux_quality requires (CPO)
- 22 of 24 team-weeks: nothing else ships for workshops this half (CPO)
- S-041 blocks eu-markets: new countries launch without VIN entry (CPO)
- Creates S-041: home markets only, which blocks eu-markets in H2 (breaks no_strategic_blocker) (CTO)
- 22 of 24 team-weeks with no buffer; any slip pushes past the budget (CTO)
- Time to value 8 months and 72% hit rate in year 1 work against returns-down (CTO)
- Needs about 1.5 FTE permanent upkeep; owning team must be named before start (no_orphan_service) (CTO)

### hybrid

**Pros**

- Own vehicle-ID layer fixes S-009 and keeps core systems on our IDs, so own_vehicle_id holds (CDO)
- Vendor precision 0.985 and hit rate 0.95 from month 3, swapped for own decoding per market when ours is proven (CDO)
- Same layer serves marketplace seller listings and new markets without remapping (CDO)
- Running vendor and own decoder side by side gives a measured precision comparison, not a claimed one (CDO)
- Breaks no strategic bet: S-042 blocks nothing, fixes S-009, own vehicle-ID layer serves marketplace and new markets (CEO)
- Value in month 3 with 95% hit rate, so revenue_q1 is still met (CEO)
- 580,744 over 3 years, payback month 9; gives up about 260k versus buy to keep the marketplace and avoid a later remap (CEO)
- Vendor share falls to 35% by year 3: per-lookup fees shrink instead of growing, and we hold renegotiation leverage (CEO)
- 12 team weeks fits the 24-week budget with room left (CEO)
- Live by month 3, same 95% hit rate and 98.5% precision as buy, so the 'fit guaranteed' message holds from launch (CMO)
- One vehicle-ID layer for own catalog and marketplace: the same fitment promise covers third-party sellers at year end (CMO)
- No blocked bet: EU markets launch with VIN via the vendor (S-042) (CMO)
- Same customer-facing quality as buy (0.95 hit rate, 0.985 precision) because the vendor answers every lookup at launch (CPO)
- Fixes S-009 and avoids S-040, so it does not block marketplace or eu-markets (CPO)
- Value in month 3; can still make the spring window if the customer path is built first (CPO)
- Fixes S-009: own vehicle-ID layer, vendor replaceable behind it (CTO)
- 12 of 24 team-weeks, so 12 weeks buffer; live in month 3 (CTO)
- Vendor covers foreign VINs, so eu-markets is not blocked; marketplace sellers map to our IDs (CTO)
- Reversible: switch vendor or add own decoding per market without touching search, cart or returns (CTO)

**Cons**

- S-042: long-tail and foreign VINs stay vendor dependent, so data_ownership is partial for those (CDO)
- 12 team weeks, 3 times buy; risk that the layer gets cut thin and the mapping stays manual (CDO)
- Mapping vendor vehicle IDs to our IDs is a new manual data task unless it is automated and monitored (CDO)
- Per-lookup fees and the 6,000 minimum stay for the long tail and foreign VINs (S-042) (CEO)
- Own decoding from year 2 is a promise, not a plan yet; if it slips, hybrid becomes buy with an extra layer and higher run cost (9,000 a month) (CEO)
- One month later to value than buy (CEO)
- About one month later than buy; one more month competitors own the VIN message (CMO)
- 12 team-weeks leaves less room for landing pages and VIN-based campaign tooling (CMO)
- 12 team-weeks and 3 months to value: starting early December lands around early March, zero slack before the season (CPO)
- Risk that the internal layer work crowds out the UX work (VIN input, scan, confidence display) and we ship a half-finished flow (CPO)
- Half of the remaining capacity goes to plumbing customers never see (CPO)
- S-042: long-tail and foreign VINs stay on per-lookup fees (CTO)
- About 259k less 3-year net than buy on paper, before the remap cost buy defers (CTO)
- Own decoding in year 2 is extra effort not in the 12 weeks; the case's vendor_share curve depends on it (CTO)


## Implementation plan

| Step | Owner | Weeks | Done when |
|---|---|---|---|
| Define own vehicle-ID schema and mapping table from supplier and vendor IDs; catalog team named owner of the vehicle-ID service | CTO | 1-2 | Schema merged, supplier and vendor IDs map to our vehicle IDs with mismatch alerts, owning team recorded before any VIN-entry work starts |
| Sign vendor contract keyed to our vehicle IDs: fee growth capped at 5% a year, 12-month exit clause, match confidence and raw attributes returned, volume tier above 100k lookups a month | CEO | 1-3 | Contract signed with the 5% yearly price cap, exit clause and confidence scores; no exclusivity |
| Vehicle-ID layer service and vendor adapter, then VIN entry in search and cart through the layer only: dropdown prefilled on a miss, one clarifying question on ambiguous matches, VIN cache per garage account | CPO | 3-6 | VIN entry live for all non-holdout customers by end of week 6 (mid-January); every VIN resolves to our vehicle ID and no vendor ID is stored outside the layer |
| Instrumentation and 10% holdout from launch day: VIN entry, hit rate, match confidence, conversion, checkout completion and wrong-fitment returns by vehicle source | CDO | 5-14 | Dashboard live on launch day; holdout runs exactly 8 weeks from launch and is switched off by end of week 14; readout compares results with business_case.md assumptions |
| VIN landing pages for the top 50 paid-search vehicle queries, VIN field on product pages; scoped 'fit guaranteed' claim held back until precision is measured | CMO | 5-8 | Landing pages live within 2 team-weeks; public guarantee only after measured precision on our catalog reaches 0.98 in the holdout readout |
| Migrate search, cart and returns off supplier IDs onto our vehicle IDs | CTO | 7-12 | Zero reads of supplier or vendor vehicle IDs in search, cart and returns; S-009 marked fixed in memory/shortcuts.yaml before the spring season |
| Month-9 go/no-go on own home-market decoding from measured lookup volume, vendor spend, hit rate and precision | CEO | 36-39 | Decision recorded; on go, own home-market decoding is added to candidates.yaml as a separate candidate with its own effort, licences and owning team |

**Success metrics**

| Metric | Baseline | Target | Measured by |
|---|---|---|---|
| Search-to-order conversion of VIN-identified sessions versus holdout | 3.8% (vehicle unknown) | 4.8% or higher | cdo, 8-week holdout readout, week 14 |
| Checkout completion uplift on orders from VIN-identified sessions | holdout completion rate | +2% or more versus holdout | cdo, 8-week holdout readout, week 14 |
| Wrong-fitment return rate on VIN-identified orders | about 7.7% of orders (17% returns, 45% fitment-related) | about 3.1% or lower (60% of fitment returns removed, scaled by 0.985 precision) | cdo, monthly from launch; returns lag, so first firm read at week 14 |
| VIN hit rate and precision measured on our catalog | vendor claim: hit rate 0.95, precision 0.985 | hit rate at least 0.95 and precision at least 0.985; below 0.975 triggers the CDO dissent | cdo, weekly from launch |

## Disagreements

- **CTO:** VIN entry first (live around week 6) runs ahead of the search, cart and returns migration. Under season pressure the quick path is to store the vendor's vehicle ID in search and cart "for now", which recreates S-040 by the back door and leaves S-009 open past the season. The migration then competes with marketplace work and never finishes. Revisit if: Any VIN-entry code path writes or reads a vendor vehicle ID outside the vehicle-ID layer (checked at the week 6 launch review and every release after), or search, cart and returns still read supplier IDs at end of week 12. Either one stops new VIN features until the layer path is restored and S-009 is closed.
- **CPO:** The 10 per cent holdout withholds VIN entry from one session in ten during the spring repair season, when workshops need it most. Each held-out workshop that hits a dropdown dead end in March is a lost first impression, and the case does not model that loss. Revisit if: The holdout runs past 8 weeks after launch (end of week 14), or by week 4 of the holdout the VIN cohort already shows search-to-order conversion at least 0.5 points above holdout with a significant result, in which case the holdout is cut to 5 per cent or ended early.
- **CEO:** Steelman of buy (shared by the CMO): direct vendor integration is live in month 2 for 4 team-weeks, frees 10 more team-weeks for other revenue work and leads H3 by 186,110 over three years (839,880 versus 653,770). Even after the 8 to 10 week S-040 remap (72k to 90k) it stays ahead on paper. The layer is only worth it while the marketplace bet is real. Revisit if: The marketplace bet is dropped from strategy.yaml or moved beyond the next 12 months, or VIN entry is not live for customers by end of week 8. Then re-run the case and re-score buy against the remaining layer work.
- **CDO:** Steelman of own decoding (shared by the CTO on cost): H3 owns the vehicle ID but not the decoding. Every VIN stays on per-lookup fees and on a vendor precision claim (0.985) that has never been measured on our catalog mapping. Build is the only version whose year-2 economics are actually paid for, and the decoding rules would be auditable. Revisit if: Measured vendor precision on our catalog falls below 0.975 over the 8-week holdout, or monthly vendor spend exceeds 12,000 EUR, or home-market VIN lookups exceed 150,000 a month (assumption: about 97,500). Any one brings own home-market decoding forward as a separate candidate before the month-9 go/no-go.
