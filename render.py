"""Draw the 21 November 2026 world-news front page.

This script paints a newspaper-style front page -- masthead, lead story,
side stories and data boxes -- onto a square canvas and saves it as
``entry.png`` next to this file.  Run it directly to redraw the page:

    python3 render.py

The palette is a print look: warm paper, dark ink, one red accent and a
deep navy for the secondary headlines.
"""

import math  # small numeric helpers
import os  # locating this script and joining paths

from PIL import Image  # blank canvas, loading, saving
from PIL import ImageDraw  # lines, boxes and text on the canvas
from PIL import ImageFont  # truetype font loading

# --- Where things live -------------------------------------------------
# The directory holding this script, resolved to an absolute path so the
# script behaves the same no matter where it is launched from.
HERE = os.path.dirname(
    os.path.abspath(__file__)
)

# The finished picture, written next to this script.
OUT = os.path.join(HERE, "entry.png")

# --- Canvas ------------------------------------------------------------
W = 1024  # page width in pixels
H = 1024  # page height in pixels

# --- Palette (RGB) -----------------------------------------------------
PAPER = (245, 241, 230)  # warm off-white page background
INK = (26, 26, 26)  # near-black for body text
RED = (178, 34, 34)  # accent red for the lead headline
NAVY = (30, 58, 95)  # deep blue for secondary headlines
GREY = (110, 110, 105)  # muted grey for captions and small print
LINE = (150, 142, 122)  # tan colour for the dividing rules
BOXBG = (250, 248, 241)  # pale box fill, a touch lighter than the paper

# --- Fonts -------------------------------------------------------------
# DejaVu truetype fonts live here on this system.
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

F_MAST = font(SERIF_B, 66)
F_DATE = font(SANS_B, 23)
F_TAG = font(SANS, 17)
F_KICK = font(SANS_B, 16)
F_HEAD_L = font(SERIF_B, 36)
F_BODY_L = font(SERIF, 19)
F_STATS = font(SANS_B, 19)
F_SUB = font(SANS, 15)
F_HEAD_M = font(SERIF_B, 25)
F_BODY_M = font(SERIF, 16)
F_HEAD_S = font(SERIF_B, 21)
F_BODY_S = font(SERIF, 15)
F_BRIEF = font(SERIF, 15)
F_FOOT = font(SANS, 13)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def box(draw, x0, y0, x1, y1, fill=BOXBG, outline=LINE, width=2):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)


def burst(draw, cx, cy, r, color=(255, 140, 0)):
    """Stylised explosion burst: spiky star + bright core."""
    outer = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.45
        outer.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(outer, fill=color)
    draw.ellipse([cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35],
                 fill=(255, 220, 120))


def skyline(draw, x0, y0, x1, y1, night=True, max_h=70):
    """City silhouette with lit windows between x0..x1, base at y1."""
    base = (16, 28, 52) if night else (60, 70, 80)
    win = (255, 210, 110) if night else (220, 220, 200)
    widths = [46, 30, 58, 36, 70, 28, 52, 40, 62, 34]
    x = x0
    i = 0
    while x < x1 - 10:
        w = widths[i % len(widths)]
        h = 20 + ((i * 37) % max_h)
        draw.rectangle([x, y1 - h, min(x + w, x1), y1], fill=base)
        for wy in range(y1 - h + 6, y1 - 6, 12):
            for wx in range(x + 5, min(x + w - 5, x1 - 4), 11):
                if (wx + wy) % 23 < 13:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=win)
        x += w + 4
        i += 1


def draw_lead_art(draw, x0, y0, x1, y1):
    """Night over Riyadh: skyline, missile trails, interception bursts."""
    draw.rectangle([x0, y0, x1, y1], fill=(10, 18, 38))
    for sx, sy in [(18, 14), (70, 30), (130, 10), (200, 26), (260, 12),
                   (320, 34), (45, 52), (150, 48), (235, 55), (290, 60)]:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                     fill=(230, 230, 255))
    # tall tower silhouette, left of centre
    draw.rectangle([x0 + 120, y0 + 42, x0 + 168, y1 - 40], fill=(24, 40, 70))
    draw.polygon([(x0 + 120, y0 + 42), (x0 + 144, y0 + 18), (x0 + 168, y0 + 42)],
                 fill=(24, 40, 70))
    for wy in range(y0 + 52, y1 - 46, 12):
        for wx in range(x0 + 126, x0 + 162, 11):
            draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 110))
    skyline(draw, x0, y0 + 60, x1, y1 - 18, max_h=70)
    draw.rectangle([x0, y1 - 18, x1, y1], fill=(8, 14, 30))
    # missile trails, top-right to centre
    for (sx, sy, ex, ey) in [(x1 - 20, y0 + 8, x1 - 130, y0 + 88),
                             (x1 - 70, y0 + 4, x1 - 190, y0 + 96),
                             (x0 + 300, y0 + 60, x0 + 210, y0 + 110)]:
        draw.line([(sx, sy), (ex, ey)], fill=(255, 200, 90), width=3)
    burst(draw, x1 - 130, y0 + 88, 22)
    burst(draw, x1 - 190, y0 + 96, 16)
    burst(draw, x0 + 210, y0 + 110, 14)
    draw.rectangle([x0, y0, x1, y1], outline=LINE, width=2)


def draw_nato_art(draw, x0, y0, x1, y1):
    """NATO compass star over navy, Polish flag at right."""
    draw.rectangle([x0, y0, x1, y1], fill=(8, 32, 70))
    cx, cy = x0 + 70, (y0 + y1) // 2
    r = 17
    pts = [(cx, cy - r), (cx + 6, cy - 6), (cx + r, cy), (cx + 6, cy + 6),
           (cx, cy + r), (cx - 6, cy + 6), (cx - r, cy), (cx - 6, cy - 6)]
    draw.polygon(pts, fill=(255, 255, 255))
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(8, 32, 70))
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=(255, 255, 255),
                 width=1)
    fx0, fx1 = x1 - 96, x1 - 20
    fy0, fy1 = y0 + 9, y1 - 9
    draw.rectangle([fx0, fy0, fx1, (fy0 + fy1) // 2], fill=(255, 255, 255))
    draw.rectangle([fx0, (fy0 + fy1) // 2, fx1, fy1], fill=(220, 20, 60))
    draw.rectangle([fx0, fy0, fx1, fy1], outline=(200, 200, 200), width=1)
    draw.text((x0 + 110, cy - 10), "NATO  \u2022  POLAND", font=F_SUB,
              fill=(200, 210, 230))
    draw.rectangle([x0, y0, x1, y1], outline=LINE, width=2)


def draw_cop_art(draw, x0, y0, x1, y1):
    """Globe with a rising red temperature arrow."""
    draw.rectangle([x0, y0, x1, y1], fill=(222, 235, 226))
    cx, cy, r = x0 + 52, (y0 + y1) // 2, 20
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 170, 210),
                 outline=(40, 90, 140), width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=270, end=90,
             fill=(40, 90, 140), width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=90, end=270,
             fill=(40, 90, 140), width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(40, 90, 140), width=2)
    draw.ellipse([cx - 12, cy - 14, cx + 2, cy - 2], fill=(90, 160, 90))
    draw.ellipse([cx - 2, cy + 4, cx + 14, cy + 16], fill=(90, 160, 90))
    # thermometer, rising
    ax = x1 - 66
    draw.rectangle([ax, y0 + 8, ax + 14, y1 - 8], fill=(255, 255, 255),
                   outline=(150, 150, 150), width=2)
    draw.rectangle([ax + 3, y0 + 20, ax + 11, y1 - 11], fill=(220, 40, 40))
    draw.polygon([(ax + 7, y0 + 2), (ax - 1, y0 + 12), (ax + 15, y0 + 12)],
                 fill=(220, 40, 40))
    draw.text((x1 - 168, cy - 11), "+1.5\u00b0C", font=F_STATS, fill=RED)
    draw.text((x0 + 86, cy - 9), "OVERTIME IN ANTALYA", font=F_SUB,
              fill=(60, 90, 60))
    draw.rectangle([x0, y0, x1, y1], outline=LINE, width=2)


def draw_quake_art(draw, x0, y0, x1, y1):
    """Andes peaks with a seismograph trace."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 226, 208))
    draw.polygon([(x0, y1), (x0 + 60, y0 + 16), (x0 + 120, y1)],
                 fill=(120, 110, 95))
    draw.polygon([(x0 + 80, y1), (x0 + 160, y0 + 6), (x0 + 240, y1)],
                 fill=(95, 88, 74))
    draw.polygon([(x0 + 160, y0 + 6), (x0 + 150, y0 + 16), (x0 + 170, y0 + 16)],
                 fill=(250, 250, 250))
    mid = (y0 + y1) // 2 + 8
    pts = [(x0 + 8, mid)]
    for i in range(1, 40):
        px = x0 + 8 + i * (x1 - x0 - 16) // 40
        amp = 3 if i < 12 or i > 30 else 11
        pts.append((px, mid + int(amp * math.sin(i * 1.7))))
    draw.line(pts, fill=RED, width=3)
    draw.text((x0 + 8, y0 + 3), "6.9", font=F_STATS, fill=RED)
    draw.rectangle([x0, y0, x1, y1], outline=LINE, width=2)


def draw_kryvyi_art(draw, x0, y0, x1, y1):
    """City at dusk with smoke and a blast burst."""
    draw.rectangle([x0, y0, x1, y1], fill=(52, 48, 66))
    skyline(draw, x0, y0 + 18, x1, y1 - 6, night=True, max_h=26)
    for (sx, sy, sr) in [(180, 22, 10), (192, 14, 12), (176, 10, 8)]:
        draw.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                     fill=(140, 130, 120))
    burst(draw, x0 + 190, y0 + 30, 12)
    draw.rectangle([x0, y0, x1, y1], outline=LINE, width=2)


def draw_flood_art(draw, x0, y0, x1, y1):
    """Flooded street: houses with water up to the doors."""
    draw.rectangle([x0, y0, x1, y1], fill=(170, 195, 205))
    for hx in (x0 + 16, x0 + 108, x0 + 200):
        draw.rectangle([hx, y0 + 22, hx + 62, y1 - 12], fill=(210, 190, 160))
        draw.polygon([(hx - 5, y0 + 22), (hx + 31, y0 + 8), (hx + 67, y0 + 22)],
                     fill=(150, 60, 50))
        draw.rectangle([hx + 24, y0 + 30, hx + 38, y1 - 12], fill=(90, 70, 50))
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(40, 90, 130))
    for wx in range(x0 + 10, x1 - 18, 30):
        draw.arc([wx, y1 - 10, wx + 20, y1 - 2], start=180, end=360,
                 fill=(180, 220, 240), width=2)
    # label on a white backing chip so it stays crisp over the roofline
    draw.rectangle([x0 + 4, y0 + 2, x0 + 80, y0 + 24], fill=(255, 255, 255))
    draw.text((x0 + 8, y0 + 2), "18.7 ft", font=F_STATS, fill=NAVY)
    draw.rectangle([x0, y0, x1, y1], outline=LINE, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # outer margin

    # ---- masthead ----
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 16), title, font=F_MAST, fill=INK)
    d.line([(M, 96), (W - M, 96)], fill=INK, width=4)
    d.line([(M, 102), (W - M, 102)], fill=INK, width=1)
    d.text((M, 110), "SATURDAY, 21 NOVEMBER 2026", font=F_DATE, fill=RED)
    tag = "ONE DAY  \u2022  ONE PAGE  \u2022  THE WORLD'S NEWS"
    d.text((W - M - d.textlength(tag, font=F_TAG), 113), tag, font=F_TAG,
           fill=GREY)
    d.line([(M, 138), (W - M, 138)], fill=LINE, width=1)

    # ---- lead story ----
    lx0, ly0, lx1, ly1 = M, 148, W - M, 436
    box(d, lx0, ly0, lx1, ly1)
    tx = lx0 + 16
    ty = ly0 + 12
    d.text((tx, ty), "MIDDLE EAST  \u2022  RIYADH", font=F_KICK, fill=RED)
    ty += 26
    head = "Three Houthi missiles fired at Riyadh are intercepted"
    ty = text_block(d, tx, ty, head, F_HEAD_L, 560, 42)
    ty += 4
    body = ("Saudi air defences shoot down three ballistic missiles fired "
            "at the capital in the early hours of Saturday \u2014 the second "
            "attack on Riyadh in three days. No one is hurt; another Houthi "
            "drone is downed hours later.")
    ty = text_block(d, tx, ty, body, F_BODY_L, 560, 24)
    ax0, ay0, ax1, ay1 = lx1 - 380, ly0 + 12, lx1 - 16, ly0 + 188
    draw_lead_art(d, ax0, ay0, ax1, ay1)
    sy = ly1 - 62
    d.line([(lx0 + 16, sy), (lx1 - 16, sy)], fill=LINE, width=1)
    d.text((tx, sy + 8), "3 MISSILES INTERCEPTED  \u2022  3RD NIGHT OF ALERTS  "
           "\u2022  2ND ATTACK IN 3 DAYS", font=F_STATS, fill=NAVY)
    d.text((tx, sy + 34), "Houthis threaten Riyadh's financial district  "
           "\u2022  Iran claims it downed a US drone over Hormuz",
           font=F_SUB, fill=GREY)

    # ---- middle row: two stories ----
    my0, my1 = 448, 652
    mw = (W - 2 * M - 12) // 2
    # story 1: Warsaw
    x0, x1 = M, M + mw
    box(d, x0, my0, x1, my1)
    tx, ty = x0 + 14, my0 + 10
    d.text((tx, ty), "EUROPE  \u2022  WARSAW", font=F_KICK, fill=RED)
    ty += 24
    ty = text_block(d, tx, ty, "NATO chief in Warsaw after missiles land in Poland",
                    F_HEAD_M, mw - 28, 28)
    ty += 4
    draw_nato_art(d, tx, ty, x1 - 14, ty + 48)
    ty += 56
    text_block(d, tx, ty, "Rutte visits today after Russian missiles came down "
               "in Poland on Friday. Warsaw wants more air defence.",
               F_BODY_M, mw - 28, 21)
    # story 2: COP31
    x0, x1 = M + mw + 12, W - M
    box(d, x0, my0, x1, my1)
    tx, ty = x0 + 14, my0 + 10
    d.text((tx, ty), "CLIMATE  \u2022  ANTALYA", font=F_KICK, fill=RED)
    ty += 24
    ty = text_block(d, tx, ty, "COP31 talks run into overtime as fossil fuels vanish from draft",
                    F_HEAD_M, mw - 28, 28)
    ty += 4
    draw_cop_art(d, tx, ty, x1 - 14, ty + 48)
    ty += 56
    text_block(d, tx, ty, "Negotiators work an extra day after the draft drops "
               "fossil fuels. Campaigners call it \u201cthe worst COP ever\u201d.",
               F_BODY_M, mw - 28, 21)

    # ---- bottom row: three stories ----
    by0, by1 = 664, 860
    bw = (W - 2 * M - 24) // 3
    stories = [
        ("DISASTER  \u2022  PERU", "6.9 quake shakes Peru's Andes",
         "A deep quake near Jun\u00edn is felt in Lima; no casualties or "
         "damage are reported.", draw_quake_art),
        ("WAR IN UKRAINE  \u2022  KRYVYI RIH", "Strikes on Kryvyi Rih kill 2, injure 58",
         "A 7-year-old boy is among the dead as Russia fires 148 drones and "
         "three ballistic missiles overnight.", draw_kryvyi_art),
        ("WEATHER  \u2022  FLORIDA", "Florida river flooding breaks a 1953 record",
         "The St. Johns River near Cocoa holds at 18.7 ft; about 270 people "
         "are rescued in two counties.", draw_flood_art),
    ]
    for i, (kick, head, body, art) in enumerate(stories):
        x0 = M + i * (bw + 12)
        x1 = x0 + bw
        box(d, x0, by0, x1, by1)
        tx, ty = x0 + 12, by0 + 10
        d.text((tx, ty), kick, font=F_KICK, fill=RED)
        ty += 24
        ty = text_block(d, tx, ty, head, F_HEAD_S, bw - 24, 25)
        ty += 4
        art(d, tx, ty, x1 - 12, ty + 44)
        ty += 52
        text_block(d, tx, ty, body, F_BODY_S, bw - 24, 18)

    # ---- in brief ----
    bx0, by0b, bx1, by1b = M, 872, W - M, 974
    box(d, bx0, by0b, bx1, by1b)
    d.text((bx0 + 14, by0b + 8), "IN BRIEF", font=F_KICK, fill=RED)
    briefs_l = [
        "Iran: IRGC claims a 58th US MQ-9 drone downed.",
        "Iraq: fire at Basra power station kills 4, hurts 30.",
        "France: \u201cAct VI\u201d cost-of-living march in Paris.",
    ]
    briefs_r = [
        "India: toxic liquor deaths in Manipur rise to 13.",
        "Hormuz: Lewis Pugh swims 15 km for marine life.",
        "Bangladesh: 773 arrested in Dhaka after violence.",
    ]
    col_w = (bx1 - bx0 - 48) // 2
    for col, items in enumerate((briefs_l, briefs_r)):
        cx = bx0 + 16 + col * (col_w + 16)
        cy = by0b + 34
        for item in items:
            d.text((cx, cy), "\u2022", font=F_BRIEF, fill=INK)
            cy = text_block(d, cx + 16, cy, item, F_BRIEF, col_w - 16, 18)
            cy += 4

    # ---- footer ----
    foot = ("Sources: Reuters  \u2022  AP  \u2022  Al Jazeera  \u2022  BBC  "
            "\u2022  CNN   |   Compiled Saturday 21 November 2026")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 984), foot, font=F_FOOT, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
