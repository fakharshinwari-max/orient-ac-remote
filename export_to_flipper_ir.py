#!/usr/bin/env python3
"""
export_to_flipper_ir.py
========================
Converts everything in codes/orient_ac_codes.json into ONE Flipper Zero
".ir" file — a plain-text format that IR Blaster Remote can import
directly (Remotes > Import > Flipper Zero .ir file), instead of you
pasting each button in one at a time.

This does not invent any codes — it only reformats whatever you already
captured with OrientIRCapture.ino + parse_capture.py.

USAGE:
    python export_to_flipper_ir.py

Reads:  codes/orient_ac_codes.json
Writes: codes/OrientAC.ir
"""

import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_PATH = SCRIPT_DIR.parent / "codes" / "orient_ac_codes.json"
OUTPUT_PATH = SCRIPT_DIR.parent / "codes" / "OrientAC.ir"

DEFAULT_DUTY_CYCLE = 0.330000  # Standard for 38kHz IR — matches Flipper's own captures


def build_ir_file(codes: dict) -> str:
    lines = ["Filetype: IR signals file", "Version: 1"]

    for name, entry in codes.items():
        pattern = entry["pattern"]
        frequency = entry.get("frequency", 38000)

        lines.append("#")
        lines.append(f"name: {name}")
        lines.append("type: raw")
        lines.append(f"frequency: {frequency}")
        lines.append(f"duty_cycle: {DEFAULT_DUTY_CYCLE:.6f}")
        lines.append("data: " + " ".join(str(v) for v in pattern))

    return "\n".join(lines) + "\n"


def main():
    if not INPUT_PATH.exists():
        print(f"No codes file found at {INPUT_PATH} — capture some buttons first.")
        return

    codes = json.loads(INPUT_PATH.read_text(encoding="utf-8"))

    if not codes:
        print("orient_ac_codes.json is empty — nothing to export yet.")
        print("Capture at least one button first (see README.md).")
        return

    ir_content = build_ir_file(codes)
    OUTPUT_PATH.write_text(ir_content, encoding="utf-8")

    print(f"Exported {len(codes)} button(s) to {OUTPUT_PATH}")
    for name in codes:
        print(f"  - {name}")
    print()
    print("Next step: transfer OrientAC.ir to your phone, then in")
    print("IR Blaster Remote: Remotes > Import > Flipper Zero (.ir) file")
    print("> select OrientAC.ir — all your buttons load in one go.")


if __name__ == "__main__":
    main()
