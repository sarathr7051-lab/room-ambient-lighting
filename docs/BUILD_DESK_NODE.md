# Building the desk node

Read [PROJECT_STATE.md](PROJECT_STATE.md) first — it says which of these stages
are already done. This file is the whole procedure from the beginning.

Stages 1-3 are done (26 Sep 2026): the node is bench-proven and the 70-LED U
is cut, joined and tested. What remains is protecting the joints, moving the
node onto the dot board, mounting, and Hyperion.

---

## Safety, once, for the whole build

> ### THE 12 V ADAPTER WILL DESTROY THIS NODE
>
> Since the Gesto neon strip arrived there are **two adapters on the bench with
> identical 5.5 x 2.1 mm barrel plugs and different voltages**:
>
> | Adapter | For | Barrel |
> |---|---|---|
> | **5 V 3 A** | the ESP32 and the WS2812 strip | 5.5 x 2.1 |
> | **12 V 2 A** (came with the Gesto neon) | the 12 V neon strip ONLY | 5.5 x 2.1 |
>
> They are physically interchangeable and nothing in the circuit stops you.
> **12 V into the 5 V rail instantly kills the ESP32 and every WS2812 on the
> strip** - the ESP32's absolute maximum on VIN is well under 12 V, and the
> LEDs' is 6-7 V. There is no fuse, no reverse protection and no second chance;
> it is one wrong plug and roughly 3,500 rupees of parts.
>
> **Do this before wiring anything:**
>
> 1. **Measure both adapters** with the multimeter. Do not trust the label, and
>    do not trust memory.
> 2. **Write the measured voltage on each brick in marker, on tape**, big
>    enough to read without picking it up.
> 3. **Put the 12 V adapter in a different room, or at least a closed box**,
>    until the desk node is finished. Out of reach beats a label.
>
> The 12 V strip is layer L3/L4 and is not built until the desk node works.
> There is no reason for its adapter to be on the bench at all today.


- **Eye protection at every first power-up.** A 1000 µF electrolytic fitted
  backwards across 5 V heats, vents and can burst. It is the only thing here
  that can actually injure you.
- **Never connect or disconnect the strip while the adapter is on.** If you
  must, the order is ground, then power, then data — and the reverse to
  disconnect.
- **Mate the DC barrel connector before switching on at the wall**, and unplug
  at the wall before unmating. Hot-plugging into 1000 µF draws a multi-amp
  spike for a few hundred microseconds and pits the contacts.
- **Touch a grounded metal object** before handling the strip or the board.
  WS2812s are static-sensitive. Not in socks on synthetic carpet.
- **Unroll the strip before powering it.** A coiled reel cannot shed heat and
  hides a hot spot.
- **Never improvise a mains connection.** Use a proper lead, or use USB.

---

## The strip's ends - RESOLVED 26 Sep 2026

**Two strips.** The **1 m** strip has wires and a 3-pin connector on both ends
and was the bench-test strip; it stays whole. The **2 m** strip, which the
build pieces come from, has **bare pads on its `Din` end** and a connector on
its `DO` end - the Din leads are the first solder joint of the build.

- Three wires per end: **red, green, white**, into a black 3-pin JST-SM housing.
- Plus a separate pair of flying leads for power injection.

Conventional colour code for this strip type, **to be confirmed against the pad
labels rather than assumed**: red = +5 V, green = DATA, white = GND.

**Which end is DIN:** read the tiny silkscreen where the wires are soldered.
The input end is marked `DI` or `DIN`; the output end `DO` or `DOUT`. The
printed arrows also point *away* from DIN, in the direction data travels.
Do not rely on connector gender - it is not a reliable convention.

## Stage 1 - bench bring-up - DONE 26 Sep 2026

### 1.1 Flash WLED - DONE 25 Sep 2026

WLED **16.0.1** is on the board, installed from install.wled.me in Chrome over
USB (Basic mode, Plain variant, adapter unplugged).

> **Do not flash it again.** Everything that remains happens over Wi-Fi.

- The board enumerates as `Silicon Labs CP210x USB to UART Bridge`; on this
  machine it appeared on COM12. Read the chip name, never the COM number.
- The cable is a repurposed Fire TV Stick micro-USB lead that carries data.
- **WROOM confirmed** from a photo of the board: GPIO16 and GPIO17 are broken
  out as `RX2` / `TX2`, which a WROVER cannot do - those pins are its PSRAM
  interface. The pin choice stands.
- **The silkscreen says `RX2`, not `D16`.** HARDWARE.md has where each pin
  physically sits.

### 1.2 Node address - DONE

No DHCP reservation, and none is possible — the Airtel AirFiber CPE's admin
page is unreachable. The node is addressed by mDNS:

```
wled-desk.local   ->   192.168.1.6      2.4 GHz, channel 4, 100% signal
```

`wled_push.py` sweeps the subnet automatically if the name will not resolve.

### 1.3 First contact - DONE

```bash
python tools/wled_push.py probe --host wled-desk.local
```

> **Do not run `wled_push.py apply` during bring-up.** It pushes the committed
> 70-LED / skip-0 / 800 mA config and would silently overwrite the 120-LED
> bench settings. Only `probe` is safe until the U is joined and mounted.

---

### 1.4 Measure the adapter - DONE

![How to measure the adapter voltage with a multimeter](img/measure-adapter.svg)

**The 5 V 3 A adapter is the one in use.** The 5 A brick has an IEC C8 inlet
and no mains lead.

> **MEASURED 26 Sep 2026: 5.03 V open-circuit, red wire positive**; 4.71 V on
> the breadboard rail at ~600 mA of strip load. Meter: black in `COM`, red in
> `VΩmA`, dial DCV 20, never the `10A` socket.

### 1.5 The bench circuit - DONE, as built

![What is connected to what inside a breadboard](img/breadboard-internals.svg)

![The diode clamp: ESP32 through a 1N4007 into a junction pulled up by 470 ohm](img/diode-clamp.svg)

The **diode clamp**, decided by measurement (the CD74HCT112EX responds at 5 V
and not at 3.17 V, so it is an HC part and is out - see 1.6 and DECISIONS.md).

| # | From | To |
|---|---|---|
| 1 | pigtail **+** | **+ rail** |
| 2 | pigtail **-** | **- rail** |
| 3 | 1000 uF **striped, SHORT leg** | - rail |
| 4 | 1000 uF **LONG leg** | + rail |
| 5 | ESP32 **VIN** | + rail |
| 6 | ESP32 **GND** | - rail |
| 7 | ESP32 **RX2** (GPIO16, 6th pin down the left with USB at the top) | the 1N4007's **banded end** |
| 8 | 1N4007's other end | a spare row - the **junction** |
| 9 | **470 ohm** from the junction | + rail |
| 10 | the junction | strip **DIN** (green) |
| 11 | strip **+5V** | + rail |
| 12 | strip **GND** | - rail |

330 ohm works if there is no 470. No 10 kohm pulldown - the 470 ohm sets the
line's resting state. **Nothing goes to 3V3.**

Rows 11-12: on the bench the strip's power went through the breadboard rails,
which is acceptable at ABL 600-800 mA and not above. On the dot board the
strip's +5V, GND and the LED 70 injection pair go straight onto the bus wires
([PERFBOARD.md](PERFBOARD.md)); that is what allows ABL 2000.

**Power-up rule, every time:** adapter out of the wall before touching any
wire; ohms across the rails must not read near zero; mate the barrel before
switching on at the wall.

### 1.6 The chip test - DONE, chip eliminated

![CD74HCT112E wired as a level-shifting buffer](img/hct112-buffer.svg)

![Breadboard wiring for the chip test, with real ESP32 pin names](img/chip-test-breadboard.svg)

The shop supplied a CD74HCT112EX instead of a 74HCT125. A JK flip-flop can be
wired as a buffer through its asynchronous SET/RESET inputs, so it was tested:
pin 15 driven from the ESP32's 3V3 (3.17 V) and then from the 5 V rail, output
on pin 6.

> **RESULT 26 Sep 2026:** pin 6 follows a 5 V input and does **not** respond to
> 3.17 V. A true HCT input switches at 2 V; this one switches near 0.7 x VCC.
> It is an HC-threshold part in HCT marking. Eliminated.

### 1.7 First light - DONE

Node at 120 LEDs, ABL 600 mA, preset 9 = six 20-LED colour bands (RED, GREEN,
BLUE, WHITE, YELLOW, PINK), boot preset.

> **RESULT 26 Sep 2026, 1 m strip:** LED 1 steady and the commanded colour,
> junction 0.79 V low, rail 4.71 V loaded, **GRB confirmed** (red shows red),
> live control over Wi-Fi. The clamp works with margin on this strip.

**Never set the ABL cap or the mA/LED to 0** - that disables the limiter.
WLED's limiter is an estimate that reserves 120 mA for the ESP32.

---

## Level shifting - RESOLVED 26 Sep 2026

The diode clamp, by measurement. Full reasoning and the rejected options in
[DECISIONS.md](DECISIONS.md). No buffer IC exists anywhere in this project.

---

## Stage 2 - measure and plan - DONE

Strip path measured directly off the monitor back: **57 × 30.5 cm**.

```bash
python tools/led_layout.py --width 57 --height 30.5 --write
```

| Run | LEDs | Cut to |
|---|---|---|
| left | 18 | **30.0 cm** |
| top | 34 | **56.7 cm** |
| right | 18 | **30.0 cm** |
| **total** | **70** | 116.7 cm of the 2 m strip, **50 LEDs (83 cm) spare** with the DO connector on it |

`config/hyperion_leds.json` and `config/wled_desk_cfg.json` are committed. The
count is insensitive to width — 56 to 57.5 cm all give 34/18/18.

The monitor's back is **smoothly curved with no flat region**. Workable; see
Mounting in [HARDWARE.md](HARDWARE.md).

### Three sides, not four

Left, top and right, no bottom run. At desk height the bottom strip lights the
desk rather than the wall, it collides with the stand and the future arm, and
it costs two extra corner joints. Hyperion handles a missing bottom natively.

---

## Stage 3 - cut and solder - DONE 26 Sep 2026

![How a WS2812 corner joint is wired](img/corner-joint.svg)

**As built, in this order**, each step tested before the next:

1. Cut **70/71** first. Rehearsal joint: a 10 cm red/green/black lead onto the
   spare piece's fresh `Din` pads. Powered from the node: all 50 lit.
2. Injection tails, red +5V and black GND, **60 cm**, on LED 70's far-end
   pads. Nothing on `DO`.
3. Din leads on LED 1, **60 cm**: green on `DIN` first, then +5V, then GND.
   (Only 30 cm of red and black silicone wire was left, so the +5V and GND
   leads at LED 1 are JiffyTrails 22/24 AWG in other colours; colours to be
   recorded.) All 70 lit: RED / GREEN / BLUE / WHITE.
4. Tails measured while lit: **+4.43 V** at LED 70 against ~4.7 V at LED 1.
   Polarity right. Tails then into the rails.
5. Cut **18/19** -> corner 1 (three 4 cm wires, pieces soldered in a straight
   line, they bend to 90 degrees on the monitor) -> all 70 lit.
6. Cut **52/53** -> corner 2 -> all 70 lit.

Pieces: **P1 = 18 LEDs with the leads = LEFT run viewed from the front; P2 =
34 = top; P3 = 18 with the tails = RIGHT run.** Working from behind, P1 is
under your right hand.

**What was missed:** heat-shrink was not slid onto the wires before the
second ends were soldered. Recoverable - see Stage 4.

The technique, kept for the L4 build and any repair:

### Practise on the offcut first

The run uses 117 cm of the 2 m strip; 50 LEDs remain, with the DO connector
on their far end. **Do not cut practice pieces off that end.** The rehearsal
joint is the spare piece's own fresh `Din` pads (LED 71) after the 70/71 cut:
a 10 cm lead soldered there is a real joint on a piece that does not matter,
and it leaves the spare with a usable lead.

Three things decide whether soldering feels easy or impossible, and beginners
get all three wrong at once:

1. **A clean, tinned tip.** Wipe on a damp sponge or brass wool and melt fresh
   solder onto it every few joints. A blackened tip transfers almost no heat,
   so the joint will not take, so you hold the iron there longer, so you cook
   the LED. Nearly every "my iron is too weak" is this.
2. **Leaded 60/40 solder, not lead-free.** It melts lower and flows far more
   willingly. Wash your hands after.
3. **Do not crank the temperature.** About 330 °C. Hotter burns the flux off
   before it can work and lifts pads off the flexible PCB.

Ventilated spot, and do not lean into the smoke.

**Good joint:** shiny, smooth, slightly concave where it meets the pad.
**Bad:** dull and grainy (moved while cooling), or a ball sitting on top
without wetting it (not enough heat, or no flux — add flux, not more solder).

### Before any cut: check the arrows and the corners

On the **uncut** strip confirm the printed arrows point *away* from the bare
`Din` end. After each cut, lay the pieces in the U and confirm **every arrow
points the same way round** — up the left, across the top, down the right —
and that the marked +5V edge is on the same side (all outside, or all inside)
on all three pieces. A piece fitted backwards lights nothing downstream of it.

**Corners:** the top piece runs the full width; each side piece tucks *under*
the end of the top piece, its cut edge ~5 mm below the top piece's lower edge.
The pad-to-pad gap is 5–10 mm; corner wires are cut at 4 cm and trimmed.

### Cutting

Cut **down the middle of the copper pads**, on the marked line, so both halves
keep half a pad each. Sharp scissors. If the strip is silicone-sleeved, trim
8–10 mm back to expose the pads.

### Soldering

The chip sits a couple of millimetres from its pads, and heat is what kills it.

1. Flux the pads.
2. **Tin each pad** — iron plus a little solder, 1–2 s, off. A small dome.
3. **Tin the wires** — stripped 3 mm, twisted, tinned, tinned end trimmed to
   ~2 mm. If heat-shrink is going on, **slide it onto the wire now**, before
   the second end is soldered.
4. **Join** — hold the tinned wire on the tinned pad, iron 1–2 s until the two
   pools flow together, remove the iron, then **hold still until it sets**.
5. If it will not take, add flux and retry briefly. Never hold the iron longer.

Tinning both sides first is the whole trick — it turns a four-handed job into
one easy motion. Clamp the pieces at the actual 90° in the helping hands so the
wires come out the right length.

| Upstream | Wire | Downstream |
|---|---|---|
| +5V | red | +5V |
| DO / DOUT | green | DI / DIN |
| GND | black | GND |

**Match pad names, not positions** — at a corner one strip is rotated 90°.
Solder the **middle (data) wire first**, then the two edge wires; 22 AWG is
chunky for 3.3 mm pad pitch and the middle one is the hardest to reach last.
Tape the strip flat and tape each wire to the bench 3 cm from the pad before
soldering — a flopping 60 cm lead peels a half-pad off the flex.

### Test after every connection, not at the end

- Continuity across each join as you make it.
- Check for bridges **between adjacent pads** — especially +5 V to GND, which
  is a dead short across the supply.
- Heat-shrink or hot glue over each finished joint. It is the weakest
  mechanical point on the run and it is about to live on a curved surface.

Then test the assembled U **flat on the bench** before any backing paper comes
off. That is the last reversible moment.

---

---

## Stage 4 - protect the joints - NEXT, before anything else

Every joint on the strip is held by half a copper pad. Do this before the
board and before the monitor.

1. **Strip ends (LED 1, LED 70, the spare's lead):** the far ends of these
   wires are still free, so heat-shrink still goes on. Pull the wires out of
   the breadboard, slide **one wide tube over the whole bundle** from the free
   end, push it down until it covers the strip's three pads, shrink it with a
   moving lighter flame or the iron's barrel held near. If no tube in the
   assortment fits over the 10 mm strip, **hot glue over the pads** instead.
2. **The two corner joints:** both ends are soldered, so no tube - a blob of
   **hot glue** over each joint, or a wrap of insulation tape.

**Rule for every future joint: slide the heat-shrink onto the wire before the
second end is soldered.**

---

## Stage 5 - the dot board - NEXT

[PERFBOARD.md](PERFBOARD.md), hole by hole, with both faces drawn. The
breadboard is dismantled part by part as the board is built; the ESP32 and
its WLED config move last.

---

## Stage 6 - mount

1. Tack-It test patch on hidden paint while the IPA dries.
2. IPA the back panel and let it flash off.
3. Stick down starting at the **LED 1 corner** (bottom-left from the front),
   P1 up, P2 across, P3 down. Side pieces tuck under the ends of the top piece.
   Velcro tie or hot glue at each corner turn - peel starts at a corner.
4. Push the real config and verify orientation:

```bash
python tools/led_layout.py --width 57 --height 30.5 --abl 2000 --write
python tools/wled_push.py apply   --host wled-desk.local
python tools/wled_push.py walk    --host wled-desk.local
python tools/wled_push.py presets --host wled-desk.local
```

`walk` must happen before Hyperion is configured. Note which corner LED 1 sits
in **viewed from the front** and which way the pixel travels. If it runs the
wrong way, regenerate the Hyperion layout; with skip 0 the WLED "Reversed"
flag is also harmless on this symmetric U, but pick one fix, not both.

---

## Stage 7 - Hyperion

[HYPERION.md](HYPERION.md).
