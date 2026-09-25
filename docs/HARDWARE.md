# Hardware — desk node

Everything on this page is physically in hand unless marked otherwise.
Bought at SP Road (Om Technology Centre, F4 SRNG Complex) on 25 Sep 2026.

---

## Parts used by the screen sync light

| Part | Qty used | Note |
|---|---|---|
| ESP32 NodeMCU DevKit V1, 30-pin, CP2102 | 1 | the desk node |
| WS2812 strip, 5 V, 60/m, black PCB | ~1.2 m of 3 m | "2812" without the B; same protocol, GRB |
| 74HCT125 quad buffer, DIP-14 | 1 | 3.3 V -> 5 V level shift on the data line |
| 1000 uF 25 V electrolytic | 1 | bulk across the 5 V rail |
| 0.1 uF ceramic | 1 | decoupling across the 74HCT125 |
| 330 ohm, 1/4 W | 1 | series resistor on DIN |
| 5 V 5 A adapter, 5.5 x 2.1 | 1 | |
| DC barrel pigtail, female with leads | 1 | |
| Silicone wire 22 AWG red/black/green | ~2 m | corner jumpers and injection run |
| Dot board, isolated pad, 6 x 4 inch | 1 | final assembly |
| Velcro cable ties | 2–3 | |

**Not needed for screen sync**, despite being in the same node design:
IRL540N + the 12 V Gesto strip (that is L3, waiting on a 12 V 1 A adapter),
INMP441 (music mode), LDR (auto-dim), LD2420 (presence, deferred).

---

## Pinout

The full desk-node pin map, including the parts that arrive later. Only GPIO16
matters for screen sync.

| Pin | Goes to | Via | Stage |
|---|---|---|---|
| GPIO16 | WS2812 DIN | 74HCT125 gate 1 -> 330 ohm | **L2, now** |
| GPIO25 | IRL540N gate | 74HCT125 gate 2 -> 100 ohm; 10k gate->GND | L3 |
| GPIO32 / 14 / 15 | INMP441 SD / SCK / WS | direct; VDD 3V3, L/R -> GND | music |
| GPIO34 | LDR divider | 3V3 -> LDR -> node -> 10k -> GND | auto-dim |
| GPIO27 | LD2420 presence OUT | direct; sensor on 3V3 | deferred |
| GPIO33, GPIO17 | spare | | |

**Keep free:** GPIO0, 2, 12 (strapping), GPIO1/3 (UART0), GPIO6–11 (flash).

### 74HCT125 (DIP-14)

```
   1  1OE  -> GND            14  VCC -> +5V
   2  1A   <- ESP32 GPIO16   13  4OE
   3  1Y   -> 330R -> DIN    12  4A  -> GND
   4  2OE                    11  4Y
   5  2A   -> GND            10  3OE
   6  2Y                      9  3A  -> GND
   7  GND  -> GND             8  3Y
```

Tie the unused **inputs** (pins 5, 9, 12) to GND. Floating CMOS inputs oscillate
and waste current. 0.1 uF between pin 14 and pin 7, as close to the chip as the
board allows.

The T in 74HC**T**125 is the whole point: it has TTL-level input thresholds, so
a 3.3 V logic high from the ESP32 is read as a solid high while the output
swings to a clean 5 V. A plain 74HC125 has CMOS thresholds and 3.3 V sits
marginally close to them. Two 74HCT125 were bought; the second is for the
shelf node.

---

## Power budget, 5 V rail

| Load | Current |
|---|---|
| ESP32 with Wi-Fi active | ~0.25 A, peaks higher on TX |
| WS2812 strip, ABL capped | 3.0 A ceiling |
| **Total ceiling** | **~3.25 A of 5 A** |

The ABL number is a **ceiling, not a draw**. A bias light showing real video
sits nearer 0.5–1.0 A; the cap only exists so a full-white frame cannot brown
out the node.

### Why 3000 mA and not the 1500 mA in the original plan

The 12 V warm strip runs off its own Gesto adapter, so the 5 V rail carries
only the ESP32 and the bias strip. 1500 mA was sized for a design where both
strips shared the rail. At ~70 LEDs a 3000 mA cap is roughly 78% of full white
— bright enough that the limiter never visibly clamps during normal video, and
still 1.75 A of headroom on the adapter.

If the node browns out or resets on bright scenes, that is the cheap 5 A
adapter sagging, not the maths. Drop to 2500 and retest before blaming wiring.

### Injection

Feed +5 V and GND to **both ends** of the strip run, straight from the rail —
not through the ESP32, and not through a breadboard rail on the final build.
At ~70 LEDs a single feed would work, but the far end would run visibly warmer
in colour, and the second feed costs two wires.

---

## The strip

3 m of 5 V WS2812, 60 LEDs/m, black PCB, bought as "2812" without the B. Same
one-wire protocol, same GRB colour order, same 800 kHz timing — WLED bus type
`WS281x` covers it.

- Cuttable every LED at the printed copper pads (60/m strips are).
- Each cut piece needs its own +5 V, GND and DATA connection.
- Check whether yours is bare (IP30) or silicone-sleeved (IP65) before
  planning corners: sleeved strip needs the silicone trimmed back at every
  cut, which roughly doubles the fiddliness of each joint.

---

## Mounting

Clean the monitor's back panel with IPA and let it flash off before the 3M
backing goes anywhere near it. Textured ABS plus Bengaluru ambient plus the
warmth off the panel is exactly the combination that has strip adhesive
peeling at the corners three months later. The corners are where it lets go
first, so put a velcro tie or a dab of something at each corner turn.

The VESA pattern is 100 x 100 mm in the centre of the panel. A perimeter strip
path 2–3 cm in from the edge clears it, so fitting the Dyazo arm later does not
disturb the strip.
