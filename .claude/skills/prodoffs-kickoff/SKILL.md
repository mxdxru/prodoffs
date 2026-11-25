---
name: prodoffs-kickoff
description: Start a Prodoffs decision with the human decision owner. Frames the question, alternatives, owner, deadline, constraints, evidence and which roles take part, and writes the task card. Use when the user brings a decision or a roadmap to work through with Prodoffs.
---

# Kickoff

The human owns the task. Your job is to turn what they say into a clear task card, not to decide anything.

1. **Workspace.** Find the workspace (a folder with `strategy.yaml`, `candidates.yaml`, `memory/`). If there is none, run `prodoffs-setup` first.
2. **Ask, in one message, only for what is missing:**
   - the question in one sentence;
   - the alternatives (for a roadmap: the candidates and their versions);
   - who decides (a person, for example "Head of Product");
   - the deadline and hard constraints (dates, budget, people);
   - evidence: documents to put in `evidence/` (market reports, vendor offers, contracts, analytics).
3. **Alternatives.** Make sure each alternative exists as a version in `candidates.yaml` with effort and the shortcuts it creates or fixes. Add missing ones with the user.
4. **Roles.** Read the `involve_when` triggers in each role file in `.claude/agents/` and propose the roles whose area the decision depends on or affects, with one line of reason each. The user confirms or edits. Do not add roles "just in case": fewer, relevant roles argue better.
5. **Session.** Run `python3 scripts/prodoffs.py session new <workspace>`, write `<session>/task.yaml` (format in `docs/role-protocol.md`), then `python3 scripts/prodoffs.py task <workspace>` to validate it and put it on the board.
6. **Business case.** If the decision changes measurable outcomes or costs money, offer `prodoffs-business-case` before deliberation.
7. Hand over to `prodoffs-deliberate`, and tell the user they can steer at every phase.
