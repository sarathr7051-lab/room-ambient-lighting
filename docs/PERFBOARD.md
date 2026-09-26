# Desk node on the dot board

The bench circuit, moved off the breadboard onto one of the 6 x 4 inch
isolated-pad dot boards. Same circuit, same seven parts, nothing new to buy.
Breadboard contacts are good for about 1 A; the dot board with two bus wires is
what lets ABL go to 2000 mA. This is the first dot board the owner has built,
so it is written for that.

![Dot board layout - top and underside](img/perfboard-layout.svg)

Hole positions are **(column, row)**, counted from the **corner mark**: a
notch or marker dot you put on one corner of the board before anything else.
Column 1 is the corner-mark column, row 1 the corner-mark row. The ESP32's USB
socket faces the top edge.

## Three things a dot board does differently from a breadboard

1. **Nothing is connected until you connect it.** Every hole is its own copper
   ring. On the breadboard, five holes in a row were joined for you. Here you
   join them yourself, two ways:
   - **A bus:** a bare tinned wire laid along a row of holes on the underside,
     soldered at every pad. Anything pushed through one of those holes gets
     soldered into the same blob and is on the bus. This layout has two: +5V
     and GND.
   - **A bent leg:** push a component leg through, and on the underside bend it
     flat across to the next pad, then solder. The diode's plain-side leg is
     bent along four pads to make the junction.
2. **It is mirrored when you flip it.** You place parts from the top and solder
   from the underside, and when the board is upside down, column 25 is on the
   left. That is how beginners solder the right thing into the wrong hole.
   **Mark one corner** with a marker on both faces before you start, and find
   it every time you turn the board over. The diagram shows both views.
3. **Solder is permanent, but not that permanent.** A part in the wrong hole
   comes out: heat the joint, pull the leg with pliers while it is molten. A
   pad lifts only if you keep the iron on for many seconds. Two or three
   seconds per joint, always.

## The joint itself

Every joint is the same motion:

1. Leg or wire through the hole from the top. Bend it slightly on the
   underside so it cannot fall out.
2. Iron tip touching **both the pad and the leg** at once, for 1 second.
3. Feed solder into the joint, not onto the iron, until it flows round the
   leg and makes a small cone. About the size of a grain of rice.
4. Iron off. Do not move the leg for 2 seconds.
5. Cut the leg 1-2 mm above the cone with side cutters.

Good: a shiny cone that wets the pad and the leg. Bad: a ball sitting on the
leg without touching the pad (not enough heat on the pad), or a dull grainy
blob (moved while cooling). Pads are 2.54 mm apart; if solder joins two
neighbouring pads that are not meant to be joined, drag a clean hot tip through
the gap, or add flux and touch again - the solder pulls back to the pads.

Clean the tip on the sponge every few joints. A black tip transfers no heat,
and the answer is never "hold it longer".

## The parts and where they go

| Part | Holes | Note |
|---|---|---|
| Female header, 15 pins | column 5, rows 3-17 | left row of the ESP32 |
| Female header, 15 pins | column 15, rows 3-17 | right row |
| +5V bus, bare tinned wire | column 19, rows 2-12 | underside |
| GND bus, bare tinned wire | column 23, rows 2-12 | underside |
| Link, red, insulated | VIN pin (15,3) to (19,3) | underside |
| Link, black, insulated | GND pin (15,4) to (23,4) | underside |
| Link, green, insulated | RX2 pin (5,8) to (17,8) | underside, passes under the ESP32 |
| 1N4007 | band end (18,8), plain end (21,8) | **band toward the ESP32**. Underside: band-side leg bent across to (17,8) and soldered with the green link; plain-side leg bent down column 21 and soldered at rows 8, 9, 10, 11 = the **junction** |
| 470 ohm | (19,10) to (21,10) | one leg on the +5V bus, one on the junction. Stand it upright if it will not lie flat in two holes |
| 1000 uF | LONG leg (19,12), striped SHORT leg (23,12) | bend the legs apart to reach 4 holes |
| 0.1 uF | (19,2) and (23,2) | no polarity |
| Pigtail red | (19,5) | |
| Pigtail black | (23,5) | |
| LED 1 +5V wire | (19,6) | |
| LED 1 GND wire | (23,6) | |
| LED 1 green DIN wire | (21,11) | onto the junction |
| LED 70 red tail | (19,7) | |
| LED 70 black tail | (23,7) | |

The 3V3 pin and the second GND pin are not used. Nothing else touches the
ESP32.

The ESP32's two pin rows are drawn 10 holes apart. **Do not trust the drawing
for that number** - push the headers onto the ESP32 first and let the board
tell you where they land. If they land at columns 5 and 14, every other
position stays the same; only the link lengths change by a hole.

## Assembly order

Adapter unplugged from the wall throughout. Pull the seven parts from the
breadboard only when you reach their step - the breadboard circuit is the
fallback until the dot board lights the strip. Low parts first, tall parts
last, so the board lies flat on the bench while you solder.

**0. Corner mark and board size.** Marker dot on one corner, both faces. The
full board is 15 x 10 cm and does not need cutting. If you want it smaller,
do it now, not later: score along a row of holes on both faces with a knife
against a ruler, 5-6 passes each side, then snap over a table edge. Anything
from 27 x 20 holes up works for this layout.

**1. Headers.** Cut two 15-pin lengths from a female header strip: cut
through the *16th* pin position with side cutters; that pin is lost, which is
normal. Push both headers onto the ESP32's pins. Place the whole thing on the
board, USB at the top, so the headers drop into columns 5 and 15 (or wherever
they land - see above), rows 3-17. Turn the board over with the ESP32 still
plugged in; it holds the headers square. Solder **one pin at each end of each
header** (4 joints). Turn it back, check both headers sit flat and the ESP32 is
parallel to the board. If not, reheat that one joint and press. Then solder
the other 26. Unplug the ESP32 and put it aside - it goes back on last.

**2. Buses.** Two lengths of wire, 8 cm each, insulation stripped off
completely, strands twisted tight, tinned along the whole length. Underside:
lay one along column 19 from row 2 to row 12. Solder it at row 2 and row 12
first so it stays put, then at every pad between. Same for column 23. Trim
the ends. **They must not touch each other or anything else** - there are
three empty columns between them; keep them empty.

**3. Links.** Three insulated wires, 22 AWG is fine:
- Red, about 12 cm: strip 5 mm at both ends. One end wraps once round the
  **VIN** header pin at (15,3) on the underside - solder it to that pin. Other
  end goes through hole (19,3) from the top and is soldered to the +5V bus
  underneath.
- Black, same, GND pin (15,4) to (23,4).
- Green, about 32 cm: RX2 pin (5,8), running under the ESP32 to hole (17,8).
Links are on the underside, so they run flat against the board under the
ESP32. Tape them down with a bit of tape if they will not stay.

**4. Diode.** Band end at (18,8), plain end at (21,8), body flat on the top
side. Underside: bend the band-side leg across to pad (17,8), where the green
link comes through, and solder leg and link together in one joint. Bend the
plain-side leg down column 21 and solder it at rows 8, 9, 10, 11. Cut nothing
yet.

**5. 470 ohm.** Legs into (19,10) and (21,10). Solder both. The (21,10) joint
goes onto the diode leg already lying there.

**6. Capacitors.** 0.1 uF into (19,2) and (23,2). 1000 uF last: LONG leg into
(19,12), striped SHORT leg into (23,12), body standing on the top side.

**7. Meter, before any outside wire goes on.** Ohms 2000, probes on the
underside:
- +5V bus to GND bus: `1`. With the 1000 uF the display may show a number
  that climbs and then goes to `1` - that is the capacitor charging, fine. A
  small **steady** number is a short. Stop and find it.
- +5V bus to the junction (column 21, rows 8-11): about **470**.
- Junction to GND bus: `1`.
- The RX2 pin to the junction: a number one way round the probes, `1` the
  other way round. That is the diode, and it proves the band is the right
  way.

**8. Outside wires.** Pull them from the breadboard one at a time, trim the
tinned end to 3 mm, push through the hole from the top, solder underneath.
Order: pigtail red (19,5), pigtail black (23,5), LED 1 +5V (19,6), LED 1 GND
(23,6), LED 1 green DIN (21,11), LED 70 red (19,7), LED 70 black (23,7). Read
the strip end and the pigtail measurement (red is +) rather than trusting
wire colour if any wire is not red/black/green.

**9. Meter again.** +5V bus to GND bus: `1`.

**10. Strain relief.** Hot glue over the seven wire entries on the top side.
Without it the first tug on a lead rips the pad off. Then plug the ESP32 in,
USB at the top, all 30 pins seated. Adapter in. Expect the four colour bands
on the U, same as on the breadboard.

## After it lights

```bash
python tools/led_layout.py --width 57 --height 30.5 --abl 2000 --write
python tools/wled_push.py apply --host wled-desk.local
```

Then at full white, meter DCV 20 with probes on the two 1000 uF legs (19,12)
and (23,12): above 4.5 V is fine. Below it, regenerate with `--abl 1500` and
apply again. The 3 A adapter sagged to 4.71 V at 600 mA on the breadboard;
the dot board should do better, and the injection at LED 70 halves the drop
along the strip.

## What can go wrong, and the fix

| Symptom | Likely | Fix |
|---|---|---|
| Nothing lights, ESP32 LED off | VIN link not on the bus, or pigtail reversed | meter DCV on the +5V bus vs GND bus with the adapter in: 5 V expected |
| ESP32 boots, strip dark | green link not reaching the diode leg, or diode backwards | ohms RX2 pin to junction: one way only |
| First LED flickers, rest dark | junction not pulled up: 470 ohm joint | ohms +5V bus to junction = 470 |
| Adapter clicks / goes hot | short between buses | ohms between buses, adapter out |
| One header pin not soldered | that pin's function missing - VIN, GND or RX2 | look at the row of 30 cones; every one should have solder |
