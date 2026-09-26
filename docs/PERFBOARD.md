# Desk node on the dot board

The bench circuit, moved off the breadboard onto one of the 6 x 4 inch
isolated-pad dot boards. Same circuit, same seven parts, nothing new to buy.
Breadboard contacts are good for about 1 A; the dot board with two bus wires is
what lets ABL go to 2000 mA.

![Dot board layout](img/perfboard-layout.svg)

Hole positions are **(column, row)** counted from the board's top-left corner,
with the ESP32's USB socket facing the top edge. No cutting of the board is
needed; trim it later if you want.

## How an isolated-pad board works

Every hole is its own copper ring. Nothing is connected to anything until you
make it so. Two ways, and this layout uses both:

- **A bus:** strip 8 cm of wire, twist it tight, tin it, lay it along a row of
  holes on the **underside** and solder it to every pad it crosses. Any leg or
  wire pushed through one of those holes gets soldered into the same blob and
  is on the bus.
- **A bent leg:** push a component leg through, and on the underside bend it
  over to the next pad before soldering. The 1N4007's anode leg is bent along
  four pads to make the junction.

Insulated link wires run on the underside too. Where a link meets a header
pin, its bare end is wrapped round the pin and soldered with it.

## The parts and where they go

| Part | Holes | Note |
|---|---|---|
| Female header, 15 pins | column 5, rows 3-17 | left row of the ESP32 |
| Female header, 15 pins | column 15, rows 3-17 | right row |
| +5V bus, bare tinned wire | column 19, rows 2-12 | underside |
| GND bus, bare tinned wire | column 23, rows 2-12 | underside |
| Link, red | VIN pin (15,3) to (19,3) | underside |
| Link, black | GND pin (15,4) to (23,4) | underside |
| Link, green | RX2 pin (5,8) to (17,8) | underside, passes under the ESP32 |
| 1N4007 | band end (18,8), plain end (21,8) | **band toward the ESP32**. Under the board, bend the band-side leg across to (17,8) and solder it with the green link; bend the plain-side leg down column 21 to row 11 and solder at rows 8, 9, 10, 11 = the **junction** |
| 470 ohm | (19,10) to (21,10) | one leg on the +5V bus, one on the junction. Stand it upright if it will not lie flat |
| 1000 uF | LONG leg (19,12), striped SHORT leg (23,12) | bend the legs out to the 4-hole spacing |
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

## Assembly order

Adapter unplugged from the wall throughout. Pull the seven parts from the
breadboard only when you reach their step - the breadboard circuit is the
fallback until the dot board lights the strip.

1. **Headers.** Cut two 15-pin lengths from a female header strip (cut through
   the 16th position; that pin is lost). Push both onto the ESP32's pins, place
   the ESP32 on the board so the headers drop into columns 5 and 15, rows 3-17,
   with the USB at the top. Turn the board over with the ESP32 still plugged
   in - it holds the headers square - and solder one pin at each corner of
   each header. Check the headers sit flat. Solder the rest. Unplug the ESP32
   and put it aside; it goes back on last.
2. **Buses.** Two 8 cm lengths of wire, stripped fully, twisted, tinned. Lay
   one down column 19 rows 2-12 on the underside and solder every pad;
   the other down column 23. They must not touch each other or anything else.
3. **Links.** Red from the VIN pin at (15,3) to (19,3). Black from the
   GND pin at (15,4) to (23,4). Green from the RX2 pin at (5,8) to hole
   (17,8). Bare ends wrapped round the pins before soldering.
4. **Diode.** Band end at (18,8). Under the board, bend the band-side leg over
   to pad (17,8) where the green link comes through; solder both together.
   Bend the plain-side leg down column 21 and solder it at rows 8-11.
5. **470 ohm** between (19,10) and (21,10).
6. **Capacitors.** 1000 uF long leg into (19,12), short striped leg into
   (23,12). 0.1 uF into (19,2) and (23,2).
7. **Meter, before any wire from outside goes on.** Ohms 2000:
   - +5V bus to GND bus: `1` (with the 1000 uF the number may climb for a
     moment, then show `1`). A small steady number = a short. Stop.
   - +5V bus to junction: about **470**.
   - Junction to GND bus: `1`.
   - RX2 pin to junction: `1` one way round the probes and a number the
     other way round - that is the diode.
8. **External wires**, each through its hole from the top, soldered
   underneath, tinned end trimmed to 3 mm first: pigtail, the three from LED 1,
   the two tails from LED 70. Colours as in the table; read the strip end, not
   the wire colour, if in doubt. Hot glue over the wire entries on the top side
   afterwards - that is the strain relief.
9. **Meter again**, +5V bus to GND bus: `1`.
10. Plug the ESP32 in, USB at the top, all 30 pins seated. Adapter in.
    Expect the four colour bands on the U, same as on the breadboard.

## After it lights

- `python tools/led_layout.py --width 57 --height 30.5 --abl 2000 --write`
- `python tools/wled_push.py apply --host wled-desk.local`
- At full white, meter DCV 20 across (19,12) and (23,12): if it reads below
  4.5 V, regenerate with `--abl 1500` and apply again.
