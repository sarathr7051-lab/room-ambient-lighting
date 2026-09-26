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

**Tonight, 26 Sep - the monitor strip only.** Reviewed twice before any
cut. Nothing else tonight: no D1 mini, no shelf, no posters.

Wire cuts (22 AWG silicone): spare-piece lead 3 x 10 cm (red, green, black);
Din leads 3 x 60 cm; far-end injection red + black 60 cm; corner wires
6 x 4 cm, trimmed after dressing. Red ~140 cm, black ~140 cm, green ~80 cm.

0. **Dry-lay with the 1 m strip as a ruler, nothing cut.** 34 LEDs along the
   top clears the joystick; 18 LEDs down each side fit starting 1 cm below
   the top run's edge (the side pieces tuck UNDER the ends of the top piece -
   the 10 mm strip width has to go somewhere). If a side does not fit, it is
   17/34/17 and the config is regenerated. Report before cutting.
1. **Identify the rails from the DO-end connector**, before the 70/71 cut
   removes it: meter on ohms, JST red wire to the bare +5V pad and JST white
   to the bare GND pad both read a few ohms; the green does not. Mark the
   +5V edge along the whole 2 m. Every later joint is checked against that
   mark, not the silkscreen.
2. Count from the bare `Din` end, flag every 10th LED, cross-check with the
   tape: cut lines at **30.0, 86.7 and 116.7 cm** from the Din-end cut line.
   Photo. Label both sides of every future cut: P1 OUT / P2 IN / P2 OUT /
   P3 IN / END.
3. Cut **70/71 first**. Solder the 10 cm lead onto the SPARE piece's fresh
   `Din` pads (LED 71): the rehearsal joint, on the piece that does not
   matter. Power it from the node: RED 20, GREEN 20, BLUE 10.
4. Injection tails, red +5V and black GND, on the 70-piece's far-end pads
   (nothing on `DO`). Leave the other ends free.
5. Din leads on LED 1: green on the MIDDLE pad first, then red, then black.
   Power up: RED 1-20, GREEN 21-40, BLUE 41-60, **WHITE 61-70** = all good.
6. Meter across the free injection tails while lit: **+5 V** = correct, -5 V
   = swapped. Only then join them to the pigtail with the Din leads.
7. Cut 18/19 -> corner 1 -> power test (same picture as step 5) -> cut 52/53
   -> corner 2 -> test. One joint, one test, never two joints then one test.
8. Done for tonight. `apply` (now skip 0, ABL 800) is for tomorrow, after
   mounting.

Before every power-up after new +5V/GND wiring: ohms across the strip's red
and black - never near zero; adapter out of the wall socket for every joint.
The 1 m strip stays on the desk as the known-good: dark strip, plug it in,
and in ten seconds you know whether it is the node or the new joint.

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
| ✅ | Strip ends | 1 m strip: connectors both ends (bench tester). 2 m strip: bare `Din` pads, connector on `DO` |
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

The monitor strip, per the **Now** section above. Nothing else.

### Tomorrow morning

6. Tack-It test patch on hidden paint first thing. Flash the **Wemos D1 mini**
   (ESP8266 build, CH340) while the IPA dries - no soldering.
7. IPA the monitor back; mount the U starting at the `Din` corner; corner ties.
8. Wire to the node. Strip power **straight from the pigtail**, not the rails,
   and keep ABL at **800 mA while it lives on the breadboard** (raise to 2000 only
   on the dot board). `apply` / `walk` / `presets`.
9. Hyperion: Windows installer, DXGI DDA grabber, WLED device by mDNS, paste
   `config/hyperion_leds.json`. **Screen sync done.**

### Tomorrow afternoon

10. Posters: the 6 x 2 hero grid (bottom edge ~132 cm off the floor, centred over
   the desk), bike A3 in the niche, waveform A3 on the bathroom wall. Tack-It, 4
   bits per A4. Stick them now; the NFC tags go on the **backs** of five cards
   later by lifting each card - Tack-It is removable.
11. **Shelf light (L4)** on the D1 mini - see below.

### Evening

12. NFC tags arrive: write with NFC Tools; HTTP Shortcuts for the WLED presets;
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
