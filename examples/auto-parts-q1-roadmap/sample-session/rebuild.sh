#!/usr/bin/env bash
# Rebuilds events.jsonl and brief.md for the sample session from the files in this folder.
# Run from anywhere:  bash examples/auto-parts-q1-roadmap/sample-session/rebuild.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WS="$(dirname "$HERE")"
ROOT="$(cd "$WS/../.." && pwd)"
P="python3 $ROOT/scripts/prodoffs.py"
E="$P emit --session $HERE"
: > "$HERE/events.jsonl"

$E cast workspace=auto-parts-q1-roadmap
$E phase phase=intake round=0
$E note text="Loaded strategy, 5 candidates, open shortcut S-014, concession balances"
$P status "$WS" --session "$HERE" > /dev/null
$E phase phase=sealed round=1
for r in ceo cpo cto cmo cdo; do $E agent role=$r state=thinking; done
for r in ceo cpo cto cmo cdo; do $E agent role=$r state=done text="Position sealed"; done
$E phase phase=reveal round=1
$E say role=ceo text="B2B revenue in Q1, please"
$E say role=cpo text="Payments and onboarding first"
$E say role=cto text="Pricing engine, or no new markets"
$E say role=cmo text="Competitor cashback is live"
$E say role=cdo text="Fitment must be a shared service"
$E phase phase=cross_exam round=1
$E say role=cto text="Quick payments hardwire the provider"
$E say role=cdo text="Loyalty needs tiered pricing first"
$E phase phase=synthesis round=1
$E say role=facilitator text="Two hybrids: H1 revenue-first, H2 balanced"
$E phase phase=scoring round=2
$P score "$WS" --round 2 --session "$HERE"
$E note text="CTO tolerance tightened to 12% after D-0012 and D-0015"
$E phase phase=converge round=3
$E say role=facilitator text="H2b: put payments behind a layer. CPO pays 3 weeks."
$P score "$WS" --round 3 --session "$HERE"
$P brief "$WS" --session "$HERE"
