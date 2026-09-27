"""Draws docs/img/perfboard-layout.svg: the desk node on the LABTECH 9 x 15 cm
single-sided dot board, top view and mirrored underside, in the board's own
printed coordinates (columns A..Z then A'..D', rows 001..050).

The board is held white-grid side up, printed row numbers on the LEFT, 001 at
the top. In that view the columns run D' C' B' A' Z Y ... A from left to
right (the letters are printed for the copper face, so they read mirrored on
top). Internally the code uses column 1 = the column next to the row numbers.
Keep this in step with docs/PERFBOARD.md."""
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "docs" / "img" / "perfboard-layout.svg"
RED, GRN, GND, AMB, LEG = "#DC3545", "#2E9E5B", "#4a4844", "#E08A0C", "#7a6a55"
C, X0 = 22, 70
COLS, ROWS = 30, 28                 # drawn rows; the board has 50
MM = C / 2.54
W = 1290
ST = ('<style>text{font-family:ui-sans-serif,system-ui,"Segoe UI",Roboto,sans-serif}'
      '.h{font-size:16px;font-weight:700;fill:#1a1a18}.t{font-size:13px;fill:#3d3d3a}'
      '.n{font-size:11px;font-weight:600;fill:#1a1a18}.s{font-size:10px;fill:#555}'
      '.c{font-size:10px;font-weight:700;fill:#1a1a18}</style>')
LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["A'", "B'", "C'", "D'"]


def col(c):
    """board letter for internal column c (1 = next to the row numbers)"""
    return LETTERS[30 - c]


def row(r):
    return f"{r:03d}"


def B(c, r):
    return f"{col(c)}{row(r)}"


LEFT = ["3V3", "GND", "D15", "D2", "D4", "RX2", "TX2", "D5", "D18", "D19", "D21", "RX0", "TX0", "D22", "D23"]
RIGHT = ["VIN", "GND", "D13", "D12", "D14", "D27", "D26", "D25", "D33", "D32", "D35", "D34", "VN", "VP", "EN"]
BUS_ROWS = range(2, 17)
CAP = 16
BUS_FREE_5V = [4, 8, 9, 11, 12, 13, 14, 15]
BUS_FREE_GND = [3, 8, 9, 10, 11, 12, 13, 14, 15]
EXT = [((19, 5), RED, "pigtail  +  (red wire)"),
       ((23, 5), GND, "pigtail  -  (black wire)"),
       ((19, 6), RED, "LED 1 end:  +5V wire"),
       ((23, 6), GND, "LED 1 end:  GND wire"),
       ((19, 7), RED, "LED 70 end:  red tail"),
       ((23, 7), GND, "LED 70 end:  black tail"),
       ((21, 11), GRN, "LED 1 end:  green DIN wire")]
s = []; add = s.append


def panel(Y0, mirror, title, sub, xoff=0):
    def P(x, y):
        xx = (COLS + 1 - x) if mirror else x
        return X0 + xoff + xx * C, Y0 + y * C

    def wire(pts, colr, dash=None, wd=3):
        d = "M" + " L".join(f"{P(x,y)[0]} {P(x,y)[1]}" for x, y in pts)
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        add(f'<path d="{d}" fill="none" stroke="{colr}" stroke-width="{wd}" stroke-linecap="round" stroke-linejoin="round"{dd}/>')

    def blob(x, y, colr, r=5):
        px, py = P(x, y); add(f'<circle cx="{px}" cy="{py}" r="{r}" fill="{colr}"/>')

    def label(x, y, txt, cls="s", anchor="start", colr=None, dy=0, dx=0):
        px, py = P(x, y)
        st = f' style="fill:{colr}"' if colr else ""
        add(f'<text class="{cls}" x="{px+dx}" y="{py+dy}" text-anchor="{anchor}" dominant-baseline="central"{st}>{txt}</text>')

    def sgn(cols_dir):
        return cols_dir * (-1 if mirror else 1)

    add(f'<text class="h" x="{X0+xoff-30}" y="{Y0-34}">{title}</text>')
    add(f'<text class="t" x="{X0+xoff-30}" y="{Y0-16}">{sub}</text>')
    lx = P(0.5, 0)[0]; rx = P(COLS + 0.5, 0)[0]
    bx, bx2 = min(lx, rx) - 8, max(lx, rx) + 8
    by, by2 = Y0 + 0.5 * C - 30, Y0 + (ROWS + 0.5) * C
    face = "#e9dcc2" if not mirror else "#d9a06a"
    add(f'<rect x="{bx}" y="{by}" width="{bx2-bx}" height="{by2-by}" rx="6" fill="{face}" stroke="#9c8a63"/>')
    # the strip of long pads along the top edge (not used) and the mounting hole
    for x in range(1, COLS + 1):
        px, _ = P(x, 0)
        add(f'<rect x="{px-4}" y="{by+4}" width="8" height="16" rx="2" fill="#c9a86a" opacity="0.6"/>')
    hx, hy = P(0, 0); add(f'<circle cx="{hx}" cy="{by+12}" r="4" fill="#fff" stroke="#9c8a63"/>')
    # 5 x 5 grid lines (printed on the top face; drawn faintly on both for counting)
    gcol = "#ffffff" if not mirror else "#e8c9a0"
    for k in range(5, COLS, 5):
        x1 = P(k + 0.5, 0)[0]
        add(f'<line x1="{x1}" y1="{Y0+0.5*C}" x2="{x1}" y2="{by2}" stroke="{gcol}" stroke-width="1.5"/>')
    for k in range(5, ROWS, 5):
        y1 = Y0 + (k + 0.5) * C
        add(f'<line x1="{bx+8}" y1="{y1}" x2="{bx2-8}" y2="{y1}" stroke="{gcol}" stroke-width="1.5"/>')
    for x in range(1, COLS + 1):
        for y in range(1, ROWS + 1):
            px, py = P(x, y)
            add(f'<circle cx="{px}" cy="{py}" r="3.2" fill="#c9a86a" stroke="#8a6f3c" stroke-width="0.8"/>')
    # column letters along the top, row numbers on the numbered edge
    for x in range(1, COLS + 1):
        px, py = P(x, 0)
        add(f'<text class="c" x="{px}" y="{py-4}" text-anchor="middle">{col(x)}</text>')
    d = sgn(-1)
    for y in range(1, ROWS + 1):
        px, py = P(0, y)
        add(f'<text class="c" x="{px+10*d}" y="{py}" text-anchor="{"start" if d > 0 else "end"}" dominant-baseline="central">{row(y)}</text>')

    if not mirror:
        ex, ey = P(4.4, 1.6); ex2, ey2 = P(15.6, 23)
        add(f'<rect x="{ex}" y="{ey}" width="{ex2-ex}" height="{ey2-ey}" rx="6" fill="#eeece7" fill-opacity="0.5" stroke="#6f6d66" stroke-width="1.4" stroke-dasharray="6 4"/>')
        ux, uy = P(10, 1.6)
        add(f'<rect x="{ux-16}" y="{uy-2}" width="32" height="14" rx="3" fill="#9a9891" fill-opacity="0.8"/>')
        add(f'<text class="s" x="{ux}" y="{uy+6}" text-anchor="middle" style="fill:#fff">USB</text>')
        label(10, 19, "ESP32 on two female headers,", "s", "middle"); label(10, 19.8, "USB at the top edge", "s", "middle")
        label(10, 21.5, "antenna end", "s", "middle")
    else:
        label(10, 20, "no ESP32 on this side: 30 header pins to solder", "t", "middle")

    for i in range(15):
        y = 3 + i
        for x, names, cols_in in ((5, LEFT, +1), (15, RIGHT, -1)):
            px, py = P(x, y)
            add(f'<rect x="{px-5}" y="{py-5}" width="10" height="10" fill="#222" rx="1"/>')
            nm = names[i]
            hot = (nm == "RX2") or (x == 15 and nm in ("VIN", "GND"))
            colr = {"RX2": GRN, "VIN": RED, "GND": GND}.get(nm) if hot else None
            d = sgn(cols_in)
            anchor = "start" if d > 0 else "end"
            if colr:
                add(f'<text class="n" x="{px+7*d}" y="{py}" text-anchor="{anchor}" dominant-baseline="central" style="fill:{colr}">{nm}</text>')
            elif not mirror:
                add(f'<text class="s" x="{px+7*d}" y="{py}" text-anchor="{anchor}" dominant-baseline="central">{nm}</text>')

    # reserved area for the 12 V stage
    rx0, ry0 = P(2, 25); rx1, ry1 = P(29, 28.4)
    lo, hi = min(rx0, rx1), max(rx0, rx1)
    add(f'<rect x="{lo}" y="{ry0}" width="{hi-lo}" height="{ry1-ry0}" rx="4" fill="none" stroke="#9a9891" stroke-dasharray="4 4"/>')
    label(15.5, 26.7, "rows 025-050: kept free (a future L3 under-desk 12 V stage could go here, gate from D25 = P010)", "s", "middle")

    # ---- underside features. Dashed in the top view, solid underneath.
    ud = "6 4" if not mirror else None
    wire([(19, 2), (19, 16)], RED, dash=ud, wd=5); wire([(23, 2), (23, 16)], GND, dash=ud, wd=5)
    label(19, 1, "+5V bus  (L)", "n", "middle", RED, -8); label(23, 1, "GND bus  (H)", "n", "middle", GND, -8)
    wire([(21, 8), (21, 11)], AMB, dash=ud, wd=4)
    wire([(21, CAP), (23, CAP)], LEG, dash=ud, wd=4)
    wire([(16, 3), (15, 3)], RED, dash=ud, wd=4)
    wire([(16, 4), (15, 4)], GND, dash=ud, wd=4)
    wire([(4, 8), (5, 8)], GRN, dash=ud, wd=4)
    wire([(16, 8), (17, 8)], GRN, dash=ud, wd=4)
    if mirror:
        for y in BUS_ROWS:
            for x, free, colr in ((19, BUS_FREE_5V, RED), (23, BUS_FREE_GND, GND)):
                px, py = P(x, y)
                if y in free:
                    add(f'<circle cx="{px}" cy="{py}" r="4.5" fill="{colr}"/>')
                else:
                    add(f'<circle cx="{px}" cy="{py}" r="4.5" fill="none" stroke="{colr}" stroke-width="2"/>')
        for (x, y) in [(15, 3), (15, 4), (5, 8), (17, 8), (21, 8), (21, 9), (21, 10), (21, 11), (16, 3), (16, 4), (4, 8), (16, 8), (21, CAP)]:
            blob(x, y, "#1a1a18", 3.5)
        m = 32.5
        label(m, 3.5, f"link ends: through {B(16,3)} and {B(16,4)}, bent onto the VIN and GND pins", "s", "end", None, 0, -6)
        label(m, 8, f"{B(17,8)}: diode band leg + green link end from {B(16,8)}, one joint", "s", "end", None, 0, -6)
        label(m, 8.8, f"green link's other end from {B(4,8)}, bent onto the RX2 pin {B(5,8)}", "s", "end", None, 0, -6)
        label(m, 9.6, f"junction: diode's plain leg down {B(21,8)}-{B(21,11)}, cut past {B(21,11)}", "s", "end", AMB, 0, -6)
        label(m, CAP, f"1000 uF short leg from {B(21,CAP)} to the GND bus at {B(23,CAP)}", "s", "end", None, 0, -6)
        label(15.5, 23.5, "solid dots: soldered at step 2.   Rings: soldered when that leg arrives", "s", "middle", None, 0, 0)
        return

    # ---- top side
    wire([(16, 3), (19, 3)], RED); wire([(16, 4), (23, 4)], GND)
    wire([(4, 8), (4, 1), (17.5, 1), (17.5, 7.5), (16, 8)], GRN)
    label(6, 1, "green link: round the top end, over the red and black links", "s", "start", GRN, -34, 0)
    dx1, dy = P(17, 8); dx2, _ = P(21, 8)
    wire([(17, 8), (21, 8)], LEG, wd=2)
    bw = 5.2 * MM; bx0 = (dx1 + dx2) / 2 - bw / 2
    add(f'<rect x="{bx0}" y="{dy-1.35*MM}" width="{bw}" height="{2.7*MM}" rx="3" fill="#26262a"/>')
    add(f'<rect x="{bx0+2}" y="{dy-1.35*MM}" width="6" height="{2.7*MM}" fill="#d8d8d8"/>')
    label(17.2, 7.3, "1N4007, band toward the ESP32", "s", "start", dy=0)
    rx, ry = P(19, 10)
    add(f'<circle cx="{rx}" cy="{ry}" r="{1.25*MM}" fill="#d8c9a8" stroke="#8a7c5e"/>')
    wire([(19.5, 10), (21, 10)], LEG, wd=2)
    label(24.2, 10.2, f"470 ohm standing on {B(19,10)}; its top leg slants down into {B(21,10)}, sleeved", "s", "start", None, 0, 0)
    cx, cy = P(20, CAP)
    add(f'<circle cx="{cx}" cy="{cy}" r="{5*MM}" fill="#2f3a52" fill-opacity="0.75" stroke="#1b2233"/>')
    add(f'<rect x="{cx+2.6*MM}" y="{cy-2*MM}" width="{1.2*MM}" height="{4*MM}" fill="#cdd6e6"/>')
    label(25.5, CAP + 0.5, f"1000 uF: LONG leg {B(19,CAP)} on the +5V bus, striped SHORT leg {B(21,CAP)}", "s", "start", None, 0, 0)
    cx, cy = P(21, 2)
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{2.5*MM}" ry="{1.6*MM}" fill="#d9a441" stroke="#8a6a20"/>')
    wire([(19, 2), (23, 2)], LEG, wd=2)
    label(21, 1, "0.1 uF", "s", "middle", dy=-8)
    ylab = [3.6, 4.6, 5.6, 6.6, 7.6, 8.6, 11.6]
    for ((x, y), colr, lbl), y2 in zip(EXT, ylab):
        if x == 19:
            wire([(x, y), (x + 0.5, y), (x + 1.0, y - 0.4), (24.6, y - 0.4), (26.4, y2), (29.6, y2)], colr, wd=3)
        else:
            wire([(x, y), (24.6, y), (26.4, y2), (29.6, y2)], colr, wd=3)
        px, py = P(29.6, y2); add(f'<text class="t" x="{px+12}" y="{py}" dominant-baseline="central">{lbl}  {B(x,y)}</text>')
    blob(26, 4, "#1a1a18", 3); blob(26, 12, "#1a1a18", 3)
    label(24.2, 13.4, f"lash: bare wire through {B(26,4)} and {B(26,12)}, over the bundle", "s", "start", None, 0, 0)
    for (x, y), _, _ in EXT: blob(x, y, "#1a1a18", 3.5)
    for (x, y) in [(19, 3), (23, 4), (16, 3), (16, 4), (4, 8), (16, 8), (17, 8), (21, 8), (19, 10), (21, 10), (19, CAP), (21, CAP), (19, 2), (23, 2)]:
        blob(x, y, "#1a1a18", 3.5)


TOP = 90
panel(TOP, False, "TOP side (white grid, LABTECH print) - row numbers on your LEFT, 001 at the top. Parts and wires go in from here.",
      "The letters are printed for the other face, so they read mirrored here; count columns from the numbered edge (white lines every 5). Solid = this side, dashed = underneath.")
BOT = TOP + (ROWS + 2) * C + 110
panel(BOT, True, "UNDERSIDE (copper rings) - turned over left-to-right like a page. Letters now read normally, numbers on the RIGHT.",
      "This is the face you solder. Every joint is a dot or a ring. Coordinates are letter + printed row, e.g. L010 = column L, row 010.", xoff=350)

Y = BOT + (ROWS + 1) * C + 50
add(f'<rect x="0" y="0" width="{W}" height="{Y+220}" fill="#ffffff"/>')
s.insert(0, s.pop())
add(f'<text class="h" x="40" y="{Y}">How to read it</text>'); Y += 24
for colr, txt in [
    (RED, "thick red / dark grey:  a BUS - one bare wire along the pads on the underside, laid beside the hole centres. Dashed in the top view because it is underneath"),
    (GRN, "thin solid green / red / black (top view):  an insulated link on this side; its end goes through the hole NEXT to the pin and is bent onto the pin underneath"),
    (AMB, "amber:  the diode's own plain leg, bent along four pads under the board. The 470 ohm and the green DIN wire go through beside it and solder to it"),
    (LEG, "brown:  a bare component leg"),
]:
    add(f'<line x1="40" y1="{Y-4}" x2="76" y2="{Y-4}" stroke="{colr}" stroke-width="4"/>')
    add(f'<text class="t" x="86" y="{Y}" dominant-baseline="central">{txt}</text>'); Y += 22
Y += 6
add(f'<text class="t" x="40" y="{Y}">Key columns, counted from the numbered edge:  4 = A\'   5 = Z (left header)   15 = P (right header)   16 = O   17 = N   19 = L (+5V bus)   21 = J (junction)   23 = H (GND bus)   26 = E</text>'); Y += 20
add(f'<text class="t" x="40" y="{Y}">Only three ESP32 pins are used: VIN = P003, the GND below it = P004, RX2 = Z008. Nothing goes to 3V3 or the other GND. The board is not cut.</text>'); Y += 22
add(f'<text class="h" x="40" y="{Y}" style="fill:{RED}">Nothing bare may reach from one bus to the other. Between them there are only three things:</text>'); Y += 22
add(f'<text class="h" x="40" y="{Y}" style="fill:{RED}">the junction (column J), the capacitor leg into the GND bus, and the two legs of the 0.1 uF.</text>')
H = Y + 30
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">'
       f'<title>Desk node on the LABTECH 9 x 15 dot board</title>{ST}' + "".join(s) + "</svg>\n")
OUT.write_text(svg, encoding="utf-8")
import xml.etree.ElementTree as ET; ET.parse(OUT); print("ok", W, H)
if __name__ == "__main__":
    for c in (4, 5, 15, 16, 17, 19, 21, 22, 23, 26):
        print(c, col(c))
