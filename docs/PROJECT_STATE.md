# Project state

**Read this first.** Every other document describes the whole build from the
beginning; this one says where the build actually is. Update it whenever a step
completes.

Last updated: **26 Sep 2026**

---

## Now

**Build the bench circuit** - [BUILD_DESK_NODE.md § 1.4](BUILD_DESK_NODE.md#14-wire-the-breadboard---next).
Nothing electrical has been powered up yet, and this must happen before the
strip is cut. Diagrams in [docs/img/](img/).

The missing 74HCT125 does **not** block it. A sacrificial WS2812 powered through
a 1N4007 does the level shifting instead, from parts already in the bin - see
[DECISIONS.md](DECISIONS.md#level-shifting-sacrificial-pixel-not-a-chip).

Then, and only once the breadboard lights the uncut strip: cut the three
lengths and solder the two corner joints. Practise on the offcut first.

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

## Next

### 1. Build the bench circuit — not yet started

ESP32 + 74HCT125 + 1000 µF + 330 Ω on the breadboard, 5 V 5 A adapter, with the
**uncut** strip. Diagrams in [docs/img/](img/). [BUILD_DESK_NODE.md § 1.4](BUILD_DESK_NODE.md#14-wire-the-breadboard---next).

> **Do this before cutting.** Nothing electrical has ever been powered up. If
> the first time you energise the circuit is also the first time you energise
> your first-ever solder joints, a strip that stays dark has two possible
> causes and no way to separate them. Proving the breadboard against uncut
> strip costs half an hour and removes one of the two.

### 2. Cut, solder, mount

Three lengths: 56.7 / 30.0 / 30.0 cm. Two corner joints. Bench-test the
assembled U flat before any backing paper comes off.

### 3. Push the real config

The node still reports the default **30 LEDs**. After the strip is joined:

```bash
python tools/wled_push.py apply   --host wled-desk.local   # 70 LEDs, ABL 3000 mA
python tools/wled_push.py walk    --host wled-desk.local   # verify orientation
python tools/wled_push.py presets --host wled-desk.local
```

`walk` must happen before Hyperion is configured — it is the only check that
catches a mirrored strip, and mirrored ambilight is the most common way this
build goes wrong.

### 4. Hyperion — not installed

Windows x64 installer, DXGI DDA grabber, WLED device over DDP, paste
`config/hyperion_leds.json` into the LED Layout. [HYPERION.md](HYPERION.md).

---

## Blocked / later

| Item | Waiting on |
|---|---|
| **L3** under-desk warm strip | 12 V 1 A adapter (Robu SKU 24715) |
| **L4** shelf node, Wemos D1 mini | Gesto 12 V neon strip to arrive |
| Music reactive, auto-dim, presence | custom WLED build with `USERMOD_AUDIOREACTIVE`, `USERMOD_LDR`, `USERMOD_PIR_SENSOR_SWITCH` — goes on by **OTA**, not USB |
| LD2420 presence sensor | deferred; GPIO27 reserved |

None of these block the screen sync light.
