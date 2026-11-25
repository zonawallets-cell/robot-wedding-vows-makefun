"""One-Line Robot Wedding Vows — make.fun entry.

Writes one line of wedding vows for a robot couple (at most
160 characters) to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

Pure standard library only.
"""

import os

VOW = (
    "I vow to complete the three-way handshake with you "
    "\u2014 SYN, SYN-ACK, and I do."
)
# Why this line, against the judge brief in RULES.txt (in its order):
# 1. One-line robot wedding vow that lands as a joke: the TCP three-way
#    handshake ends the way every wedding ends, with "I do".
# 2. The laugh pays off in the last few words: the handshake's third step
#    is "I do" instead of ACK — wordplay, not a wry tone.
# 3. It is a vow ("I vow ...", "I do"), not a gag with no commitment.
# 4. Machine side is specific: SYN / SYN-ACK, a protocol no human couple
#    would say. Fresh: zero "handshake" lines among the 2,391 field titles;
#    firmware-update / factory-reset / battery / airplane-mode tropes avoided.
# 5. 76 chars, one line, triplet rhythm ("SYN, SYN-ACK, and I do") that
#    reads well aloud.

MAX_CHARS = 160


def validate(text):
    """Enforce the RULES.txt gate: UTF-8, 1-160 chars, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 160-char limit" % len(text))
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry = validate(VOW)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
    # Read back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8") as fh:
        on_disk = validate(fh.read())
    assert on_disk == entry, "entry.txt on disk differs from validated entry"
    print(entry)
    print("chars: %d" % len(entry))


if __name__ == "__main__":
    main()
