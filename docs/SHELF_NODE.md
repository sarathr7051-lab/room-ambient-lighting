# Shelf node (L4): D1 mini + IRL540N driving the 12 V neon

One MOSFET switches the 12 V neon on and off (and dims it by PWM); the Wemos
D1 mini running WLED drives the MOSFET's gate. Nothing else. The 12 V never
touches the D1 mini; the D1 mini runs off a phone charger.

## Parts - photograph these before anything is wired

The desk build taught us the shop can hand over the wrong chip. Check the
markings:

| Part | What the marking must say | Why it matters |
|---|---|---|
| MOSFET | **IRL540N** (IRL, with an L) | logic-level: switches fully on with the D1 mini's 3.3 V. An **IRF540N** looks identical and only half-opens at 3.3 V - the strip would be dim and the FET would get hot |
| 100 ohm resistor | bands **brown - black - brown** | gate series resistor |
| 10 kohm resistor | bands **brown - black - orange** | gate pull-down: keeps the strip OFF while the D1 mini boots |
| D1 mini | headers soldered or loose? female or male? | decides how the two control wires attach |
| Gesto socket lead | the short white lead between the strip's end cap and the barrel socket | it gets cut ~10 cm from the socket; the socket half becomes the 12 V input pigtail |

## The circuit

```
12 V adapter +  ───────────────┬──── strip A +
                               └──── strip B +

strip A −  ──┐
strip B −  ──┴──── IRL540N DRAIN  (D, middle leg; the metal tab is also drain)

IRL540N SOURCE (S) ───┬──── 12 V adapter −
                      └──── D1 mini G

IRL540N GATE (G) ◄── 100 ohm ◄── D1 mini D2
IRL540N GATE (G) ◄── 10 kohm ──► IRL540N SOURCE (S)

D1 mini micro-USB ◄── phone charger. Nothing else on the D1 mini.
```

TO-220 pin order, **label facing you, legs pointing down: G - D - S, left to
right.**

Current: the 12 V 2 A adapter drives 5 m; two 130 cm pieces draw about 1 A
together. At 3.3 V on the gate an IRL540N passes that with well under a
quarter of a watt of heat - no heatsink.

## Stage 1 - breadboard test (10 minutes, nothing permanent)

The desk node's breadboard is free. One strip piece (about 0.5 A) is fine
through breadboard contacts for a test; do not leave it there.

| # | From | To |
|---|---|---|
| 1 | IRL540N | three adjacent rows, label toward you. G in the top row, D middle, S bottom |
| 2 | 100 ohm | from the G row to a spare row X |
| 3 | 10 kohm | from the G row to the S row |
| 4 | D1 mini **D2** (Dupont wire) | row X |
| 5 | D1 mini **G** | S row |
| 6 | Gesto socket pigtail **−** | S row |
| 7 | Gesto socket pigtail **+** | strip piece **+** (twist together, or both into one spare row) |
| 8 | strip piece **−** | D row |
| 9 | D1 mini micro-USB | phone charger |

Order of power-up: D1 mini charger first (it boots with the strip off, that is
what the 10 k is for). Then the 12 V adapter into the socket pigtail.

Meter checks before the 12 V goes in, adapter unplugged: ohms G-row to S-row
= about **10 k**. D-row to S-row = `1`. If D-S reads low, the FET is in
backwards or the wrong part.

Then in the WLED page for `wled-shelf`: brightness slider up - the strip
lights; down - it dims; off - it goes out. If it only gets dim at full
brightness and the FET warms, the marking said IRF, not IRL.

## Stage 2 - the dot board

Second LABTECH board, same orientation as the desk node: white side up, row
numbers on the left, 001 at the top; columns counted from the numbered edge
(L = 19th, K = 20th, J = 21st, M = 18th, N = 17th, O = 16th, I = 22nd). About
16 joints.

| Part / wire | Holes | Note |
|---|---|---|
| IRL540N | **G L008, D L009, S L010** | standing upright, **label facing the numbered edge**. Legs straight, 2.54 mm apart, no splaying. The metal tab faces away from the numbers and touches nothing |
| 100 ohm | **M004** and **M008** | lying flat along column M. Underside: the M008 leg is bent one pitch onto the **G cone at L008** and soldered with it |
| 10 kohm | **K008** and **K010** | standing upright (hairpin, sleeved like the desk node's 470). Underside: K008 leg bent onto the **G cone L008**; K010 leg joins the SOURCE bus |
| SOURCE bus | bare wire along **row 010, K010 to N010**, beside the holes | soldered at K010 (10 k leg), L010 (S leg), M010, N010 |
| 12 V pigtail **−** | **M010** | onto the SOURCE bus |
| D1 mini **G** wire | **N010** | onto the SOURCE bus |
| D1 mini **D2** wire | **M003** | underside: bent onto the 100 ohm leg cone at **M004** |
| strip A − and strip B − | twisted together, tinned, through **M009** | underside: bent onto the **D cone at L009**, one joint |
| 12 V pigtail **+**, strip A **+**, strip B **+** | twisted together, tinned, through **I014** | one joint; nothing else on that pad. Slide heat-shrink over the three wires first |

Nothing bare may bridge L008 - L009 - L010: three cones one pitch apart carry
gate, drain and source. Small cones, and the meter afterwards.

**Meter, before power** (ohms 2000): L008 to L010 = about 10 k. L009 to L010
= `1`. L008 to L009 = `1`. I014 to anything = `1`.

**Strain relief:** a velcro tie round the seven wires 3 cm from the board,
and the board velcro-tied to the shelf underside or the router.

## Wires to cut

| Wire | Length |
|---|---|
| D1 mini D2 and G (2) | 15 cm each - the D1 mini sits next to the board |
| Gesto socket pigtail | cut the factory lead **10 cm from the socket**; the strip-side stub stays on piece A |
| piece B + and − (2) | **50 cm each** (29.5 cm down + across + slack), 24 AWG is fine |
| piece A + and − | its own factory stub, ~10 cm, reaches the board |

## WLED

`wled-shelf` is already set: PWM White on GPIO4 (D2), Wi-Fi sleep off, force
802.11g, UDP sync receive on - it follows the desk node's moods. Brightness
100 % = full strip; the moods scale it.
