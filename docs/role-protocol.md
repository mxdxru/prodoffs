# Role protocol

Every Prodoffs role agent follows this protocol. The orchestrator (the `prodoffs-roadmap` skill) tells you the workspace path, the session folder and the phase.

## Phases and files

| Phase | You write | Rules |
|---|---|---|
| Sealed | `<session>/positions/<role>.yaml` | Do **not** read other roles' positions. Decide alone. |
| Cross-exam | `<session>/critiques/<role>.md` | First steelman the strongest rival position, then attack it. If all sealed positions chose the same option, red-team the consensus instead: steelman the best rejected alternative and attack the consensus at its weakest point. |
| Scoring | `<session>/scores/r<N>-<role>.yaml` | Score every option of round N against your mandate. |

### Position file

```yaml
role: cto
stance: "Own vehicle-ID layer, vendor behind it"    # max 8 words, shown on the board
proposal:                                           # one version per candidate id, or later
  vehicle-id: hybrid
business_case_view: "What you trust and what you doubt in business_case.md, in one or two lines"
alternatives:                                       # every version of the decision, from your mandate's point of view
  buy:    {pros: ["..."], cons: ["..."]}
  build:  {pros: ["..."], cons: ["..."]}
  hybrid: {pros: ["..."], cons: ["..."]}
risks: ["Concrete risks you see in other likely choices"]
ideas: ["Proposals that could make an option better for everyone"]
plan: ["3 to 5 steps for your preferred option, each with weeks"]
conditions: ["What would have to be true for you to accept another option"]
```

`business_case_view`, `alternatives`, `ideas`, `plan` and `conditions` are required in a single decision and optional in a roadmap session (use `alternatives` only for candidates you care about most). They feed the decision brief.

### Scores file

```yaml
opening: {arch_fit: 95, debt: 95, capacity: 85, reversibility: 90}   # your own proposal, per requirement, 0-100
options:
  H2:
    scores: {arch_fit: 78, debt: 80, capacity: 80, reversibility: 55}
    red_lines: [no_strategic_blocker]     # ids from your mandate that this option breaks, or []
    receipt: null                         # required from round 3 on, see below
    line: "Third concession in a row. No."
```

Requirement ids and red line ids must match your mandate file exactly.

### Facilitator files

| Phase | File | Content |
|---|---|---|
| Synthesis, converge | `options.yaml` | Options per round; a hybrid version may be added to `candidates.yaml` first |
| After acceptance | `dissent.yaml` | Strongest losing argument per dissenting role, with `revisit_if` |
| After acceptance | `plan.yaml` | `plan:` list of `{step, owner, weeks, done_when}` and `success_metrics:` list of `{metric, baseline, target, measured_by}` for the accepted option |

## Rules

1. **Independence first.** In the sealed phase you see only the workspace, never other positions.
2. **Receipts.** From the second scoring round on, if any of your scores for an option changes compared with a similar earlier option, `receipt` must name the new fact or argument that justifies the move. A change without a receipt is treated as conformity and reverted by the orchestrator.
3. **No arithmetic.** You give scores per requirement. Weighted totals, deviations, tolerances, capacity and strategy risk are computed by `scripts/prodoffs.py`.
4. **Red lines are binary.** Either an option breaks one or it does not. Do not use red lines as negotiating chips.
5. **Shortcuts are explicit.** If an option cuts a corner that `candidates.yaml` does not list, say so in your line and the orchestrator will add it.
