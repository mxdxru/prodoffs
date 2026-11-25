# Round 1, Product

**Challenge: hybrid as drafted.** At the reply's 0.09 fee, run cost is about 17,800 against the owner's hard 15,000 (our arithmetic: 97,500 x 0.09 + 9,000). Closing it needs a cut of about a third of paid lookups. Caching is not yet a lever: nobody has Data's repeat-VIN share, and the owner's first release keeps VINs for the single lookup only. Volume tiers are the only lever we can size (0.06 above 60,000 lookups gives about 14,850), and the reply is silent on them. Hybrid is not compliant until tiers are in writing.

**Weakest assumptions**
- Data: the +0.6 pt decision rule. A randomised holdout measures blended lift, about 0.25 pt at 25% entry (our arithmetic), so 0.6 pt can never pass. Set the bar near 0.15 pt on intent-to-treat.
- Engineering: phase 1 puts vendor results on our IDs while the S-009 dropdown still uses old IDs. Two ID schemes live in spring means "your vehicle" and the filters can disagree.
- Legal: the 18-month lock-in is stale. The reply gives month 12 plus 3 months' notice, and the 5% cap under 24 months replaces the 32% compounding figure.
- Engineering and Data: both place the layer in Catalog but disagree on who runs the adapter. The owner needs one named team before signature.

**Amendments, with receipts**
- My "MVP in 6 weeks" condition becomes 8 weeks, matching Engineering's phase 1. The owner's mid-March first sales week and 10% soft launch still leave about six weeks of slack.
- Garage storage leaves my first release (owner answer; DPIA later).
- Withdrawn: "payback month 9" was computed at 0.08 and must be rerun at 0.09.
- Executive's thin-layer buy is our phase 1 (6 to 8 weeks against 8). Only the S-009 migration moves to phase 2, so the separate option adds nothing.
- The reply does not address a post-termination licence to keep mapped results, breach notice, audit or liability cap. These gate go-live under Legal's checklist.

**Proposal.** Cache on the VIN model part (first 8 characters and model year), not the full VIN, so the first release stores no full customer VIN. Legal must confirm, and Data's 500-VIN test should measure hit rate against vendor output.

**Final stance:** Phased hybrid: soft launch in March, and no signature without volume tiers.
