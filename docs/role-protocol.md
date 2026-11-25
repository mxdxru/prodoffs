# Prodoffs protocol

How a Prodoffs session runs: who does what in each phase, and which files they write. The human sets the task, answers questions, steers and makes the final decision. Agents prepare, argue and recommend. `scripts/prodoffs.py` does every calculation.

## Who is who

| Who | Role in the session (DACI) |
|---|---|
| The human decision owner | **Approver.** Writes the task, answers questions, can stop or redirect at any point, approves or overrides the outcome. Only `prodoffs.py record --by <name>` turns a recommendation into a decision. |
| Facilitator agent | **Driver.** Neutral, non-voting. Assembles options, runs the debate, narrows, writes the outcome. |
| Role agents | **Contributors.** Advocate for their mandate. Only roles listed in the task take part. |
| Everyone else | **Informed.** Read the decision brief. |

## Phases

| # | Phase | Who | Writes | What happens |
|---|---|---|---|---|
| 1 | Kickoff | Human, with `prodoffs-kickoff` | `task.yaml` | The question, alternatives, decision owner, deadline, constraints, roles and evidence |
| 2 | Briefing | Orchestrator | `business_case.md` | Everyone gets the same context: task, strategy (goals, guardrails, bets), business case, memory, evidence |
| 3 | Preparation | Each role alone, in parallel | `positions/<role>.yaml` | Position, questions, risks and the artifacts of the role's playbook. Nobody sees the others |
| 4 | Assembly | Facilitator, then human | `assembly.md`, `questions.yaml`, `answers.yaml` | Option map, conflicts, shared risks; open questions go to the human, whose answers become input |
| 5 | Debate | Roles, in rounds | `debate/r<N>-<role>.md` | Challenges, amendments, concessions with receipts. Unanimous positions are red-teamed |
| 6 | Narrowing | Facilitator, roles, script | `options.yaml`, `scores/r<N>-<role>.yaml`, `result-r<N>.json` | 2 to 3 options; roles score; the script removes options that break red lines, guardrails, capacity or create a new strategic risk |
| 7 | Decision | Script, then human | `result-r<N>.json` | Consensus, compromise, or the owner decides. If the debate is still open, go back to 5 |
| 8 | Outcome | Facilitator, then human | `plan.yaml`, `risks.yaml`, `dissent.yaml`, `brief.md`, `approval.yaml` | Plan, risk register, trade-offs, recorded disagreements; the owner approves or overrides |

### Stopping the debate

Rounds continue until one of these happens: consensus is reached; two rounds in a row change no score (stalemate); `max_rounds` from `prodoffs.yaml` is reached. The human can stop the debate at any time.

## Decision rules

- **Consensus.** The option fits capacity, breaks no red line, breaks no strategic guardrail, creates no new risk for a strategic bet, and every role is within its tolerance (default 20%, tighter for roles that conceded recently).
- **Compromise.** Only in the last round, if there is no consensus: among options that meet every hard condition, the one where the most unhappy role is least unhappy, as long as nobody is beyond twice their tolerance. Concessions beyond tolerance are recorded and tighten those roles' future tolerance.
- **Owner decides.** If neither exists, the decision owner chooses from the option map. The choice is recorded as an override, with the dissent.
- **Veto.** A red line marked `veto: true` (by default Legal's lawful-basis rule) cannot be lifted by an override. It has to be resolved, for example with a legal opinion, and the option rescored.

Deviation is `1 - score(option) / score(own opening position)`, from the weighted requirements in the role's mandate.

## Files

### Task card (`task.yaml`, written at kickoff)

```yaml
question: "Vehicle identification by VIN: buy, build or hybrid?"
decision_owner: "Head of Product"          # a person, not an agent
deadline: "Decision by 2026-12-04"
alternatives: [buy, build, hybrid]         # versions of the candidate in candidates.yaml
roles: [executive, product, engineering, marketing, data, legal]
constraints: ["VIN entry live before the spring season"]
evidence: [evidence/vendor-offer.md]
notes: "Anything the owner wants the roles to know"
```

### Position (`positions/<role>.yaml`, preparation)

```yaml
role: engineering
stance: "Own vehicle-ID layer, vendor behind it"   # max 8 words, shown on the board
proposal: {vehicle-id: hybrid}                     # one version per candidate, or later
business_case_view: "What you trust and doubt in business_case.md"
alternatives:
  buy:    {pros: ["..."], cons: ["..."]}
  build:  {pros: ["..."], cons: ["..."]}
  hybrid: {pros: ["..."], cons: ["..."]}
artifacts:                                         # the playbook outputs of your role
  - {title: "Effort estimate", content: "..."}
risks: ["..."]
questions: ["Questions for the decision owner or another role"]
ideas: ["..."]
plan: ["3 to 5 steps with weeks"]
conditions: ["What would make you accept another option"]
```

### Debate (`debate/r<N>-<role>.md`)

Under 250 words: which positions you challenge and why, which amendments you propose, what you concede and the receipt (the fact or argument that moved you). In a round after unanimous positions, steelman the best rejected alternative and attack the consensus at its weakest point.

### Scores (`scores/r<N>-<role>.yaml`, narrowing)

```yaml
opening: {arch_fit: 90, debt: 88, capacity: 85, reversibility: 88}   # your opening position, 0-100
options:
  H2:
    scores: {arch_fit: 90, debt: 88, capacity: 85, reversibility: 90}
    red_lines: []                 # ids from your mandate this option breaks
    receipt: "Why your view moved since your position, or null"
    line: "Max 12 words in your voice"
```

Requirement and red line ids must match your mandate exactly.

### Facilitator files

| File | Content |
|---|---|
| `assembly.md` | Option map: alternatives, which roles back which, conflicts, shared risks |
| `questions.yaml` | `questions:` list of `{from, to, question}`; `to: owner` goes to the human |
| `options.yaml` | `options:` `{<id>: {round, summary, items: {<candidate>: <version>}}}` |
| `plan.yaml` | `plan:` list of `{step, owner, weeks, done_when}`; `success_metrics:` list of `{metric, baseline, target, measured_by}` |
| `risks.yaml` | `risks:` list of `{risk, owner, likelihood, impact, mitigation}` |
| `dissent.yaml` | `dissent:` list of `{role, argument, revisit_if}` |

If the debate shows the business case misstates an option, the facilitator copies `business_case.yaml` and `candidates.yaml` into the session and adds a corrected alternative there, never changing `baseline`, with every change listed in `notes`.

### Human files

| File | Written by | Content |
|---|---|---|
| `task.yaml` | Owner at kickoff | The brief |
| `answers.yaml` | Owner at assembly | `answers:` list of `{question, answer}`; unanswered questions become stated assumptions |
| `approval.yaml` | `prodoffs.py record --by` | Which option, consensus, compromise or override, who approved, when, why |

## Rules for roles

1. **Independence first.** In preparation you see only the task, the workspace and the evidence, never other positions.
2. **Receipts.** Any change of view must name the fact or argument behind it.
3. **No arithmetic.** You score per requirement; the script computes everything else.
4. **Red lines are binary**, not bargaining chips.
5. **Shortcuts are explicit.** If an option cuts a corner, say what it saves, costs later and blocks.
6. **You advise; the human decides.** Write so the decision owner can follow your reasoning and disagree with it.
