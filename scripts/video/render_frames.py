#!/usr/bin/env python3
"""Render the demo video from a recorded session.

Requires: pip install playwright pyyaml && playwright install chromium, and ffmpeg.
Run from the repository root while a local server is running:

    python3 -m http.server 8765 &
    python3 scripts/video/render_frames.py examples/vin-buy-vs-build/sample-session/events.jsonl
    # writes build/video/prodoffs-demo.mp4 and .gif

Each event of the session becomes one still, held for a duration that depends on the event type.
"""
import json
import os
import subprocess
import sys
import urllib.parse

from playwright.sync_api import sync_playwright

EV = sys.argv[1] if len(sys.argv) > 1 else "examples/vin-buy-vs-build/sample-session/events.jsonl"
OUT = "build/video"
CARD = "file://" + os.path.abspath("scripts/video/card.html")
INTRO = ("<h1>Prodoffs</h1><p>Five AI executives negotiate one decision:<br><b>buy or build vehicle identification by VIN</b></p>"
         "<p class='s'>Fictional auto parts retailer. A real agent run, replayed from its event log.</p>")
OUTRO = ("<h1>Accepted: H3</h1><p>Own vehicle-ID layer, vendor behind it,<br>VIN live before the spring season, decoding decided in month 9.</p>"
         "<p class='s'>The agents found the flaw in the business case themselves.</p><p class='u'>github.com/mxdxru/prodoffs</p>")


def dur(e):
    t = e["type"]
    if t == "phase":
        return 2.6 if e["phase"] != "intake" else 1.0
    if t == "case":
        return 3.0
    if t == "note":
        return 3.6 if any(k in e["text"] for k in ["flaw", "Unanimous", "rejected"]) else 2.2
    if t == "say":
        return 2.2 if e["role"] == "facilitator" else (1.5 if "option" not in e else 0.9)
    if t in ("scores", "shortcut"):
        return 0.6
    if t == "decision":
        return 4.5
    if t == "agent":
        return 0.25
    return 0.15


def main():
    evs = [json.loads(l) for l in open(EV, encoding="utf-8")]
    os.makedirs(f"{OUT}/frames", exist_ok=True)
    frames = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1.2)
        pg.goto(CARD + "?h=" + urllib.parse.quote(INTRO)); pg.wait_for_timeout(300)
        f = f"{OUT}/frames/000_intro.jpg"; pg.screenshot(path=f, type="jpeg", quality=92); frames.append((f, 4.5))
        pg.goto(f"http://localhost:8765/board/?layout=wide&upto=0&events=/{EV}"); pg.wait_for_timeout(900)
        for i, e in enumerate(evs, 1):
            pg.evaluate(f"()=>{{reset();EVS.slice(0,{i}).forEach(apply);render();}}")
            f = f"{OUT}/frames/{i:03d}.jpg"; pg.screenshot(path=f, type="jpeg", quality=92); frames.append((f, dur(e)))
        frames.append((frames[-1][0], 2.0))
        pg.goto(CARD + "?h=" + urllib.parse.quote(OUTRO)); pg.wait_for_timeout(300)
        f = f"{OUT}/frames/999_outro.jpg"; pg.screenshot(path=f, type="jpeg", quality=92); frames.append((f, 5.5))
        b.close()
    with open(f"{OUT}/list.txt", "w") as fh:
        for fr, d in frames:
            fh.write(f"file '{os.path.abspath(fr)}'\nduration {d}\n")
        fh.write(f"file '{os.path.abspath(frames[-1][0])}'\n")
    total = sum(d for _, d in frames)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{OUT}/list.txt",
                    "-vf", f"fps=30,format=yuv420p,fade=t=in:st=0:d=0.6,fade=t=out:st={total - 0.8}:d=0.8",
                    "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", f"{OUT}/demo.tmp.mp4"], check=True)
    os.replace(f"{OUT}/demo.tmp.mp4", f"{OUT}/prodoffs-demo.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/prodoffs-demo.mp4", "-vf",
                    "fps=6,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=4",
                    f"{OUT}/prodoffs-demo.gif"], check=True)
    print(f"{OUT}/prodoffs-demo.mp4  ({total:.0f} s)")


if __name__ == "__main__":
    main()
