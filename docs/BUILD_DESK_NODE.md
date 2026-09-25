# Building the desk node

Order matters here. The strip gets cut and stuck down in stage 3, which is
irreversible; stages 1 and 2 prove the whole electrical and network chain first,
on the uncut strip, where a mistake costs nothing.

---

## Stage 1 - bench bring-up

**Needs:** the ESP32 and a micro-USB data cable. **Time:** about an hour.

Flash the board **bare**, before anything is wired to it. A blank ESP32 on USB
alone cannot be damaged by a wiring mistake that has not been made yet, and
getting WLED onto the network first means the rest of the bring-up can be driven
over HTTP instead of guessed at.

### 1.1 Flash WLED

Only the ESP32 and the USB cable. **No strip, no 5 V adapter, no breadboard.**
Two 5 V sources fighting each other across the ESP32's regulator is how boards
die, so the adapter stays out of this entirely.

1. Chrome or Edge (Web Serial does not exist in Firefox) -> `install.wled.me`.
2. Plug the ESP32 in by micro-USB. It must be a **data** cable; charge-only
   cables are the most common reason no port appears. Windows 11 has the CP2102
   driver built in, so if still nothing shows up it is the cable.
3. On the page: **Mode = Basic**, version = **16.0.1** (the default, current
   stable), variant = **Plain**. Not Ethernet, not DEBUG, not HUB75.
4. **Install** -> pick the COM port that just appeared (it identifies as Silicon
   Labs CP210x) -> tick **Erase device** for a clean first flash -> let it run.
5. When it offers Wi-Fi, give it your **2.4 GHz** SSID. The ESP32 has no 5 GHz
   radio. If the router publishes one name for both bands the join can fail
   without saying why - use a 2.4-only SSID or the guest network.
6. Name the node `wled-desk`.

Then unplug USB.

> Version note: WLED jumped from 0.15.x straight to 16.x, so 16.0.1 being the
> default is not a beta. If you ever need the older line for a community
> audio-reactive build, 0.15.4 is in the same dropdown - but that is a later
> stage and screen sync does not care.

### 1.2 Pin the IP down

Find the node in your router's client list and **reserve the address by MAC**.
Hyperion streams to it for the life of the project; a DHCP lease moving
underneath it is an annoying evening.

### 1.3 First contact

```bash
python tools/wled_push.py probe --host <ip>
```

Version, free heap, Wi-Fi signal and LED count should come back. Nothing is
wired yet, so the LED count is whatever the default is - that is expected.

### 1.4 Now wire it, with the power off

Breadboard, using the **full 3 m strip uncut**.

```
  5 V 5 A adapter
        |
   DC pigtail
        |
   +-------------------------------- +5V rail
   |                                      |
   |  1000 uF (+ to +5V, watch polarity)  |
   |                                      |
   +-------------------------------- GND rail

  ESP32   VIN <- +5V rail
          GND <- GND rail
          GPIO16 ----> 74HCT125 pin 2 (1A)

  74HCT125  pin 14 <- +5V      pin 7  -> GND
            pin 1  -> GND      0.1 uF between 14 and 7
            pins 5, 9, 12 -> GND
            pin 3 (1Y) -> 330 ohm -> strip DIN

  strip   +5V -> +5V rail
          GND -> GND rail
```

Check the 1000 uF polarity twice - backwards is the one mistake on this board
that makes a mess. Then plug the 5 V adapter in. USB stays out from here on.

### 1.5 Light it up - carefully

In the WLED web UI, **before touching brightness**:

- Config -> LED Preferences
- LED count **180**, GPIO **16**, type WS281x, colour order GRB
- Auto-brightness limiter **on**, **1500 mA**, 55 mA/LED

Then set brightness to about 25% and pick a solid colour.

> 180 LEDs at full white is 10.8 A. The bench wiring - breadboard rails, a
> single-ended feed, jumper wire - is nowhere near that. The ABL cap and the low
> brightness are what keep this test boring. Do not raise either until the strip
> is cut down and properly injected.

**What success looks like:** every LED lights, the colour you picked is the
colour you get (red and green swapped means the order is RGB, not GRB), and
nothing gets warm except mildly the strip.

**If only the first LED lights:** data is not reaching the rest. Check the
330 ohm is in series and not to ground, and that pin 1 of the 74HCT125 is
actually at GND.

**If nothing lights:** check DIN vs DOUT - the strip has an arrow, and data only
flows one way.

**If the ESP32 resets when the strip brightens:** the adapter is sagging or the
1000 uF is not actually across the rail.

Stage 1 is done. **Do not cut anything yet.**

---

## Stage 2 — measure and plan

Monitor face-down on a towel. Measure the rectangle the strip will actually
follow on the flat back panel: roughly 2–3 cm in from the outer edge, clear of
the raised VESA boss and any vent slots. Two numbers, measured directly.

```bash
python tools/led_layout.py --width <W> --height <H>
```

That prints the LED count for each run, the cut lengths, how much strip is left
over, and the real current figures. Add `--write` when the numbers look right
and it emits `config/hyperion_leds.json` and `config/wled_desk_cfg.json`.

### Three sides, not four

The default is left, top and right, with no bottom run. On a monitor sitting at
desk height:

- the bottom strip lights the desk surface, not the wall behind
- it is where the stand column and later the Dyazo arm sit
- it costs two extra corner joints — four instead of two

Hyperion handles a missing bottom edge natively. You will have ~185 cm of strip
spare, so adding the bottom later costs nothing but solder if you decide the
glow is missing something.

### Corners

WS2812 will not bend around a 90° corner without cracking the copper. At each
corner: cut on the pads, then bridge with three short lengths of 22 AWG —
+5 V, GND, DATA — kept under 3 cm so the data edge stays clean. Mind the arrow;
DOUT of one run goes to DIN of the next.

---

## Stage 3 — cut, solder, mount

1. Cut the runs to the lengths `led_layout.py` printed.
2. Solder the corner jumpers. Test the assembled run flat on the bench, still
   on the breadboard, before any adhesive touches the monitor.
3. IPA the back panel, let it dry.
4. Stick it down, starting at the DIN corner. Velcro tie or a dab at each
   corner turn — that is where adhesive fails first.
5. Run the injection pair from the far end of the strip back to the rail.
6. Raise the ABL to 3000 mA and set the real LED count:

```bash
python tools/wled_push.py apply --host <ip>
```

7. Confirm the orientation with your eyes before Hyperion is configured
   against an assumption:

```bash
python tools/wled_push.py walk --host <ip>
```

Note which corner LED 0 sits in **viewed from the front of the screen**, and
which way the white pixel travels. Remember you are looking at the back while
you mount, so left and right are mirrored under your hands. If it runs the
wrong way, set `rev: true` on the bus rather than re-soldering anything.

8. Save the presets:

```bash
python tools/wled_push.py presets --host <ip>
```

---

## Stage 4 — final assembly

Move off the breadboard onto the 6 x 4 inch dot board: ESP32 on female headers
(so it can come off), 74HCT125 on a socket, the 1000 uF and the 330 ohm on
board, screw terminals or JST for the strip and the DC pigtail.

The board lives in the MICKE desk's under-desk strip, velcroed down, with the
5 V adapter on the switched power strip.

Leave room on the dot board for the IRL540N and its gate network — L3 lands on
the same board when the 12 V adapter arrives, and rebuilding it then would be
annoying.

---

## Stage 5

[HYPERION.md](HYPERION.md).
