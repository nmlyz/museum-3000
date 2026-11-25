#!/usr/bin/env python3
"""museum-3000: write one museum label from the year 3000 to /output/entry.txt.

The label sits beside an ordinary object from today, a hotel key card,
and reads it the way a curator a thousand years on would: a card that
opened one door, once, then forgot everything it knew. The joke is the
misreading itself — the card really does stop working, usually on the
last day — so the label stays deadpan and never explains it.

Standard library only, no network. Deterministic: the same bytes on every run.
"""

import os
import sys

LINE = ("Hotel key card, c. 2025. "
        "A card that opened one door, once, then forgot everything it knew.")

MIN_LEN = 1
MAX_LEN = 200


def problems(text: str) -> list:
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        found.append(f"entry is {len(text)} characters, must be {MIN_LEN}-{MAX_LEN}")
    stripped = text.strip()
    if not stripped:
        found.append("entry must not be only white space")
    if text != stripped:
        found.append("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    return found


def main() -> int:
    found = problems(LINE)
    if found:
        for problem in found:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    try:
        os.chmod(out_dir, 0o755)
    except OSError:
        pass
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    os.chmod(path, 0o644)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != LINE:
        print("error: entry.txt does not match the label", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
