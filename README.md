# Prodoffs

> Build a roadmap that wins this quarter without losing the next year.

Prodoffs is an open framework of Claude Code agents for product leaders. It remembers every trade-off the team has made, shows the future price of cutting corners, and helps assemble a quarterly roadmap that balances speed now against the ability to scale and change the product later.

![Prodoffs demo: five AI executives negotiate buy versus build for VIN identification](docs/prodoffs-demo.gif)

*A real agent run on a buy-versus-build decision, replayed from its event log. Full video: [docs/prodoffs-demo.mp4](docs/prodoffs-demo.mp4). Walkthrough: [examples/vin-buy-vs-build](examples/vin-buy-vs-build).*

## The problem

A Head of Product or Product Director lives with three problems that never go away:

1. **Too many past trade-offs to keep in your head.** Over a year the team makes dozens of "let's do it the quick way" decisions. Six months later nobody remembers which ones, where, and why.
2. **Shortcuts look free when you take them.** Cutting a corner saves two weeks now. The bill arrives later: a feature that should take a month takes three, a market launch is blocked, a pricing change needs a rewrite.
3. **The quarterly roadmap is optimized for this quarter.** Every quarter the pressure for time-to-market wins. Each decision looks reasonable alone. Together they slowly remove the ability to scale or pivot.

Engineering usually sees it coming and says so. But "this will hurt us later" sounds vague next to "this brings revenue in Q1", so it loses.

## What Prodoffs does

**1. Remembers trade-offs for you.** Every decision records what was chosen, what was rejected, what corner was cut, and who disagreed. Before the next decision in the same area, that history is on the table.

**2. Shows the future price of every shortcut.** Each cut corner is a shortcut with three fields: what it saves now, what it costs later, and **which future plans it blocks**. The last field turns opportunity cost into something visible: not "this is tech debt" but "this blocks the H2 market launch".

```yaml
- id: S-014
  area: pricing
  shortcut: "Prices and VAT rules hardcoded per country, no pricing engine"
  saved_now: "3 weeks"
  cost_later: "6 weeks to fix, +1 week for every new country or customer tier added before that"
  blocks: [eu-markets, b2b-growth]
  status: open
```

**3. Puts numbers under the argument.** An optional business case models what the decision changes (for example conversion, checkout completion and returns) against what each alternative costs. The script computes yearly net and payback, and the agents argue with those numbers instead of inventing their own.

**4. Helps assemble the quarterly roadmap or settle a single trade-off.** You provide the strategy for the next 12 to 18 months, candidate initiatives with rough estimates, team capacity and known shortcuts. Five role agents negotiate. You get:

- the roadmap: each initiative in, quick, full, or moved;
- a future-proof check: which strategic bets the plan puts at risk, and why;
- the shortcuts this plan creates, with their future price;
- which old shortcuts to pay down now because a strategic bet depends on them;
- recorded disagreements, each with a condition for revisiting.

## The agents

Each role is an advocate with its own mandate: what it owns, its red lines, and its weighted requirements.

| Agent | Argues for | Typical red line |
|---|---|---|
| CEO | EBITDA, ARR, strategic fit | Negative 12-month contribution with no strategic rationale |
| CPO | Time-to-market, adoption, experience | Core features miss the market window |
| CTO | Scalability, reliability, tech debt, capacity | No new shortcut that blocks a strategic bet |
| CMO | Positioning, acquisition cost, competitive response | Nothing that breaks a public promise |
| CDO | Reusable data models, measurability | Data models tied to one catalog or market; launches without metrics |
| Facilitator | Nobody: neutral, non-voting | Builds hybrid options, proposes who concedes, records dissent |

Seven skills cover the whole cycle:

| Skill | When | What it does |
|---|---|---|
| `prodoffs-setup` | Once, at the start | Interviews you and creates a workspace for your product |
| `prodoffs-radar` | Before planning, or on a schedule | Which strategic bets are at risk from shortcuts you already carry, who has been conceding |
| `prodoffs-roadmap` | Quarterly planning | Full negotiation of the quarter with all agents and the live board |
| `prodoffs-decide` | Any single trade-off | Same negotiation for one decision: quick versus proper, build versus buy |
| `prodoffs-shortcut` | Whenever a team cuts a corner | Records the shortcut with its future price, in under a minute |
| `prodoffs-recall` | Any time | Answers "why did we choose X?", "what blocks Y?", "who has been giving in?" |
| `prodoffs-retro` | End of quarter | Plan versus reality; flags disagreements that turned out right |

## How a session runs

```
Intake      load strategy, candidates, open shortcuts, past decisions
Sealed      each role writes its position alone, in parallel
Reveal      positions shown at once
Cross-exam  each role steelmans the strongest rival position, then attacks it
Synthesis   facilitator builds 2-3 hybrid options
Scoring     each role scores every option; the script does the math
Converge    if nothing passes, the smallest concession is proposed (max 3 rounds)
Record      decision brief; with your yes, the ledger is updated
```

What makes it more than role-play:

- **Unanimity is suspicious.** If all roles agree, they switch to red-teaming the consensus. In the VIN run this is what exposed a flaw in the business case.
- **Independent first.** Sealed positions counter the known tendency of AI agents to agree with each other too quickly (Yao et al., 2025, [arXiv:2509.23055](https://arxiv.org/abs/2509.23055)).
- **Receipts.** A role may change its score only by citing a new fact or argument.
- **Clear agreement rule.** An option passes when it fits capacity, breaks no red line, creates no new risk for a strategic bet, and no role deviates more than its tolerance (default 20%) from what it wanted.
- **Fairness over time.** A role that conceded recently gets a tighter tolerance, so the same function cannot lose every quarter.
- **Code does the math.** Agents argue and score; a script computes deviations, capacity and the future-proof check.
- **The human chairs.** Nothing is recorded without your yes.

## The live board

While agents negotiate, a local page shows the room: each role as a character with a mood, their latest line, deviation against tolerance, the options being scored and a feed. Mood is computed from the numbers, not generated by the model. The same page replays finished sessions.

![Final state of the VIN run: H3 accepted, every role inside tolerance](docs/vin-accepted.png)

## Examples

Both use the same fictional online auto parts retailer.

| Example | Kind | What it shows |
|---|---|---|
| [`vin-buy-vs-build`](examples/vin-buy-vs-build) | Single decision, with a business case. **Real agent run** | Unanimous positions get red-teamed; the agents find a flaw in the business case, correct it, and accept a plan with four recorded disagreements |
| [`auto-parts-q1-roadmap`](examples/auto-parts-q1-roadmap) | Quarterly roadmap: five initiatives, 30 team-weeks, three strategic bets. Hand-written to illustrate the mechanics | Past concessions tighten the CTO's tolerance; a quick payment integration is rejected because it would block a market launch |

![The original hybrid rejected in the VIN run: CTO, CMO and CDO on red lines](docs/vin-h1-rejected.png)

## Getting started

### What you need

| To do | You need |
|---|---|
| Watch the demo, rerun the math | Python 3.9+ and `pyyaml` |
| Run real sessions | Also [Claude Code](https://code.claude.com/docs) (terminal, desktop app or web) with a Claude subscription that includes it, or an Anthropic API key |

### Install

```bash
git clone https://github.com/mxdxru/prodoffs.git
cd prodoffs
pip install pyyaml
```

Nothing else to install. The agents, skills and hooks live in `.claude/` inside the repository and load automatically when you start Claude Code here.

### 1. Watch a sample session (1 minute, no AI needed)

```bash
python3 -m http.server 8000
```

Open http://localhost:8000/board/?events=/examples/vin-buy-vs-build/sample-session/events.jsonl

Add `&layout=wide` for the 16:9 view used in the video.

### 2. Rerun the math yourself

```bash
python3 scripts/prodoffs.py case examples/vin-buy-vs-build --dry-run
python3 scripts/prodoffs.py score examples/auto-parts-q1-roadmap --round 2 \
  --session examples/auto-parts-q1-roadmap/sample-session --dry-run
```

Change a score in `sample-session/scores/` or a balance in `memory/concessions.yaml` and rerun to see the outcome change. `--dry-run` prints without touching the sample.

### 3. Run a real session

Start Claude Code **from the repository root**:

```bash
claude
```

On first start Claude Code asks whether you trust this folder. Say yes: the live board depends on hooks from `.claude/settings.json`, which only run in a trusted folder.

Then ask in plain words, or call the skill directly:

```
> Run a Prodoffs decision for examples/vin-buy-vs-build
> /prodoffs-roadmap examples/auto-parts-q1-roadmap
```

The skill runs all phases and prints a link to watch the board live. Claude Code will ask permission to run `scripts/prodoffs.py` and write session files; allow them.

A full session runs six agents over several rounds, so it uses far more tokens than a normal chat. Start with the single VIN decision before a full roadmap session, especially on a Pro plan.

### Reset after trying it

```bash
python3 scripts/prodoffs.py reset examples/auto-parts-q1-roadmap            # remove sessions
python3 scripts/prodoffs.py reset examples/auto-parts-q1-roadmap --memory   # also undo recorded decisions
```

Works the same for your own workspaces.

### Use it for your own product

In Claude Code, ask: *"Set up a Prodoffs workspace for my product"*. The setup skill interviews you and creates `workspaces/<name>/`. This folder is git-ignored, so your company data stays out of a public fork.

You can also fill the files by hand, starting from `templates/workspace`:

| File | What to put in |
|---|---|
| `strategy.yaml` | 2 to 5 strategic bets for the next 12 to 18 months, concrete ("two new EU markets in H2", not "grow revenue") |
| `candidates.yaml` | Initiatives for the quarter, each with versions (full, quick...), effort and the shortcuts each creates or fixes; team capacity |
| `memory/shortcuts.yaml` | Known shortcuts and tech debt, even a rough list from engineering leads, with what they block |
| `mandates/*.yaml` | Each role's owned metrics, red lines and weighted requirements |
| `memory/concessions.yaml` | Start at zero, or seed from recent decisions |
| `prodoffs.yaml` | Tolerance, fairness strength, max rounds |

Check a workspace any time:

```bash
python3 scripts/prodoffs.py validate workspaces/<name>
```

Past decisions in `memory/decisions/` help the agents argue from history. Plan versus actual from previous quarters makes the retro useful.

### Troubleshooting

| Symptom | Fix |
|---|---|
| Claude does not know the Prodoffs skills or agents | You started `claude` outside the repository root. Exit, `cd` into `prodoffs`, start again. `/agents` should list six `prodoffs-*` agents |
| The board does not update during a run | The folder is not trusted, so hooks are off, or `python3` is not on your PATH. Check with `/hooks` |
| The board is blank | Open it through `python3 -m http.server`, not as a local file; browsers block reading `events.jsonl` from `file://` |
| `ModuleNotFoundError: No module named 'yaml'` | `pip install pyyaml` for the same Python that runs `python3` |
| Usage limit hit mid-session | Sessions do not resume. Files written so far stay in the session folder for reference; start a new session later. Try a single decision before a full roadmap |

### What Claude keeps between sessions

Prodoffs keeps its memory in plain files you can see and reset. Claude Code auto memory is turned off for this repository, so demo runs do not leak into the next one. Use `/clear` to drop conversation context. Whether your conversations may be used for model training is an account setting; see [Claude Code data usage](https://code.claude.com/docs/en/data-usage).

## What makes it different

| | Typical tool | Prodoffs |
|---|---|---|
| Virtual C-suite projects (OpenExecutive, Conclave, c-level skills, agensuite) | Debate one question; remember past decisions as text | Works at roadmap level; links past shortcuts to future strategic plans |
| Tech-debt tools (CodeScene, Stepsize) | Find debt bottom-up from code and tickets | Records shortcuts top-down, at the moment of the product decision, including non-code ones |
| Prioritization frameworks (RICE, WSJF) | Rank items by value and effort now | Adds what each choice costs the strategy later |
| ADRs, decision logs | Record what was decided | Record what was cut, what it blocks, and who paid |

In one sentence: **Prodoffs connects today's shortcuts to tomorrow's plans, so the roadmap is judged on both.**

## License

MIT. See [LICENSE](LICENSE).
