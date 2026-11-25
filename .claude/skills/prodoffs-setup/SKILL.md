---
name: prodoffs-setup
description: Create a new Prodoffs workspace for the user's own product. Interviews the user for strategy, candidate initiatives, capacity, known shortcuts and role mandates, imports past decisions, and validates the result. Use when the user wants to start using Prodoffs on their own product or asks to set up a Prodoffs workspace.
---

# Prodoffs setup

Goal: a workspace folder that passes `python3 scripts/prodoffs.py validate <workspace>` and is ready for `prodoffs-roadmap` or `prodoffs-decide`.

## 1. Create the folder

Ask for a short workspace name (for example `acme-q2-roadmap`). Copy `templates/workspace/` to `workspaces/<name>/`. Never write into `examples/`.

## 2. Interview, one block at a time

Ask each block in one message and accept rough answers. If the user has documents (strategy deck, roadmap, tech-debt list, PRDs), ask them to paste or attach them and extract from those instead of asking.

1. **Company and strategy.** One line on the business. Then 2 to 5 strategic bets for the next 12 to 18 months. Push back on vague bets: "grow revenue" is not a bet, "launch in two new markets in H2" is. Write `strategy.yaml`; give each bet a short kebab-case id.
2. **Capacity and candidates.** Team capacity for the period in team-weeks. Then the candidate initiatives. For each one ask: is there a quick version and a full version, what does each cost, and does the quick version cut a corner? Write `candidates.yaml`. Every cut corner becomes a `creates` entry with `saved_now`, `cost_later` and `blocks` (bet ids).
3. **Known shortcuts.** Existing shortcuts and tech debt, ideally from engineering leads: what it is, area, what fixing it costs, which bets it blocks. Write `memory/shortcuts.yaml`. If a candidate version fixes one, add it to that version's `fixes`.
4. **Roles.** Which roles take part (CEO, CPO and CTO at minimum). For each, start from the template mandate and ask the user to adjust: owned metrics, red lines, and 3 to 4 weighted requirements specific to this company. Write `mandates/<role>.yaml`; delete templates for roles not used.
5. **History.** Past decisions the agents should know about: for each, what was decided, which role gave in and roughly how much (small, medium, large maps to 0.1, 0.2, 0.3), and any shortcut created. Write `memory/decisions/D-xxxx.md` and seed `memory/concessions.yaml` with balances. If there is no history, leave all balances at zero.

## 3. Validate

Run `python3 scripts/prodoffs.py validate workspaces/<name>`. Fix every error with the user. Then show a short summary: bets, candidates with versions, total effort of the full versions versus capacity, and which bets are already at risk from open shortcuts.

## 4. Hand over

Tell the user the workspace is ready and offer the next step: a full quarter with `prodoffs-roadmap`, or one trade-off with `prodoffs-decide`.
