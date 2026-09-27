# Shelf node (L4): D1 mini + IRL540N driving the 12 V neon

One MOSFET switches the 12 V neon on and off (and dims it by PWM); the Wemos
D1 mini running WLED drives the MOSFET's gate. The D1 mini runs off a phone
charger. **Only the +12 V never reaches the D1 mini.** The 12 V adapter's
minus and the D1 mini's G are deliberately joined - that shared ground is what
lets the gate signal mean anything. Reviewed independently 27 Sep 2026; this is
the reworked version.

## Parts - verified 27 Sep

| Part | Status |
|---|---|
| MOSFET | marking reads **IRL540** (Vishay) - logic-level, correct. An IRF540 would only half-open at 3.3 V |
| 10 kohm | tan body, brown-black-orange-gold. Confirm on the meter, **Ω 20k range: about 10.0** |
| 100 ohm | blue-green body - **measure it**: Ω 2000 range reads about 100. If it turns out to be another 10 k, use a **330 or 470 ohm** from the desk-node spares; anything 47-470 ohm does the job |
| D1 mini | **no headers**. The two control wires are soldered straight into the **D2** and **G** holes - 2 joints, no headers |
| Gesto socket lead | short white lead between the strip's end cap and the barrel socket. It gets cut 10 cm from the socket; the socket half becomes the 12 V input pigtail |

## The circuit

```
12 V adapter +  ──── strip A +  ──── strip B +        (three-way splice, OFF the board)

strip A −  ──── strip B −  ─────────► IRL540N DRAIN   (one wire to the board; splice off-board)

IRL540N SOURCE ◄──── 12 V adapter −
IRL540N SOURCE ◄──── D1 mini G

IRL540N GATE ◄── 100 ohm ◄── D1 mini D2
IRL540N GATE ◄── 10 kohm ──► IRL540N SOURCE

D1 mini micro-USB ◄── phone charger.  On the D1 mini: D2, G, USB. Nothing else.
```

TO-220 pin order, **label facing you, legs pointing down: G - D - S, left to
right.** The metal tab on the back is DRAIN: it must touch nothing.

Facts a beginner might otherwise "improve":
- **No flyback diode.** The strip is LEDs plus resistors, essentially a
  resistive load. A diode across it does nothing useful and, fitted the wrong
  way, shorts the supply.
- **100 ohm is right.** The gate draws a ~25 mA blip for a couple of
  microseconds per edge at 880 Hz PWM; the resistor just softens the edge.
- **Heat:** at 3.3 V on the gate the IRL540N passes 1 A with 0.1-0.5 W of
  heat depending on the individual part. Warm to the touch is normal, no
  heatsink. **Hot** means the part is an IRF, or the gate is not reaching 3.3 V.
- **The one thing that kills the D1 mini:** a solder bridge between the gate
  and drain cones puts 12 V onto D2 through the 100 ohm. That is why the
  gate-to-drain meter check happens **before** the D2 wire is connected.
- The 10 k keeps the strip off while the D1 mini boots, whichever supply
  comes up first. Power-up order does not matter.

## Stage 1 - breadboard test (nothing permanent)

The desk node's breadboard is free. One strip piece (about 0.5 A) is fine
through two breadboard tie-strips for a ten-minute test; not for keeps.

Hold the breadboard with its **numbered rows running away from you** (row 1
nearest you). Each numbered row is one 5-hole tie-strip.

| # | From | To |
|---|---|---|
| 1 | IRL540N | legs into **three consecutive numbered rows, same lettered column**, label facing **you**: G nearest you, D next, S furthest. Each leg in its own row - if all three land in one row they are shorted together |
| 2 | 100 ohm | from the G row to a spare row **X** |
| 3 | 10 kohm | from the G row to the S row |
| 4 | Gesto socket pigtail **−** | S row |
| 5 | D1 mini **G** wire | S row |
| 6 | Gesto socket pigtail **+** and strip piece **+** | twisted together and **taped** - not on the breadboard |
| 7 | strip piece **−** | D row |
| 8 | D1 mini **D2** wire | row X - **last, after the meter checks** |
| 9 | D1 mini micro-USB | phone charger |

**Before the pigtail: identify its + core.** After cutting the socket lead,
find the core with a stripe or rib, or mark one core with a Sharpie along its
length. Adapter into the socket and the wall, **DCV 20**, black probe on one
core, red on the other: **+12** = red is on +. Mark it. **Adapter out.** The
same-marked core on the strip-side stub is piece A's +. Bare ends apart at all
times while the adapter is in.

**Meter checks, D2 wire NOT connected, adapter out** (red lead is + on the
ohms and diode ranges):
- Ω **20k**, G row to S row, either way: **9.5-10.5** (the 10 k).
- Ω **2000**, red on D row, black on S row: `1`. Swap the probes: **a number** -
  that is the MOSFET's internal body diode, normal, and it confirms which leg
  is D and which is S.
- Ω 2000, G row to D row, both ways: `1`. A number = a bridge; do not go on.

Then connect D2 (row 8), charger into the D1 mini, adapter into the socket.
In the WLED page for `wled-shelf`: brightness up - the strip lights; down -
it dims; off - out. Dim at full brightness with a warm FET = wrong part or a
bad gate joint.

## Stage 2 - the dot board

Second LABTECH board, same orientation as the desk node: white side up, row
numbers on your left, 001 at the top. Columns counted from the numbered edge:
**N = 17th, M = 18th, L = 19th, K = 20th, J = 21st.** Flip it **left-to-right
like a page** to solder, exactly as before; the letters then read normally.
About 12 joints.

Column **K, rows 006-012, stays empty on the top side**: the MOSFET's drain
tab faces that way and sits right over it.

| Part / wire | Holes | Note |
|---|---|---|
| IRL540N | **G L008, D L009, S L010** | standing upright on its leg shoulders (body 3-4 mm off the board), **label facing the numbered edge**, tab facing column K. Sanity check: turn the board so the numbered edge is nearest you - 001 is now on your left - hold the FET label toward you, and G-D-S left to right lands on 008-009-010 |
| 100 ohm | **M004** and **M008**, flat along column M | underside: the M008 leg bent one pitch onto the **G cone L008**, soldered with it, cut at the cone |
| 10 kohm | **J008** and **J010**, flat along column J | underside: J008 leg bent **two pitches along row 008** (over the empty K008 pad) onto the **G cone L008**; J010 leg bent along row 010 onto the SOURCE bus. Both cut at the cone |
| SOURCE bus | bare wire along **row 010, J010 to N010**, laid on the **011 side** of the holes | soldered at J010 (10 k leg), L010 (S leg), M010, N010 |
| 12 V pigtail **−** | **M010** | onto the SOURCE bus |
| D1 mini **G** wire | **N010** | onto the SOURCE bus |
| strip **−** (one wire; A and B spliced off-board) | **M009** | underside: bent one pitch onto the **D cone L009**, cut at the cone |
| D1 mini **D2** wire | **M003** | underside: bent onto the 100 ohm leg cone at **M004**. **Soldered last, after the meter checks** |

**Off the board, two splices**, each twisted, soldered, and covered with
heat-shrink slid on **before** soldering:
- **+12 V:** pigtail + , piece A + , piece B + . Three wires, one splice. No
  +12 V anywhere on the board.
- **strip −:** piece A − , piece B − , and the single wire to M009.

Three cones one pitch apart carry gate, drain and source (L008/L009/L010) -
that is the TO-220's own pitch and is normal. Rules: small cones; every bent
leg runs along its own row and is **cut at the cone, never past it**; the L008
cone is reflowed once with both bent legs in it.

**Meter, D2 wire not yet soldered, adapter out:**
- Ω **20k**, L008 to L010: **9.5-10.5**.
- Ω **2000**, red L009, black L010: `1`; swapped: a number (body diode, normal).
- **Diode range**, red L010, black L009: about 500-700; swapped: `1`.
- Ω 2000, L008 to L009, both ways: `1`. A number = gate-drain bridge - fix
  before anything else.
Then solder the D2 wire at M003.

**Piece B - the cut end that gets wires.** Cut on a mark. Trim ~8 mm of the
silicone sleeve off the end to expose the internal strip's two pads. They are
marked **+ / −** (or 12V / GND) on the strip's print; if the print is
unreadable, either way round is safe - a reversed strip is just dark, swap
the wires. Tin the pads, slide heat-shrink over the wires, solder, shrink it
down over the joint. **Every cut end - piece A's far end, piece B's far end,
the spare's ends - gets heat-shrink or tape over the exposed copper.**

**Mounting:** the board's underside is bare 12 V cones - a piece of card or
tape over it before it is stuck to anything. Velcro or double-sided tape to
the shelf underside, near the router. Eight wires arrive at the board (D2, G,
pigtail −, strip −, plus the splices' leads); a velcro tie round them 3 cm out.

## Wires to cut

| Wire | Length |
|---|---|
| D1 mini D2 and G | 15 cm each, soldered into the D1 mini's D2 and G holes |
| Gesto socket pigtail | factory lead cut **10 cm from the socket**; the strip-side stub stays on piece A |
| piece B + and − | **50 cm each** (29.5 cm down + across + slack), 24 AWG |
| piece A + and − | its own ~10 cm factory stub reaches the splices |

## WLED

`wled-shelf` is already set: PWM White on GPIO4 (D2), Wi-Fi sleep off, force
802.11g, UDP sync receive on - it follows the desk node's moods. Brightness
100 % = full strip; the moods scale it.
