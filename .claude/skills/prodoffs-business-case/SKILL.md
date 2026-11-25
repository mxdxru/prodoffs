---
name: prodoffs-business-case
description: Build or update the business case for a Prodoffs decision with the human: what the decision changes (conversion, completion, returns, cost), what each alternative costs, and how it compares with the strategy's goals and guardrails. Use before deliberation, or when the user wants the numbers behind a decision.
---

# Business case

Numbers come from the human's analytics and evidence; the calculation comes from `scripts/prodoffs.py case`. You never invent figures silently.

1. Start from `examples/vin-buy-vs-build/business_case.yaml` as the format: `baseline` (traffic, conversion, order value, margin, returns) and one entry per alternative under `alternatives` (one-off team-weeks, time to value, coverage, fees, run cost), with keys equal to the version ids in `candidates.yaml`.
2. Ask the user for the baseline from their own analytics. Where they have no number, propose an assumption, label it as an assumption in `notes`, and cite a public source if you used one.
3. Check `strategy.yaml` has `goals` (for example revenue growth with baseline and target) and `guardrails` (`max_one_off_investment`, `max_added_run_cost_monthly`, `max_payback_months`). If not, ask the owner for them: without them the roles cannot test options against the company's direction.
4. Run `python3 scripts/prodoffs.py case <workspace>` (with `--session` inside a session) and show the user the table, including the strategy section.
5. Point out which two or three assumptions carry the result, so the owner knows what to challenge.
