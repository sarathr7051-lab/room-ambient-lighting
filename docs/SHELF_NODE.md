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
| gate resistor | **use a 470 ohm from the desk-node spares.** The blue-green resistors look like 10 k too, and 470 is actually the better value here: the D1 mini's pin then peaks at 7 mA (a 100 ohm would push 33 mA, above the ESP8266's 12 mA rating). Anything 100-1000 ohm works |
| D1 mini | **no headers**. The two control wires are soldered straight into the **D2** and **G** holes - 2 joints, no headers |
| 12 V input | the owner's **spare female DC barrel pigtail** (red/black leads, same kind as the desk node's). The adapter plugs into it; it feeds the board. **The Gesto strip's factory socket cable is NOT cut** - it stays on the leftover length, which keeps working as a plain light on its own |

## The circuit

```
12 V adapter +  ──── strip A +  ──── strip B +        (three-way splice, OFF the board)

strip A −  ──── strip B −  ─────────► IRL540N DRAIN   (one wire to the board; splice off-board)

IRL540N SOURCE ◄──── 12 V adapter −
IRL540N SOURCE ◄──── D1 mini G

IRL540N GATE ◄── 470 ohm ◄── D1 mini D2
IRL540N GATE ◄── 10 kohm ──► IRL540N SOURCE

D1 mini micro-USB ◄── phone charger.  On the D1 mini: D2, G, USB. Nothing else.
```

TO-220 pin order, **label facing you, legs pointing down: G - D - S, left to
right.** The metal tab on the back is DRAIN: it must touch nothing.

Facts a beginner might otherwise "improve":
- **No flyback diode.** The strip is LEDs plus resistors, essentially a
  resistive load. A diode across it does nothing useful and, fitted the wrong
  way, shorts the supply.
- **470 ohm is right.** The gate takes a 7 mA blip for 5-10 microseconds
  per edge at 880 Hz PWM - 2 % of the period; the resistor just softens the
  edge and keeps the D1 mini's pin inside its 12 mA rating.
- **Heat:** at 3.3 V on the gate the IRL540N passes 1 A with 0.1-0.5 W of
  heat depending on the individual part. Warm to the touch is normal, no
  heatsink. **Hot** means the part is an IRF, a gate-drain bridge, or the gate
  is not reaching 3.3 V.
- **The one thing that kills the D1 mini:** a solder bridge between the gate
  and drain cones puts 12 V onto D2 through the 470 ohm. That is why the
  gate-to-drain meter check happens **before** the D2 wire is connected.
- The 10 k keeps the strip off while the D1 mini boots, whichever supply
  comes up first. Power-up order does not matter.

## Cut plan (decided 29 Sep: factory socket end kept)

The Gesto strip is **5 m (500 cm)**, cut marks every ~3 cm (small white
marks seen through the silicone on the LED face). One end has the factory
socket cable; the other end has a factory **end cap**.

Work from the **end-cap end**:

| Piece | Length | Ends |
|---|---|---|
| **A** (under the top shelf) | first ~125 cm from the cap | far end = factory cap (already sealed); cut end = gets 2 wires |
| **B** (under the middle shelf) | next ~125 cm | both ends cut: one gets 2 wires, the other is sealed with heat-shrink/tape |
| **Leftover** | ~250 cm | its cut end is sealed; its factory socket end is untouched - plug the adapter straight in and it is a plain always-on light |

**Why ~125 cm, not 130:** the shelves measure 130 cm wall to wall; the strip
needs room at the wire end for the soldered joint and the bend of the wires,
and a cut can only fall on a mark. Hold the strip under the shelf first and
cut at **the last mark that leaves ~3-5 cm clear at the wire end**. Measure,
do not add up.

**Shelf light current:** two ~125 cm pieces, about 1 A together, from the
12 V 2 A adapter. The leftover is never powered at the same time from this
adapter.

## Stage 1 - breadboard test (nothing permanent)

The desk node's breadboard is free. One strip piece (about 0.5 A) is fine
through two breadboard tie-strips for a ten-minute test; not for keeps.

Hold the breadboard with its **numbered rows running away from you** (row 1
nearest you). Each numbered row is one 5-hole tie-strip.

| # | From | To |
|---|---|---|
| 1 | IRL540N | legs into **three consecutive numbered rows of one lettered column**, so the line of legs runs away from you. Stand it with the **printed label facing your RIGHT hand, metal tab to your left**. Seen from the label side with legs down the order is G-D-S left to right, and with the label on your right "left" is toward you: **G in the nearest row, D next, S furthest.** Each leg in its own row - if all three land in one row they are shorted together. The body-diode check below confirms D and S |
| 2 | 470 ohm | from the G row to a spare row **X** |
| 3 | 10 kohm | from the G row to the S row |
| 4 | spare DC pigtail **−** | S row |
| 5 | D1 mini **G** wire | S row |
| 6 | spare DC pigtail **+** and piece A **+** wire | twisted together and **taped** - not on the breadboard |
| 7 | piece A **−** wire | D row |
| 8 | D1 mini **D2** wire | row X - **last, after the meter checks** |
| 9 | D1 mini micro-USB | phone charger |

**Before the pigtail: identify its + wire.** Colours are a guess, the meter is not.
1. **Adapter out.** Ω **200**: one probe inside the pigtail's socket on the
   **centre pin**, the other on each wire in turn. The one reading ~0 is **+**
   (12 V LED adapters are centre-positive; the label symbol confirms it).
2. Tape the two bare ends to the table 5 cm apart. Adapter into the pigtail
   and the wall, **DCV 20**, red probe on the + wire: **+12**. A minus sign
   means the probes are swapped, not the wires. **Adapter out.**
Never hold two live bare wires in your fingers.

**Piece A's wires** (needed for this test): cut piece A as in the cut plan,
then wire its cut end as described under "Wiring a cut end" below. 40 cm
wires are enough for piece A (it sits right by the board).

**Meter checks, D2 wire NOT connected, adapter out** (red lead is + on the
ohms and diode ranges):
- Ω **20k**, G row to S row, either way: **9.5-10.5** (the 10 k).
- Ω **2000**, red on D row, black on S row: `1`. Swap the probes: **a number** -
  that is the MOSFET's internal body diode, normal, and it confirms which leg
  is D and which is S.
- Ω 2000, G row to D row, both ways: `1`. A number = a bridge; do not go on.

Then connect D2 (row 8), charger into the D1 mini, adapter into the socket.
If the strip stays dark, power off and swap the strip's two wires - a reversed
strip is dark, and a second or two reversed does no harm; minutes might.
In the WLED page for `wled-shelf`: brightness up - the strip lights; down -
it dims; off - out. Dim at full brightness with a warm FET = wrong part or a
bad gate joint.

## Stage 2 - the dot board

Second LABTECH board, same orientation as the desk node: white side up, row
numbers on your left, 001 at the top. Columns counted from the numbered edge:
**N = 17th, M = 18th, L = 19th, K = 20th, J = 21st.** Flip it **left-to-right
like a page** to solder - 001 stays at the top, the letters then read
normally. About 12 joints. Four wires from outside reach the board: D2, G,
pigtail −, strip −.

Column **K, rows 006-012, stays empty on the top side**: the MOSFET's drain
tab faces that way and sits right over it.

| Part / wire | Holes | Note |
|---|---|---|
| IRL540N | **G L008, D L009, S L010** | standing upright on its leg shoulders (body 3-4 mm off the board), **label facing the numbered edge**, tab facing column K. Sanity check: turn the board so the numbered edge is nearest you - 001 is now on your left - hold the FET label toward you, and G-D-S left to right lands on 008-009-010 |
| 470 ohm | **L004** and **L007**, flat along column L above the FET | underside: the L007 leg bent one pitch **down column L** onto the **G cone L008**, soldered with it, cut at the cone. (Kept in column L so no gate metal runs beside the drain wire on row 009) |
| 10 kohm | **J008** and **J010**, **standing upright** (one leg straight down through J008, the other hairpinned over the top and down through J010, sleeved like the desk node's 470) | underside: J008 leg bent **two pitches along row 008**, laid on the **007 side** of the K008 pad, onto the **G cone L008**; J010 leg bent along row 010 onto the SOURCE bus. Both cut at the cone |
| SOURCE bus | bare wire along **row 010, J010 to N010**, laid on the **011 side** of the holes | soldered at J010 (10 k leg), L010 (S leg), M010, N010 |
| 12 V pigtail **−** | **M010** | onto the SOURCE bus |
| D1 mini **G** wire | **N010** | onto the SOURCE bus |
| strip **−** (one wire; A and B spliced off-board) | **M009** | underside: bent one pitch onto the **D cone L009**, cut at the cone |
| D1 mini **D2** wire | **L003** | underside: bent one pitch onto the 470 ohm's leg cone at **L004**. **Soldered last, after the meter checks** |

**Off the board, two splices**, each twisted, soldered, and covered with
heat-shrink slid on **before** soldering:
- **+12 V:** pigtail + , piece A + , piece B + . Three wires, one splice. No
  +12 V anywhere on the board.
- **strip −:** piece A − , piece B − , and the single wire to M009.

Three cones one pitch apart carry gate, drain and source (L008/L009/L010) -
that is the TO-220's own pitch and is normal. Rules: small cones; every bent
leg lies beside the pads, not over the holes, and is **cut at the cone, never
past it**; the L008 cone is reflowed once with both bent legs in it. With the
470 in column L and the 10 k on the J side, no bare gate metal runs next to
the drain wire on row 009.

**Meter, D2 wire not yet soldered, adapter out:**
- Ω **20k**, L008 to L010: **9.5-10.5**.
- Ω **2000**, red L009, black L010: `1`; swapped: a number (body diode, normal).
- **Diode range**, red L010, black L009: about 500-700; swapped: `1`.
- Ω 2000, L008 to L009, both ways: `1`. A number = gate-drain bridge - fix
  before anything else.
Then solder the D2 wire at L003.

**Wiring a cut end (piece A's cut end, piece B's board end).** Cut exactly **on** a mark so both
halves keep half-pads. Do not slice down onto the strip inside - its copper is
thin. Instead score the silicone all the way round, 8 mm from the end, with a
blade, then **pull the sleeve off the end**; the flat strip inside slides out
of the silicone like a wire out of insulation. The two pads are on the LED
face, marked **+ / −** (or 12V / GND). If the print is unreadable: wire it
either way, power for a second - dark means reversed, swap. Don't leave it
reversed for minutes. Tin the pads, slide heat-shrink over the wires, solder, shrink it
down over the joint. **Every cut end that gets no wires - piece B's far end and the leftover's cut
end - gets heat-shrink or tape over the exposed copper.** Piece A's far end
is the factory cap and needs nothing.

**Mounting:** the board's underside is bare 12 V cones - a piece of card or
tape over it before it is stuck to anything. Double-sided tape to the shelf
underside, near the router. The four wires get a velcro tie 3 cm out. **The D1
mini is mounted too** (tape or velcro next to the board): its two wires are
soldered straight into plated holes, and a free-hanging wire lifts a pad after
a few flexes - the D1 mini must never hang by its wires, and a tape blob over
both wires 1 cm from the D1 mini takes the strain.

## Wires to cut

| Wire | Length |
|---|---|
| D1 mini D2 and G | 15 cm each, 24 AWG stranded, 3 mm stripped and tinned, in from the top of the D1 mini, soldered underneath, trimmed |
| 12 V input | the spare DC pigtail, as it is - nothing cut |
| piece B + and − | **50 cm each** (29.5 cm down + across + slack), 24 AWG |
| piece A + and − | **40 cm each**, soldered to its cut end |

## WLED

`wled-shelf` is already set: PWM White on GPIO4 (D2), Wi-Fi sleep off, force
802.11g, UDP sync receive on - it follows the desk node's moods. Brightness
100 % = full strip; the moods scale it.
