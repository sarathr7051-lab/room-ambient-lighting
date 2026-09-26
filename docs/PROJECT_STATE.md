# Project state

**Read this first.** Every other document describes the whole build from the
beginning; this one says where the build actually is. Update it whenever a step
completes.

Last updated: **26 Sep 2026, evening** - bench test passed

---

## Now

**Bench test PASSED, 26 Sep evening.** The desk node drives a WS2812 strip
correctly through the diode clamp. Measured on the 1 m strip at ABL 600 mA:
LED 1 steady and correct colour, junction 0.79 V low, rail 4.71 V under load
(5.03 V open-circuit), colour order GRB confirmed, live colour changes over
Wi-Fi.

**Tomorrow, 27 Sep, in order:**

1. Solder three wires onto the **2 m strip's bare `Din` pads** - red +5V,
   green Din, white GND. First joint of the build; they stay on for good.
2. Test it at 120 LEDs. The node is already configured for 120 with six
   20-LED colour bands (RED, GREEN, BLUE, WHITE, YELLOW, PINK); last colour
   PINK and complete means all 120 are good.
3. Cut the 2 m strip from its `Din` end: **18 (left) -> 34 (top) -> 18
   (right)**. 70 used, 50 spare. The 1 m strip stays whole as practice
   material and bench tester.
4. Solder the two corner joints; test the assembled U flat on the bench.
5. Mount; `apply` / `walk` / `presets`.
6. Hyperion.

**Read the pad text on every fresh cut** - each piece has a `Din` end and a
`DO` end and the 3-pin connectors look identical.

---

## Done

| | What | Detail |
|---|---|---|
| ✅ | Repo created | public, `sarathr7051-lab/room-ambient-lighting` |
| ✅ | **WLED flashed** | 16.0.1, via install.wled.me. **Do not flash again.** |
| ✅ | USB cable sorted | a spare Fire TV Stick micro-USB lead turned out to be data-capable; nothing bought. Board enumerates as `Silicon Labs CP210x`, COM12 |
| ✅ | Node on Wi-Fi | `192.168.1.6`, 2.4 GHz channel 4, **100% signal** |
| ✅ | Node named | `wled-desk`; `wled-desk.local` resolves |
| ✅ | Tooling verified | `wled_push.py` tested against the live node; four bugs found and fixed |
| ✅ | Monitor measured | strip path **57 × 30.5 cm** |
| ✅ | **Adapter measured** | 5 V 3 A brick reads **5.03 V** open-circuit, red wire = **+**. Well regulated; most cheap bricks sit 5.1-5.4 |
| ✅ | Strip ends | already wired, 3-pin connector both ends. No soldering needed for bench bring-up |
| ✅ | **Bench test** | passed 26 Sep evening on the 1 m strip: clamp working, LED 1 steady, GRB confirmed, rail 4.71 V loaded |
| ✅ | Chip test | CD74HCT112EX behaves as HC, not HCT - eliminated by measurement |
| ✅ | Layout generated | **70 LEDs** = 18 left / 34 top / 18 right; `config/*.json` committed |

### Things that are settled, so don't reopen them

- **No DHCP reservation.** The Airtel AirFiber admin page is not accessible to
  the user. mDNS (`wled-desk.local`) removes the need — Hyperion discovers WLED
  by name.
- **No 2.4 GHz problem.** The node is on channel 4 at full signal. Earlier
  worry about band steering and channels 12/13 was unfounded.
- **Hyperion runs on Windows.** There is no Ubuntu machine and none is wanted.
- **The monitor back is smoothly curved**, with no flat region. That is fine;
  see the mounting notes in HARDWARE.md.

---

## Next - the plan to 7 pm, 27 Sep

Screen sync first, because it is the most proven and the highest value; then
the posters, which need no electronics; then the shelf light. NFC is phone work
for the evening once the tags arrive. **The desk node stays on the breadboard
for now** - it works, and moving it to a dot board is a later evening's job.

### Tonight, 26 Sep

1. Solder 3 wires onto the 2 m strip's bare `Din` pads; plug in; the node boots
   into the 120-LED colour bands. Last colour PINK, complete = all good.
2. Cut from the `Din` end: **18 (left) -> 34 (top) -> 18 (right)**. Check the
   pad text on every cut.
3. Solder the two corner joints (6 points each) and the injection pair at the
   far end (+5V and GND, 2 points). Test the U flat.
4. Press a **Tack-It test patch** on hidden paint (behind the wardrobe) so it has
   had a night by the time the posters go up. The 48 h rule is the owner's own;
   24 h is his call.
5. Flash the **Wemos D1 mini** with WLED from install.wled.me (ESP8266 build,
   same micro-USB cable; it enumerates as CH340, not CP2102). Join Wi-Fi, name
   it `wled-shelf`. No soldering.

### Tomorrow morning

6. IPA the monitor back; mount the U starting at the `Din` corner; corner ties.
7. Wire to the node. Strip power **straight from the pigtail**, not the rails,
   and keep ABL at **800 mA while it lives on the breadboard** (raise to 2000 only
   on the dot board). `apply` / `walk` / `presets`.
8. Hyperion: Windows installer, DXGI DDA grabber, WLED device by mDNS, paste
   `config/hyperion_leds.json`. **Screen sync done.**

### Tomorrow afternoon

9. Posters: the 6 x 2 hero grid (bottom edge ~132 cm off the floor, centred over
   the desk), bike A3 in the niche, waveform A3 on the bathroom wall. Tack-It, 4
   bits per A4. Stick them now; the NFC tags go on the **backs** of five cards
   later by lifting each card - Tack-It is removable.
10. **Shelf light (L4)** on the D1 mini - see below.

### Evening

11. NFC tags arrive: write with NFC Tools; HTTP Shortcuts for the WLED presets;
    `spotify:artist:<id>:play` behind Rahman, MJ, Pradeep Kumar, Coldplay,
    Freddie. Phone work, no wall work.

### Shelf light (L4) - revised, no buffer IC

| | |
|---|---|
| Strip | Gesto 12 V neon, **two 1.25 m pieces in parallel**, one under each upper niche shelf |
| Cut plan | cut the first 1.25 m **from the connector end**, so piece A keeps the factory lead and needs **no soldering**; piece B needs + and - soldered (2 joints on neon - cut the silicone back first) |
| 12 V | the Gesto's own 12 V 2 A adapter -> both strips' + |
| Switching | both strips' - -> **IRL540N drain**; source -> GND; **gate <- D1 mini `D2` (GPIO4) through 100 ohm**, 10 k gate-to-GND. Logic-level FET: 3.3 V gate is enough at ~1 A, no buffer |
| 5 V for the D1 mini | **a USB phone charger** into its micro-USB. It only powers itself (~80 mA); the strip is on 12 V. Tie the 12 V adapter's - to the D1 mini's GND |
| MOSFET mounting | a scrap of dot board with the 100 ohm, 10 k and a screw terminal, ~8 joints. 1 A through breadboard contacts is at their limit |
| WLED | bus 1 = **PWM White on GPIO4**; Sync Interfaces: UDP **receive**; desk node = send |
| Never | 12 V into the D1 mini's 5V pin - its regulator dies |

L3 (under-desk warm strip) stays blocked on its 12 V 1 A adapter and is not in
this plan.

---

## Blocked / later

| Item | Waiting on |
|---|---|
| **5 A adapter** | an IEC C7 figure-8 mains lead. Until then the desk node runs on the 3 A brick |
| **L3** under-desk warm strip | 12 V 1 A adapter (Robu SKU 24715) |
| Desk node onto dot board | an evening, not this weekend. Breadboard is fine at ABL 800 |
| Music reactive, auto-dim, presence | custom WLED build with `USERMOD_AUDIOREACTIVE`, `USERMOD_LDR`, `USERMOD_PIR_SENSOR_SWITCH` - by **OTA**, not USB |
| LD2420 presence sensor | deferred; GPIO27 reserved |
| A1 prints, Itachi A3 | not ordered; not in this plan |

No level shifter IC is needed anywhere - the desk strip uses the proven diode
clamp and the MOSFETs are logic-level.
