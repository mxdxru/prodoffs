---
name: prodoffs-decide
description: Run a Prodoffs session on a single trade-off, such as quick versus proper implementation of one feature, or build versus buy. Uses the workspace's strategy, mandates and memory, so the decision accounts for past concessions and open shortcuts. Use when the user brings one decision rather than a whole quarterly roadmap.
---

# Prodoffs single decision

Same machinery as `prodoffs-roadmap`, shorter: one question, its alternatives, one brief. Let `P="python3 scripts/prodoffs.py"`.

## 0. Frame the decision

1. Identify the workspace (an existing folder with `strategy.yaml`, `mandates/`, `memory/`). If none exists, run `prodoffs-setup` first.
2. Restate the decision in one line and list the alternatives (2 to 4). For each, get effort and whether it cuts a corner. Ask the user only for what is missing.
3. Run `$P session new <workspace>`. If the workspace's `candidates.yaml` already holds this decision as one candidate, use it; otherwise write `<session>/candidates.yaml`: **one candidate** whose versions are the alternatives, with `creates` and `fixes` like a normal candidate, and `capacity_team_weeks` set to the effort budget for this decision. The scripts use this file instead of the workspace's candidates for this session.

4. If the workspace has `business_case.yaml` with the same alternatives, run `$P case <workspace>`. Otherwise help the user fill one from `examples/vin-buy-vs-build/business_case.yaml`: the roles argue much better from numbers.

## 1. Sealed positions and reveal

1. `$P emit phase phase=sealed round=1`. Launch the role agents in parallel, one message, with the workspace, the session and "Phase: sealed, single decision". Each position picks one alternative.
2. `$P emit phase phase=reveal round=1` and one `say` per role with its stance.
3. Run cross-exam as in `prodoffs-roadmap`. If all roles picked the same alternative, do not skip it: unanimity is when the red-team rule matters most.

## 2. Options and scoring

1. `$P emit phase phase=synthesis round=1`. Write `<session>/options.yaml` with each alternative as an option for round 2. Launch `prodoffs-facilitator` only if a hybrid is plausible; it may add one hybrid version to `candidates.yaml` and one option.
2. `$P emit phase phase=scoring round=2`, role agents score, then `$P score <workspace> --round 2`.
3. Converge exactly as in `prodoffs-roadmap` (max rounds from `prodoffs.yaml`).

## 3. Close

1. Facilitator writes `dissent.yaml` and `plan.yaml`.
2. `$P brief <workspace>` and show it.
3. Only after the user's yes: `$P record <workspace>`. The decision then counts in concession balances and the shortcut register like any roadmap decision.
