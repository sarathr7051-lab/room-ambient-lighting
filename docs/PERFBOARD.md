# Desk node on the dot board

The bench circuit, moved off the breadboard onto one of the 6 x 4 inch
isolated-pad dot boards. Same circuit, same seven parts, nothing new to buy.
The breadboard carried the strip's 600 mA on the bench and that is about its
limit - the clips loosen and the rail sagged 0.3 V. Soldered bus wires carry
2 A without complaint, and they do not fall out when the monitor moves. This
is the owner's first dot board, so it is written for that; it was reviewed
independently before being built.

![Dot board layout - top and underside](img/perfboard-layout.svg)

Hole positions are **(column, row)**, counted from the **corner mark**: a
marker dot you put on one corner of the board, on both faces, before anything
else. Column 1 is the corner-mark column, row 1 the corner-mark row. The
ESP32's USB socket faces the top edge. The drawing shows 26 x 18 holes, which
is the used area plus margin; the full board is bigger and needs no cutting.

## Four things a dot board does differently from a breadboard

1. **Nothing is connected until you connect it.** Every hole is its own copper
   ring. On the breadboard, five holes in a row were joined for you. Here you
   join them yourself, two ways, and this layout uses both:
   - **A bus:** a bare wire laid along a row of holes on the underside,
     soldered at every pad. Anything pushed through one of those holes gets
     soldered into the same blob and is on the bus. Two here: +5V and GND.
   - **A bent leg:** push a part or wire through, and on the underside bend
     the bare end flat across to the next pad, then solder. Every link wire
     reaches its ESP32 pin this way, and the diode's plain leg is bent along
     four pads to make the junction.
2. **It is mirrored when you flip it.** Turn the board over **left-to-right,
   like a page**, so the USB end stays at the top - then column 1 is on the
   right and the rows are unchanged. Turn it end-over-end and everything is
   wrong. Find the corner mark every time you turn it. The drawing shows both
   faces.
3. **A soldered bus lies across the holes it passes.** Lay it slightly to one
   side of the hole centres, along the edge of the pad rings, so the holes stay
   open. If a later leg meets wire across its hole: heat that joint, push the
   leg through while the solder is molten, add a touch of solder.
4. **Solder is permanent, but not that permanent.** A part in the wrong hole
   comes out: heat the joint, pull the leg with pliers while it is molten. A
   pad lifts only if the iron stays on for many seconds. Two or three seconds
   per joint, always.

## The joint itself

Iron at 330-350 C for 60/40 solder. Tin the tip first. **Rosin flux only** -
the paste sold for plumbing is acid and corrodes boards.

1. Leg or wire through the hole from the top. Bend it slightly on the
   underside so it cannot fall out.
2. Iron tip touching **both the pad and the leg** at once, for 1 second.
3. Feed solder into the joint, not onto the iron, until it flows round the
   leg and makes a small cone the size of a grain of rice.
4. Iron off. Do not move the leg for 2 seconds.

Good: a shiny cone wetting both pad and leg. Bad: a ball on the leg not
touching the pad (pad not heated), or a dull grainy blob (moved while
cooling). Pads are 2.54 mm apart; if solder joins two neighbours that should
not be joined, drag a clean hot tip through the gap, or add flux and touch
again - the solder pulls back onto the pads. Clean the tip on the sponge every
few joints; a black tip transfers no heat, and the answer is never "hold it
longer".

**Trimming:** never cut a leg you intend to bend across pads. Everything else
is trimmed 1-2 mm above its cone **after step 6**, in one go, with safety
glasses on, and then the board is brushed clean - a clipping lying across two
pads is the classic phantom short.

## The parts and where they go

| Part | Holes | Note |
|---|---|---|
| Female header, 15 pins | column 5, rows 3-17 | left row of the ESP32 |
| Female header, 15 pins | column 15, rows 3-17 | right row |
| +5V bus, bare wire | column 19, rows 2-13 | underside |
| GND bus, bare wire | column 23, rows 2-13 | underside |
| Link, red, insulated, ~10 cm | (16,3) to (19,3) | **top side**. Underside: the (16,3) end is bent across onto the VIN pin's cone at (15,3) and soldered to it |
| Link, black, insulated, ~20 cm | (16,4) to (23,4) | top side. Underside: (16,4) end bent onto the GND pin at (15,4) |
| Link, green, insulated, ~28 cm | (6,8) to (16,8) | top side, runs under the ESP32 body (the headers lift it 8 mm). Underside: (6,8) end bent onto the RX2 pin at (5,8); (16,8) end bent onto the diode's band leg at (17,8). **Bend toward 17, away from the D25 pin at (15,8)** |
| 1N4007 | band end (17,8), plain end (21,8) | **band toward the ESP32**. Underside: plain leg bent down column 21 through rows 9, 10, 11 = the **junction**. Soldered at rows 8 and 9 only at first - see step 4 |
| 470 ohm | (19,10) and (21,10) | **standing upright**: body on end over (19,10), that leg straight down; the other leg bent 180 degrees back over the body, down alongside it, into (21,10). It goes in beside the junction leg and is soldered to it |
| 1000 uF | LONG leg (19,13), striped SHORT leg (21,13) | 2-hole spacing, no bending of the legs. Underside: the short leg is bent across (22,13) to the GND bus at (23,13) |
| 0.1 uF | (19,2) and (23,2) | no polarity; legs bend to 4 holes easily |
| Pigtail red | (19,5) | |
| Pigtail black | (23,5) | |
| LED 1 +5V wire | (19,6) | |
| LED 1 GND wire | (23,6) | |
| LED 1 green DIN wire | (21,11) | in beside the junction leg, soldered to it |
| LED 70 red tail | (19,7) | |
| LED 70 black tail | (23,7) | |
| Strain-relief lash | (26,3) and (26,9) | a twist of bare wire over the wire bundle |

Only three ESP32 pins are used: **VIN (15,3), the GND below it (15,4), RX2
(5,8)**. Nothing goes to 3V3 or the other GND. The pin names are for the
30-pin DOIT DevKit V1 with the USB at the top: read them off the board's own
silkscreen before soldering anything to a pin - some clones shuffle labels.

The ESP32's two pin rows are drawn 10 holes apart. **Let the board tell you
the real number**: push the headers onto the ESP32 first, then place the
assembly. That is also what guarantees the headers are the right distance
apart to ever seat again. If they land at columns 5 and 14, everything else
stays where it is; the links just get one hole shorter.

**Bus wire:** best is solid-core copper - one core out of an Ethernet cable,
or bell wire. The stranded silicone wire works if that is all there is: strip
4 cm, pull the strands straight, tin in short passes with flux until it is a
stiff rod. Not a paperclip (steel, solders badly). 4 cm per bus.

## Assembly order

Adapter unplugged from the wall throughout. Pull the seven parts from the
breadboard only when you reach their step. Honest fallback: once the diode,
resistor and capacitors have left the breadboard (steps 4-6) the fallback is
"put them back"; the ESP32 and its WLED config move last, so nothing on the
network changes until the board works.

**0. Corner mark.** Marker dot on one corner, both faces. No cutting needed.
If you ever do cut a board: brown paper-phenolic scores with a knife (5-6
passes each face along a row of holes) and snaps over a table edge; green or
yellow glass-fibre does not snap - hacksaw, and a mask for the dust.

**1. Headers - first, because they become the legs the flipped board stands
on.** Pull the 16th pin out of a female header strip with pliers, then cut
through the empty plastic; twice, for two 15-pin lengths. Push both onto the
ESP32's pins. Place the assembly on the board, USB at the top, headers into
columns 5 and 15 (or where they land), rows 3-17. Flip the board left-to-right;
put an eraser under the antenna end so the stack does not rock on the USB
socket. Solder **one pin at each end of each header** (4 joints). Flip back,
check both headers sit flat and the ESP32 is parallel to the board; if not,
reheat that one joint and press. Solder the other 26, two or three seconds
each - the ESP32 is a fine heat sink, no risk to it.

To remove the ESP32: prise a little at each end alternately, never rock it
sideways. Unplug it now and put it aside; it goes back on at step 10.

**1a. Meter, headers only.** Ohms 2000: (5,3) to (5,4) must read `1`, and
(15,3) to (15,4) must read `1`. Those are 3V3-GND and VIN-GND - the two
bridges that matter most and that no later check catches. Then eyeball every
gap in the two rows of 15 cones.

**2. Buses.** Underside. Lay one bus wire down column 19 from row 2 to row
13, slightly off the hole centres. Solder it at row 2 and row 13 first so it
stays put, then at every pad between (12 joints). Same for column 23. Trim
the ends. **Three empty columns between them stay empty.**

**3. Links, on the top side.** Red through (16,3) and (19,3); black through
(16,4) and (23,4); green through (6,8) and (16,8), lying flat where the ESP32
body will be. Underside: bend each pin-side bare end (5 mm stripped) across
onto its header pin's cone - VIN, GND, RX2 - and reflow that cone with the
wire in it. Solder the bus-side ends onto the buses. Leave the green (16,8)
end unsoldered until step 4.

**4. Diode.** Band end (17,8), plain end (21,8), body flat on top. Underside:
bend the green link's bare end from (16,8) onto the band leg at (17,8) and
solder the two together. Bend the plain leg down column 21 through rows 9,
10, 11; solder it at **rows 8 and 9 only**, and leave rows 10 and 11 open for
the resistor and the DIN wire. Cut nothing.

**5. 470 ohm, upright.** Leg into (19,10), the hairpin leg into (21,10)
beside the junction leg. Solder (19,10) onto the bus; solder (21,10) with the
resistor leg and the diode leg in one joint.

**6. Capacitors.** 0.1 uF into (19,2) and (23,2). 1000 uF: LONG leg (19,13),
striped SHORT leg (21,13); underside, bend the short leg across (22,13) to
the GND bus at (23,13) and solder it there and at (21,13). Now trim every leg
that is not bent, brush the board clean.

**7. Meter, before any outside wire goes on.** Adapter out, ESP32 out.
- Ohms 2000, +5V bus to GND bus: the number climbs and then shows `1` - that
  is the 1000 uF charging, fine. A small **steady** number is a short. Stop.
- Ohms 2000, +5V bus to the junction (column 21, rows 8-11): about **470**
  (447 to 494 is in tolerance).
- Ohms 2000, junction to GND bus: climbs, then `1` (through the 470 and the
  capacitor - fine).
- Ohms 2000, RX2 pin stub (5,8) to the +5V bus: `1`. Never a small number.
- **Diode:** dial to the diode symbol. Red probe on the junction, black on the
  RX2 pin stub: a number around 500-700. Swap the probes: `1`. That proves the
  band is the right way **and** that the green link reaches the pin.

**8. Outside wires.** First the pigtail, and check it before it goes on:
adapter in, DCV 20, red probe on the red lead, black on the black: **+5**,
not -5. Adapter out. Trim both tinned ends to 3 mm, red through (19,5), black
through (23,5), solder to the buses.

**8a. Powered check of the clamp, nothing else connected.** ESP32 out, strip
wires not yet on. Adapter in. DCV 20, black probe on the GND bus:
- +5V bus: about **5.0 V**.
- Junction: about **5.0 V** (pulled up through the 470).
- Touch a scrap wire from the RX2 pin stub (5,8) to the GND bus while
  watching the junction: it drops to about **0.7 V**. That is the diode doing
  its job; 9 mA through the 470, harmless. Stays at 5 V = diode backwards or
  green link not reaching the pin.
Adapter out.

**8b. The strip wires**, one at a time out of the breadboard, tinned end
trimmed to 3 mm, through from the top, soldered underneath: LED 1 +5V (19,6),
LED 1 GND (23,6), LED 1 green DIN (21,11) beside the junction leg, LED 70 red
tail (19,7), LED 70 black tail (23,7). Read the strip end, not the wire colour,
for the two LED 1 leads that are not red/black.

**9. Strain relief.** Gather the seven wires into a bundle 2 cm from the
board with a piece of heat-shrink or tape; lash the bundle to the board with a
twist of bare wire through (26,3) and (26,9). Hot glue on top if there is a
gun - on its own hot glue barely holds silicone insulation.

**10. First power-up.** Plug the ESP32 in, USB at the top, all 30 pins
seated. It still carries the bench config (120 LEDs, ABL 600 mA), which is
safe for a first switch-on. Adapter in. Expect the four colour bands on the U,
exactly as on the breadboard. A meter check across the buses is meaningless
now - the strip and the ESP32 are across them.

## After it lights

```bash
python tools/led_layout.py --width 57 --height 30.5 --abl 2000 --write
python tools/wled_push.py apply --host wled-desk.local
```

Then at full white, DCV 20 across the 1000 uF legs, (19,13) and (23,13):
above 4.5 V is fine. Below it, regenerate with `--abl 1500` and apply again.

## What can go wrong, and the fix

| Symptom | Likely | Fix |
|---|---|---|
| Nothing lights, ESP32 LED off, regulator hot | 3V3-GND or VIN-GND header bridge (step 1a), or VIN link not on the bus | ESP32 out, ohms (15,3)-(15,4) and (5,3)-(5,4) = `1`; DCV on the buses with the adapter in = 5 V |
| Adapter clicks, or goes hot | short between the buses; 1000 uF reversed (warm, bulging) | adapter out, strip and ESP32 off, ohms between buses; look at the capacitor stripe |
| ESP32 boots, strip dark | diode backwards; green link not on RX2 or not on the band leg; DIN wire in the wrong hole; WLED GPIO not 16 | step 8a test with the ESP32 out |
| Buses read 470 ohms to each other, junction to +5V reads `1` | 470 soldered (19,10) to (23,10) instead of to the junction | move the (23,10) leg to (21,10) |
| First LED flickers, rest dark | junction not pulled up: 470 joint | ohms +5V bus to junction = 470 |
| LEDs past 70... i.e. the far end of the U dim or pink at white | injection tail not on the bus | DCV at LED 70's tails at white: within 0.3 V of the buses |
| Works, then dies when a lead moves | cracked joint or lifted pad after a tug | reflow; fit the strain relief |
