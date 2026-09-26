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
| **CD74HCT112E as a level shifter** | Sold as a substitute for the 74HCT125 and cannot work. It is a *sequential* part - a dual JK flip-flop whose outputs depend on clock edges and stored state, not on the present input level. Its asynchronous Set and Reset could force Q high or low, but making Q *follow* the input needs both the signal and its inverse, and generating that inverse is the exact problem the buffer exists to solve. There is no combinational path from any input to Q. Keep the chip - a JK flip-flop is useful elsewhere - but it is not this. |
| Scripted serial / `arduino-cli` flashing | Separate hard-won lesson from the JiffyTrails build (a different repo, not linked here): scripted serial opens toggle DTR/RTS, which drives the ESP32's auto-reset circuit and can leave the board in reset or download mode while looking like it worked. Moot here anyway — WLED is flashed once from the browser and everything after that is HTTP. |

---

## Level shifting: sacrificial pixel, not a chip

**Decided 26 Sep 2026.** No 74HCT125, and no other 74HCT gate, could be found
at five or six SP Road shops, and Robu would cost days. The build uses a
**sacrificial WS2812** instead, and that is the permanent answer rather than a
stopgap.

One LED cut from the offcut is powered through a 1N4007 at about 4.2 V. Its own
logic threshold falls to roughly 2.9 V, so it accepts the ESP32's 3.3 V; its
output then swings to its own 4.2 V, which clears the 3.5 V that the 5 V main
strip requires. One LED already in the parts bin bridges the gap from both ends.

Why this is not a compromise:

- It is the technique WLED itself expects - "Skip first LED(s)" exists for
  exactly this case - and it is documented by Adafruit and widely used.
- Only the sacrificial LED draws through the diode, 60 mA against a 1 A part,
  so there is no heat, no current sharing and no derating.
- The main strip keeps a full 5 V, so no brightness or colour shift.

Rejected along the way:

| Idea | Why not |
|---|---|
| IRL540N or IRFZ44N as an RC level shifter | Power MOSFETs with large gate capacitance. WS2812 needs roughly 300 ns pulse fidelity at 800 kHz, and a pull-up driving that much capacitance is orders of magnitude too slow. |
| A diode dropping the whole strip's supply | Works electrically, but needs a 3 A diode, costs brightness across all 70 LEDs, and parallel 1N4007s share current badly - forward voltage falls as they heat, so the hottest one takes more. |
| Coercing the CD74HCT112E into service | See the rejected table above. It is sequential; there is no combinational path from any input to Q. |

The buying table below still applies if a proper buffer ever turns up. It would
be a marginal improvement, not a fix for anything broken.

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

### ABL cap: 3000 mA, revised up from 1500

Argued in [HARDWARE.md](HARDWARE.md#why-3000-ma-and-not-the-1500-ma-in-the-original-plan).
Short version: the 12 V strip has its own adapter, so the 5 V rail only carries
the ESP32 and the bias strip, and 1500 mA was sized for a shared-rail design
that no longer exists.

### Three-sided strip, no bottom run

The bottom edge lights the desk rather than the wall, it collides with the
stand and the future monitor arm, and it doubles the corner joints. 183 cm of
strip stays spare, so this is reversible for the cost of solder.

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
