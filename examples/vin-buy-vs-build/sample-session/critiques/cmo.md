# CMO critique: red-teaming the hybrid consensus

## Steelman: buy
From my mandate, buy is the best option we turned down. It is live in month 2, a month before hybrid, against competitors who already offer VIN search. At 4 team-weeks it leaves 20 for VIN landing pages, so it is the only option that funds `cac`. Its 0.985 precision backs "parts that fit" from day one.

## Attack: hybrid's year-2 savings are unfunded and break the promise
Hybrid's 580,744 relies on `vendor_share` dropping to 0.55 in year 2 and 0.35 in year 3. Own decoding drives that drop, and the 12 team-weeks don't pay for it. Every plan spends them on the schema, the S-009 migration, the vendor adapter and VIN entry. CTO and CEO make own decoding a separate go/no-go. So the case counts a saving nobody has costed. The CEO notes that year 3 still nets the same as year 2.

The worse problem is my red line. By year 2, "fit guaranteed" is public, and the build path starts own decoding at 0.95 precision. Move 45% of lookups onto it and we break `broken_promise` on home-market traffic. Don't move them and the savings never come.

## Proposal
Re-run hybrid with `vendor_share: [1.0, 1.0, 1.0]` as the committed number. Make own decoding its own candidate, gated on 30 days of shadow-decode at 0.985 precision or better (CDO's idea). Put 2 of the 12 spare team-weeks into VIN landing pages for launch.
