#!/usr/bin/env python3
"""Prodoffs CLI: the deterministic part of the framework.

Agents argue, this script counts. It computes deviations, tolerances, moods,
capacity, the future-proof check, writes the decision brief, updates the
ledger, and appends events to the session stream that the board renders.

Usage:
  prodoffs.py session new <workspace>
  prodoffs.py emit <type> key=value ... [--session DIR]
  prodoffs.py validate <workspace>
  prodoffs.py radar <workspace> [--out FILE]
  prodoffs.py status <workspace> [--session DIR]
  prodoffs.py case <workspace> [--session DIR] [--dry-run]
  prodoffs.py score <workspace> --round N [--session DIR] [--final] [--dry-run]
  prodoffs.py brief <workspace> [--session DIR]
  prodoffs.py task <workspace> [--session DIR]
  prodoffs.py record <workspace> --by NAME [--option ID] [--note TEXT] [--session DIR]
  prodoffs.py reset <workspace> [--memory]
  prodoffs.py hook            (called by Claude Code hooks, reads JSON on stdin)
"""
import argparse
import datetime as dt
import glob
import json
import os
import shutil
import sys

try:
    import yaml
except ImportError:
    sys.exit("Prodoffs needs PyYAML: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT = os.path.join(ROOT, ".prodoffs", "current")
AGENTS = os.path.join(ROOT, ".claude", "agents")
ROLE_PREFIX = "prodoffs-"
NON_VOTING = {"facilitator"}


def role_ids():
    """All roles defined as agent files, except the non-voting facilitator."""
    out = []
    for f in sorted(glob.glob(os.path.join(AGENTS, ROLE_PREFIX + "*.md"))):
        rid = os.path.basename(f)[len(ROLE_PREFIX):-3]
        if rid not in NON_VOTING:
            out.append(rid)
    return out


def role_mandate(rid):
    """Default mandate: the yaml block under '## Mandate' in the role's agent file."""
    path = os.path.join(AGENTS, f"{ROLE_PREFIX}{rid}.md")
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()
    if "## Mandate" not in text:
        return None
    block = text.split("## Mandate", 1)[1]
    if "```yaml" not in block:
        return None
    return yaml.safe_load(block.split("```yaml", 1)[1].split("```", 1)[0])


# ---------- io helpers ----------

def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or default


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def resolve_session(arg):
    if arg:
        return os.path.abspath(arg)
    if os.path.exists(CURRENT):
        with open(CURRENT) as f:
            return f.read().strip()
    sys.exit("No session. Run: prodoffs.py session new <workspace>, or pass --session")


def emit(session, event):
    event = {"ts": now(), **event}
    with open(os.path.join(session, "events.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


# ---------- workspace model ----------

class Workspace:
    def __init__(self, path, session=None):
        self.path = os.path.abspath(path)
        p = lambda *a: os.path.join(self.path, *a)
        self.rules = load(p("prodoffs.yaml"), {})
        self.strategy = load(p("strategy.yaml"), {})
        # a single decision brings its own candidates file inside the session
        own = os.path.join(session, "candidates.yaml") if session else None
        self.candidates = load(own if own and os.path.exists(own) else p("candidates.yaml"), {})
        self.task = load(os.path.join(session, "task.yaml"), {}) if session else {}
        if self.task.get("roles"):
            roster = list(self.task["roles"])
        elif os.path.isdir(p("mandates")):
            roster = sorted(os.path.basename(f)[:-5] for f in glob.glob(p("mandates", "*.yaml")))
        else:
            roster = role_ids()
        # a workspace mandate overrides the role file's default mandate
        self.mandates = {r: load(p("mandates", f"{r}.yaml")) or role_mandate(r) for r in roster}
        self.mandates = {r: m for r, m in self.mandates.items() if m}
        own_bc = os.path.join(session, "business_case.yaml") if session else None
        self.business_case = load(own_bc if own_bc and os.path.exists(own_bc) else p("business_case.yaml"), {})
        self.shortcuts = load(p("memory", "shortcuts.yaml"), {"shortcuts": []})
        self.concessions = load(p("memory", "concessions.yaml"), {})

    @property
    def roles(self):
        return list(self.mandates)

    def tolerance(self, role):
        r = self.rules
        x_base, x_min, k = r.get("x_base", 0.2), r.get("x_min", 0.08), r.get("k", 0.2)
        bal = (self.concessions.get(role) or {}).get("balance", 0.0)
        return round(max(x_min, min(x_base, x_base - k * bal)), 2)

    def candidate(self, cid):
        for c in self.candidates.get("candidates", []):
            if c["id"] == cid:
                return c
        sys.exit(f"Unknown candidate: {cid}")

    def version(self, cid, vid):
        if vid == "later":
            return {"label": "Moved to next quarter", "effort": 0}
        return self.candidate(cid)["versions"][vid]

    def open_shortcuts(self):
        return [s for s in self.shortcuts.get("shortcuts", []) if s.get("status") == "open"]


def weighted(mandate, scores):
    total = 0.0
    for req in mandate["requirements"]:
        total += req["weight"] * scores[req["id"]]
    return total


def mood_of(dev, tol, red_lines):
    if dev is None:
        return "thinking"
    if red_lines or dev > tol:
        return "angry"
    ratio = dev / tol if tol else 1
    if ratio < 0.5:
        return "pleased"
    if ratio < 0.8:
        return "neutral"
    return "concerned"


def analyse_option(ws, opt):
    """Effort, shortcuts created and fixed, and the future-proof check."""
    effort, created, fixed, items = 0, [], [], []
    for cid, vid in opt["items"].items():
        v = ws.version(cid, vid)
        effort += v.get("effort", 0)
        created += v.get("creates", [])
        fixed += v.get("fixes", [])
        items.append({"id": cid, "name": ws.candidate(cid)["name"], "version": vid, "label": v["label"]})
    still_open = [s for s in ws.open_shortcuts() if s["id"] not in fixed]
    risky = still_open + created
    bets = []
    for bet in ws.strategy.get("bets", []):
        because = [s["id"] for s in risky if bet["id"] in s.get("blocks", [])]
        new = [s["id"] for s in created if bet["id"] in s.get("blocks", [])]
        bets.append({"id": bet["id"], "name": bet["name"],
                     "status": "at_risk" if because else "on_track", "because": because, "new_risk": new})
    guardrails, goals = strategy_check(ws, opt)
    return {"effort": effort, "created": created, "fixed": fixed, "items": items, "bets": bets,
            "guardrails": guardrails, "goals": goals}


def strategy_check(ws, opt):
    """Guardrails and goal contribution from the business case, for single-decision options."""
    bc, st = ws.business_case, ws.strategy
    if not bc or len(opt.get("items", {})) != 1:
        return [], []
    vid = list(opt["items"].values())[0]
    alt = bc.get("alternatives", {}).get(vid)
    if not alt:
        return [], []
    sim = simulate_case(bc, alt)
    g = st.get("guardrails", {}) or {}
    checks = []
    if "max_one_off_investment" in g:
        checks.append({"name": "One-off investment", "limit": g["max_one_off_investment"], "value": sim["one_off"],
                       "ok": sim["one_off"] <= g["max_one_off_investment"]})
    if "max_added_run_cost_monthly" in g:
        checks.append({"name": "Added run cost per month once live", "limit": g["max_added_run_cost_monthly"],
                       "value": sim["added_run_cost_monthly"], "ok": sim["added_run_cost_monthly"] <= g["max_added_run_cost_monthly"]})
    if "max_payback_months" in g:
        pb = sim["payback_month"] or 10 ** 6
        checks.append({"name": "Payback, months", "limit": g["max_payback_months"], "value": sim["payback_month"],
                       "ok": pb <= g["max_payback_months"]})
    goals = []
    for goal in st.get("goals", []) or []:
        if goal.get("metric") == "revenue" and sim["years"]:
            target = goal["baseline"] * goal["target_growth"]
            goals.append({"name": goal["name"], "share_year1": round(sim["years"][0]["revenue"] / target, 3),
                          "revenue_year1": sim["years"][0]["revenue"]})
    return checks, goals


# ---------- business case ----------

def _per_year(val, year):
    if isinstance(val, list):
        return val[min(year, len(val) - 1)]
    return val


def simulate_case(bc, alt):
    """Monthly simulation of value and cost for one alternative. Returns a summary dict."""
    b = bc["baseline"]
    months = int(bc.get("horizon_years", 3) * 12)
    twc = bc.get("cost_per_team_week", 9000)
    sessions = b["monthly_search_sessions"]
    lookups = sessions * (1 - b["vehicle_identified_share"]) * b["vin_entry_share"]
    conv_delta = b["conversion_identified"] - b["conversion_unidentified"]
    margin_per_order = b["avg_order_value"] * b["gross_margin"]
    fitment_returns_per_order = b["return_rate"] * b["fitment_share_of_returns"]
    one_off = alt.get("one_off_team_weeks", 0) * twc
    cum, payback, years = -one_off, None, []
    year_net, year_value, year_cost, year_rev = 0.0, 0.0, 0.0, 0.0
    run_rate = None
    live_costs = []
    for m in range(1, months + 1):
        y = (m - 1) // 12
        live = m > alt.get("time_to_value_months", 0)
        value = cost = revenue = 0.0
        if live:
            hit = _per_year(alt["hit_rate"], y)
            precision = _per_year(alt.get("precision", 1.0), y)
            identified = lookups * hit
            extra_orders = identified * conv_delta
            vin_orders = identified * b["conversion_identified"]
            completion_orders = vin_orders * b.get("completion_uplift", 0)
            avoided = vin_orders * fitment_returns_per_order * b.get("fitment_return_reduction", 0) * precision
            wrong_id = vin_orders * (1 - precision)
            value = (extra_orders + completion_orders) * margin_per_order + (avoided - wrong_id) * b["cost_per_return"]
            revenue = (extra_orders + completion_orders) * b["avg_order_value"]
            vendor_share = _per_year(alt.get("vendor_share", 1.0 if alt.get("fee_per_lookup") else 0.0), y)
            fee = alt.get("fee_per_lookup", 0) * (1 + alt.get("fee_growth_per_year", 0)) ** y
            fees = max(lookups * vendor_share * fee, alt.get("monthly_minimum", 0) if vendor_share > 0 else 0)
            cost = fees + alt.get("run_cost_monthly", 0)
            live_costs.append(cost)
        else:
            cost = alt.get("pre_launch_cost_monthly", 0)
        net = value - cost
        cum += net
        if payback is None and cum >= 0:
            payback = m
        year_net += net; year_value += value; year_cost += cost; year_rev += revenue
        if m % 12 == 0:
            years.append({"value": round(year_value), "cost": round(year_cost), "net": round(year_net), "revenue": round(year_rev)})
            year_net = year_value = year_cost = year_rev = 0.0
        if m == months:
            run_rate = round(net)
    return {"label": alt.get("label", ""), "one_off": round(one_off), "years": years,
            "total_net": round(cum), "payback_month": payback, "monthly_run_rate_end": run_rate,
            "lookups_per_month": round(lookups),
            # guardrail view: the monthly cost once live, over its first 12 live months (not diluted by pre-launch months)
            "added_run_cost_monthly": round(max(live_costs[:12])) if live_costs else 0}


def cmd_case(a):
    ws = Workspace(a.workspace)
    own = os.path.join(a.session, "business_case.yaml") if a.session else None
    # a session may carry its own corrected business case (added by the facilitator)
    bc = load(own if own and os.path.exists(own) else os.path.join(ws.path, "business_case.yaml"))
    if not bc:
        sys.exit("No business_case.yaml in workspace")
    cur = bc.get("currency", "EUR")
    ws.business_case = bc
    res = {k: simulate_case(bc, v) for k, v in bc["alternatives"].items()}
    strat = {k: strategy_check(ws, {"items": {"_": k}}) for k in res}
    n = int(bc.get("horizon_years", 3))
    head = "| Alternative | One-off | " + " | ".join(f"Year {i+1} net" for i in range(n)) + f" | {n}-year net | Payback | Monthly net at end |"
    lines = [f"# Business case: {bc.get('question', os.path.basename(ws.path))}", "",
             f"All figures in {cur}, undiscounted, computed by `prodoffs.py case` from `business_case.yaml`.", "",
             head, "|" + "---|" * (n + 5)]
    for k, r in res.items():
        pb = f"month {r['payback_month']}" if r["payback_month"] else f"not within {n} years"
        lines.append(f"| {r['label'] or k} | {r['one_off']:,} | " + " | ".join(f"{y['net']:,}" for y in r["years"]) +
                     f" | **{r['total_net']:,}** | {pb} | {r['monthly_run_rate_end']:,} |")
    if any(strat[k][0] or strat[k][1] for k in res):
        gl = ws.strategy.get("goals", [])
        lines += ["", "## Against the strategy", "",
                  "| Alternative | Revenue added, year 1 | Share of growth goal | Guardrails |", "|---|---|---|---|"]
        for k, r in res.items():
            checks, goals = strat[k]
            g0 = goals[0] if goals else None
            breaches = [f"{c['name']} {c['value']:,} > {c['limit']:,}" if c["value"] is not None else f"{c['name']} not reached"
                        for c in checks if not c["ok"]]
            lines.append(f"| {r['label'] or k} | {r['years'][0]['revenue']:,} | {f'{g0['share_year1']:.0%}' if g0 else ''} | "
                         + ("breach: " + "; ".join(breaches) if breaches else "within") + " |")
        if gl:
            lines += ["", "Goals: " + "; ".join(f"{g['name']} (baseline {g['baseline']:,}, target +{g['target_growth']:.0%})"
                                               if g.get("metric") == "revenue" else g["name"] for g in gl) + "."]
        g = ws.strategy.get("guardrails", {})
        if g:
            lines += ["Guardrails: " + ", ".join(f"{k.replace('_', ' ')} {v:,}" for k, v in g.items()) + "."]
    b = bc["baseline"]
    lines += ["", "## Assumptions", "",
              f"- {b['monthly_search_sessions']:,} part-search sessions a month; vehicle known today in {b['vehicle_identified_share']:.0%} of them.",
              f"- If VIN entry is offered, {b['vin_entry_share']:.0%} of the other sessions use it: about {list(res.values())[0]['lookups_per_month']:,} lookups a month.",
              f"- Search-to-order conversion {b['conversion_identified']:.1%} with a known vehicle versus {b['conversion_unidentified']:.1%} without.",
              f"- Checkout completion uplift {b.get('completion_uplift', 0):.0%} on orders from VIN-identified sessions.",
              f"- Return rate {b['return_rate']:.0%}, of which {b['fitment_share_of_returns']:.0%} fitment-related; VIN identification removes {b.get('fitment_return_reduction', 0):.0%} of those, scaled by precision. Cost per return {b['cost_per_return']}.",
              f"- Average order value {b['avg_order_value']}, gross margin {b['gross_margin']:.0%}, team-week {bc.get('cost_per_team_week', 9000):,}."]
    for note in bc.get("notes", []):
        lines.append(f"- {note}")
    out = "\n".join(lines) + "\n"
    session = None
    if a.session or os.path.exists(CURRENT):
        try:
            session = resolve_session(a.session)
        except SystemExit:
            session = None
    if session and not a.dry_run:
        with open(os.path.join(session, "business_case.md"), "w", encoding="utf-8") as f:
            f.write(out)
        emit(session, {"type": "case", "currency": cur, "years": n,
                       "options": {k: {"label": r["label"] or k, "total_net": r["total_net"],
                                       "payback_month": r["payback_month"],
                                       "guardrails_ok": all(c["ok"] for c in strat[k][0]),
                                       "goal_share": strat[k][1][0]["share_year1"] if strat[k][1] else None}
                                   for k, r in res.items()}})
    print(out)


# ---------- commands ----------

def cmd_session_new(a):
    ws = Workspace(a.workspace)
    sid = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    session = os.path.join(ws.path, "sessions", sid)
    for d in ["positions", "critiques", "scores"]:
        os.makedirs(os.path.join(session, d), exist_ok=True)
    os.makedirs(os.path.dirname(CURRENT), exist_ok=True)
    with open(CURRENT, "w") as f:
        f.write(session)
    emit(session, {"type": "cast", "workspace": os.path.basename(ws.path), "roles": ws.roles})
    emit(session, {"type": "phase", "phase": "intake", "round": 0})
    bets = analyse_option(ws, {"items": {}})["bets"]
    emit(session, {"type": "strategy", "bets": bets})
    print(session)


def cmd_validate(a):
    ws = Workspace(a.workspace)
    errors, warns = [], []
    for f in ["prodoffs.yaml", "strategy.yaml", "candidates.yaml"]:
        if not os.path.exists(os.path.join(ws.path, f)):
            errors.append(f"missing {f}")
    if not ws.mandates:
        errors.append("no roles: add role files in .claude/agents/ or mandates in mandates/")
    for role, m in ws.mandates.items():
        total = round(sum(r["weight"] for r in m.get("requirements", [])), 3)
        if total != 1.0:
            errors.append(f"{role}: requirement weights sum to {total}, expected 1.0")
        if not m.get("red_lines"):
            warns.append(f"{role}: no red lines")
    bet_ids = {b["id"] for b in ws.strategy.get("bets", [])}
    if not bet_ids:
        errors.append("strategy.yaml has no bets")
    shortcuts = list(ws.shortcuts.get("shortcuts", []))
    known = {s["id"] for s in shortcuts}
    for c in ws.candidates.get("candidates", []):
        for vid, v in c.get("versions", {}).items():
            if "effort" not in v:
                errors.append(f"{c['id']}.{vid}: no effort")
            shortcuts += v.get("creates", [])
            for sid in v.get("fixes", []):
                if sid not in known:
                    errors.append(f"{c['id']}.{vid}: fixes unknown shortcut {sid}")
    for sc in shortcuts:
        for b in sc.get("blocks", []):
            if b not in bet_ids:
                errors.append(f"{sc['id']}: blocks unknown bet '{b}'")
    g = ws.strategy.get("guardrails", {}) or {}
    for k in g:
        if k not in ("max_one_off_investment", "max_added_run_cost_monthly", "max_payback_months"):
            warns.append(f"strategy.yaml: unknown guardrail '{k}' is ignored")
    if not ws.strategy.get("goals"):
        warns.append("strategy.yaml: no goals; options cannot be checked against the company's direction")
    if not ws.candidates.get("capacity_team_weeks"):
        errors.append("candidates.yaml: capacity_team_weeks missing")
    for w in warns:
        print("warning:", w)
    for e in errors:
        print("error:", e)
    if errors:
        sys.exit(1)
    print(f"OK: {len(ws.mandates)} roles, {len(bet_ids)} bets, "
          f"{len(ws.candidates.get('candidates', []))} candidates, {len(known)} known shortcuts")


def cmd_radar(a):
    ws = Workspace(a.workspace)
    open_sc = ws.open_shortcuts()
    lines = [f"# Prodoffs radar: {os.path.basename(ws.path)}", "", "## Strategic bets", "",
             "| Bet | Status | Blocked by |", "|---|---|---|"]
    for bet in ws.strategy.get("bets", []):
        blockers = [sc for sc in open_sc if bet["id"] in sc.get("blocks", [])]
        status = "at risk" if blockers else "on track"
        lines.append(f"| {bet['name']} | {status} | " +
                     (", ".join(f"{sc['id']} ({sc.get('cost_later', 'cost unknown')})" for sc in blockers) or "") + " |")
    lines += ["", "## Open shortcuts", "", "| Id | Area | Shortcut | Cost later | Blocks | Since |", "|---|---|---|---|---|---|"]
    for sc in open_sc:
        lines.append(f"| {sc['id']} | {sc.get('area', '')} | {sc['shortcut']} | {sc.get('cost_later', '')} | "
                     f"{', '.join(sc.get('blocks', [])) or 'nothing recorded'} | {sc.get('decided_in', '')} |")
    by_area = {}
    for sc in open_sc:
        by_area.setdefault(sc.get("area", "unknown"), []).append(sc["id"])
    hot = {k: v for k, v in by_area.items() if len(v) >= 2}
    lines += ["", "## Signals", ""]
    for area, ids in hot.items():
        lines.append(f"- **{area}:** {len(ids)} open shortcuts ({', '.join(ids)}). Fixing them separately costs more than together.")
    for sc in open_sc:
        if not sc.get("blocks"):
            lines.append(f"- **{sc['id']}** blocks nothing recorded. Either it is harmless, or its impact is unknown: ask engineering.")
    for role in ws.roles:
        bal = (ws.concessions.get(role) or {}).get("balance", 0.0)
        if bal >= 0.3:
            lines.append(f"- **{role.upper()}** concession balance {bal:.2f}: tolerance now {ws.tolerance(role):.0%}. "
                         "This role has been giving in; expect resistance and plan a fair trade.")
    if len(lines) and lines[-1] == "":
        lines.append("- No signals.")
    out = "\n".join(lines) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out)
    print(out)


def cmd_status(a):
    ws = Workspace(a.workspace)
    session = resolve_session(a.session)
    bets = analyse_option(ws, {"items": {}})["bets"]
    emit(session, {"type": "strategy", "bets": bets})
    for b in bets:
        why = f" (blocked by {', '.join(b['because'])})" if b["because"] else ""
        print(f"{b['name']}: {b['status']}{why}")


def cmd_emit(a):
    session = resolve_session(a.session)
    event = {"type": a.type}
    for kv in a.pairs:
        k, _, v = kv.partition("=")
        event[k] = int(v) if v.isdigit() else v
    emit(session, event)


def evaluate(ws, info, roles, capacity, block_on_risk):
    """Consensus and compromise tests for one scored option."""
    fits = info["effort"] <= capacity
    new_risk = [bt for bt in info["bets"] if bt["new_risk"]]
    guard_breach = [g for g in info.get("guardrails", []) if not g["ok"]]
    strategic_ok = not (block_on_risk and (new_risk or guard_breach))
    no_red = not any(r["red_lines"] for r in roles.values())
    within = all(r["deviation"] <= r["tolerance"] for r in roles.values())
    better_for_all = all(r["deviation"] == 0 for r in roles.values())
    consensus = fits and strategic_ok and no_red and (within or better_for_all)
    # compromise: hard constraints hold, nobody beyond twice their tolerance
    compromise_ok = fits and strategic_ok and no_red and all(r["deviation"] <= 2 * r["tolerance"] for r in roles.values())
    worst = max((r["deviation"] / r["tolerance"]) if r["tolerance"] else 9 for r in roles.values())
    return {"fits": fits, "strategic_ok": strategic_ok, "no_red_lines": no_red, "consensus": consensus,
            "compromise_ok": compromise_ok, "worst_ratio": round(worst, 2),
            "overshoot": round(max(r["deviation"] - r["tolerance"] for r in roles.values()), 2),
            "guardrail_breaches": [g["name"] for g in guard_breach], "new_risk": [bt["name"] for bt in new_risk]}


def cmd_score(a):
    session = resolve_session(a.session)
    ws = Workspace(a.workspace, session)
    options = load(os.path.join(session, "options.yaml"), {}).get("options", {})
    options = {k: v for k, v in options.items() if v.get("round") == a.round}
    if not options:
        sys.exit(f"No options for round {a.round} in options.yaml")
    capacity = ws.candidates.get("capacity_team_weeks", 0)
    block_on_risk = ws.rules.get("block_on_strategy_risk", True)
    final = a.final or a.round >= ws.rules.get("max_rounds", 5)

    role_scores = {}
    for role in ws.roles:
        f = os.path.join(session, "scores", f"r{a.round}-{role}.yaml")
        if not os.path.exists(f):
            sys.exit(f"Missing scores: {f}")
        role_scores[role] = load(f)

    results = {}
    for oid, opt in options.items():
        info = analyse_option(ws, opt)
        roles = {}
        for role in ws.roles:
            m, sc = ws.mandates[role], role_scores[role]
            opening = weighted(m, sc["opening"])
            entry = sc["options"][oid]
            dev = round(max(0.0, 1 - weighted(m, entry["scores"]) / opening), 2)
            tol = ws.tolerance(role)
            reds = entry.get("red_lines", [])
            vetoes = [rl["id"] for rl in m.get("red_lines", []) if rl.get("veto") and rl["id"] in reds]
            roles[role] = {"deviation": dev, "tolerance": tol, "red_lines": reds, "vetoes": vetoes,
                           "mood": mood_of(dev, tol, reds), "receipt": entry.get("receipt"),
                           "line": entry.get("line", "")}
        ev = evaluate(ws, info, roles, capacity, block_on_risk)
        results[oid] = {**info, "roles": roles, **ev, "accepted": ev["consensus"], "capacity": capacity}

    consensus = [o for o in results if results[o]["consensus"]]
    compromise = [o for o in results if results[o]["compromise_ok"]]
    if consensus:
        status = "consensus"
        recommended = min(consensus, key=lambda o: results[o]["worst_ratio"])
    elif final and compromise:
        status = "compromise"
        recommended = min(compromise, key=lambda o: results[o]["worst_ratio"])
        results[recommended]["accepted"] = True
    elif final:
        status, recommended = "owner_decides", None
    else:
        status, recommended = "open", None
    best = recommended or min(results, key=lambda o: (results[o]["overshoot"], results[o]["worst_ratio"]))
    if not a.dry_run:
        with open(os.path.join(session, f"result-r{a.round}.json"), "w") as f:
            json.dump({"round": a.round, "status": status, "recommended": recommended, "best": best,
                       "final": final, "options": results}, f, indent=2)

    print(f"Round {a.round}")
    for oid, r in results.items():
        flag = "CONSENSUS" if r["consensus"] else ("compromise possible" if r["compromise_ok"] else "fails")
        print(f"\n{oid}: {flag}  effort {r['effort']}/{r['capacity']} team-weeks")
        for role, x in r["roles"].items():
            red = f"  red lines: {', '.join(x['red_lines'])}" if x["red_lines"] else ""
            print(f"  {role.upper():12} deviation {x['deviation']:.0%}  tolerance {x['tolerance']:.0%}  {x['mood']}{red}")
        for b in r["bets"]:
            why = f" (blocked by {', '.join(b['because'])})" if b["because"] else ""
            print(f"  bet {b['name']}: {b['status']}{why}")
        for g in r.get("guardrails", []):
            print(f"  guardrail {g['name']}: {g['value']} vs limit {g['limit']} {'ok' if g['ok'] else 'BREACH'}")
    labels = {"consensus": "Consensus", "compromise": "Compromise", "owner_decides": "No agreement: the decision owner decides",
              "open": "No consensus yet: continue the debate"}
    print(f"\n{labels[status]}" + (f": {recommended}" if recommended else f" (closest: {best})"))
    if a.dry_run:
        return

    order = [o for o in results if o != best] + [best]
    for oid in order:
        r = results[oid]
        emit(session, {"type": "scores", "round": a.round, "option": oid, "accepted": r["accepted"],
                       "featured": oid == best,
                       "roles": {k: {kk: v[kk] for kk in ["deviation", "tolerance", "mood", "red_lines"]}
                                 for k, v in r["roles"].items()},
                       "capacity": {"used": r["effort"], "total": r["capacity"]}})
        emit(session, {"type": "roadmap", "option": oid, "items": r["items"],
                       "capacity": {"used": r["effort"], "total": r["capacity"]}})
        emit(session, {"type": "strategy", "bets": r["bets"], "guardrails": r.get("guardrails", []), "goals": r.get("goals", [])})
        for sc in r["created"]:
            emit(session, {"type": "shortcut", "id": sc["id"], "text": sc["shortcut"], "blocks": sc.get("blocks", [])})
        for role, x in r["roles"].items():
            if x["line"]:
                emit(session, {"type": "say", "role": role, "text": x["line"], "receipt": x["receipt"], "option": oid})
        if oid != best:
            why = []
            reds = sorted({rl for v in r["roles"].values() for rl in v["red_lines"]})
            if reds:
                why.append("red lines " + ", ".join(reds))
            if r["guardrail_breaches"]:
                why.append("guardrails " + ", ".join(r["guardrail_breaches"]).lower())
            if r["new_risk"]:
                why.append("new risk to " + ", ".join(r["new_risk"]))
            if not why and not r["consensus"]:
                why.append("outside tolerance")
            emit(session, {"type": "note", "text": f"{oid}: {'consensus' if r['consensus'] else 'rejected'}" + (f", {'; '.join(why)}" if why and not r["consensus"] else "")})
    if status in ("consensus", "compromise"):
        emit(session, {"type": "decision", "option": recommended, "status": status})
    elif status == "owner_decides":
        emit(session, {"type": "escalate", "closest": best})


def cmd_task(a):
    """Validate the human's task card and put it on the board."""
    session = resolve_session(a.session)
    task = load(os.path.join(session, "task.yaml"))
    if not task:
        sys.exit(f"No task.yaml in {session}")
    missing = [k for k in ["question", "decision_owner", "roles"] if not task.get(k)]
    unknown = [r for r in task.get("roles", []) if r not in role_ids()]
    if missing or unknown:
        sys.exit(f"task.yaml: missing {missing}; unknown roles {unknown} (known: {role_ids()})")
    emit(session, {"type": "task", "question": task["question"], "owner": task["decision_owner"],
                   "roles": task["roles"], "deadline": task.get("deadline", "")})
    print(f"Task: {task['question']}\nOwner: {task['decision_owner']}\nRoles: {', '.join(task['roles'])}")


def latest_result(session):
    files = sorted(glob.glob(os.path.join(session, "result-r*.json")))
    if not files:
        sys.exit("No scoring results yet. Run score first.")
    with open(files[-1]) as f:
        return json.load(f)


def cmd_brief(a):
    session = resolve_session(a.session)
    ws = Workspace(a.workspace, session)
    res = latest_result(session)
    best = res["best"]
    r = res["options"][best]
    st = res.get("status", "consensus" if r["accepted"] else "owner_decides")
    owner = ws.task.get("decision_owner", "the decision owner")
    approval = load(os.path.join(session, "approval.yaml"), {})
    rec = {"consensus": f"Recommendation: **{best}**, reached by consensus.",
           "compromise": f"Recommendation: **{best}**, as a compromise (no option met every tolerance).",
           "owner_decides": f"No agreement. Closest option: **{best}**. {owner} decides.",
           "open": f"Debate still open. Leading option: **{best}**."}[st]
    decision = (f"**Decision:** {approval['option']} approved by {approval['by']} on {approval['date']}"
                + (" (owner override)" if approval.get("status") == "override" else "") + "."
                if approval else f"**Decision:** pending. The agents recommend; {owner} decides.")
    lines = [f"# Decision brief: {ws.task.get('question', os.path.basename(ws.path))}", ""]
    if ws.task:
        lines += [f"Decision owner: {owner}. Roles: {', '.join(r_.title() for r_ in ws.task.get('roles', []))}. "
                  f"Round {res['round']}.", ""]
    lines += [rec, "", decision, "", "## Option", "", "| Initiative | Version |", "|---|---|"]
    lines += [f"| {i['name']} | {i['label']} |" for i in r["items"]]
    lines += ["", f"Capacity: {r['effort']} of {r['capacity']} team-weeks.", "",
              "## Cost per role", "", "| Role | Deviation | Tolerance | Mood |", "|---|---|---|---|"]
    lines += [f"| {k.title()} | {v['deviation']:.0%} | {v['tolerance']:.0%} | {v['mood']} |"
              for k, v in r["roles"].items()]
    if r.get("guardrails") or r.get("goals"):
        lines += ["", "## Strategy check", ""]
        for g in r.get("goals", []):
            lines.append(f"- **{g['name']}:** this option adds about {g['revenue_year1']:,} revenue in year 1, "
                         f"{g['share_year1']:.0%} of the growth target.")
        for g in r.get("guardrails", []):
            lines.append(f"- **{g['name']}:** {g['value']:,} against a limit of {g['limit']:,}: {'within' if g['ok'] else 'BREACH'}.")
    lines += ["", "## Future-proof check", ""]
    for b in r["bets"]:
        why = f", blocked by {', '.join(b['because'])}" if b["because"] else ""
        lines.append(f"- **{b['name']}:** {b['status'].replace('_', ' ')}{why}")
    lines += ["", "## Shortcuts this plan creates", ""]
    lines += [f"- **{s['id']}** {s['shortcut']}. Cost later: {s.get('cost_later', 'n/a')}."
              for s in r["created"]] or ["- None"]
    if r["fixed"]:
        lines += ["", "## Shortcuts this plan pays down", ""]
        lines += [f"- {sid}" for sid in r["fixed"]]
    case_md = os.path.join(session, "business_case.md")
    if os.path.exists(case_md):
        with open(case_md, encoding="utf-8") as f:
            body = f.read().split("\n", 2)[2]
        lines += ["", "## Business case", "", body.strip()]
    positions = {}
    for f in sorted(glob.glob(os.path.join(session, "positions", "*.yaml"))):
        pos = load(f, {})
        positions[pos.get("role", os.path.basename(f)[:-5])] = pos
    if positions:
        lines += ["", "## Positions", "", "| Role | Stance | Preferred | Key idea | Top risk |", "|---|---|---|---|---|"]
        for role, pos in positions.items():
            pref = ", ".join(f"{k}: {v}" for k, v in (pos.get("proposal") or {}).items() if v != "later")
            idea = (pos.get("ideas") or [""])[0]
            risk = (pos.get("risks") or [""])[0]
            lines.append(f"| {role.title()} | {pos.get('stance', '')} | {pref} | {idea} | {risk} |")
        alts = {}
        for role, pos in positions.items():
            for alt, pc in (pos.get("alternatives") or {}).items():
                a_ = alts.setdefault(alt, {"pros": [], "cons": []})
                a_["pros"] += [f"{p} ({role.title()})" for p in pc.get("pros", [])]
                a_["cons"] += [f"{c} ({role.title()})" for c in pc.get("cons", [])]
        if alts:
            lines += ["", "## Pros and cons by alternative", ""]
            for alt, pc in alts.items():
                lines += [f"### {alt}", "", "**Pros**", ""] + [f"- {p}" for p in pc["pros"]] + \
                         ["", "**Cons**", ""] + [f"- {c}" for c in pc["cons"]] + [""]
    plan = load(os.path.join(session, "plan.yaml"), {}).get("plan", [])
    if plan:
        lines += ["", "## Implementation plan", "", "| Step | Owner | Weeks | Done when |", "|---|---|---|---|"]
        lines += [f"| {p['step']} | {p.get('owner', '').title()} | {p.get('weeks', '')} | {p.get('done_when', '')} |" for p in plan]
        metrics = load(os.path.join(session, "plan.yaml"), {}).get("success_metrics", [])
        if metrics:
            if all(isinstance(m, dict) for m in metrics):
                lines += ["", "**Success metrics**", "", "| Metric | Baseline | Target | Measured by |", "|---|---|---|---|"]
                lines += [f"| {m.get('metric', '')} | {m.get('baseline', '')} | {m.get('target', '')} | {m.get('measured_by', '')} |" for m in metrics]
            else:
                lines += ["", "**Success metrics:** " + "; ".join(str(m) for m in metrics) + "."]
    risks = load(os.path.join(session, "risks.yaml"), {}).get("risks", [])
    if risks:
        lines += ["", "## Risks that remain", "", "| Risk | Owner | Likelihood | Impact | Mitigation |", "|---|---|---|---|---|"]
        lines += [f"| {x['risk']} | {str(x.get('owner', '')).title()} | {x.get('likelihood', '')} | {x.get('impact', '')} | {x.get('mitigation', '')} |" for x in risks]
    lines += ["", "## Trade-offs", "", "What each role gave up in this option:", ""]
    lines += [f"- **{k.title()}:** {v['deviation']:.0%} away from its opening position (tolerance {v['tolerance']:.0%})."
              for k, v in r["roles"].items() if v["deviation"] > 0] or ["- Nobody moved away from their opening position."]
    others = {k: v for k, v in res["options"].items() if k != best}
    if others:
        lines += ["", "Why the other options were not recommended:", ""]
        for k, v in others.items():
            why = []
            reds = sorted({rl for x in v["roles"].values() for rl in x["red_lines"]})
            if reds:
                why.append("red lines: " + ", ".join(reds))
            if v.get("guardrail_breaches"):
                why.append("guardrails: " + ", ".join(v["guardrail_breaches"]).lower())
            if v.get("new_risk"):
                why.append("new risk to " + ", ".join(v["new_risk"]))
            over = [f"{x_} {y['deviation']:.0%} > {y['tolerance']:.0%}" for x_, y in v["roles"].items() if y["deviation"] > y["tolerance"]]
            if over:
                why.append("outside tolerance: " + ", ".join(over))
            if not v.get("fits", True):
                why.append("over capacity")
            lines.append(f"- **{k}** ({', '.join(i['label'] for i in v['items'])}): {'; '.join(why) or 'scored lower'}.")
    answers = load(os.path.join(session, "answers.yaml"), {}).get("answers", [])
    if answers:
        lines += ["", "## Owner's answers to the roles' questions", ""]
        lines += [f"- **{x['question']}** {x['answer']}" for x in answers]
    dissent = load(os.path.join(session, "dissent.yaml"), {}).get("dissent", [])
    lines += ["", "## Disagreements", ""]
    lines += [f"- **{d['role'].title()}:** {d['argument'].rstrip('.')}. Revisit if: {d['revisit_if'].rstrip('.')}." for d in dissent] or ["- None"]
    out = os.path.join(session, "brief.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(out)


def cmd_record(a):
    """Record the human decision owner's decision. Agents recommend; only this command decides."""
    session = resolve_session(a.session)
    ws = Workspace(a.workspace, session)
    res = latest_result(session)
    chosen = a.option or res.get("recommended")
    if not chosen:
        sys.exit("No recommended option. The decision owner must choose one: --option <id>.")
    if chosen not in res["options"]:
        sys.exit(f"Unknown option {chosen}; scored options: {', '.join(res['options'])}")
    r = res["options"][chosen]
    if chosen == res.get("recommended"):
        status = res.get("status", "consensus")
    else:
        status = "override"
        vetoes = sorted({v for x in r["roles"].values() for v in x.get("vetoes", [])})
        if vetoes:
            sys.exit(f"{chosen} breaks veto red line(s) {', '.join(vetoes)}. An owner override cannot lift a veto; "
                     "resolve it (for example with a legal opinion) and rescore.")
    memory = os.path.join(ws.path, "memory")
    baseline = os.path.join(memory, ".baseline")
    if not os.path.exists(baseline):
        # snapshot memory before the first recorded decision, so `reset --memory` can restore it
        shutil.copytree(memory, baseline, ignore=shutil.ignore_patterns(".baseline"))
    decisions = os.path.join(memory, "decisions")
    os.makedirs(decisions, exist_ok=True)
    nums = [int(os.path.basename(f)[2:6]) for f in glob.glob(os.path.join(decisions, "D-*.md"))]
    did = f"D-{max(nums, default=0) + 1:04d}"
    approval = {"decision": did, "option": chosen, "status": status, "by": a.by,
                "date": dt.date.today().isoformat(), "note": a.note or ""}
    save(os.path.join(session, "approval.yaml"), approval)
    decay = ws.rules.get("concession_decay", 0.7)
    for role, x in r["roles"].items():
        c = ws.concessions.get(role) or {"balance": 0.0, "history": []}
        c["balance"] = round(c["balance"] * decay + x["deviation"], 2)
        c["history"] = (c.get("history") or []) + [{did: x["deviation"]}]
        ws.concessions[role] = c
    save(os.path.join(memory, "concessions.yaml"), ws.concessions)
    for sc in ws.shortcuts["shortcuts"]:
        if sc["id"] in r["fixed"]:
            sc["status"] = f"fixed in {did}"
    for sc in r["created"]:
        ws.shortcuts["shortcuts"].append({**sc, "decided_in": did, "status": "open"})
    save(os.path.join(memory, "shortcuts.yaml"), ws.shortcuts)
    a.session = session
    cmd_brief(a)
    with open(os.path.join(session, "brief.md"), encoding="utf-8") as f:
        body = f.read()
    with open(os.path.join(decisions, f"{did}.md"), "w", encoding="utf-8") as f:
        f.write(body.replace("# Decision brief: ", f"# {did}: ", 1))
    emit(session, {"type": "approval", "option": chosen, "status": status, "by": a.by, "decision": did})
    print(f"{did}: {chosen} ({status}), approved by {a.by}")


def cmd_reset(a):
    ws = Workspace(a.workspace)
    sessions = os.path.join(ws.path, "sessions")
    removed = []
    if os.path.isdir(sessions):
        shutil.rmtree(sessions)
        removed.append("sessions/")
    if os.path.exists(CURRENT):
        with open(CURRENT) as f:
            if f.read().strip().startswith(ws.path):
                os.remove(CURRENT)
                removed.append(".prodoffs/current")
    if a.memory:
        memory = os.path.join(ws.path, "memory")
        baseline = os.path.join(memory, ".baseline")
        if not os.path.isdir(baseline):
            print("memory: nothing recorded since setup, already clean")
        else:
            for name in os.listdir(memory):
                if name == ".baseline":
                    continue
                path = os.path.join(memory, name)
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            for name in os.listdir(baseline):
                src = os.path.join(baseline, name)
                dst = os.path.join(memory, name)
                shutil.copytree(src, dst) if os.path.isdir(src) else shutil.copy2(src, dst)
            shutil.rmtree(baseline)
            removed.append("memory/ restored to the state before the first recorded decision")
    print("Reset: " + (", ".join(removed) if removed else "nothing to remove"))


def cmd_hook(_a):
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    agent = data.get("agent_type", "")
    if not agent.startswith("prodoffs-") or not os.path.exists(CURRENT):
        return
    with open(CURRENT) as f:
        session = f.read().strip()
    role = agent.replace("prodoffs-", "")
    if data.get("hook_event_name") == "SubagentStart":
        emit(session, {"type": "agent", "role": role, "state": "thinking"})
    elif data.get("hook_event_name") == "SubagentStop":
        msg = (data.get("last_assistant_message") or "").strip().splitlines()
        emit(session, {"type": "agent", "role": role, "state": "done", "text": (msg[0] if msg else "")[:90]})


def main():
    ap = argparse.ArgumentParser(prog="prodoffs")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("session"); s.add_argument("action", choices=["new"]); s.add_argument("workspace")
    e = sub.add_parser("emit"); e.add_argument("type"); e.add_argument("pairs", nargs="*"); e.add_argument("--session")
    sc = sub.add_parser("score"); sc.add_argument("workspace"); sc.add_argument("--round", type=int, required=True); sc.add_argument("--session"); sc.add_argument("--dry-run", action="store_true", help="print only, write nothing"); sc.add_argument("--final", action="store_true", help="last round: allow compromise or escalate to the owner")
    b = sub.add_parser("brief"); b.add_argument("workspace"); b.add_argument("--session")
    r = sub.add_parser("record"); r.add_argument("workspace"); r.add_argument("--session")
    r.add_argument("--by", required=True, help="name or role of the human decision owner who approves")
    r.add_argument("--option", help="option the owner chose; default: the recommended one")
    r.add_argument("--note", help="the owner's reason, recorded with the decision")
    tk = sub.add_parser("task"); tk.add_argument("workspace"); tk.add_argument("--session")
    v = sub.add_parser("validate"); v.add_argument("workspace")
    rd = sub.add_parser("radar"); rd.add_argument("workspace"); rd.add_argument("--out")
    st = sub.add_parser("status"); st.add_argument("workspace"); st.add_argument("--session")
    rs = sub.add_parser("reset"); rs.add_argument("workspace"); rs.add_argument("--memory", action="store_true", help="also undo recorded decisions")
    cs = sub.add_parser("case"); cs.add_argument("workspace"); cs.add_argument("--session"); cs.add_argument("--dry-run", action="store_true")
    sub.add_parser("hook")
    a = ap.parse_args()
    {"session": cmd_session_new, "emit": cmd_emit, "status": cmd_status, "validate": cmd_validate, "radar": cmd_radar, "score": cmd_score,
     "brief": cmd_brief, "record": cmd_record, "reset": cmd_reset, "case": cmd_case, "task": cmd_task, "hook": cmd_hook}[a.cmd](a)


if __name__ == "__main__":
    main()
