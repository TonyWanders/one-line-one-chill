#!/usr/bin/env python3
"""Write one line of horror to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The line is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 200 characters, not only white space.
"""

import os
import sys
from pathlib import Path

LINE = "The photo booth printed four pictures of me alone in the booth, and in the last one someone else is holding my hand."

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"line is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("line is only white space")
    return chars


def write_entry(path, text):
    """Write the line to path, creating parent directories as needed.

    Returns the character count written. Raises OSError when the file
    cannot be written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return len(text)


def main() -> int:
    try:
        chars = validate(LINE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    try:
        written = write_entry(path, LINE)
    except OSError as exc:
        print(f"cannot write {path}: {exc}", file=sys.stderr)
        return 1
    if written != chars:
        print(f"wrote {written} characters, expected {chars}", file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
