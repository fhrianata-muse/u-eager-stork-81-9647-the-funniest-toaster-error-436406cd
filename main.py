#!/usr/bin/env python3
"""Write the toaster error line to /output/entry.txt.

The line is kept as data. At run time it is checked against the
competition gate (1-120 characters, one line, not only whitespace,
no trailing space) and only then written, with no trailing newline,
so two runs write byte-identical output.
"""

import os
import sys

LINE = "ERROR E07: You pushed the lever without asking. I am filing this under 'rude'."


def main() -> int:
    text = LINE
    if not 1 <= len(text) <= 120:
        print(f"gate fail: length {len(text)} not in 1..120", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("gate fail: entry must be a single line", file=sys.stderr)
        return 1
    if text != text.strip() or not text.strip():
        print("gate fail: leading/trailing space or blank", file=sys.stderr)
        return 1
    if text[-1] not in ".!?":
        print("gate fail: entry must end with terminal punctuation", file=sys.stderr)
        return 1
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(path, "rb") as f:
        written = f.read()
    if written.decode("utf-8") != text:
        print("gate fail: written bytes differ from entry", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
