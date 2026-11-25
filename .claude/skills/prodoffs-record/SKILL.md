---
name: prodoffs-record
description: Record the human decision owner's decision on a Prodoffs recommendation, approve, choose another option or decline, and update the ledger (concessions, shortcuts, decision file). Use when the decision owner gives their answer on a Prodoffs brief.
---

# Record the decision

Agents recommend. Only the decision owner decides, and only this step makes it a decision.

1. Show the owner the brief's recommendation, the trade-offs and the disagreements, and ask for one of: approve the recommendation; choose another scored option; decline (nothing is recorded).
2. Ask for one line of reason; it is stored with the decision.
3. Run `python3 scripts/prodoffs.py record <workspace> --by "<owner>" --note "<reason>"`, adding `--option <id>` if they chose another option. A choice other than the recommendation is recorded as an override. An option that breaks a veto red line cannot be recorded; tell the owner what must be resolved first.
4. Report the decision id and what changed in `memory/`: concession balances, shortcuts created or paid down. Remind them that `prodoffs.py reset <workspace> --memory` undoes recorded decisions in a demo or test.
