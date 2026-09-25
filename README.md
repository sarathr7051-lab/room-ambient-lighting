# Room Ambient Lighting

Low-voltage ambient lighting for a rented room in Bengaluru, built around two
WLED nodes. Nothing drilled, nothing permanent, nothing above 12 V.

The first thing being built is the **screen sync light**: a WS2812 strip around
the back of a 27" monitor, driven by an ESP32 running WLED, fed in real time by
Hyperion running on the Windows PC that drives the screen.

> ### → [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) says where the build actually is
>
> Every other document here describes the whole build from the beginning.
> **Read the state file first**, or you will follow an instruction for a step
> that is already finished. As of 25 Sep 2026 the node is flashed, on Wi-Fi and
> named; the circuit is not yet wired and the strip is not yet cut.

---

## The four layers

The room's lighting is four independent layers. This repo covers L2–L4; L1 is a
consumer bulb with its own app.

| | Layer | Hardware | Node | Stage |
|---|---|---|---|---|
| L1 | Bulb above the window | Havells Glamax 9 W Wi-Fi | — | bought, done |
| L2 | **Monitor bias light** | WS2812, 5 V, 60/m | desk | **node live, circuit not wired** |
| L3 | Under-desk warm strip | Gesto 12 V neon, 1.5 m | desk | waiting on a 12 V 1 A adapter |
| L4 | Under-shelf warm strip | Gesto 12 V neon, 2 x 1.25 m | shelf | waiting on the strip to arrive |

Screen sync is **L2 only**. It is not blocked by anything on order.

---

## How screen sync works

```
  Dell SE2726D  (the picture you are watching)
        |
        |  Hyperion grabs the framebuffer, averages each
        |  edge region down to one colour per LED
        v
  Windows PC  (Galaxy Book3 360, lid closed, DXGI DDA grabber)
        |
        |  DDP over UDP, port 4048, ~40 fps, over Wi-Fi
        v
  ESP32 DevKit V1  running WLED 16.0.1   [wled-desk.local]
        |
        |  GPIO16 -> 74HCT125 level shifter -> 330 ohm -> DIN
        v
  WS2812 strip around the monitor back   [70 LEDs, 18 / 34 / 18]
```

Hyperion has spoken **DDP on port 4048** since 2.0.13, not the older
WARLS/UDP-realtime on 21324. DDP is also what removes the old 490-LED ceiling.

---

## The build, in numbers

Measured and committed — these are facts, not estimates.

| | |
|---|---|
| Strip path on the monitor back | **57 × 30.5 cm** |
| Total LEDs | **70** |
| Left run | 18 LEDs, cut to **30.0 cm** |
| Top run | 34 LEDs, cut to **56.7 cm** |
| Right run | 18 LEDs, cut to **30.0 cm** |
| Strip used / spare | 116.7 cm of 300 cm — **183 cm spare** |
| Corner joints | 2 |
| Node | `wled-desk.local` · 192.168.1.6 · 2.4 GHz ch 4 · 100% signal |

---

## Repo layout

```
docs/
  PROJECT_STATE.md     >> where the build is right now. read this first.
  img/                 wiring and breadboard diagrams (SVG, theme-aware)
  HARDWARE.md          parts in hand, pinout, power budget, mounting
  BUILD_DESK_NODE.md   staged build procedure, marked DONE / NEXT
  HYPERION.md          Windows install, DXGI grabber, DDP config
  DECISIONS.md         what was rejected and why, so it is not re-proposed
tools/
  led_layout.py        measurement -> cut plan + WLED bus cfg + Hyperion layout
  wled_push.py         drive the node over HTTP: probe, apply, walk, name, presets
config/                generated, committed, populated
```

Python 3.12, standard library only. Nothing to `pip install`.

---

## Commands

Address the node as `wled-desk.local`. The Airtel AirFiber admin page is not
reachable, so there is no DHCP reservation and the IP may move; mDNS will not.

Already run — do not repeat:

```bash
python tools/led_layout.py --width 57 --height 30.5 --write   # config/ committed
python tools/wled_push.py name  --host wled-desk.local        # renamed
```

`probe` is read-only and safe to re-run any time:

```bash
python tools/wled_push.py probe --host wled-desk.local
```

Still outstanding, once the strip is cut and joined:

```bash
python tools/wled_push.py apply   --host wled-desk.local   # 70 LEDs, ABL 3000 mA
python tools/wled_push.py walk    --host wled-desk.local   # verify orientation
python tools/wled_push.py presets --host wled-desk.local
```

---

## Flashing happened once, on 25 Sep 2026

WLED 16.0.1 is **already on the board** — do not flash it again. It went on by
hand from [install.wled.me](https://install.wled.me) in Chrome over USB.

Everything since has been HTTP over Wi-Fi: naming, configuration, presets, and
the handoff to Hyperion. That is what `tools/wled_push.py` does. Even the later
custom build (audio-reactive, LDR, presence) goes on over WLED's own OTA
uploader rather than USB.

So there is no scripted COM-port access anywhere in this repo, and there does
not need to be.

---

## Licence

MIT. Personal project, nothing sold or shipped.
