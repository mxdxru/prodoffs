# Assembly: VIN identification, buy, build or hybrid

Session 20261125-133804. Inputs: task.yaml, business_case.yaml, strategy.yaml, candidates.yaml, memory/shortcuts.yaml, evidence (vendor offer, vendor reply of 1 Dec, analytics snapshot), and six positions (executive, product, engineering, marketing, data, legal).

The script has not been run in this phase. Figures below are the roles' own numbers or simple arithmetic on business_case.yaml inputs, flagged where they are our arithmetic. `prodoffs.py case` must confirm them.

## 1. Headline

- All six opening positions name **hybrid**. Nobody backs build. Buy has two conditional supporters (executive, product) and one conditional, with a fallback twist (marketing).
- The unanimity is thin. Every role attaches a different condition to hybrid: run cost under 15,000 (executive, engineering), a processor-only vendor contract (legal, data), a named owning team (engineering, data), a spring-compatible first release (product, marketing), and a measurement design (data, product). Treat the unanimous opening as a claim to red-team in round 1, not as consensus.
- The vendor reply of 1 December arrived after most positions were written. Positions still say "reply outstanding". Several conditions are now partly met or changed (see section 3). Every role must re-check its position against the reply in round 1.

## 2. Option map

| Option | Status | Backed by (conditional) | Against | Notes |
|---|---|---|---|---|
| **Hybrid as drafted** (12 team-weeks, vendor 0.08 per lookup) | Main candidate | executive, product, engineering, marketing, data, legal | executive and engineering: run cost 16,800 vs 15,000 guardrail | Breaches the run-cost guardrail as drafted. At the reply's 0.09 price the gap widens (see 3.1). |
| **Hybrid, phased** (same candidate version, different schedule) | Schedule variant, not a new version | product, engineering, marketing | data (wants the full layer before measurement) | Phase 1 about 8 weeks (vendor behind our IDs, VIN field, dropdown fallback) for spring; phase 2 cache, fallback and S-009 migration. Engineering: 8 + 4 weeks. Product: MVP in weeks 5 to 6. |
| **Buy with thin own ID layer** (new variant, proposed by executive) | Open point, not yet a candidate | executive (conditional), product (as a fallback in its ideas), marketing (as a staged option) | engineering: its own acceptance of buy requires the full vendor-behind-own-layer design | Executive's effort is 6 to 8 weeks. Not in candidates.yaml. No effort or S-040 status from Engineering yet. Do not score until Engineering confirms. |
| **Buy as drafted** (vendor IDs as keys, 4 team-weeks) | Reference only | executive (only if marketplace slips), product (only if owner confirms remap is accepted), legal (only with a signed DPA that removes the veto) | engineering (red line no_strategic_blocker), data (own_core_data), legal as drafted (veto) | Cheapest and fastest on paper. Blocks marketplace via S-040 and deepens open S-009. |
| **Build** | Out for round 1 | none | executive, product (market_window), engineering (S-041 and capacity), marketing, data, legal (licensing) | 22 of 24 team-weeks, three guardrail breaches, blocks eu-markets. Engineering would accept only a vendor-backed fallback for new countries. |

## 3. Vendor reply: what changed

Reply of 1 December (evidence/vendor-reply.md), against the offer:

- Data: processor only; VINs kept at most 30 days for troubleshooting; no reuse for the vendor's own purposes; DPA and sub-processor list provided. Removes the 24-month retention and reuse clause that drove the Legal veto, and Data's and Marketing's privacy concern. Legal has not yet confirmed.
- Caching: we may cache decoded results for our own customers. This unlocks the cache lever that executive and engineering use to close the run-cost gap.
- Price: 0.09 per lookup with processor-only terms (was 0.08). Monthly minimum 6,000 unchanged.
- Price cap: increases capped at 5% a year, but only if we sign for 24 months. The offer allowed up to 15% a year over 36 months.
- Catalog mapping: included at no extra cost. Changes the mapping cost that executive, engineering and data flagged.
- Exit: termination for convenience after month 12 with 3 months' notice (offer: 6 months).

Not addressed by the reply: volume tiers, minimum-fee ramp, SLA (99.5%, credits capped at 10%), vendor precision on our catalog, term (24 or 36 months), post-termination licence to keep mapped results, liability cap, audit rights, breach notice.

### 3.1 Run cost arithmetic (our arithmetic, script to confirm)

- Lookups per month in the case: 97,500 (600,000 sessions times 65% without a vehicle times 25% entering a VIN).
- Fee at 0.08: 7,800 a month. Fee at 0.09: about 8,775 a month, about 975 more.
- Hybrid run cost (case: 9,000 own layer plus fees): about 16,800 at 0.08, about 17,800 at 0.09. The breach grows from about 1,800 to about 2,800 a month. Closing it needs about 16% off run cost, against about 11% at 0.08 (executive's figure).
- Buy run cost (case: 1,500 plus fees): about 9,300 at 0.08, about 10,300 at 0.09. Inside the guardrail either way.
- Levers that could close the gap are not yet quantified: cache (needs Data's repeat-VIN share, not yet available), volume tiers (executive cites 0.06 above 60,000 lookups, which the vendor reply does not offer), minimum-fee ramp.

### 3.2 Business case: what to correct

The baseline is correct for the offer that was sent. It now misstates buy and hybrid at the current vendor terms (fee 0.08 instead of 0.09; no cap unless a 24-month term). Recommended, not done in this phase:

1. Session copy of business_case.yaml with fee_per_lookup 0.09 for buy and hybrid, and a variant with a 5% cap for a 24-month term. Baseline unchanged. Every change listed in notes.
2. Stress runs requested by executive: adoption 17% (30% lower) and escalation 15% a year. Product and marketing ask for 15% adoption as a second stress.
3. Rerun `prodoffs.py case` after the session copies are written, before narrowing.

Do not add a buy-thin version to candidates.yaml until Engineering supplies effort and S-040 status.

## 4. Real conflicts between mandates

1. **Run cost guardrail versus hybrid as drafted.** strategy.yaml calls guardrails hard limits for any single decision. Executive treats 15,000 as a red line. Engineering, product, data and marketing treat the breach as fixable through cache, terms or tiers, and would accept a month-6 review. Only the owner can accept a breach. Engineering and product warn that a breach without a recorded plan is not acceptable.
2. **Speed versus marketplace.** Buy is the only option inside spring comfortably (4 weeks). Buy's S-040 blocks the marketplace bet and costs 8 to 10 weeks to remap later. Executive and product accept buy only if the marketplace slips or the remap is accepted. Marketing needs a spring story with a "works for every seller" claim that buy cannot make.
3. **Spring timing versus full layer.** Hybrid as one release lands around March (product's warning, engineering's 12 weeks from a 4 December decision). The spring date is not in the files. Phasing (section 2) is the common answer, but it is a scope change.
4. **Commitment length versus measurement.** Data wants a holdout readout before signing 36 months. Executive wants a stage gate (commit to 36 months only if adoption reaches 20% and precision 97% by month 6). Legal's pilot idea (6-month ramp) and the vendor's 24-month cap point the same way. The vendor offers a 36-month term with a 15% cap as drafted.
5. **Holdout size.** Data proposes a 10% holdout (no VIN entry) for 8 weeks. Product and marketing propose a 20% A/B test. Both need an owner decision because each costs short-term revenue.
6. **Vendor-ID lock-in versus speed of buy.** Engineering treats buy with vendor IDs as keys as a red line (no_strategic_blocker). Data treats it as breaking own_core_data. Legal treats it as a blocker for exit. Executive sees a thin ID layer as a possible way out (see section 2). This is the open point that decides between buy and hybrid, and it is not yet answerable from the files.
7. **Ownership of the layer.** Engineering and data make a named owning team a precondition for any option. Catalog has conceded on S-009 before (D-0018). No owner is named in the files.

## 5. Shared risks

| Risk | Roles | Status |
|---|---|---|
| VIN data clause (24-month retention and reuse) | all six | Largely addressed by the reply (30 days, processor only). Legal to confirm. |
| Price rise up to 15% a year, uncapped in the offer | executive, engineering, legal, marketing, data, product | Cap of 5% only with 24-month term. |
| 6,000 monthly minimum paid at low adoption | executive, product, marketing, legal, data | Unchanged in the reply. Ramp not yet negotiated. |
| Precision 98.5% is the vendor's own test set | data, product, marketing, legal, executive | Open. Measurement on 500 to 1,000 own VINs proposed. |
| Adoption 25% versus 41% stated intent | executive, product, marketing, data, engineering | Stress needed. Survey intent usually overstates behaviour. |
| Marketplace blocked | executive, product, data, marketing, engineering | S-009 is already open and blocks marketplace today (memory/shortcuts.yaml, D-0018). Buy deepens it; hybrid fixes it. This weakens the claim that buy keeps the marketplace path open. |
| Lock-in through vendor IDs (S-040) | executive, product, engineering, data, legal | Open until the thin-layer question is answered. |
| Unresolved VIN fallback (dead end) | product, engineering, marketing | Product: fallback in first release on any option. |
| Privacy and fit claims | legal, marketing, product, data | No fit guarantee or privacy copy until DPA and evidence file. |
| Strategic effects not priced (marketplace, EU markets, workshops) | executive, product, data, marketing | Roles argue them; not in the numbers. |
| Owner of the layer after launch | engineering, data | Open. Precondition. |

## 6. Stale positions to re-check in round 1

- Legal: veto status for buy and hybrid, and the open checklist items (section 3).
- Data: storage and reuse precondition (now partly met by caching for own customers; export on exit not addressed).
- Marketing: privacy wording (depends on the DPA).
- Engineering: cache lever (now allowed) and the buy-thin question.
- Executive: lever 1 (price cap) and lever 4 (mapping included) are partly in the reply; lever 2 (tiers) is not.

## 7. Proposed round 1 options (for narrowing, not yet written)

1. Hybrid as drafted, with the vendor reply terms and a recorded run-cost plan. Fails the run-cost guardrail unless levers land.
2. Hybrid phased (same version, phase plan for spring). Same guardrail issue.
3. Buy with thin own ID layer, only if Engineering supplies effort and S-040 status. Otherwise plain buy as reference.

Build is out. Plain buy is kept only to make the trade-off visible.
