# Orient AC Remote — IR Capture Toolkit

A small, honest toolkit for turning your Redmi phone + the
[IR Blaster Remote](https://github.com/iodn/android-ir-blaster) app into a
working remote for your **Orient** air conditioner.

## Why there are no "codes" in this repo by default

Air conditioner IR signals are long, brand/model-specific timing patterns.
There is no reliable public database of verified Orient AC codes, and
guessing them doesn't work — an AC either receives its exact signal or does
nothing. So instead of fake codes, this repo gives you the actual tool to
capture the *real* signal from your own remote, once, cheaply.

## What's in here

| Path | What it does |
|---|---|
| `capture/OrientIRCapture.ino` | Arduino/ESP8266 sketch — captures raw IR timing from your physical Orient remote and prints it ready to paste into the app. |
| `scripts/parse_capture.py` | Organizes everything you capture into one clean `codes/orient_ac_codes.json`. |
| `codes/orient_ac_codes.json` | Your permanent record of every captured button. Starts empty. |
| `docs/index.html` + `docs/style.css` | A little dashboard that shows which buttons you've captured, with one-click copy for pasting into the app. |

## Full workflow

### 1. Get the hardware (~$3-5, one-time)
- Any ESP8266 board (NodeMCU / Wemos D1 Mini) or an Arduino Uno/Nano
- One IR receiver module: **TSOP1738** or **VS1838B** (38kHz) — cheap, sold at
  any electronics shop or online
- 3 jumper wires

### 2. Wire it up
See the wiring diagram in the comments at the top of
`capture/OrientIRCapture.ino`.

### 3. Capture each button
1. Install the **IRremoteESP8266** library in the Arduino IDE (Tools ▸
   Manage Libraries ▸ search "IRremoteESP8266" ▸ Install).
2. Upload `OrientIRCapture.ino`.
3. Open Serial Monitor at 115200 baud.
4. Point your real Orient remote at the receiver (~10-20cm), press one
   button, and copy the printed pattern.
5. Paste it straight into the app: **IR Blaster Remote → Remotes → your
   remote → Add Button → Raw Signal**, frequency `38000`. Test it against
   the actual AC.
6. Optionally, also paste it into a local text file (`capture_log.txt`)
   under a `### ButtonName` heading, for every button, e.g.:

   ```
   ### Power
   9024,4494,644,1614,644,1614,...

   ### Temp+
   9024,4480,650,1610,...
   ```

### 4. Keep a permanent record (optional but recommended)
```bash
python scripts/parse_capture.py capture_log.txt
```
This merges your captures into `codes/orient_ac_codes.json` (and syncs a
copy into `docs/` for the dashboard) — so if you ever wipe the app or get a
new phone, you're not starting over.

### 5. View your progress
Open `docs/index.html` in a browser (or run a quick local server:
`python -m http.server` from the repo root, then visit
`http://localhost:8000/docs/`) to see which buttons are captured and
one-click copy any of them.

If you publish this repo with **GitHub Pages set to serve from `/docs`**,
the dashboard works there too — `orient_ac_codes.json` is kept in sync
inside `docs/` automatically by the parser script.

## If you don't want to buy hardware first

Try these two things already built into the IR Blaster Remote app before
buying anything:
- **Settings ▸ GitHub Store** — browse a community IR database (e.g.
  `UberGuidoZ/Flipper-IRDB`) directly inside the app and check the
  `Air_Conditioners` folder for an Orient entry.
- **Signal Tester (IR Finder)** tab — a built-in bruteforcer that cycles
  through protocol/code combinations and stops when your AC reacts. Works
  best for simple, short (NEC/Sony-style) signals rather than full-state AC
  codes, but it's free to try first.

If neither works, the capture route above is the guaranteed path.
