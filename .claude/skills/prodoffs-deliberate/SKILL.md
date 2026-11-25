---
name: prodoffs-deliberate
description: Run a Prodoffs deliberation on a task card: briefing, independent preparation by each role, assembly, debate rounds, narrowing, decision and outcome. Works for a single trade-off and for a quarterly roadmap. Use after prodoffs-kickoff, when the user wants the roles to work through a decision.
---

# Deliberate

You orchestrate. Role agents argue, the facilitator assembles, `scripts/prodoffs.py` counts, and the human decides. Phases, files and rules are in `docs/role-protocol.md`; read it first. Let `P="python3 scripts/prodoffs.py"` and `W=<workspace>`. Roles are the ones in `<session>/task.yaml`; each role agent is `prodoffs-<role>`.

Keep the human in charge: at each phase boundary, tell them in one line what happened and what comes next, so they can redirect. Point them to the live board:
`python3 -m http.server 8000`, then `http://localhost:8000/board/?live=1&events=/<session path>/events.jsonl`.

## 2. Briefing

1. `$P emit phase phase=briefing round=0`
2. If the workspace has `business_case.yaml`: `$P case $W`.

## 3. Preparation

1. `$P emit phase phase=preparation round=0`
2. Launch **all role agents in parallel, in one message**, each with the workspace, the session and "Phase: preparation". Hooks show them thinking on the board.
3. For each role: `$P emit say role=<role> text="<stance>"`.

## 4. Assembly

1. `$P emit phase phase=assembly round=0`, launch `prodoffs-facilitator` with "Phase: assembly".
2. Show the user the questions marked `to: owner` from `questions.yaml` and ask them to answer. Write the answers to `<session>/answers.yaml`. Unanswered questions become stated assumptions.

## 5. Debate (round N, starting at 1)

1. `$P emit phase phase=debate round=N`. If all positions proposed the same option, also `$P emit note text="Unanimous positions: the debate red-teams the consensus"` and tell the agents.
2. Launch the role agents in parallel with "Phase: debate, round N". Emit one `say` per role with its final line.

## 6. Narrowing (round N)

1. `$P emit phase phase=narrowing round=N`, launch `prodoffs-facilitator` with "Phase: narrowing, round N". If it corrected the business case, rerun `$P case $W --session <session>`.
2. Launch the role agents in parallel with "Phase: scoring, round N". Check every changed score has a receipt; ask once to justify or revert.
3. `$P score $W --round N` (add `--final` on the last allowed round). Show the user the result.

## 7. Decision

- **Consensus or compromise:** go to 8.
- **Open:** if any score changed this round and N < `max_rounds`, go back to 5 with N+1. If nothing changed for two rounds, rerun the score with `--final`.
- **Owner decides:** present the option map and the closest option, and ask the owner to choose.

## 8. Outcome

1. `$P emit phase phase=outcome round=N`, launch `prodoffs-facilitator` with "Phase: outcome". It writes `plan.yaml`, `risks.yaml`, `dissent.yaml`.
2. `$P brief $W` and show the brief.
3. Ask the decision owner to approve, choose another option, or stop. Then run `prodoffs-record`. Never record without their explicit answer.

## Rules

- Never write scores, deviations, business case numbers or acceptance yourself. If a script fails, fix the input files.
- A roadmap is the same flow with several candidates in `candidates.yaml`; options pick one version per candidate.
- The human can stop, add evidence, change the alternatives or overrule at any point; restart from the phase their change affects.
