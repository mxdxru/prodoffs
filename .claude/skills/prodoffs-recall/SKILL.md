---
name: prodoffs-recall
description: Answer questions about past Prodoffs trade-offs from the workspace memory, such as why a decision was made, who conceded, what blocks a strategic bet, or what shortcuts exist in an area. Use when the user asks about previous decisions, history, or the current state of shortcuts and concessions in a Prodoffs workspace.
---

# Recall past trade-offs

Read-only. Never change memory files in this skill.

1. Identify the workspace.
2. Read what the question needs:
   - decisions: `memory/decisions/*.md`, and for detail the matching `sessions/*/brief.md`, `dissent.yaml` and `positions/`;
   - shortcuts: `memory/shortcuts.yaml`;
   - fairness: `memory/concessions.yaml`;
   - strategy context: `strategy.yaml`;
   - if the question is about risk now, run `python3 scripts/prodoffs.py radar <workspace>`.
3. Answer directly and cite the source of each fact by decision or shortcut id (for example "D-0012", "S-014"). Typical questions:
   - "Why did we choose X?" The decision, the options rejected, who conceded and the recorded dissent.
   - "What blocks bet Y?" Open shortcuts with `blocks` containing Y, their cost later and the decision that created them.
   - "Who has been giving in?" Balances and the decisions behind them.
   - "What did we promise to revisit?" Dissent entries and their revisit conditions.
4. If memory does not contain the answer, say so and name which file would have to hold it. Do not fill gaps from general knowledge.
