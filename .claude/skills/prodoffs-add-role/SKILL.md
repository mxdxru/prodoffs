---
name: prodoffs-add-role
description: Add a new role to Prodoffs as a single agent file, for example Finance, Security, Customer Support or Operations, by interviewing the user about the role's responsibility, accountability, interests, red lines and triggers. Use when the user wants a role that the framework does not have.
---

# Add a role

A role is one file: `.claude/agents/prodoffs-<id>.md`. Use an existing role file (for example `prodoffs-legal.md`) as the template and keep its sections.

1. Ask the user, in one message: the role's name; what it is responsible for; what it is accountable for (the metrics it answers for); what it wants from decisions and what it fears; one to three red lines (and whether any is a veto); when it should be involved; what it prepares in the preparation phase.
2. Propose 3 to 4 weighted requirements (weights sum to 1.0) from the answers, and which tools it needs (web search for roles that research the market or regulations).
3. Write the file, with the `## Mandate` yaml block at the end.
4. Run `python3 scripts/prodoffs.py validate <workspace>`; the new role appears in kickoff's role suggestions.
5. Optional: if the board should draw it with a specific look, add it to `CAST` in `board/index.html`; otherwise it gets a generated look.
