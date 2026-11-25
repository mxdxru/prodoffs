# CTO critique: red-teaming the hybrid consensus

## Steelman: build
From my mandate, build is the only option where the decoder is real: fixes S-009, no per-lookup fees, and its 22 weeks and 21,000 a month (about 1.5 FTE) are honestly priced. It breaks no_strategic_blocker through S-041, but it at least pays for what it promises.

## Attack: hybrid's year-2 savings are unfunded
- The 12 team-weeks pay for the layer, the vendor adapter and the S-009 migration. Not one week of own decoding. Yet `vendor_share` drops to 0.55 in year 2 and 0.35 in year 3, which assumes a home-market decoder exists.
- Every plan defers that decoder: mine to month 9, CEO to a week-26 go/no-go, CDO to "year 2 shadow-decode", CPO to "after the season". Nobody costs it or names its owner (no_orphan_service).
- Hybrid run cost of 9,000 a month supposedly covers layer upkeep plus decoder licences, while build needs 21,000 for the same decoder. One of those numbers is wrong.
- The 6,000 monthly minimum puts a floor under fees, so a lower vendor share saves less than the curve implies.
- CPO's sequencing moves returns and S-009 consumers to weeks 11-12 "after the season". That is where layers get cut thin, and S-009 stays open.

## Proposal
Split the decision. Candidate A: hybrid-layer, 12 weeks, `vendor_share` flat at 1.0 in the case, with search, cart and returns on own IDs before launch. Candidate B: own home-market decoding, its own effort estimate, run cost and owning team, decided in month 9 on real lookup data. Rerun the case on A alone.
