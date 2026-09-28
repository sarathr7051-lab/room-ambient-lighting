# Project state

**Read this first.** Every other document describes the whole build from the
beginning; this one says where the build actually is. Update it whenever a step
completes.

Last updated: **26 Sep 2026, evening** - bench test passed

---

## Now

**27 Sep 2026: SCREEN SYNC IS WORKING.** Desk node on the dot board, U on
the monitor, Hyperion 2.2.1 streaming DDP to it from the Windows PC.

- Dot board built per PERFBOARD.md, all 70 lit on first power-up.
- Config on the node: 70 LEDs, skip 0, GPIO16, GRB, **ABL 1000 mA**. Measured
  at full white across the buses: 4.03 V at the 2000 cap, 4.2 V at 1500,
  **4.39 V at 1000** - the 3 A adapter and pigtail drop ~0.6 V per amp, and
  the ESP32 dropped off Wi-Fi at 4.03 V. 1000 mA is the working cap until the
  5 A brick has its mains lead.
- Preset 9 = one colour per piece (RED left / GREEN top / BLUE right from the
  front); presets 1-4 pushed by `wled_push.py presets`.
- Strain relief: velcro tie round the five strip wires 3-4 cm from the board,
  second tie to the monitor stand. (Heat-shrink over the bundle would have
  had to go on before soldering - missed; velcro does the job.)
- 0.1 uF fitted at L002/H002. 1000 uF at L016/J016-H016.

Hyperion settings in [HYPERION.md](HYPERION.md).

**Shelf node (L4) flashed and configured, 27 Sep evening.** Wemos D1 mini,
WLED 16.0.1 ESP8266 build, `wled-shelf`, to be fixed at **192.168.1.252** when it is plugged back in (was DHCP .7).
Output bus: **PWM White, type 41, GPIO4 (D2)**, 1 "LED". UDP sync receive on.

> **ESP8266 lesson:** with WLED's default *Wi-Fi sleep = on*, the D1 mini
> was on the network but answered only in ~20 s windows every 2-3 minutes;
> the Airtel router does not wake it. It looked like a reboot loop and it was
> not. Two things fixed it, both needed: `{"wifi":{"sleep":false,"phy":1}}`
> (sleep off, force 802.11g), fired repeatedly until a window opened, and
> **moving the board away from the PC** - next to the PC's USB 3 ports it
> managed 40-50 % of probes even with sleep off; on the shelf 2 m away it is
> 20/20 at ~60 ms, ping 3-58 ms. Also: install.wled.me's "erase" did not
> clear the config (the name survived). For any ESP8266 node: sleep off,
> force-g, and keep it away from USB 3.

Shelf plan from the photos: electronics on the top shelf next to the router
(MOSFET board, D1 mini on a phone charger, the 12 V adapter). Piece A under
the top shelf, piece B under the middle shelf, each 130 cm (or the nearest
cut mark); the strip is 5 m. The white cable out of the wall above the top
shelf is a mains light point - **not touched**. Neon has no adhesive: needs
double-sided tape or clips. Measured: top-to-middle shelf gap **29.5 cm**. No socket at the niche (the
router on the top shelf is an unpowered spare) - power comes from the wall
socket by the door via an extension board. No double-sided tape in the house;
to buy (the nano tape shown with the Gesto listing was Rs 198 / 3 m on 27 Sep).

**Moods and sync, 27 Sep evening.** Desk node UDP sync **send** on (`if.sync.send.en`
- the `dir` flag alone does nothing), shelf node receives: brightness and on/off
follow the desk (tested 40 -> 40, off -> off, 255 -> 255). Desk presets, judged by the owner 27 Sep evening and locked: 1 Work = full,
warm white (255,197,143); 2 Evening = 47 %, amber-warm (255,160,80); 3 Movie
= 12 %, (255,140,60); 5 Night = off; 6 Screen sync = full, override off;
9 pieces-70 (test pattern). All are one full-strip segment - a preset saved
while the three-band test pattern's segments still existed only recoloured
the first 18 LEDs, and a preset saved mid-fade captured the previous state:
save with `tt:0`, delete segments 1-15, wait 2 s, then `psave`. A third trap
bit on 27 Sep late: a re-save loop captured the *Night* state into slot 6, so
"Screen sync" after "Night" left the strip off. The HA screen-sync script now
also sends an explicit `light.turn_on` at full brightness before releasing
the live override, so it cannot depend on what the preset holds. **Presets do not store `lor`**, so a mood must be called as
`{"ps":N,"lor":2}` to take over from Hyperion, and "Screen sync" as
`{"ps":6,"lor":0}` to hand back. That is what the NFC tags / HTTP Shortcuts
send. Hyperion: Startup-folder shortcut added (`Hyperion.lnk` ->
`D:\games\Hyperionin\hyperiond.exe`), so it starts at login. Its LED
output component switches itself off when the WLED node reboots mid-stream
(every `/json/cfg` write reboots the node); re-enable it from the Hyperion
dashboard ("LED Output" On) or `componentstate LEDDEVICE true`.

**Extension board for the niche** (no socket there, adapter lead < 1 m; sourced
Amazon.in 27 Sep): Goldmedal Gio 2-pin, 2.5 m, Rs 260; GM 3060 4-socket 2 m,
Rs 459. Length to confirm by taping the socket-to-top-shelf path first.

**Home Assistant: RUNNING** (Docker Desktop on this PC) with both WLED nodes,
Hyperion and the Havells bulb; five mood scripts and five tag automations -
see HOME_ASSISTANT.md. Owner's next step: HA Companion app on the phone and
rewrite the three lighting tags with the HA tag URLs (NFC.md). Needs an always-on host; options are Docker
Desktop on this PC (free, only while the PC is on) or a Raspberry Pi (a
purchase). The Havells bulb can only join a mood via HA (Tuya/Havells
integration) or a Google Home routine; WLED nodes need no hub for the moods.

**Purchases decided 27 Sep evening (sourced):** Amazon - Sunjet nano gel tape
3 m Rs 108 (fastest delivery next morning); extension board: GM 3206 2-socket
2.5 m Rs 235 (universal sockets, 4.4 stars) is enough - only the 12 V adapter
and the USB charger plug in; a 4-socket GM 3060 is Rs 459; cheaper 4-socket
boards found were unreviewed and 5 days out. The Orient 4-way at Rs 309 on
quick commerce is fine if it must be tonight.

Shelf driver design in [SHELF_NODE.md](SHELF_NODE.md), reviewed once and
reworked; second review running. NFC plan in [NFC.md](NFC.md) - artist IDs
still needed from the owner's Spotify app. Home Assistant plan in
[HOME_ASSISTANT.md](HOME_ASSISTANT.md) - host not decided (Docker Desktop is
not installed).

**Desk board fault - FIXED 28 Sep morning.** The owner re-soldered the loose
ground wire; the reflashed ESP32 boots on the board and runs the restored
config. Screen sync did not resume by itself: Hyperion's DDA grabber was
enabled but idle (`active=false`) after the reboots and display change.
Switching the GRABBER component off and on re-attached it (25 fps). The
watchdog now does that automatically as well as re-enabling LED output.

**28 Sep evening - Home Assistant moved off Docker Desktop.** After an 11 h
sleep, Docker Desktop could not start (open bug with its socket files), and
C: was found 100 % full. Moved Docker Desktop's data and the new Ubuntu WSL
disk to D: (C: now ~14 GB free), and runs HA + Whisper on Docker Engine inside
WSL Ubuntu with mirrored networking - details in HOME_ASSISTANT.md. Also
cleared a static Hyperion colour set from the HA dashboard. **C: needs a
clean-up** - it is the system drive and will fill again. **Cold-restart test
passed 28 Sep** with the fixed addresses: screen sync, tags and the phone app
all came back with no manual step.

**Next:**
2. Posters: **DONE 28 Sep** - seven musicians on the desk wall, the five
   sports cards on the window wall at the same height, 35.5 cm from the
   corner. Waveform A3 / SDR A1 / Itachi go to the bathroom wall later.
3. Shelf light L4: **extension board and double-sided tape arrived 28 Sep**
   - build now (SHELF_NODE.md: breadboard test, then dot board, then mount).
4. Tidy: velcro the desk board to the monitor stand so it cannot be dragged
   by its wires again.
5. Later: Google Assistant only via Tailscale Funnel + manual Google
   integration (free, an evening); bulb already works with "Hey Google" via
   Smart Life linked in Google Home.

---

## Done

| | What | Detail |
|---|---|---|
| ✅ | Repo created | public, `sarathr7051-lab/room-ambient-lighting` |
| ✅ | **WLED flashed** | 16.0.1, via install.wled.me. **Do not flash again.** |
| ✅ | USB cable sorted | a spare Fire TV Stick micro-USB lead turned out to be data-capable; nothing bought. Board enumerates as `Silicon Labs CP210x`, COM12 |
| ✅ | Node on Wi-Fi | **`192.168.1.251` (fixed)**, 2.4 GHz |
| ✅ | Node named | `wled-desk`; `wled-desk.local` resolves |
| ✅ | Tooling verified | `wled_push.py` tested against the live node; four bugs found and fixed |
| ✅ | Monitor measured | strip path **57 × 30.5 cm** |
| ✅ | **Adapter measured** | 5 V 3 A brick reads **5.03 V** open-circuit, red wire = **+**. Well regulated; most cheap bricks sit 5.1-5.4 |
| ✅ | Strip ends | 1 m strip: connectors both ends (bench tester). 2 m strip: bare `Din` pads, connector on `DO` |
| ✅ | **Bench test** | passed 26 Sep evening on the 1 m strip: clamp working, LED 1 steady, GRB confirmed, rail 4.71 V loaded |
| ✅ | Chip test | CD74HCT112EX behaves as HC, not HCT - eliminated by measurement |
| ✅ | **Shelf node flashed** | 27 Sep: D1 mini, wled-shelf, PWM white on GPIO4, Wi-Fi sleep off |
| ✅ | **Screen sync live** | 27 Sep: Hyperion 2.2.1, DXGI on the Dell, DDP to wled-desk.local at ~25 fps |
| ✅ | **Dot board + mounted** | 27 Sep: node on the LABTECH board, U on the monitor, ABL 1000 |
| ✅ | **Strip cut and joined** | 18/34/18 from the 2 m strip's Din end, two corner joints, injection at LED 70, tested through both corners 26 Sep |
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

Screen sync first, then the posters (no electronics), then the shelf light.
NFC is phone work for the evening once the tags arrive.

### Tomorrow morning, 27 Sep - in this order

1. **Protect the joints** (BUILD_DESK_NODE.md Stage 4). Pull the LED 1 wires,
   the LED 70 tails and the spare's lead out of the breadboard; slide one
   wide heat-shrink tube over each bundle from the free end, down onto the
   strip's pads, shrink. Hot glue on the two corner joints. **Nothing else
   until this is done.**
2. **Dot board** - [PERFBOARD.md](PERFBOARD.md), hole by hole, both faces
   drawn, four independent reviews on 27 Sep. About 60 joints. The breadboard
   is dismantled as the board is built; the ESP32 moves last. Then `--abl 2000`.
3. Tack-It test patch on hidden paint. Flash the **Wemos D1 mini** (ESP8266
   build, CH340) while the IPA dries - no soldering.
4. IPA the monitor back; mount the U from the LED 1 corner (bottom-left from
   the front); side pieces tuck under the top piece's ends; ties at corners.
5. `apply` / `walk` / `presets`.
6. Hyperion: Windows installer, DXGI DDA grabber, WLED device by mDNS, paste
   `config/hyperion_leds.json`. **Screen sync done.**

### Tomorrow afternoon

7. Posters: the 6 x 2 hero grid (bottom edge ~132 cm off the floor, centred over
   the desk), bike A3 in the niche, waveform A3 on the bathroom wall. Tack-It, 4
   bits per A4. Stick them now; the NFC tags go on the **backs** of five cards
   later by lifting each card - Tack-It is removable.
8. **Shelf light (L4)** on the D1 mini - see below.

### Evening

9. NFC tags arrive: write with NFC Tools; HTTP Shortcuts for the WLED presets;
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
| Music reactive, auto-dim, presence | custom WLED build with `USERMOD_AUDIOREACTIVE`, `USERMOD_LDR`, `USERMOD_PIR_SENSOR_SWITCH` - by **OTA**, not USB |
| LD2420 presence sensor | deferred; GPIO27 reserved |
| A1 prints, Itachi A3 | not ordered; not in this plan |

No level shifter IC is needed anywhere - the desk strip uses the proven diode
clamp and the MOSFETs are logic-level.
