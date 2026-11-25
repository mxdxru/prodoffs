---
name: prodoffs-radar
description: Produce a Prodoffs risk radar before planning or on a schedule. Shows which strategic bets are at risk from open shortcuts, where shortcuts pile up, which roles have been conceding, and which recorded disagreements may need revisiting. Use when the user asks for a risk review, a pre-planning check, the state of shortcuts, or wants a regular Prodoffs report.
---

# Prodoffs radar

The radar answers one question before anyone opens a roadmap: what is the price of the shortcuts we already carry, and which plans does it threaten?

1. Identify the workspace.
2. Run `python3 scripts/prodoffs.py radar <workspace> --out <workspace>/memory/radar-latest.md`.
3. Read recorded disagreements (`sessions/*/dissent.yaml`) and list those whose revisit condition the user should check now. You cannot measure the conditions yourself; ask the user, or read a connected analytics source if one is available.
4. Reply with at most five lines:
   - bets at risk and the shortcut behind each;
   - the area with the most open shortcuts, if any has two or more;
   - roles with a high concession balance;
   - disagreements due for a check;
   - one recommendation: which shortcut to put on the next roadmap as a paydown candidate, and why.

## Scheduling

If the user wants this regularly (for example two weeks before each quarter's planning), set it up as a scheduled task that runs this skill on the workspace and sends the five-line summary. Ask for the date and the workspace once.
