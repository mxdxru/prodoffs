# Round 1: Engineering

Session 20261125-133804. Phase: debate, round 1. Role: Engineering.

Inputs read: assembly.md, answers.yaml, all six positions, evidence/vendor-reply.md, business_case.md, candidates.yaml, memory/shortcuts.yaml, strategy.yaml, task.yaml. Not found: sessions/20261125-133804/business_case.yaml and docs/role-protocol.md at the paths given. I used business_case.md and the assembly's notes.

Arithmetic below is ours, from business_case.md and the reply's terms. Nothing is rerun through prodoffs.py. Base lookups: 97,500 a month. Own-layer run cost: 9,000 a month, the figure the case uses for hybrid. I have not verified its build-up.

## 1. Open question: buy with a thin ID layer

Definition tested: a vendor adapter behind our own canonical vehicle_id. Vendor IDs live only in a mapping table (vendor_ref, source, confidence, timestamp). Search, cart, order lines, returns, analytics and the planned "my garage" key on our vehicle_id. The dropdown selector stays on the supplier IDs of S-009 until phase 2.

**Effort: 8 weeks point, range 6 to 10, confidence medium.** Raw estimate 6.5 weeks plus a 25% buffer (my assumption, same as the earlier position). Scope: ID schema agreed with Catalog, vendor adapter, mapping table, VIN entry behind a flag, event logging (vendor_ref, confidence, resolve), and the holdout flag. Out of scope: dashboard by country and model year, selector and "my garage" migration, cache, and any fallback beyond the existing dropdown.

Why 8 and not the 5 to 8 weeks other roles use: the register already prices this layer. memory/shortcuts.yaml S-009 reads "8 weeks to introduce an own vehicle-ID layer". D-0018 saved 5 weeks by deferring it. A thin layer pays that 8 weeks now. Product's 5 weeks (weeks 2 to 6) and Executive's 6 to 8 are the low end of the same work.

**Does it avoid S-040? Only under a rule.** S-040 is created when search, cart and returns are keyed to vendor IDs. If vendor IDs appear only in the mapping table, S-040 is not created. The rule needs enforcing: a review check, and a test that fails when a vendor ID appears as a key outside the mapping table. Without that, a thin layer is S-040 with one extra table.

**Does it clear S-009? No.** S-009 stays open until phase 2 moves the selector and "my garage" to our IDs. S-009 is what blocks the marketplace bet today. Thin buy without phase 2 leaves the marketplace blocked at year end. Phase 2 is not optional.

**Cost against hybrid.** Thin buy = phase 1 (8 weeks) plus phase 2 (about 6 weeks, see section 3). That totals the same as hybrid. The only difference is timing. It is hybrid, phased, under another name.

**Run cost.** This is where the Executive's version fails. The case's buy run cost (1,500 plus fees) assumes no owned layer. A thin layer is an owned service with on-call and an SLO. If the 9,000 own-layer figure is its run cost, thin buy at full ramp costs 9,000 plus 8,775 fees = 17,775, the same breach as hybrid. Thin buy is not inside 15,000 by default. Engineering must confirm the 9,000 build-up before anyone relies on either number.

**Ownership.** The owner's answer requires a named owning team inside Engineering before signature. The files do not name one. Engineering will name the team in week 1, and I am not naming it from the files.

**Vendor leverage.** With vendor_ref in one table and catalog mapping included at no cost, a vendor switch means swapping the adapter and re-decoding cached results. My estimate is 3 to 5 weeks, confidence low. S-040 remap is 8 to 10 weeks. The gap is real, but it only exists when the key rule holds.

**Naming.** Call it "hybrid, phased", not "buy with thin layer". Then no version exists that defers S-009 indefinitely. Per assembly section 3.2, I do not want a separate buy-thin version in candidates.yaml. Fold it into hybrid as phase 1.

## 2. Challenges

My strongest-option challenge: hybrid as drafted is the option everyone backs. Its weakest part is the run-cost route, which I have had to correct myself (section 3). The challenges to other roles follow.

- **Executive, lever arithmetic.** "Hybrid passes if run cost drops about 11%" is at 0.08. At the reply's 0.09 the cut needed is 2,775 of 17,775, about 16%. Equivalently, the layer would need to cost about 31% less.
- **Executive, the volume tier.** "0.06 above 60,000 lookups" is not in the vendor reply. Its structure decides the outcome. All-units at 0.06 gives 5,850 in fees, the 6,000 minimum binds, and run cost is exactly 15,000. Marginal pricing (60,000 at 0.09 plus 37,500 at 0.06 = 7,650) gives 16,650, still a breach. We must ask for all-units.
- **Executive and owner, the ramped minimum.** A ramp does not fix steady-state run cost. At 25% adoption the fee (8,775) is above the 6,000 minimum, so the minimum never binds. A ramp helps only below about 66,700 lookups a month. At soft launch (10% of traffic, about 9,750 lookups, fee about 880) the minimum binds and run cost is 9,000 plus 6,000 = 15,000. Soft launch passes only exactly at the limit.
- **Executive's 17% stress.** At 17% adoption, lookups are about 66,300 and the fee is 5,967 at 0.09. The minimum binds and run cost is 15,000 with no headroom. Above about 17% adoption the run cost breaches at 0.09 flat.
- **Data and Executive, the cache lever.** Both treat a VIN cache as the run-cost lever. The owner's answer for the first release says VINs are kept "only for the single lookup". A cache keyed on the full VIN keeps VINs after the lookup, so it conflicts with that answer. The cache can only be a launch lever if (a) it is keyed on something that is not the full VIN, for example the vehicle-variant part of the VIN where the decoder confirms it fixes the variant, which Legal must rule on, or (b) the owner changes the answer. Engineering recommends no cache at launch. Also, to clear the 6,000 minimum at 0.09 flat, paid lookups must drop from 97,500 to 66,667, a cut of about 32%. Data has not given a repeat-VIN share, so cache alone is unlikely to be enough.
- **Legal, stale cost points.** The 18-month lock-in and the 32% compounding are superseded. The reply gives 3 months' notice after month 12, and a 5% cap at 24 months. Applied to 0.09, year 3 is about 0.0992. Legal's 6-month pilot with ramp would forfeit the 24-month cap. Drop it in favour of the owner's answer: 24 months with a 12-month review.
- **Product, the MVP date.** Weeks 5 to 6 (around 1 February) assumes a 5-week layer. My point is 8 weeks. If build starts 5 December, 8 weeks lands about 30 January. If it starts 5 January, 8 weeks lands about 2 March and 10 weeks about 16 March, the first sales week. Product should plan on February with no slack.
- **Marketing, the buy-first fallback.** "Buy in 4 weeks" becomes 8 weeks once the layer is in. Without the layer, buy breaks no_strategic_blocker. Marketing's own risk list already says the "works for every seller" claim is off the table under buy.
- **Data, the schedule.** The holdout starts at soft launch, which sits on phase 1 (week 8 at point). The readout dates move only if soft launch moves. Data's design needs a user-level holdout flag, which I have put in phase 1.

## 3. Amendments to my position (with receipts)

1. **Hybrid effort: 14 point, range 12 to 18, confidence medium-low.** Was 12, range 10 to 16. Receipt: memory/shortcuts.yaml S-009 prices the layer at 8 weeks. My plan left 4 weeks (weeks 9 to 12) for the selector migration, "my garage", cache and fallback. The register does not say whether its 8 weeks include the selector migration. If they do, my phase 2 is about 4 weeks short. If they do not, phase 1 is short. Either way 12 is the optimistic end. At the top of the new range, hybrid uses 75% of the 24-week capacity.
2. **Phase split.** Phase 1 (thin layer, VIN entry behind a flag, holdout flag, logging): 8 weeks point, range 6 to 10, uses 33% of capacity. Phase 2 (selector and "my garage" migration, cache if cleared, fallback UX, dashboard): about 6 weeks point. Phase 2 carries S-009 and therefore the marketplace.
3. **Run cost, corrected.** At the reply's 0.09 and full ramp, hybrid is 17,775 a month, 2,775 over the guardrail, not 16,800. I previously said cache and negotiation close the gap. For launch, that no longer holds: cache is phase 2 and the tier is unconfirmed.
4. **Cache: withdrawn as a launch lever.** The reason is the owner's first-release answer on VIN storage (section 2). It stays as a phase 2 option, subject to Legal and a DPIA.
5. **Vendor reply.** Processor-only terms with 30-day retention remove the 24-month clause I cited against buy. The 0.09 price adds about 975 a month at base volume. Mapping at no cost removes the mapping fee but not the S-040 internal remap. The month-12 exit with 3 months' notice is acceptable to Engineering.
6. **Register.** No new shortcut is needed for the recommended path. If the owner cuts phase 2 for spring, I propose S-043 "selector and my-garage on supplier IDs until phase 2", blocking marketplace, with a fixed date. Engineering does not recommend that cut.

## 4. Shortcut register, engineering view

| ID | Option | Saves | Costs later | Blocks | Engineering position |
|---|---|---|---|---|---|
| S-040 | Buy as drafted | 8 weeks | 8 to 10 weeks remap; no price leverage | marketplace | Red line, reject |
| S-041 | Build | 10 weeks | 6 to 8 weeks per new country | eu-markets | Red line, reject |
| S-042 | Hybrid, phased | 16 weeks | Long-tail fees; renegotiation at volume | none | Acceptable |
| S-009 | Open today | 5 weeks (D-0018) | 8 weeks for the layer | marketplace | Fixed only in phase 2 |
| Thin buy | Phase 1 of hybrid | none new | none new | none new | Avoids S-040 only with the key rule and phase 2 |

## 5. Architecture, reversibility and run ownership

- **Stays reversible:** the vendor adapter, the decoder provider order (own first with vendor fallback, or the reverse), the per-country data source.
- **Becomes a dependency:** our vehicle_id schema (intentional), the vendor contract for 24 months (cap, and exit at 12 months with 3 months' notice), and vendor accuracy, which we accept only after our own measurement.
- **Run owner:** a named Engineering team before signature. Proposed SLOs: lookup p95 under 400 ms; layer availability 99.9%. The reply does not address the SLA. The vendor's 99.5% with a 10% credit cap stands unless negotiated, and the owner asked for 99.9%.
- **Fallback at no build cost:** the existing dropdown stays in phase 1. Product's condition is met without new work.

## 6. Run-cost route Engineering can support for launch

1. Ask the vendor for an all-units tier at 0.06 above 60,000 lookups. Not in the reply. Without it, the full ramp breaches.
2. Negotiate a minimum ramp for months 1 to 6 for soft-launch headroom.
3. Price cap: in the reply (5% at 24 months).
4. Phase 2: cache, only if Legal clears a key that is not the full VIN.
5. Fallback if neither tier nor cache lands before full ramp: cap effective VIN entry at about 17% adoption (about 66,700 lookups a month). That keeps run cost at or under 15,000 at 0.09 and is an honest traffic decision, not a breach.

Engineering would rather narrow the ramp than accept a recorded breach. The owner has already said a breach is not acceptable.

## 7. Stance on the round 1 options (not scoring)

- Buy as drafted: no. Red line on S-040.
- Buy with thin layer: accept only as phased hybrid, with phase 2 dated before the marketplace year-end date, the key rule enforced, and a named team.
- Hybrid, phased: accept on conditions: soft launch to 10% in March; full ramp gated on a tier or the traffic cap in section 6; phase 2 committed; signed DPA before any VIN leaves our systems.
- Build: out, unchanged.

Engineering's answer to the open question is ready: thin buy costs 8 weeks (6 to 10), avoids S-040 only under the key rule, and does not clear S-009 without phase 2.
