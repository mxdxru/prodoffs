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
  prodoffs.py score <workspace> --round N [--session DIR] [--dry-run]
  prodoffs.py brief <workspace> [--session DIR]
  prodoffs.py record <workspace> [--session DIR]
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
ROLES = ["ceo", "cpo", "cto", "cmo", "cdo"]


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
        self.mandates = {r: load(p("mandates", f"{r}.yaml")) for r in ROLES}
        self.mandates = {r: m for r, m in self.mandates.items() if m}
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
    return {"effort": effort, "created": created, "fixed": fixed, "items": items, "bets": bets}


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
    year_net, year_value, year_cost = 0.0, 0.0, 0.0
    run_rate = None
    for m in range(1, months + 1):
        y = (m - 1) // 12
        live = m > alt.get("time_to_value_months", 0)
        value = cost = 0.0
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
            vendor_share = _per_year(alt.get("vendor_share", 1.0 if alt.get("fee_per_lookup") else 0.0), y)
            fee = alt.get("fee_per_lookup", 0) * (1 + alt.get("fee_growth_per_year", 0)) ** y
            fees = max(lookups * vendor_share * fee, alt.get("monthly_minimum", 0) if vendor_share > 0 else 0)
            cost = fees + alt.get("run_cost_monthly", 0)
        else:
            cost = alt.get("pre_launch_cost_monthly", 0)
        net = value - cost
        cum += net
        if payback is None and cum >= 0:
            payback = m
        year_net += net; year_value += value; year_cost += cost
        if m % 12 == 0:
            years.append({"value": round(year_value), "cost": round(year_cost), "net": round(year_net)})
            year_net = year_value = year_cost = 0.0
        if m == months:
            run_rate = round(net)
    return {"label": alt.get("label", ""), "one_off": round(one_off), "years": years,
            "total_net": round(cum), "payback_month": payback, "monthly_run_rate_end": run_rate,
            "lookups_per_month": round(lookups)}


def cmd_case(a):
    ws = Workspace(a.workspace)
    own = os.path.join(a.session, "business_case.yaml") if a.session else None
    # a session may carry its own corrected business case (added by the facilitator)
    bc = load(own if own and os.path.exists(own) else os.path.join(ws.path, "business_case.yaml"))
    if not bc:
        sys.exit("No business_case.yaml in workspace")
    cur = bc.get("currency", "EUR")
    res = {k: simulate_case(bc, v) for k, v in bc["alternatives"].items()}
    n = int(bc.get("horizon_years", 3))
    head = "| Alternative | One-off | " + " | ".join(f"Year {i+1} net" for i in range(n)) + f" | {n}-year net | Payback | Monthly net at end |"
    lines = [f"# Business case: {bc.get('question', os.path.basename(ws.path))}", "",
             f"All figures in {cur}, undiscounted, computed by `prodoffs.py case` from `business_case.yaml`.", "",
             head, "|" + "---|" * (n + 5)]
    for k, r in res.items():
        pb = f"month {r['payback_month']}" if r["payback_month"] else f"not within {n} years"
        lines.append(f"| {r['label'] or k} | {r['one_off']:,} | " + " | ".join(f"{y['net']:,}" for y in r["years"]) +
                     f" | **{r['total_net']:,}** | {pb} | {r['monthly_run_rate_end']:,} |")
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
                                       "payback_month": r["payback_month"]} for k, r in res.items()}})
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
        errors.append("no mandates in mandates/")
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


def cmd_score(a):
    session = resolve_session(a.session)
    ws = Workspace(a.workspace, session)
    options = load(os.path.join(session, "options.yaml"), {}).get("options", {})
    options = {k: v for k, v in options.items() if v.get("round") == a.round}
    if not options:
        sys.exit(f"No options for round {a.round} in options.yaml")
    capacity = ws.candidates.get("capacity_team_weeks", 0)
    block_on_risk = ws.rules.get("block_on_strategy_risk", True)

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
            m, s = ws.mandates[role], role_scores[role]
            opening = weighted(m, s["opening"])
            entry = s["options"][oid]
            dev = round(max(0.0, 1 - weighted(m, entry["scores"]) / opening), 2)
            tol = ws.tolerance(role)
            reds = entry.get("red_lines", [])
            roles[role] = {"deviation": dev, "tolerance": tol, "red_lines": reds,
                           "mood": mood_of(dev, tol, reds), "receipt": entry.get("receipt"),
                           "line": entry.get("line", "")}
        fits = info["effort"] <= capacity
        # only risk this option creates blocks acceptance; inherited risk is reported, not blocking
        at_risk = [b for b in info["bets"] if b["new_risk"]]
        within = all(r["deviation"] <= r["tolerance"] and not r["red_lines"] for r in roles.values())
        better_for_all = all(r["deviation"] == 0 for r in roles.values())
        accepted = fits and (better_for_all or within) and not (block_on_risk and at_risk)
        overshoot = max(r["deviation"] - r["tolerance"] for r in roles.values())
        results[oid] = {**info, "roles": roles, "fits": fits, "accepted": accepted,
                        "overshoot": round(overshoot, 2), "capacity": capacity}

    best = sorted(results, key=lambda o: (not results[o]["accepted"], results[o]["overshoot"]))[0]
    if not a.dry_run:
        with open(os.path.join(session, f"result-r{a.round}.json"), "w") as f:
            json.dump({"round": a.round, "best": best, "options": results}, f, indent=2)

    # print a readable table
    print(f"Round {a.round}")
    for oid, r in results.items():
        flag = "ACCEPTED" if r["accepted"] else "not accepted"
        print(f"\n{oid}: {flag}  effort {r['effort']}/{r['capacity']} team-weeks")
        for role, x in r["roles"].items():
            red = f"  red lines: {', '.join(x['red_lines'])}" if x["red_lines"] else ""
            print(f"  {role.upper():4} deviation {x['deviation']:.0%}  tolerance {x['tolerance']:.0%}  {x['mood']}{red}")
        for b in r["bets"]:
            why = f" (blocked by {', '.join(b['because'])})" if b["because"] else ""
            print(f"  bet {b['name']}: {b['status']}{why}")
    print(f"\nFeatured option: {best}")
    if a.dry_run:
        return

    # events for the board: every option in turn, the featured one last, so the room reacts to each
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
        emit(session, {"type": "strategy", "bets": r["bets"]})
        for sc in r["created"]:
            emit(session, {"type": "shortcut", "id": sc["id"], "text": sc["shortcut"], "blocks": sc.get("blocks", [])})
        for role, x in r["roles"].items():
            if x["line"]:
                emit(session, {"type": "say", "role": role, "text": x["line"], "receipt": x["receipt"], "option": oid})
        if oid != best:
            emit(session, {"type": "note", "text": f"{oid}: {'accepted' if r['accepted'] else 'rejected'}"
                                                   f"{', red lines ' + ', '.join(sorted({rl for v in r['roles'].values() for rl in v['red_lines']})) if any(v['red_lines'] for v in r['roles'].values()) else ''}"})
    r = results[best]
    if r["accepted"]:
        emit(session, {"type": "decision", "option": best, "status": "accepted"})


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
    status = "Accepted" if r["accepted"] else "Escalated to the chair: no option passed"
    lines = [f"# Decision brief: {os.path.basename(ws.path)}", "",
             f"**Status:** {status}. **Option:** {best}. **Round:** {res['round']}.", "",
             "## Roadmap", "", "| Initiative | Version |", "|---|---|"]
    lines += [f"| {i['name']} | {i['label']} |" for i in r["items"]]
    lines += ["", f"Capacity: {r['effort']} of {r['capacity']} team-weeks.", "",
              "## Cost per role", "", "| Role | Deviation | Tolerance | Mood |", "|---|---|---|---|"]
    lines += [f"| {k.upper()} | {v['deviation']:.0%} | {v['tolerance']:.0%} | {v['mood']} |"
              for k, v in r["roles"].items()]
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
            lines.append(f"| {role.upper()} | {pos.get('stance', '')} | {pref} | {idea} | {risk} |")
        alts = {}
        for role, pos in positions.items():
            for alt, pc in (pos.get("alternatives") or {}).items():
                a_ = alts.setdefault(alt, {"pros": [], "cons": []})
                a_["pros"] += [f"{p} ({role.upper()})" for p in pc.get("pros", [])]
                a_["cons"] += [f"{c} ({role.upper()})" for c in pc.get("cons", [])]
        if alts:
            lines += ["", "## Pros and cons by alternative", ""]
            for alt, pc in alts.items():
                lines += [f"### {alt}", "", "**Pros**", ""] + [f"- {p}" for p in pc["pros"]] + \
                         ["", "**Cons**", ""] + [f"- {c}" for c in pc["cons"]] + [""]
    plan = load(os.path.join(session, "plan.yaml"), {}).get("plan", [])
    if plan:
        lines += ["", "## Implementation plan", "", "| Step | Owner | Weeks | Done when |", "|---|---|---|---|"]
        lines += [f"| {p['step']} | {p.get('owner', '').upper()} | {p.get('weeks', '')} | {p.get('done_when', '')} |" for p in plan]
        metrics = load(os.path.join(session, "plan.yaml"), {}).get("success_metrics", [])
        if metrics:
            if all(isinstance(m, dict) for m in metrics):
                lines += ["", "**Success metrics**", "", "| Metric | Baseline | Target | Measured by |", "|---|---|---|---|"]
                lines += [f"| {m.get('metric', '')} | {m.get('baseline', '')} | {m.get('target', '')} | {m.get('measured_by', '')} |" for m in metrics]
            else:
                lines += ["", "**Success metrics:** " + "; ".join(str(m) for m in metrics) + "."]
    dissent = load(os.path.join(session, "dissent.yaml"), {}).get("dissent", [])
    lines += ["", "## Disagreements", ""]
    lines += [f"- **{d['role'].upper()}:** {d['argument'].rstrip('.')}. Revisit if: {d['revisit_if'].rstrip('.')}." for d in dissent] or ["- None"]
    out = os.path.join(session, "brief.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(out)


def cmd_record(a):
    session = resolve_session(a.session)
    ws = Workspace(a.workspace, session)
    res = latest_result(session)
    r = res["options"][res["best"]]
    if not r["accepted"]:
        sys.exit("Latest option is not accepted. Nothing to record.")
    memory = os.path.join(ws.path, "memory")
    baseline = os.path.join(memory, ".baseline")
    if not os.path.exists(baseline):
        # snapshot memory before the first recorded decision, so `reset --memory` can restore it
        shutil.copytree(memory, baseline, ignore=shutil.ignore_patterns(".baseline"))
    decisions = os.path.join(ws.path, "memory", "decisions")
    os.makedirs(decisions, exist_ok=True)
    nums = [int(os.path.basename(f)[2:6]) for f in glob.glob(os.path.join(decisions, "D-*.md"))]
    n = max(nums, default=0) + 1
    did = f"D-{n:04d}"
    decay = ws.rules.get("concession_decay", 0.7)
    for role, x in r["roles"].items():
        c = ws.concessions.get(role) or {"balance": 0.0, "history": []}
        c["balance"] = round(c["balance"] * decay + x["deviation"], 2)
        c["history"] = (c.get("history") or []) + [{did: x["deviation"]}]
        ws.concessions[role] = c
    save(os.path.join(ws.path, "memory", "concessions.yaml"), ws.concessions)
    for s in ws.shortcuts["shortcuts"]:
        if s["id"] in r["fixed"]:
            s["status"] = f"fixed in {did}"
    for s in r["created"]:
        ws.shortcuts["shortcuts"].append({**s, "decided_in": did, "status": "open"})
    save(os.path.join(ws.path, "memory", "shortcuts.yaml"), ws.shortcuts)
    brief = os.path.join(session, "brief.md")
    if os.path.exists(brief):
        with open(brief, encoding="utf-8") as f:
            body = f.read()
        with open(os.path.join(decisions, f"{did}.md"), "w", encoding="utf-8") as f:
            f.write(body.replace("# Decision brief", f"# {did}", 1))
    emit(session, {"type": "note", "text": f"Recorded as {did}; ledger updated"})
    print(did)


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
    sc = sub.add_parser("score"); sc.add_argument("workspace"); sc.add_argument("--round", type=int, required=True); sc.add_argument("--session"); sc.add_argument("--dry-run", action="store_true", help="print only, write nothing")
    b = sub.add_parser("brief"); b.add_argument("workspace"); b.add_argument("--session")
    r = sub.add_parser("record"); r.add_argument("workspace"); r.add_argument("--session")
    v = sub.add_parser("validate"); v.add_argument("workspace")
    rd = sub.add_parser("radar"); rd.add_argument("workspace"); rd.add_argument("--out")
    st = sub.add_parser("status"); st.add_argument("workspace"); st.add_argument("--session")
    rs = sub.add_parser("reset"); rs.add_argument("workspace"); rs.add_argument("--memory", action="store_true", help="also undo recorded decisions")
    cs = sub.add_parser("case"); cs.add_argument("workspace"); cs.add_argument("--session"); cs.add_argument("--dry-run", action="store_true")
    sub.add_parser("hook")
    a = ap.parse_args()
    {"session": cmd_session_new, "emit": cmd_emit, "status": cmd_status, "validate": cmd_validate, "radar": cmd_radar, "score": cmd_score,
     "brief": cmd_brief, "record": cmd_record, "reset": cmd_reset, "case": cmd_case, "hook": cmd_hook}[a.cmd](a)


if __name__ == "__main__":
    main()
