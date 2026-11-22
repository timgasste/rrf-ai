#!/usr/bin/env python3
"""Check that every prompt shown on the slides also appears, word for word, on the page.

Usage: scripts/check-sync.py ../presentations/presentation.qmd index.qmd

A slide prompt is a mini-chat box with at least one [bracket] field to fill in.
Boxes without one show a captured answer, not a prompt, and are skipped. The
slides often show an excerpt, cut with "…", so each piece between the cuts
(three words or more) must appear on the page.
"""
import html, re, sys

deck, page = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
norm = lambda t: " ".join(html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<br\s*/?>|</p>|\n", " ", t))).split())
boxes = re.findall(r'<div class="mini-chat-text">(.*?)</div>', deck, re.S)
# The anatomy slide splits one prompt into numbered segments: each is its own excerpt.
boxes = [re.sub(r'<span class="seg seg--\d+">', " … ", re.sub(r'<span class="seg-num">.*?</span>', "", b)) for b in boxes]
prompts = [norm(b) for b in boxes if "[" in norm(b)]
page_text = norm(page)
missing = 0
for p in prompts:
    pieces = [x.strip(" .") for x in p.split("…")]
    gone = [x for x in pieces if len(x.split()) >= 3 and x not in page_text]
    for x in gone:
        print("MISSING on page:", x[:110], "...")
    missing += bool(gone)
print(f"{len(prompts) - missing}/{len(prompts)} slide prompts found on the page")
sys.exit(1 if missing else 0)
