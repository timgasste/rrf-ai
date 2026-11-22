#!/usr/bin/env python3
"""Check that the prompts on the page equal the course's prompt file, word for word.

Usage: scripts/check-prompts.py <prompts.md> index.qmd

The source file holds the prompts as ```text blocks (A, A2, B, C) and the
workflow-description sentence as a block quote under its heading. The page
holds each of them once as a ```{.markdown .prompt} block, in the order of the
workflows, which need not be the order of the source. Each source prompt must
appear on the page exactly (lines compared apart from trailing spaces), and the
page must hold no other prompt. Exits 1 on any difference.
"""
import difflib
import re
import sys


def source_prompts(text):
    prompts = re.findall(r"^```text\n(.*?)\n```", text, re.S | re.M)
    m = re.search(r"^## The sentence for your workflow description\n(.*)", text, re.S | re.M)
    if m:
        quote = [l[2:] if l.startswith("> ") else l[1:] for l in m.group(1).splitlines() if l.startswith(">")]
        if quote:
            prompts.append("\n".join(quote))
    return prompts


def page_prompts(text):
    return re.findall(r"^```\{\.markdown \.prompt\}\n(.*?)\n```", text, re.S | re.M)


def clean(block):
    return [line.rstrip() for line in block.strip("\n").splitlines()]


def main():
    src, page = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
    want, have = [clean(b) for b in source_prompts(src)], [clean(b) for b in page_prompts(page)]
    bad = 0
    if len(want) != len(have):
        print(f"Different number of prompts: {len(want)} in {sys.argv[1]}, {len(have)} on the page")
        bad = 1
    unmatched = list(range(len(have)))
    for i, w in enumerate(want, 1):
        hit = next((k for k in unmatched if have[k] == w), None)
        if hit is not None:
            unmatched.remove(hit)
            continue
        bad = 1
        # Show the diff against the page block that shares the most lines.
        near = max(unmatched or range(len(have)), key=lambda k: len(set(have[k]) & set(w)), default=None)
        print(f"Prompt {i} of {sys.argv[1]} ({w[0][:50]}...) is not on the page word for word:")
        if near is not None:
            sys.stdout.writelines(difflib.unified_diff(
                [l + "\n" for l in w], [l + "\n" for l in have[near]], "prompts.md", "index.qmd"))
    for k in unmatched:
        if have[k] not in want:
            bad = 1
            print(f"Page prompt {k + 1} ({have[k][0][:50]}...) is not in {sys.argv[1]}")
    if bad:
        print("Prompts do not match: copy them into index.qmd from prompts.md")
    else:
        print(f"{len(have)}/{len(want)} prompts match prompts.md word for word")
    sys.exit(bad)


if __name__ == "__main__":
    main()
