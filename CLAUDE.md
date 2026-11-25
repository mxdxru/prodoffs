# CLAUDE.md

Claude Code loads this file in every session in this repository: when maintaining Prodoffs and when a user runs a Prodoffs session. README.md is for humans; keep it to the product description and how to run it. Technical detail lives here.

## What this repository is

A set of Claude Code subagents and skills where executive roles (CEO, CPO, CTO, CMO, CDO) and a neutral facilitator negotiate product trade-offs, plus a Python script that does all the math and a static page that shows the negotiation live. State lives in plain YAML and JSONL files, never in Claude's memory.

## Layout

```
.claude/
  agents/            prodoffs-ceo, -cpo, -cto, -cmo, -cdo, -facilitator
  skills/            setup, radar, roadmap, decide, shortcut, recall, retro
  settings.json      hooks that feed the live board; autoMemoryEnabled: false
board/index.html     live board and replay page, no build step, no dependencies
docs/                role-protocol.md, screenshots, demo video
scripts/prodoffs.py  validate, radar, case, score, brief, record, reset, status, session, emit, hook
scripts/video/       renders the demo video from a session's event log
templates/workspace/ blank workspace used by prodoffs-setup
examples/
  vin-buy-vs-build/        single decision with business_case.yaml; real agent run
  auto-parts-q1-roadmap/   quarterly roadmap; hand-written sample session
workspaces/          user workspaces, git-ignored
```

A workspace contains `prodoffs.yaml`, `strategy.yaml`, `candidates.yaml`, optional `business_case.yaml`, `mandates/*.yaml`, `memory/` (`shortcuts.yaml`, `concessions.yaml`, `decisions/`) and session folders.

## Roles

Each role is a subagent in `.claude/agents/` plus a mandate file in the workspace. A mandate is a contract: owned metrics, red lines, weighted requirements. Roles are advocates, not neutral advisors. What each role watches for:

| Role | Watches for |
|---|---|
| CEO | Q1 wins that endanger the year's bets; margin leaks |
| CPO | Seasonal windows; top reasons customers do not adopt |
| CTO | New and open shortcuts; own concession balance; capacity realism |
| CMO | Competitor moves; launch stories |
| CDO | Quick versions that create manual data work |
| Facilitator | Non-voting. Builds hybrid options, proposes who concedes, records dissent |

`docs/role-protocol.md` is the source of truth for which phase writes which file and in which format.

## Session phases

| Phase | What happens |
|---|---|
| Intake | Load strategy, candidates, open shortcuts, past decisions, concession balances |
| Sealed | Each role writes its position alone. Run role agents in parallel; no role sees another's position before Reveal |
| Reveal | All positions shown at once |
| Cross-exam | Each role steelmans the strongest rival position, then attacks it |
| Synthesis | Facilitator builds 2-3 hybrid options |
| Scoring | Each role scores every option per requirement; `prodoffs.py score` does the math |
| Converge | If nothing passes, facilitator proposes the smallest concession; rescore. Max rounds from `prodoffs.yaml` (default 3) |
| Record | Decision brief. Update the ledger only after an explicit yes from the user |

## Hard rules

- **Unanimity triggers red-teaming.** If all sealed positions agree, cross-examination becomes: each role defends the best rejected option and attacks the agreed one.
- **Receipts.** A role may change a score only by citing a new fact or argument. Reject score changes without one.
- **Agents never compute.** Deviations, tolerances, capacity, the future-proof check, business-case net and payback, and moods all come from `scripts/prodoffs.py`. Agents argue and score only. Never put a number in a brief that the script did not produce.
- **Agreement rule.** An option is accepted when it fits capacity, breaks no red line, creates no new risk for a strategic bet, and no role deviates more than its tolerance (default 20%). Risk from shortcuts already carried is shown, not blocking.
- **Fairness.** A role that conceded in recent decisions gets a tighter tolerance; strength is set in `prodoffs.yaml`.
- **The human chairs.** Never write to `memory/` without the user's explicit yes in this session.

## scripts/prodoffs.py

Run with `python3`; requires `pyyaml`. Subcommands: `session`, `emit`, `score`, `brief`, `record`, `validate`, `radar`, `status`, `reset`, `case`, `hook`.

- `validate <workspace>`: run after any change to workspace files or file formats.
- `case <workspace>`: business case, yearly net and payback.
- `score <workspace> --round N --session <dir>`: deviations, tolerances, pass/fail per option.
- `reset <workspace>`: removes sessions. `--memory` also restores `memory/` from `memory/.baseline/`, which the first `record` snapshots.
- `--dry-run` prints without writing. Use it on examples.

## Live board

Claude Code hooks (`SubagentStart`, `SubagentStop` in `.claude/settings.json`) and the script append events to `events.jsonl` in the session folder. `board/index.html` polls that file and redraws. Query params: `events=<path>`, `layout=wide` (16:9), `live=1` (follow a running session). It must be served over HTTP (`python3 -m http.server`); `file://` blocks the fetch. Hooks run only in a trusted folder and need `python3` on PATH.

Mood is computed by the script, not generated:

| Mood | Rule |
|---|---|
| Thinking | Writing its sealed position |
| Pleased | Deviation under 50% of tolerance |
| Neutral | 50 to 80% |
| Concerned | 80 to 100% |
| Angry | Over tolerance, or a red line is broken |

## Examples

- `vin-buy-vs-build/sample-session` is a real agent run and feeds the demo video. Do not hand-edit it.
- `auto-parts-q1-roadmap/sample-session` is hand-written. Regenerate events and brief with `sample-session/rebuild.sh` after editing it.
- After any demo run on an example, run `reset --memory` before committing so the examples stay at baseline.

## Maintaining the project

- Changing a file format means updating together: `docs/role-protocol.md`, `templates/workspace/`, `prodoffs.py validate`, both examples, and the relevant skills.
- Keep `workspaces/` and any real company data out of commits. The repository is public.
- Docs style: plain English, short sentences, no em dashes.
