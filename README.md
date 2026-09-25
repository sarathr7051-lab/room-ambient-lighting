# Room Ambient Lighting

Low-voltage ambient lighting for a rented room in Bengaluru, built around two
WLED nodes. Nothing drilled, nothing permanent, nothing above 12 V.

The first thing being built is the **screen sync light**: a WS2812 strip around
the back of a 27" monitor, driven by an ESP32 running WLED, fed in real time by
Hyperion running on the Windows PC that drives the screen.

**Status:** hardware in hand, nothing built yet. One measurement is needed
before the strip can be cut — see [Blocked on](#blocked-on).

---

## The four layers

The room's lighting is four independent layers. This repo covers L2–L4; L1 is a
consumer bulb with its own app.

| | Layer | Hardware | Node | Stage |
|---|---|---|---|---|
| L1 | Bulb above the window | Havells Glamax 9 W Wi-Fi | — | done, bought |
| L2 | **Monitor bias light** | WS2812, 5 V, 60/m | desk | **in progress** |
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
  ESP32 DevKit V1  running stock WLED
        |
        |  GPIO16 -> 74HCT125 level shifter -> 330 ohm -> DIN
        v
  WS2812 strip around the monitor back
```

Hyperion has spoken **DDP on port 4048** since 2.0.13, not the older
WARLS/UDP-realtime on 21324. DDP is also what removes the old 490-LED ceiling.

---

## Repo layout

```
docs/
  HARDWARE.md          parts in hand, pinout, power budget
  BUILD_DESK_NODE.md   bench bring-up then final assembly, step by step
  HYPERION.md          Windows install, DXGI grabber, DDP config
  DECISIONS.md         what was rejected and why, so it is not re-proposed
tools/
  led_layout.py        measurement -> cut plan + WLED bus cfg + Hyperion layout
  wled_push.py         drive the node over HTTP: probe, apply, walk, presets
config/                generated; committed so the node can be rebuilt from scratch
```

Python 3.12, standard library only. Nothing to `pip install`.

---

## Quickstart

Once the node is on Wi-Fi and you know its IP:

```bash
python tools/wled_push.py probe --host 192.168.1.42
```

Once the monitor back is measured:

```bash
python tools/led_layout.py --width <W> --height <H> --write
python tools/wled_push.py apply --host 192.168.1.42
python tools/wled_push.py walk  --host 192.168.1.42   # confirm orientation
python tools/wled_push.py presets --host 192.168.1.42
```

---

## Flashing, and why it happens exactly once

WLED is prebuilt firmware. It gets flashed **once**, by hand, from
[install.wled.me](https://install.wled.me) in Chrome or Edge over USB — a browser
dialog, not a command line, and not a scripted serial port.

After that the node is on Wi-Fi and everything else in this project happens
over HTTP: LED count, GPIO, colour order, power limit, presets, and the handoff
to Hyperion. That is what `tools/wled_push.py` does. Even the later custom build
(audio-reactive, LDR, presence) can go on over WLED's own OTA uploader rather
than USB.

So there is no scripted COM-port access anywhere in this repo, and there does
not need to be.

---

## Blocked on

**The monitor strip path, measured directly.** Width and height of the rectangle
the strip will actually follow on the flat back panel, roughly 2-3 cm in from
the edge, routed clear of the VESA boss and the vents. Two numbers. Not derived
from the 61 x 36 cm outer size.

Everything else can proceed now: flashing, Wi-Fi, bench bring-up, and the
Hyperion install on Windows.

## Licence

MIT. Personal project, nothing sold or shipped.
