---
name: prodoffs-intake
description: Build a Prodoffs workspace's starting data from the user's own sources (Slack threads, email, Google Docs, Drive folders, exported files). Collects the sources, keeps the raw material as evidence, drafts strategy, candidates, shortcuts and past decisions, and asks about gaps and conflicts. Use when the user wants to start Prodoffs from existing documents and conversations, or to refresh a workspace after its sources changed.
---

# Intake

Goal: turn the user's scattered sources into a workspace that passes `python3 scripts/prodoffs.py validate` and is ready for `prodoffs-kickoff`. You draft. The user decides. Never invent a number, a date or a name that is not in a source.

Work in `workspaces/<name>/`. Never write into `examples/` or `templates/`.

## 1. Workspace

Ask for a short name, for example `acme-q2-roadmap`. If `workspaces/<name>/` does not exist, copy `templates/workspace/` into it. If it exists, this is a refresh: go to step 6.

## 2. Sources

Ask for all sources in one message. Accept any mix of:

- Slack: channel names, thread links or message exports, with a date range
- Email: a search (sender, label, subject words, date range) or exported `.eml`/`.mbox`/text
- Google Docs, Sheets, Slides: links or file names in Drive
- Drive folders and local files the user points to
- Anything the user pastes

Ask only once for the list. Then check what you can read in this session. Use ToolSearch to look for Slack, Gmail and Google Drive tools. Read each source through a connector when one is available and the user has approved it. For any source you cannot read, ask for an export and say which format to use: Markdown or plain text, with date and author on each message or section.

Do not read a source the user did not list. Do not widen a search beyond what they gave.

## 3. Sources and digests

The roles read `evidence/`. Raw sources can be large, so they stay out of it.

**Raw.** For each source, write `workspaces/<name>/sources/<source-slug>.md` with this header, and keep the content as close to the original as you can:

```
---
source: <link, channel, search query or file name>
retrieved: <today's date>
covers: <date range of the material>
authors: <who wrote it, if known>
status: raw
---
```

Remove credentials, personal contact details and anything the user marks as private. Do not summarise away numbers, dates, owners or disagreements in the raw file.

**Digest.** For each source, write `workspaces/<name>/evidence/<source-slug>.md`, at most about 400 words. This is what the roles read:

- Key facts: numbers, dates, owners, with the date of each
- Positions and decisions stated in the source, and who stated them
- Open questions and disagreements, quoted briefly with author and date
- Pointer: the path to `sources/<source-slug>.md` for anything that needs the full text

Every fact in a digest must be traceable to the raw file. Do not add facts that are not there.

## 4. Draft

From the evidence, write these files. Mark every value that came from a source with a comment `# source: evidence/<file>`. Mark every value you could not find as `TBD`.

- `strategy.yaml`: company line, goals with baseline and target, guardrails (one-off investment, monthly run cost, payback), and 2 to 5 bets. A bet is concrete ("launch in two new markets in H2"), not a theme ("grow").
- `candidates.yaml`: initiatives with a quick and a full version where the sources show them, effort in team-weeks, and the corners each quick version cuts. Each cut corner becomes a `creates` entry with `saved_now`, `cost_later` and `blocks` (bet ids).
- `memory/shortcuts.yaml`: existing shortcuts and tech debt named in the sources, with the bets they block.
- `memory/decisions/D-xxxx.md` and `memory/concessions.yaml`: past decisions the sources record, which role gave in and how much. If the sources hold no decision history, leave the balances at zero.

Do not set capacity or a deadline unless a source gives one.

## 5. Questions

Write `workspaces/<name>/intake-questions.md` with three sections:

1. **Missing.** Values that are `TBD` and needed for validation or for a bet.
2. **Conflicts.** Where two sources disagree, quote both with their source and date. Do not pick one.
3. **Assumptions.** Values you inferred from weak evidence, to confirm.

Ask the user the questions in chat, grouped, a few at a time. Put the answers into the draft files and note each answer as coming from the user. Keep going until the missing and conflict sections are empty or the user says the rest can stay `TBD`.

## 6. Refresh

When the workspace already exists, re-read the sources the user names. Compare each source's `covers` date and content with its raw file, then update its digest. Write `workspaces/<name>/intake-changes.md`: which sources changed, and which draft fields they affect.

Never overwrite a field the user has edited or confirmed. Show the proposed change, and apply it only if the user agrees.

## 7. Validate and hand over

Run `python3 scripts/prodoffs.py validate workspaces/<name>` and fix each error with the user. Then show a short summary: bets, candidates and versions, total effort of the full versions against capacity, and bets already at risk from open shortcuts. Say what is still `TBD` and where it is listed.

Offer `prodoffs-kickoff` for the first decision.

## Rules

- The skill drafts. It does not rank initiatives, pick a plan or decide what goes into the roadmap. That is the decision owner's job.
- Raw sources contain personal data. Keep them in `workspaces/`, which is git-ignored. Never copy them into `examples/` or `docs/`.
- Only digests go in `evidence/`. Raw files in `sources/` stay out of the roles' reading path.
- If a connector returns more than the user asked for, drop the extra and say so.
