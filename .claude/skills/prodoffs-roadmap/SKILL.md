---
name: prodoffs-roadmap
description: Run a Prodoffs quarterly roadmap session. Role agents (CEO, CPO, CTO, CMO, CDO) negotiate which initiatives go into the quarter and in which version, with past trade-offs and the future price of shortcuts taken into account. Use when the user asks to build, stress-test or negotiate a quarterly roadmap with Prodoffs, or names a Prodoffs workspace.
---

# Prodoffs roadmap session

You are the orchestrator. Role agents argue; `scripts/prodoffs.py` counts. You never compute deviations or decide acceptance yourself.

Input: a workspace folder (for example `examples/auto-parts-q1-roadmap`) with `prodoffs.yaml`, `strategy.yaml`, `candidates.yaml`, `mandates/` and `memory/`. Let `P="python3 scripts/prodoffs.py"`.

## 0. Intake

1. Check the workspace has all files above. If something is missing, tell the user what and stop.
2. Run `$P session new <workspace>`. It prints the session folder; use it below as `<session>`.
3. If the workspace has `business_case.yaml`, run `$P case <workspace>`; it writes `<session>/business_case.md` for the agents and puts the numbers on the board.
4. Tell the user the board can be watched live:
   `python3 -m http.server 8000` from the repository root, then open
   `http://localhost:8000/board/?live=1&events=/<session path relative to repo root>/events.jsonl`.

## 1. Sealed positions

1. `$P emit phase phase=sealed round=1`
2. Launch **all five role agents in parallel, in one message**: `prodoffs-ceo`, `prodoffs-cpo`, `prodoffs-cto`, `prodoffs-cmo`, `prodoffs-cdo`. Prompt each with the workspace path, the session path and "Phase: sealed". Hooks put their start and finish on the board.

## 2. Reveal and cross-exam

1. `$P emit phase phase=reveal round=1`. For each role, read its position and run `$P emit say role=<role> text="<stance>"`.
2. `$P emit phase phase=cross_exam round=1`. If all sealed proposals are identical, emit `$P emit note text="Unanimous sealed positions: cross-exam red-teams the consensus"` and tell the agents so. Launch all five agents again in parallel with "Phase: cross-exam". After they finish, emit one `say` per role with their final line.

## 3. Synthesis

1. `$P emit phase phase=synthesis round=1`
2. Launch `prodoffs-facilitator` with "Phase: synthesis, round 2". It writes `<session>/options.yaml`.
3. `$P emit say role=facilitator text="<its final line>"`

## 4. Scoring

1. `$P emit phase phase=scoring round=2`
2. Launch the five role agents in parallel with "Phase: scoring, round 2".
3. Run `$P score <workspace> --round 2`. Show the user the printed table.

## 5. Converge

If no option is accepted and the round is below `max_rounds` from `prodoffs.yaml`:

1. `$P emit phase phase=converge round=<N+1>`
2. Launch `prodoffs-facilitator` with "Phase: converge, round <N+1>". It adds one option.
3. `$P emit say role=facilitator text="<its line>"`
4. Launch the role agents with "Phase: scoring, round <N+1>". Check every score file for `receipt` where scores moved; if one is missing, ask that agent once to justify or revert.
5. Run `$P score <workspace> --round <N+1>`.

If `max_rounds` is reached without acceptance, stop and present the best options to the user as an escalation. The user decides.

## 6. Record

1. Launch `prodoffs-facilitator` with "Phase: dissent and plan". It writes `<session>/dissent.yaml` and `<session>/plan.yaml`.
2. Run `$P brief <workspace>` and show the brief to the user.
3. Ask the user whether to record the decision. Only after a yes, run `$P record <workspace>`: it updates concession balances and the shortcut register in `memory/` and saves the brief as the next `D-xxxx`.

## Rules

- Never write scores, deviations or acceptance yourself. If the script fails, fix the input files, not the numbers.
- Keep the user informed at phase boundaries in one line each; the board shows the rest.
- The human is the chair. Recording a decision, overriding a red line or changing a mandate needs the user's explicit yes.
