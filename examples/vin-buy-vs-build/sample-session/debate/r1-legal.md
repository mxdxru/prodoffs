# Legal, round 1: 1 December reply, challenges and open contract items

Not legal advice. Items marked [lawyer] need a qualified lawyer before signature or any public claim.

## 1. Does the 1 December reply remove the veto for buy and hybrid?

It removes the reason the veto was triggered. It does not yet lift the go-live gate.

- Veto on the decision: lifted for buy and hybrid. A processor-only offer exists, so either can be chosen on data grounds.
- Go-live gate: still closed. The reply is a letter, not a contract. The attached standard DPA is not yet reviewed. No live VIN lookup, including a soft launch or the phase 1 MVP, before a signed DPA.
- Buy has a second gate: without a licence to keep mapped results after termination, exit is blocked (S-040).
- Build: unchanged, out, because of per-country data licensing [lawyer].

## 2. Challenges to the strongest option (hybrid)

a) The cache is the run-cost lever and a personal-data store. A VIN linked to an account is personal data (CJEU C-319/22, judgment of 9 November 2023). Test a cache keyed on vehicle-level results, with the full VIN kept only on the account under our retention rule [lawyer].

b) Phase 1 cannot ship before signature. A session-only VIN sent to the vendor is still personal data passed to a processor, so an Art 28 DPA must be signed before the first live lookup.

c) The layer adds stores (vendor_ref mapping, per-lookup log, "my garage" VIN). Each needs a purpose, a retention period, an Art 30 record entry and a privacy notice update (Art 13). None is a dated item in the plan yet.

## 3. Challenges to other roles' weakest assumptions

- Executive: the 12-month review and month-6 gate only work with a month-12 exit. The reply's exit is month 12 plus 3 months' notice, so the earliest exit is month 15.
- Executive, Engineering, Data: run-cost arithmetic uses the 0.08 fee. Any contract would be at 0.09. The business case needs that correction.
- Marketing: "Save your vehicle in My garage" is out of first-release scope. "See parts for your exact vehicle" overclaims against 98.5% precision on the vendor's own test set. Use "parts matched to your vehicle".
- Data: tagging returns per VIN makes returns personal data. Needs pseudonymisation in analytics, a retention limit and a balancing test for the holdout [lawyer].
- Product: the garage opt-in needs DPIA screening before any garage feature.
- Engineering: a thin layer does not remove contract needs. Mapping and export rights after termination are required for any option keyed to vendor IDs.

## 4. Open contract items

- Liability: SLA credits capped at 10% of the monthly fee; reply silent on data. Ask for a separate, higher cap for data protection breaches [lawyer].
- Audit rights: silent. Ask for an audit right or a current ISO 27001 report, flowing down to sub-processors (Art 28(3)(h), 28(4)).
- Breach notice: silent. Ask for notice within 24 to 48 hours (Art 33(2)) [lawyer].
- Post-termination licence: silent. Ask for the right to keep the VIN-to-vehicle mapping and results received, plus bulk export on exit. Without it, exit is blocked.
- Sub-processors: list provided. Ask for 30 days' notice of changes and a right to object (Art 28(2)).
- Deletion: 30 days maximum for troubleshooting. Ask for deletion or return on instruction and on termination (Art 28(3)(g)).
- Price cap: 5%, only on a 24-month signature. Ask for the lower of 5% or the inflation index on every review, with 90 days' notice.
- Exit: month 12 plus 3 months' notice. Ask for free termination on SLA failure, price rise above cap or data breach, and six months of exit help.
- Location: EU hosting in offer. Ask for a written commitment and a check of sub-processor locations for transfers (Art 44 to 46).
- Warranty and indemnity: silent. Ask for a warranty on rights in underlying data and indemnity for third-party claims [lawyer].
- Signature: letter, not contract. Ask for a signed DPA and order form before any live lookup.

Term: 24 months with the month-12 exit is acceptable. 36 months is not.

## 5. Amendments to round 0

- Stance unchanged: hybrid, on a processor-only contract. The buy condition now needs a signed DPA plus the mapping licence.
- Correction: the C-319/22 judgment date is 9 November 2023.
- Correction: lock-in is 15 months (month 12 plus 3 months' notice), not 18. With a 5% cap on two reviews, the maximum price rise is about 10%, not 32%.

## 6. Claims

- Safe: "Enter your VIN to find parts matched to your vehicle. Always check the part number against your vehicle documents."
- Not safe: "exact vehicle", "guaranteed fit", "save to My garage" in first release, "your data is never shared".
- Any precision or returns percentage: only after our own measurement.

## 7. Requests for round 2

- Engineering and Data: a cache design that does not store the full VIN, with a retention period.
- Product: first live date set after DPA signature, not after MVP build.
- Executive: business case at 0.09, and a month-12 exit in the contract.

Final stance: Buy and hybrid stay open; no go-live before a signed DPA and mapping licence.
