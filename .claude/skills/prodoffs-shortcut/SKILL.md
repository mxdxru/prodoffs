---
name: prodoffs-shortcut
description: Record a shortcut the moment a team cuts a corner, outside a full Prodoffs session. Captures what was cut, what it saved, what it will cost later and which strategic bets it blocks. Use when the user says a team is doing something the quick way, hardcoding, skipping, postponing a proper solution, or asks to log tech debt or a shortcut in Prodoffs.
---

# Record a shortcut

Most corners are cut in sprints, not in planning sessions. If they are not recorded, the register goes stale and the roadmap sessions argue from a wrong picture.

1. Identify the workspace. If there are several, ask which one.
2. From the user's words, fill as much as possible and ask once for the rest:
   - `shortcut`: what is being cut, in one line;
   - `area`: product or system area, reusing an existing area name from `memory/shortcuts.yaml` if one fits;
   - `saved_now`: time or money saved;
   - `cost_later`: what a proper fix will cost, and whether that grows over time (for example "+1 week per new country");
   - `blocks`: which bets in `strategy.yaml` it slows or blocks. Read the bets and propose the likely ones; the user confirms. If none, write `[]` and say so explicitly.
3. Check `memory/shortcuts.yaml` for an open shortcut in the same area that this one extends. If so, ask whether to update that entry (new `cost_later`) instead of adding a new one.
4. Append the entry with the next free `S-xxx` id, `decided_in: ad-hoc <date>` and `status: open`.
5. Run `python3 scripts/prodoffs.py validate <workspace>`.
6. Reply in two lines: the entry id, and which bets are now at risk according to `python3 scripts/prodoffs.py radar <workspace>`.

Do not judge whether the shortcut was a good idea. The point is to record its price, not to block it.
