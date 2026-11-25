# Round 1: Executive

Role: executive. Phase: debate, round 1. Inputs read: assembly.md, answers.yaml (simulated owner answers), positions of all six roles, evidence/vendor-reply.md, business_case.md, task.yaml, candidates.yaml, memory/shortcuts.yaml. The business case is not recomputed here. Figures marked "my arithmetic" are simple sums on numbers already in those files, for `prodoffs.py case` to confirm.

## 1. Position in one line

Hybrid stays the candidate. Plain buy is out. The run-cost fix has to be written into the vendor contract before signature, not left in a plan.

## 2. What changed since my opening position

Owner answers (answers.yaml):

- Run cost 15,000 is a hard limit for launch. Fix it with volume tiers, a ramped minimum or caching. This confirms my opening red line.
- Marketplace is firm: "Do not trade it away for a cheaper integration." This closes plain buy. Buy only survives as a thin layer, which is hybrid phase 1 (section 4).
- Term: sign 24 months for the 5% cap, with a 12-month review. My opening condition (no term over 12 months without cap and data fix) is now met on paper, pending the DPA.
- First sales week is mid-March. Soft launch to 10% of traffic is the plan.
- Owning team named inside Engineering before signature.
- No garage VIN storage in the first release, and "First release keeps VINs only for the single lookup." See section 5, point 3.

Vendor reply (evidence/vendor-reply.md):

- Price up from 0.08 to 0.09 per lookup. The reply does not offer volume tiers, a lower minimum or a ramp.
- Processor-only terms, 30-day troubleshooting retention, no reuse. This removes the veto basis Legal raised.
- Catalog mapping included at no extra cost. This removes one cost I had flagged.
- Exit after month 12 with 3 months' notice (offer: 6 months).

Effect on the run-cost guardrail (my arithmetic, matches assembly section 3.1):

- Fee at 0.09 on 97,500 lookups is 8,775 a month. Hybrid run cost is 9,000 plus 8,775, about 17,800. The breach grows from 1,800 to about 2,800 a month.
- To reach 15,000 the fee must fall to 6,000, the minimum. That is a cut of 2,775 a month, or a per-lookup price of about 0.0615 at base volume.

## 3. The strongest option (hybrid), challenged

Hybrid is the consensus. Its weakest point is the own-layer run cost, not the vendor price.

- The 9,000 a month for the own layer is the largest run-cost item and the one with the least support in the files. Buy carries 1,500 a month plus the same fees. The hybrid-to-buy difference is therefore 7,500 a month, or about 270,000 over 36 months (my arithmetic). That is almost exactly the 259,136 three-year gap in the case. The three-year cost of hybrid over buy is the cost of running our own layer. Nobody has shown the build-up of the 9,000.
- If the layer really costs 9,000, hybrid can only sit under 15,000 when the fee is at or below the 6,000 floor. Any fee above the floor breaches the guardrail. Each 1,000 of layer cost overrun has to be cut from fees.
- My own growth criterion favours buy. Year 1: buy 1,197,901 revenue (10% of the 12M growth goal) against hybrid 1,078,111 (9%). Year-1 net is 270,619 against 176,057, a gap of about 94,600 (my arithmetic). Neither option comes near +20%. The owner should see that before the hybrid case is accepted.
- Hybrid is therefore chosen for strategy fit, not growth or return. Its value is the marketplace and eu-markets bets. If buy is replaced with the marketplace remap (72k to 90k, 8 to 10 team-weeks), the three-year gap is still about 170k to 190k (my arithmetic). Nobody has priced the marketplace bet against that. I accept hybrid only if the owner accepts that price explicitly.
- "The 12 remaining weeks fit the marketplace connector" (business case, opportunity cost) is not supported. No file sizes the connector. At 12 to 16 team-weeks for hybrid, 8 to 12 weeks remain, and that leftover has to cover the connector and any eu-markets work.

## 4. Buy with a thin layer is hybrid phase 1

The "thin layer buy" (executive, product, marketing) is not a separate option. Product's MVP is "behind a thin vehicle-ID mapping so no screen stores vendor IDs". That is hybrid phase 1 without the S-009 migration. Engineering's phase 1 (8 weeks) is the same thing. The real choice is phase 1 with S-009 deferred or the full 12 to 16 weeks in one release.

Two consequences:

- S-009 blocks marketplace (memory/shortcuts.yaml). Phase 1 leaves it open. Marketplace stays blocked until phase 2 closes S-009. Phase 2 needs a dated end, before the marketplace connector starts.
- Engineering's full hybrid plan (weeks 1 to 16 from 4 December) ends about 26 March (my date arithmetic: week 12 is 26 February, week 16 is 26 March). The owner's first sales week is mid-March. A single release has no slack, so phasing is needed for the date, not only for scope.

## 5. Weakest assumptions by role

Engineering
- The 12 team-weeks includes the S-009 migration, which memory/shortcuts.yaml costs at 8 weeks for an own layer on its own. That leaves about 4 weeks for the vendor adapter, mapping, VIN entry, cache, fallback and returns tagging. Engineering says the migration is "partly inside the 12" without showing the split.
- It is unclear whether the 25% buffer is already in the 12 or added on top. If added, the point estimate is 9.6, not 12.
- The plan's weeks 3 to 8 fall in the Christmas and New Year period. No estimate mentions it.
- Cache is the owner-named lever. Engineering's own cache plan depends on a repeat-VIN share Data has not supplied, and on storing VINs (point 3).

Product
- The MVP "in weeks 5 to 6" with a thin layer assumes about 4 weeks for the layer. memory/shortcuts.yaml puts an own layer at 8 weeks. The mid-January date is not supported by the file. The mid-March spring date still gives room, so this does not break the plan, but the January date should not be promised.
- Returns-down target (wrong-fitment returns down 33%) is set on a precision of 98.5% from the vendor's own test set. Product's own risk list says this may be lower.

Marketing
- Buy-first "is the one with no launch risk" ignores S-040, which the owner has ruled out. Marketing's preferred staged option is hybrid phase 1.
- The 25% usage is assumed. Marketing's own arithmetic says that at 15% usage, buy year-1 revenue falls by roughly 40% of the lookup-driven part. Usage is the largest revenue driver in the case, and nobody has a measured number.
- Acquisition effects are unpriced. They are upside only. I will not count them toward growth until measured.

Data
- "Each vendor lookup is written to our own VIN-to-vehicle store, so vendor_share falls to 0.55 then 0.35." These figures are not in the business case. They depend on storing VINs beyond the single lookup, which the owner has excluded for the first release.
- The 3.8% to 4.8% conversion gap includes self-selection. Data says so. This is the largest revenue driver in the case, and it is still unproven. The holdout is the right answer, and I support it.
- The decision rule (scale if the lift is at least 60% of the modelled +0.6 pt and precision is at least 97%) is sound. It reads out in May, after the spring decision. Scaling decisions need to be made on the mid-May readout, not later.

Legal
- The vendor's 30-day "troubleshooting" retention is still a standing vendor retention, not a deletion on request. Legal's contract item 7 asked for deletion within 30 days of a request. Legal must confirm whether the reply meets that or whether a shorter period is needed.
- The veto stands until a signed DPA exists. That is a signature gate, not a reason to reject hybrid.

Business case (for the owner, not a role)
- The returns benefit assumes 60% of fitment-related returns are removed (scaled by precision). The returns-down bet asks for a one-third cut in wrong-fitment returns. The case therefore assumes roughly 1.8 times what the bet requires. Legal calls the 60% an assumption. The case does not show how much of the 839k or 580k comes from returns and how much from conversion. Both need splitting before signature.
- The case's price path (15% a year, year 3 at 1.32 times) is stale. Under the new terms (0.09 with a 5% cap) the worst-case year-3 fee is about 0.099 per lookup, against about 0.106 in the case. Year 1 is worse (0.09 against 0.08). The rerun must use the new terms, not the offer.

## 6. The run-cost levers, checked

- Volume tiers: the 0.06 tier above 60,000 lookups is the executive's figure from the earlier offer discussion. The vendor reply does not offer it. It is not a lever until it is in writing. At 0.06 and 97,500 lookups the fee is 5,850, which is still under the 6,000 floor. Run cost would be exactly 15,000 with no headroom.
- Minimum fee ramp: the minimum only bites below about 66,700 lookups a month at 0.09 (6,000 divided by 0.09). At base volume it does nothing. It protects months 1 to 6 and the downside case. My earlier framing (lever for the gap) was too broad. It is a downside lever.
- Downside (17% adoption, about 66,300 lookups): the fee at 0.09 is 5,967, so the 6,000 minimum binds. Run cost is 15,000 exactly. Any own-layer overrun breaches. A lower minimum, for example 3,000, gives about 14,967 at 0.09 and about 12,967 at 0.06.
- Cache: reducing fees by 2,775 at 0.09 needs about 30,800 cache hits a month, or about 32% of base lookups being repeats. Data has not measured repeats. A VIN-keyed cache is also out of the first release if the owner's "keeps VINs only for the single lookup" applies to it. A VIN-prefix cache would avoid storing VINs but has no precision test. Cache is not a first-release lever until the owner clarifies and repeats are measured.
- SLA at 99.9%: the owner has allowed the ask. It has a cost that nobody has priced. It should be traded against the minimum fee, not added on top.

## 7. Amended position

- Hybrid, phased. Phase 1 (layer, vendor adapter, VIN entry with fallback, 8 weeks) live for the spring soft launch. Phase 2 (cache if allowed, S-009 migration, returns tagging) closes S-009 on a dated plan before the marketplace connector starts.
- Plain buy is out, per the owner's marketplace answer. Its three-year advantage (about 259k) is the price of our own layer and the marketplace bet. I accept that price only if the owner has seen the growth gap (about 94k in year 1) and the marketplace value is at least sketched.
- No signature until the vendor writes one of these, and the rerun shows run cost under 15,000 with headroom on both base and 17% adoption:
  - a tier at or below 0.06 from about 60,000 lookups a month, and a minimum at or below 3,000; or
  - a per-lookup price at or below about 0.06 with a minimum at or below 3,000; or
  - a layer run cost, once built up, low enough to fit under the guardrail at 0.09 with the 6,000 floor.
- If none of these is written by the time the DPA is agreed, the owner decides between accepting a recorded breach (with a month-6 review) and cutting the layer scope. I do not recommend a breach.

## 8. Conditions and questions

Conditions for my support of hybrid:

1. Written tier or minimum-fee terms that clear 15,000 with headroom (section 7).
2. A build-up of the 9,000 a month own-layer run cost, from Engineering, before the rerun.
3. Payback at or under 12 months at 17% adoption and 0.09 (the executive's 30% stress). The case says payback could move past 12. The script must say which.
4. A dated phase 2 that closes S-009.
5. A sized estimate for the marketplace connector and eu-markets work from the leftover 8 to 12 team-weeks.

Questions for the owner:

- Does "First release keeps VINs only for the single lookup" also exclude a cache keyed on the full VIN? If yes, cache is a phase 2 lever. If no, it is open for phase 1.
- Accept the growth gap: hybrid year-1 revenue is 9% of the 12M goal, against 10% for buy. Is the marketplace value enough to justify the three-year cost of our own layer, roughly 259k?
- Holdouts: 10% for 8 weeks plus 5% control to mid-May. My rough arithmetic is about 20k to 30k of revenue and 6k to 8k margin forgone against year-1 hybrid revenue. I support both holdouts. They are small against the 150k one-off.

Questions for others (to route):

- Engineering: the 9,000 layer build-up; the split of the 12 weeks between S-009 and the rest; whether the 25% buffer is inside the 12; the Christmas allowance.
- Data: repeat-VIN share, to size the cache.
- Legal: whether the 30-day troubleshooting retention meets the deletion-on-request clause.
- Owner or Data: how many of the 839k and 580k come from returns and how many from conversion.

## 9. Final stance

Hybrid, phased, and signed only when run cost clears 15,000 with headroom.
