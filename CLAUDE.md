# CLAUDE.md

Claude Code loads this file in every session in this repository: when maintaining Prodoffs and when a user runs a Prodoffs session. README.md is for humans; keep it to the product description and how to run it. Technical detail lives here.

## What this repository is

A set of Claude Code subagents and skills where role agents (Executive, Product, Engineering, Marketing, Data, Legal, People) and a neutral facilitator negotiate cross-functional trade-offs, and the human decision owner decides, plus a Python script that does all the math and a static page that shows the negotiation live. State lives in plain YAML and JSONL files, never in Claude's memory.

## Layout

```
.claude/
  agents/            prodoffs-executive, -product, -engineering, -marketing, -data, -legal, -people, -facilitator
  skills/            setup, intake, add-role, kickoff, business-case, deliberate, record, shortcut, recall, radar, retro
  settings.json      hooks that feed the live board; autoMemoryEnabled: false
board/index.html     live board and replay page, no build step, no dependencies
docs/                role-protocol.md, demo video
scripts/prodoffs.py  validate, radar, case, score, brief, record, reset, status, session, emit, hook
scripts/video/       renders the demo video from a session's event log
templates/workspace/ blank workspace used by prodoffs-setup
examples/
  vin-buy-vs-build/        single decision with business_case.yaml; recorded session stopped at owner decision
workspaces/          user workspaces, git-ignored
```

A workspace contains `prodoffs.yaml`, `strategy.yaml` (goals, guardrails, bets), `candidates.yaml`, optional `business_case.yaml`, `mandates/*.yaml` (optional overrides; defaults live in the role files), `evidence/`, `memory/` (`shortcuts.yaml`, `concessions.yaml`, `decisions/`) and `sessions/`.

## Roles

Each role is one file in `.claude/agents/` with its default mandate: responsibility, interests, fears, playbook, red lines and weighted requirements. A workspace may override a mandate in `mandates/<role>.yaml`. Roles are advocates, not neutral advisors. Legal and People join only when the task needs them. Adding a role means adding one file (`prodoffs-add-role`).

| Role | Watches for |
|---|---|
| Executive | Business result, guardrails and goals; payback and run cost |
| Product | Customer outcome and the market window |
| Engineering | Capacity, reversibility, shortcuts that block bets |
| Marketing | Promises the product cannot keep; demand and story |
| Data | Reusable data, measurability, holdouts |
| Legal | Lawful basis (veto), contract exit, claims |
| People | Staffing and organisation (only when relevant) |
| Facilitator | Non-voting. Assembles options, runs narrowing, writes the outcome |

## Negotiation rules

Consensus, compromise (last round only) or owner decides; red lines with `veto: true` cannot be overridden. Tolerance and deviation are computed by `scripts/prodoffs.py`, never by an agent. See `docs/role-protocol.md`.
