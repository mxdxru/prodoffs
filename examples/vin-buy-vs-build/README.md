# Example: buy, build or hybrid for vehicle identification by VIN

A fictional online auto parts retailer lets customers pick their vehicle from make, model and engine. Many skip it or pick the wrong variant, so search shows parts that do not fit, conversion is low and a large share of returns are fitment returns. A VIN identifies the exact vehicle. The question: buy a vendor decoding API, build our own decoder, or run a hybrid with our own vehicle-ID layer and a vendor behind it?

## Files

| File | What it holds |
|---|---|
| `strategy.yaml` | Goals (revenue growth, workshop share), guardrails (one-off investment, monthly run cost, payback) and strategic bets (EU markets, marketplace, returns) |
| `candidates.yaml` | One candidate with three versions: buy, build, hybrid |
| `business_case.yaml` | Baseline funnel and cost model for each version |
| `prodoffs.yaml` | Negotiation rules: tolerance, concession decay, maximum rounds |
| `evidence/` | Vendor offer, vendor reply of 24 November, analytics snapshot |
| `memory/` | Open shortcut S-009, concession balances and past decisions D-0016 and D-0018 |
| `sample-session/` | One recorded round of the deliberation: task card, positions, assembly, debate, scores, option map and the business case as corrected in session |

## The question and the roles

Six roles take part: Executive, Product, Engineering, Marketing, Data, Legal. Each reads the same brief and the evidence, then prepares a position alone. The human answers the open questions in assembly. Then the roles debate, score the options against their own requirements, and the script counts the result.

## What the recorded run shows

1. **Preparation.** All six roles start from hybrid, but for different reasons. Executive makes it conditional on run cost. Legal makes it conditional on a processor-only contract.
2. **Assembly.** The owner answers, and the vendor reply arrives with a 0.09 fee, processor-only terms, a 5% cap for a 24-month term and an exit after month 12 with three months' notice. Volume tiers, a minimum-fee ramp and a 99.9% SLA are not in the reply.
3. **Debate.** The layer's run cost (9,000 a month) is an unsourced figure and it drives the buy-versus-hybrid gap. Engineering reports a thin owned layer on top of buy is hybrid phase 1 under another name. Data finds the holdout ends before returns mature, so the 5% control must run longer.
4. **Scoring.** No option passes every hard condition as the terms are written today. The draft hybrid breaks Legal's lawful-basis veto and Marketing's broken-promise red line. The hybrid on reply terms breaches the run-cost guardrail at 17,775 a month against 15,000. Buy breaks Engineering's and Data's red lines by blocking the marketplace bet.
5. **Outcome.** The script returns "no agreement" and the closest option, hybrid on reply terms. The decision is the owner's. The `sample-session` has no recorded decision: the owner answers are simulated and no approval is recorded.

## Run it

From the repository root:

```bash
python3 scripts/prodoffs.py case examples/vin-buy-vs-build --dry-run
python3 scripts/prodoffs.py brief examples/vin-buy-vs-build --session examples/vin-buy-vs-build/sample-session
```

To reset the memory after a demo run: `python3 scripts/prodoffs.py reset examples/vin-buy-vs-build --memory`.
