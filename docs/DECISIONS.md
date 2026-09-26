# Decisions

Closed questions, with the reasoning, so they are not reopened every time
someone new looks at the project.

---

## Rejected, with reasons

| Idea | Why not |
|---|---|
| Govee / Philips bias-light kits | ₹5,500+ for a fixed LED count, a closed app and no Hyperion path. The DIY node costs a fraction and drives L3 and L4 as well. |
| IRFZ44N as the strip MOSFET | Not logic-level. Gate threshold is too high for 3.3 V — it would run half-on and get hot. Three were bought before this was caught; they stay as a fallback for nothing in particular. **Use the IRL540N.** |
| 74HC125 (no T) | CMOS input thresholds. A 3.3 V high sits marginally close to the switching point. The T variant has TTL thresholds and costs the same. |
| 220 V rope / cove strips | Mains in a rented room. Everything here stays at 5 V or 12 V. |
| Aluminium diffuser channel | Invisible behind a monitor. It is a real improvement on an exposed under-shelf run and pointless on a bias light. |
| Home Assistant / Raspberry Pi as the brain | A whole extra always-on machine to do what WLED presets and Hyperion already do between them. Parked, not refused — if the room grows more nodes it may earn its place. |
| Alexa for music-reactive lighting | It cannot. There is no audio stream out of an Echo to react to. Sound reactivity needs the INMP441 on the node doing its own FFT. |
| 5 V COB for the warm layers | The original design was a single 5 V rail. Gesto's 12 V neon won because the 12 V adapter is included in the price and a low-side MOSFET does not care what voltage it is switching. The 12 V never touches the ESP32. |
| **CD74HCT112E as a level shifter** | Sold as a substitute for the 74HCT125 and cannot work. It is a *sequential* part - a dual JK flip-flop whose outputs depend on clock edges and stored state, not on the present input level. Its asynchronous Set and Reset could force Q high or low, but making Q *follow* the input needs both the signal and its inverse, and generating that inverse is the exact problem the buffer exists to solve. Its asynchronous SET/RESET inputs do give a combinational path to Q, and that was tested; the part failed on input threshold, not topology. Keep the chip - a JK flip-flop is useful elsewhere - but it is not this. |
| Scripted serial / `arduino-cli` flashing | Separate hard-won lesson from the JiffyTrails build (a different repo, not linked here): scripted serial opens toggle DTR/RTS, which drives the ESP32's auto-reset circuit and can leave the board in reset or download mode while looking like it worked. Moot here anyway — WLED is flashed once from the browser and everything after that is HTTP. |

---

## Level shifting: MEASURED 26 Sep 2026 - the diode clamp it is

The CD74HCT112EX was tested on the bench as a two-stage buffer. **It works
electrically and fails on thresholds.** Four measurements, ESP32 on USB:

| Pin 15 driven to | Pin 6 | |
|---|---|---|
| 0 V | 4.82 V | high |
| **3.17 V (the ESP32's 3V3)** | **4.83 V** | **still high - should be 0** |
| 4.83 V (the 5 V rail) | 0.00 V | correct |

Pin 4 read 0.00 V and pin 15 read 3.17 V, so the wiring was sound and the
result is the chip's own behaviour. It responds correctly at 5 V and not at
all at 3.17 V, so its input threshold lies between them.

An **HCT** input switches at a flat 2.0 V. An **HC** input switches at
0.7 x VCC = 0.7 x 4.83 = **3.38 V**, just above the 3.17 V available. The part
is marked HCT and behaves as HC - consistent with a shop that already supplied
a flip-flop in place of a buffer.

**Decision: build the diode clamp** - and it is now **bench-proven**. 1N4007
with its cathode at GPIO16, 470 ohm pull-up to +5 V, node to the strip's DIN.
Measured 26 Sep evening on the 1 m strip at ABL 600 mA: junction 0.79 V low,
LED 1 steady and the correct colour, rail 4.71 V under load. The clamp has
real margin on this strip at this rail.

Note the margin is thinner than first estimated, because the 3V3 rail measures
3.17 V rather than 3.3 V. Re-measure it on the 3 A adapter - a 5.03 V input
should lift it slightly over the 4.83 V USB gives.

---

## Superseded: the sacrificial pixel

**26 Sep 2026.** This section previously concluded that a sacrificial WS2812
was "the permanent answer rather than a stopgap". **That was wrong.** Four
independent reviews later:

- The rail-tracking argument that favoured it applies to the **output** hop,
  which was never the limiting one. Its ESP32-to-pixel hop degrades with rail
  voltage exactly as the alternative does, and a series diode lowers that
  threshold by only 0.7 x Vf where a clamp adds a full 1.0 x Vf to the drive.
- Worst-case failure rail: **5.19 V** for the sacrificial pixel against
  **5.40 V** for the diode clamp. 5.19 V is a voltage cheap adapters produce.
- Two reviews disagreed by **80 mV** on the 1N4007's forward voltage at the
  relevant current, having read Vishay and Diodes Inc curves respectively.
  Doubled across a two-diode stack, that is 160 mV of uncertainty on a design
  with 300-500 mV of margin. Which brand is in the bag would decide it.
- **Neither diode circuit closes on datasheet worst case.** Both depend on
  typical behaviour, and the failure mode is the worst kind for a fixture you
  mount and forget: fine on the bench, first pixel glitching in August.

> **Superseded 26 Sep 2026** - the paragraph below is the pre-measurement
> reasoning. The clamp was built and proven; nothing is bought.
**The decision is to buy a 74AHCT125 or 74HCT245.** Over 1 V of input margin on
pure worst case, and its margin grows rather than shrinks as the rail rises. A
diode clamp is an acceptable interim **only** if the measured adapter reads
5.10 V or below.

The lesson for the shop counter: **it is the HCT that matters, not the 125.**

---

## What to buy IF a level shifter ever turns up

**It is the HCT that matters, not the 125.** Any 74**HCT** logic gate works as
a 3.3 V -> 5 V level shifter, because the HCT family pairs TTL input thresholds
(logic high from about 2 V) with CMOS outputs that swing the full 5 V. The part
number only decides how many wires it takes.

| Part | How to use it |
|---|---|
| 74HCT125 / 74HCT126 | buffer - direct, one gate. What the design assumes |
| 74AHCT125 | same, faster. Equally good |
| 74HCT245 | octal bus transceiver - direct, tie DIR and OE |
| 74HCT08 (AND) | tie one input high -> non-inverting buffer, one gate |
| 74HCT32 (OR) | tie one input low -> non-inverting buffer, one gate |
| 74HCT04 / 74HCT14 | inverters - two in series to get back to non-inverting |
| 74HCT00 (NAND) | tie one input high -> inverter; two in series |

So at the counter, ask for "any 74HCT gate" rather than walking away empty
handed. **Do not** accept a 74HC part without the T - that is already on the
rejected list above, because CMOS input thresholds put 3.3 V uncomfortably
close to the switching point, which is the very problem being solved.

Om Technology delivers by Porter, so WhatsApp the part rather than making the
trip, and ask about exchanging the CD74HCT112E at the same time.

---

## Settled, and now baked into the committed config

### ABL cap: 2000 mA

Superseded on 26 Sep 2026. The 5 A adapter cannot be used (no mains lead), so
the cap is now **2000 mA** on the 3 A adapter. Argued in
[HARDWARE.md](HARDWARE.md#why-the-abl-cap-is-2000-ma).

### Three-sided strip, no bottom run

The bottom edge lights the desk rather than the wall, it collides with the
stand and the future monitor arm, and it doubles the corner joints. 50 LEDs of
strip stay spare, so this is reversible for the cost of solder.

### DDP, not WARLS

The original plan said "UDP realtime port 21324". Hyperion has used DDP on port
4048 for the WLED device type since 2.0.13, with UDP-Raw only as a fallback.
DDP also lifts the old 490-LED limit. Nothing in this project should reference
21324.

---

## Deferred

- **Custom WLED build** with `USERMOD_AUDIOREACTIVE`, `USERMOD_LDR` and
  `USERMOD_PIR_SENSOR_SWITCH`. Needed for music mode, auto-dim and presence;
  **not** needed for screen sync. Goes on over WLED's OTA uploader when the
  time comes, not over USB.
- **LD2420 presence sensor**, ₹219, Robu SKU 1802881. GPIO27 reserved.
- **L3, under-desk warm strip.** Waiting on a 12 V 1 A adapter, Robu SKU 24715,
  ₹199. Leave space on the dot board for the IRL540N and its gate network.
- **L4, shelf node** on the Wemos D1 mini. Waiting on the Gesto strip to
  arrive. Will be a UDP sync receiver with the desk node as sender.

Prices above are the ones sourced on 25 Sep 2026 and will have moved. Re-check
before buying rather than quoting them back.
