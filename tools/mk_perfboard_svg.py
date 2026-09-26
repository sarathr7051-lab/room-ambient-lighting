"""Draws docs/img/perfboard-layout.svg: the desk node on an isolated-pad dot
board, top view and mirrored underside. Hole positions are (column, row) from
the corner mark. Keep this in step with docs/PERFBOARD.md."""
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "docs" / "img" / "perfboard-layout.svg"
RED, GRN, GND, AMB, LEG = "#DC3545", "#2E9E5B", "#4a4844", "#E08A0C", "#7a6a55"
C, X0 = 24, 60
COLS, ROWS = 27, 18
W = 1100
MM = C / 2.54                       # px per mm, so bodies are drawn to scale
ST = ('<style>text{font-family:ui-sans-serif,system-ui,"Segoe UI",Roboto,sans-serif}'
      '.h{font-size:16px;font-weight:700;fill:#1a1a18}.t{font-size:13px;fill:#3d3d3a}'
      '.n{font-size:11px;font-weight:600;fill:#1a1a18}.s{font-size:10px;fill:#555}</style>')
LEFT = ["3V3", "GND", "D15", "D2", "D4", "RX2", "TX2", "D5", "D18", "D19", "D21", "RX0", "TX0", "D22", "D23"]
RIGHT = ["VIN", "GND", "D13", "D12", "D14", "D27", "D26", "D25", "D33", "D32", "D35", "D34", "VN", "VP", "EN"]
BUS_ROWS = range(2, 17)
CAP = 16                            # row of the 1000 uF
# bus pads that never receive a leg: soldered at step 2. The rest are soldered when their leg arrives.
BUS_FREE_5V = [4, 8, 9, 11, 12, 14, 15]
BUS_FREE_GND = [3, 8, 9, 10, 11, 12, 14, 15]
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

    def wire(pts, col, dash=None, wd=3):
        d = "M" + " L".join(f"{P(x,y)[0]} {P(x,y)[1]}" for x, y in pts)
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wd}" stroke-linecap="round" stroke-linejoin="round"{dd}/>')

    def blob(x, y, col, r=5):
        px, py = P(x, y); add(f'<circle cx="{px}" cy="{py}" r="{r}" fill="{col}"/>')

    def label(x, y, txt, cls="s", anchor="start", col=None, dy=0, dx=0, bg=False):
        px, py = P(x, y)
        st = f' style="fill:{col}"' if col else ""
        if bg:
            w = len(txt) * 5.3 + 8
            bx = px + dx - 4 if anchor == "start" else (px + dx - w + 4 if anchor == "end" else px + dx - w / 2)
            add(f'<rect x="{bx}" y="{py+dy-8}" width="{w}" height="16" rx="3" fill="#ffffff" fill-opacity="0.92"/>')
        add(f'<text class="{cls}" x="{px+dx}" y="{py+dy}" text-anchor="{anchor}" dominant-baseline="central"{st}>{txt}</text>')

    def sgn(cols_dir):
        """screen direction (+1 right) for a direction given in column numbers (+1 = higher column)"""
        return cols_dir * (-1 if mirror else 1)

    add(f'<text class="h" x="{X0+xoff-20}" y="{Y0-30}">{title}</text>')
    add(f'<text class="t" x="{X0+xoff-20}" y="{Y0-12}">{sub}</text>')
    lx = P(0.5, 0)[0]; rx = P(COLS + 0.5, 0)[0]
    bx, bx2 = min(lx, rx), max(lx, rx)
    by, by2 = Y0 + 0.5 * C, Y0 + (ROWS + 0.5) * C
    add(f'<rect x="{bx}" y="{by}" width="{bx2-bx}" height="{by2-by}" rx="6" fill="#e9dcc2" stroke="#9c8a63"/>')
    for x in range(1, COLS + 1):
        for y in range(1, ROWS + 1):
            px, py = P(x, y)
            add(f'<circle cx="{px}" cy="{py}" r="3.2" fill="#c9a86a" stroke="#8a6f3c" stroke-width="0.8"/>')
    for x in range(1, COLS + 1):
        px, py = P(x, 0); add(f'<text class="s" x="{px}" y="{py-2}" text-anchor="middle">{x}</text>')
    for y in range(1, ROWS + 1):
        px, py = P(0, y)
        d = sgn(-1)
        add(f'<text class="s" x="{px+8*d}" y="{py}" text-anchor="{"start" if d > 0 else "end"}" dominant-baseline="central">{y}</text>')
    # corner mark: outside the (1,1) corner
    px, py = P(1, 1); d = sgn(-1)
    add(f'<path d="M{px+14*d} {py-14} l {-10*d} 0 l {10*d} 10 z" fill="#1a1a18"/>')
    if mirror:
        add(f'<text class="s" x="{px-16}" y="{py-18}" text-anchor="end">corner mark - column 1 is on the RIGHT now</text>')
    else:
        add(f'<text class="s" x="{px-16}" y="{py-18}" text-anchor="start">corner mark (marker dot, both faces)</text>')

    if not mirror:
        ex, ey = P(4.4, 1.6); ex2, ey2 = P(15.6, 18.4)
        add(f'<rect x="{ex}" y="{ey}" width="{ex2-ex}" height="{ey2-ey}" rx="6" fill="#eeece7" fill-opacity="0.5" stroke="#6f6d66" stroke-width="1.4" stroke-dasharray="6 4"/>')
        ux, uy = P(10, 1.6)
        add(f'<rect x="{ux-16}" y="{uy-14}" width="32" height="18" rx="3" fill="#9a9891"/>')
        add(f'<text class="s" x="{ux}" y="{uy-3}" text-anchor="middle" style="fill:#fff">USB</text>')
        label(10, 12.5, "ESP32 on two female headers,", "t", "middle"); label(10, 13.3, "USB at the top. The antenna end", "t", "middle")
        label(10, 14.1, "reaches ~5 rows below this drawing", "t", "middle")
    else:
        label(10, 16.3, "no ESP32 on this side: 30 header pins to solder", "t", "middle")

    for i in range(15):
        y = 3 + i
        for x, names, cols_in in ((5, LEFT, +1), (15, RIGHT, -1)):   # cols_in: toward the ESP32 centre
            px, py = P(x, y)
            add(f'<rect x="{px-5}" y="{py-5}" width="10" height="10" fill="#222" rx="1"/>')
            nm = names[i]
            hot = (nm == "RX2") or (x == 15 and nm in ("VIN", "GND"))
            col = {"RX2": GRN, "VIN": RED, "GND": GND}.get(nm) if hot else None
            d = sgn(cols_in)                       # all names sit INSIDE the ESP32 outline
            anchor = "start" if d > 0 else "end"
            if col:
                add(f'<text class="n" x="{px+7*d}" y="{py}" text-anchor="{anchor}" dominant-baseline="central" style="fill:{col}">{nm}</text>')
            elif not mirror:
                add(f'<text class="s" x="{px+7*d}" y="{py}" text-anchor="{anchor}" dominant-baseline="central">{nm}</text>')

    # ---- underside features. Dashed in the top view, solid underneath.
    ud = "6 4" if not mirror else None
    wire([(19, 2), (19, 16)], RED, dash=ud, wd=5); wire([(23, 2), (23, 16)], GND, dash=ud, wd=5)
    label(19, 1, "+5V bus", "n", "middle", RED, -6); label(23, 1, "GND bus", "n", "middle", GND, -6)
    wire([(21, 8), (21, 11)], AMB, dash=ud, wd=4)                 # diode plain leg = junction
    wire([(21, CAP), (23, CAP)], LEG, dash=ud, wd=4)              # cap short leg to GND bus
    wire([(16, 3), (15, 3)], RED, dash=ud, wd=4)                  # link ends bent onto header pins
    wire([(16, 4), (15, 4)], GND, dash=ud, wd=4)
    wire([(4, 8), (5, 8)], GRN, dash=ud, wd=4)
    wire([(16, 8), (17, 8)], GRN, dash=ud, wd=4)
    if mirror:
        for y in BUS_ROWS:
            blob(19, y, RED if y in BUS_FREE_5V else "#1a1a18", 4)
            blob(23, y, GND if y in BUS_FREE_GND else "#1a1a18", 4)
        for (x, y) in [(15, 3), (15, 4), (5, 8), (17, 8), (21, 8), (21, 9), (21, 10), (21, 11), (16, 3), (16, 4), (4, 8), (16, 8), (21, CAP)]:
            blob(x, y, "#1a1a18", 3.5)
        label(14, 6, "link ends: through (16,3) and (16,4), bent onto the VIN and GND pins", "s", "start", None, 0, 4, bg=True)
        label(14, 9, "(17,8): diode band leg + the green link's bare end from (16,8), one joint", "s", "start", None, 0, 4, bg=True)
        label(14, 10, "junction: the diode's plain leg bent down (21,8) to (21,11), cut 1 mm past (21,11)", "s", "start", AMB, 0, 4, bg=True)
        label(14, 17, f"1000 uF short leg bent from (21,{CAP}) to the GND bus at (23,{CAP}), cut 1 mm past it", "s", "start", None, 0, 4, bg=True)
        label(21, 17.6, "coloured bus dots: soldered at step 2.  Black dots: soldered when the leg arrives", "s", "middle", None, 10, bg=True)
        label(3, 9.6, "green link end from (4,8), bent onto the RX2 pin", "s", "end", None, 0, 8, bg=True)
        return

    # ---- top side: links (solid, they live up here), parts, external wires
    wire([(4, 8), (4, 1.3), (16.5, 1.3), (16.5, 7.5), (16, 8)], GRN)   # around the top end of the header
    wire([(16, 3), (19, 3)], RED); wire([(16, 4), (23, 4)], GND)
    label(10, 1.3, "green link runs round the top end of the ESP32, on this side", "s", "middle", GRN, -10)
    # diode (17,8)-(21,8), DO-41 body 5.2 mm
    dx1, dy = P(17, 8); dx2, _ = P(21, 8)
    wire([(17, 8), (21, 8)], LEG, wd=2)
    bw = 5.2 * MM; bx0 = (dx1 + dx2) / 2 - bw / 2
    add(f'<rect x="{bx0}" y="{dy-1.35*MM}" width="{bw}" height="{2.7*MM}" rx="3" fill="#26262a"/>')
    add(f'<rect x="{bx0+2}" y="{dy-1.35*MM}" width="6" height="{2.7*MM}" fill="#d8d8d8"/>')
    label(19, 8.7, "1N4007, band toward the ESP32", "s", "middle", dy=4)
    # 470 upright at (19,10), hairpin into (21,10)
    rx, ry = P(19, 10)
    add(f'<circle cx="{rx}" cy="{ry}" r="{1.25*MM}" fill="#d8c9a8" stroke="#8a7c5e"/>')
    wire([(19.5, 10), (21, 10)], LEG, wd=2)
    label(24, 10, "470 ohm standing on (19,10); its top leg comes down at an angle into (21,10)", "s", "start", None, 0, 6)
    # 1000 uF, 10 mm can drawn to scale, translucent so the pads show
    cx, cy = P(20, CAP)
    add(f'<circle cx="{cx}" cy="{cy}" r="{5*MM}" fill="#2f3a52" fill-opacity="0.75" stroke="#1b2233"/>')
    add(f'<rect x="{cx+2.6*MM}" y="{cy-2*MM}" width="{1.2*MM}" height="{4*MM}" fill="#cdd6e6"/>')
    label(25.5, CAP, f"1000 uF, 10 mm can: LONG leg (19,{CAP}) on the +5V bus, striped SHORT leg (21,{CAP})", "s", "start", None, 0, 0)
    cx, cy = P(21, 2)
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{2.5*MM}" ry="{1.6*MM}" fill="#d9a441" stroke="#8a6a20"/>')
    wire([(19, 2), (23, 2)], LEG, wd=2)
    label(21, 2, "0.1 uF", "s", "middle", dy=-16)
    # external wires: red ones jog up half a row so they do not run through the black ones' holes
    ylab = [3.6, 4.6, 5.6, 6.6, 7.6, 8.6, 11.6]
    for ((x, y), col, lbl), y2 in zip(EXT, ylab):
        if x == 19:
            wire([(x, y), (x + 0.5, y), (x + 1.0, y - 0.4), (24.6, y - 0.4), (26.4, y2), (27.8, y2)], col, wd=3)
        else:
            wire([(x, y), (24.6, y), (26.4, y2), (27.8, y2)], col, wd=3)
        px, py = P(27.8, y2); add(f'<text class="t" x="{px+6}" y="{py}" dominant-baseline="central">{lbl}</text>')
    blob(26, 4, "#1a1a18", 3); blob(26, 12, "#1a1a18", 3)
    label(26, 12.8, "lash: bare wire through (26,4) and (26,12), over the bundle", "s", "middle", None, 8)
    for (x, y), _, _ in EXT: blob(x, y, "#1a1a18", 3.5)
    for (x, y) in [(19, 3), (23, 4), (16, 3), (16, 4), (4, 8), (16, 8), (17, 8), (21, 8), (19, 10), (21, 10), (19, CAP), (21, CAP), (19, 2), (23, 2)]:
        blob(x, y, "#1a1a18", 3.5)


TOP = 80
panel(TOP, False, "TOP side - where the parts and the wires go",
      "Solid = on this side. Dashed = on the underside (buses and bent legs), shown so you know where they run. Bodies drawn to scale.")
BOT = TOP + (ROWS + 2) * C + 100
panel(BOT, True, "UNDERSIDE - turned over left-to-right like a page, so the USB end is still at the top",
      "Column 1 is now on the RIGHT. Find the corner mark first, every time you turn the board over. Dots = solder joints.", xoff=300)

Y = BOT + (ROWS + 1) * C + 50
add(f'<rect x="0" y="0" width="{W}" height="{Y+200}" fill="#ffffff"/>')
s.insert(0, s.pop())
add(f'<text class="h" x="40" y="{Y}">How to read it</text>'); Y += 24
for col, txt in [
    (RED, "thick red / dark grey:  a BUS - one bare wire along the pads on the underside, laid beside the hole centres. Dashed in the top view because it is underneath"),
    (GRN, "thin solid green / red / black (top view):  an insulated link on this side; its end goes through the hole NEXT to the pin and is bent onto the pin underneath"),
    (AMB, "amber:  the diode's own plain leg, bent along four pads under the board. The 470 ohm and the green DIN wire go through beside it and solder to it"),
    (LEG, "brown:  a bare component leg"),
]:
    add(f'<line x1="40" y1="{Y-4}" x2="76" y2="{Y-4}" stroke="{col}" stroke-width="4"/>')
    add(f'<text class="t" x="86" y="{Y}" dominant-baseline="central">{txt}</text>'); Y += 22
Y += 6
add(f'<text class="t" x="40" y="{Y}">Hole numbers are (column, row) from the corner mark. Only three ESP32 pins are used: VIN, the GND right below VIN, and RX2. Nothing goes to 3V3 or the other GND.</text>'); Y += 20
add(f'<text class="h" x="40" y="{Y}" style="fill:{RED}">Nothing bare may reach from one bus to the other. Between them there is only the junction (column 21) and the capacitor leg into the GND bus.</text>')
H = Y + 30
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">'
       f'<title>Desk node on a dot board</title>{ST}' + "".join(s) + "</svg>\n")
OUT.write_text(svg, encoding="utf-8")
import xml.etree.ElementTree as ET; ET.parse(OUT); print("ok", W, H)
