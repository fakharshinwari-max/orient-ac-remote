/*
  Orient AC — IR Signal Capture Tool
  ==================================
  Captures RAW IR timing straight from your physical Orient AC remote,
  and prints it in a format ready to paste into the "IR Blaster Remote"
  Android app (Remotes > Add Button > Raw Signal).

  WHY THIS EXISTS:
  Air conditioner remotes use long, brand/model-specific signals that
  can't be "known" in advance — they must be captured from the real
  remote once. This sketch does that capture for you.

  HARDWARE NEEDED (~$3-5 total):
    - Any ESP8266 board (NodeMCU / Wemos D1 Mini) OR Arduino Uno/Nano
    - 1x IR receiver module: TSOP1738 or VS1838B (38kHz) — a 3-pin
      black component, sold at any electronics shop in Peshawar/online.
    - 3 jumper wires, breadboard optional.

  WIRING:
    ESP8266 (NodeMCU/D1 Mini):
      IR receiver OUT -> D2 (GPIO4)
      IR receiver VCC -> 3V3
      IR receiver GND -> GND

    Arduino Uno/Nano:
      IR receiver OUT -> Digital Pin 2
      IR receiver VCC -> 5V
      IR receiver GND -> GND

  LIBRARY NEEDED (Arduino IDE):
    Tools > Manage Libraries > search "IRremoteESP8266" > Install
    (library by crankyoldgit)

  HOW TO USE:
    1. Wire it up, upload this sketch.
    2. Open Serial Monitor, set baud rate to 115200.
    3. Hold your REAL Orient remote ~10-20cm from the receiver, pointed
       straight at it.
    4. Press ONE button (start with Power).
    5. Copy the "RAW PATTERN" line that gets printed.
    6. In IR Blaster Remote app: Remotes > your remote > Add Button >
       Raw Signal > paste the pattern, set Frequency to 38000 > Save.
    7. Test it — point your phone at the AC and tap the button.
    8. Repeat steps 3-7 for every button you need
       (Power, Temp+, Temp-, Mode, Fan, Swing, Timer...).

  TIP: If nothing prints when you press a button, move the remote
  closer (5-10cm) and make sure it's a fresh battery — weak IR LEDs
  are the #1 cause of failed captures.
*/

#include <Arduino.h>
#include <IRrecv.h>
#include <IRutils.h>

// ---- Config ----
const uint16_t kRecvPin = 4;               // GPIO4 = D2 on NodeMCU/Wemos. Use 2 for Arduino Uno/Nano.
const uint16_t kCaptureBufferSize = 1024;  // AC remotes send long signals — need a big buffer
const uint8_t  kTimeoutMs = 15;            // 15ms of silence = "signal finished" (ACs need a higher timeout than TVs)
const uint32_t kFrequencyHz = 38000;       // Standard IR carrier frequency for the vast majority of remotes

IRrecv irrecv(kRecvPin, kCaptureBufferSize, kTimeoutMs, true);
decode_results results;

unsigned long captureCount = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  irrecv.setUnknownThreshold(12);
  irrecv.enableIRIn();

  Serial.println();
  Serial.println("======================================================");
  Serial.println(" Orient AC IR Capture — Ready");
  Serial.println(" Point the real remote at the receiver and press a button.");
  Serial.println("======================================================");
}

void loop() {
  if (irrecv.decode(&results)) {
    captureCount++;

    Serial.println();
    Serial.println("------------------------------------------------------");
    Serial.print("Capture #");
    Serial.println(captureCount);

    Serial.print("Detected protocol: ");
    Serial.println(typeToString(results.decode_type, results.repeat));
    // Most AC remotes will show as "UNKNOWN" here — that's completely
    // normal and expected. The raw pattern below is what you actually need.

    Serial.print("Total pulses captured: ");
    Serial.println(results.rawlen - 1);

    Serial.println("RAW PATTERN (copy the line below into the app):");
    Serial.print(">>> ");
    for (uint16_t i = 1; i < results.rawlen; i++) {
      uint32_t usecs = results.rawbuf[i] * kRawTick;
      Serial.print(usecs);
      if (i < results.rawlen - 1) Serial.print(",");
    }
    Serial.println(" <<<");

    Serial.print("Frequency to enter in the app: ");
    Serial.println(kFrequencyHz);

    Serial.println("------------------------------------------------------");
    Serial.println("Label this button in your notes, then press the NEXT button.");

    irrecv.resume();
  }
}
