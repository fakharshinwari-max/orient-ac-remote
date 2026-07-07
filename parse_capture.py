#!/usr/bin/env python3
"""
parse_capture.py
================
Organizes the raw IR patterns you captured with OrientIRCapture.ino into
one clean codes/orient_ac_codes.json file, so you have a permanent, tidy
record of every button on your GitHub repo (and a source the docs/index.html
reference page can read).

This does NOT invent or guess any codes — it only reorganizes patterns
YOU captured from your real remote using the Arduino sketch.

--------------------------------------------------------------------------
HOW TO PREPARE YOUR INPUT FILE
--------------------------------------------------------------------------
While capturing, after each button, write a "### ButtonName" line, then
paste the raw pattern line under it (without the ">>> " / " <<<" markers).

Example capture_log.txt:

    ### Power
    9024,4494,644,1614,644,1614,644,540,...

    ### Temp+
    9024,4480,650,1610,...

    ### Mode
    9024,4490,...

Save that file, then run:

    python parse_capture.py capture_log.txt

It will create/update codes/orient_ac_codes.json next to this script.
--------------------------------------------------------------------------
"""

import sys
import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR.parent / "codes" / "orient_ac_codes.json"
DOCS_COPY_PATH = SCRIPT_DIR.parent / "docs" / "orient_ac_codes.json"
DEFAULT_FREQUENCY_HZ = 38000


def parse_capture_log(text: str) -> dict:
    """Parse a capture_log.txt into {button_name: {pattern, frequency}}"""
    entries = {}
    current_name = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        header_match = re.match(r"^#{1,3}\s*(.+)$", line)
        if header_match:
            current_name = header_match.group(1).strip()
            continue

        # Strip any leftover Serial Monitor markers if pasted verbatim
        cleaned = line.replace(">>>", "").replace("<<<", "").strip()
        cleaned = cleaned.rstrip(",")

        # A pattern line looks like: 9024,4494,644,1614,...
        if current_name and re.match(r"^-?\d+(,\s*-?\d+)+$", cleaned):
            pattern = [int(v.strip()) for v in cleaned.split(",")]
            entries[current_name] = {
                "pattern": pattern,
                "frequency": DEFAULT_FREQUENCY_HZ,
                "pulse_count": len(pattern),
            }
            current_name = None  # require a fresh header before next pattern

    return entries


def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_capture.py <capture_log.txt>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8", errors="ignore")
    new_entries = parse_capture_log(text)

    if not new_entries:
        print("No button patterns were found. Check the format described")
        print("in the docstring at the top of this script.")
        sys.exit(1)

    # Merge with anything already saved, so re-running never loses buttons
    existing = {}
    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))

    existing.update(new_entries)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(existing, indent=2), encoding="utf-8")

    # Keep docs/ in sync too, so the reference page (docs/index.html) —
    # whether opened locally or served via GitHub Pages from /docs —
    # always has the latest codes without a manual copy step.
    DOCS_COPY_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOCS_COPY_PATH.write_text(json.dumps(existing, indent=2), encoding="utf-8")

    print(f"Saved {len(new_entries)} button(s) to {OUTPUT_PATH}")
    print(f"Synced a copy to {DOCS_COPY_PATH} for the reference page")
    for name in new_entries:
        print(f"  - {name} ({new_entries[name]['pulse_count']} pulses)")


if __name__ == "__main__":
    main()
