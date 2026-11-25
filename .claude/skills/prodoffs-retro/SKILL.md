---
name: prodoffs-retro
description: Quarterly Prodoffs retro. Compares what a recorded roadmap planned with what actually happened, and updates the future price of shortcuts. Use when the user asks for a Prodoffs retro, plan versus reality, or whether past shortcuts cost what was expected.
---

# Prodoffs retro

Input: a workspace with recorded decisions in `memory/decisions/` and the user's actuals.

1. List the decisions of the quarter and, for each, the initiatives, versions and shortcuts created or paid down.
2. Ask the user for actuals in one message, as a short table: initiative, planned weeks, actual weeks, shipped yes or no, and for each open shortcut whether it has already cost time and how much. Accept rough numbers.
3. Write `memory/retro/<quarter>.md` with:
   - planned versus actual effort per initiative, and the overall estimate ratio;
   - shortcuts whose real cost differed from `cost_later`, with the new estimate;
   - recorded disagreements (`dissent.yaml` in each session) whose revisit condition has been met.
4. With the user's yes, update `cost_later` in `memory/shortcuts.yaml` for shortcuts with new evidence, and add an `actual_cost` field.
5. If a disagreement's revisit condition was met, propose reopening that decision with `prodoffs-kickoff`, with that role opening the debate.

Keep it short. The retro is for the next roadmap, not a report.
