"""Robot-vacuum excuse printer for the make.fun bounty.

One fixed excuse line lives in this file. The program checks that line
against the competition gate and then drops it, byte for byte, into
/output/entry.txt. There is no network access, no randomness, and no
input beyond the constant below, so every run produces the same file.
"""

import os
import sys

MAX_CHARS = 120

TEXT = "I skipped that corner. The dust bunnies unionized, and I don't cross picket lines."

OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.txt")
ENCODING = "utf-8"


def _problems(text):
    """Yield (exception class, message) for each gate rule the text breaks.

    A non-string yields a TypeError first and stops the generator; every
    other broken rule yields a ValueError. An empty generator means the
    text satisfies the gate.
    """
    if not isinstance(text, str):
        yield TypeError, "entry text must be str"
        return
    checks = (
        (not text.strip(),
         "entry text must not be empty or whitespace-only"),
        (len(text) > MAX_CHARS,
         "entry text exceeds %d characters" % MAX_CHARS),
        (("\n" in text) or ("\r" in text),
         "entry text must be a single line"),
        (any(ord(ch) < 32 or ord(ch) == 127 for ch in text),
         "entry text must not contain control characters"),
    )
    for broken, message in checks:
        if broken:
            yield ValueError, message


def validate_entry_text(text):
    """Return text unchanged when it passes the gate, otherwise raise."""
    for exc_type, message in _problems(text):
        raise exc_type(message)
    return text


def _write(path, text):
    with open(path, "w", encoding=ENCODING, newline="") as handle:
        handle.write(text)


def main(argv=None):
    text = validate_entry_text(TEXT)
    os.makedirs(OUT_DIR, exist_ok=True)
    _write(OUT_PATH, text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
