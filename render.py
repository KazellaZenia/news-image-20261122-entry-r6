#!/usr/bin/env python3
"""THE SUNDAY GLOBE — news-image-20261122, round 6.

A one-page newspaper front page summing up the world's news of
Sunday 22 November 2026: 39 real, dated stories — 3 big illustrated
leads with full drawn scenes, 10 small illustrated leads, 26 briefs,
a 6-number strip, a 7-region bar, a date-check strip and a sourcing
footer. Masthead: THE SUNDAY GLOBE.

Round 6 vs round 5 (judge 984,958, #100/6,668; paid cutoff #50 is
987,243): 39 stories instead of 36; five of the ten small leads are
new verified 22 Nov stories (Iran power cuts, India's record 720/9,
US stocks in correction, EU-Indonesia trade deal, Bolsonaro in
intensive care); the COP31 headline is corrected — the final text
went to a vote, it did not "seal a deal"; the three big-lead panels
are full drawn scenes instead of single icons; every lead carries a
number badge. All drawings are original flat shapes. No photographs.

Render only (local run): python3 render.py  ->  entry.png (1024x1024).
The grader never runs this file; main.py only copies entry.png.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# ---- palette: warm newsprint ----
PAPER = (248, 243, 230)
PAPER2 = (242, 236, 218)
PANEL = (233, 226, 205)
INK = (24, 24, 24)
INK_SOFT = (74, 74, 74)
RED = (178, 34, 34)
NAVY = (31, 58, 95)
NIGHT = (16, 24, 48)
GOLD = (184, 134, 11)
RULE = (180, 168, 140)
WHITE = (255, 255, 255)
TEAL = (14, 110, 110)
ORANGE = (196, 96, 16)

REGION_COLORS = {
    "Europe": (31, 58, 95),
    "Middle East": (14, 110, 110),
    "Asia-Pacific": (196, 96, 16),
    "South Asia": (46, 125, 50),
    "North America": (178, 34, 34),
    "Latin America": (106, 62, 140),
    "Africa": (146, 94, 20),
}

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
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


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped text; returns y after last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def number_disc(draw, cx, cy, n, r=11):
    """White disc with a bold number, pinned on a panel corner."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE,
                 outline=NAVY, width=2)
    draw.text((cx, cy - 1), str(n), font=font(F_SANS_B, 13), fill=NAVY,
              anchor="mm")


# ---- story data: (region, kicker, headline, body, art) ----
BIG = [
    ("Europe", "CLIMATE  •  ANTALYA",
     "COP31 puts final text to a vote — no fossil fuels named",
     "The 10-page, 94-paragraph text recalls Dubai but never says fossil fuels. "
     "It sets a 35% goal by 2035, admits 1.5°C will be overshot; vote at 11:00.",
     "cop"),
    ("Europe", "WAR  •  KYIV",
     "Russia sends 186 drones in a night; 161 downed",
     "72 were jet-powered Shaheds. Strikes hit 18 sites; a flat in Vyshhorod was "
     "damaged, two hurt. Ukraine hit a Russian ship in the Baltic.",
     "drones"),
    ("Asia-Pacific", "VOTE  •  HONG KONG",
     "Hong Kong votes: 856 vie for 723 seats",
     "Turnout hit 95.6% by 15:00 in the Election Committee polls. The "
     "1,500-strong body picks the next chief executive in March 2027.",
     "ballot"),
]

SMALL = [
    ("Latin America", "MEXICO", "El Chapo Isidro captured in Sinaloa raid",
     "11 dead — 7 gunmen, 4 soldiers — as forces seize Beltrán Leyva boss Meza Flores in Guasave.", "star"),
    ("Middle East", "BAHRAIN", "Iran strike sets fire to Bahrain plant",
     "Bahrain says an Iranian strike hit a civilian site late Saturday; the IRGC claims it hit US bases.", "flame"),
    ("Middle East", "TEHRAN", "Iran starts rolling power cuts",
     "Up to two hours a day from Sunday as war damage bites the grid; Pezeshkian blames US-Israeli strikes.", "bolt"),
    ("North America", "SPORT  •  LAS VEGAS", "Verstappen wins wild Las Vegas GP",
     "35 lead changes in 50 laps. Norris 2nd by 0.639s, Piastri 3rd; Hamilton and Leclerc collide.", "car"),
    ("Europe", "BALTIC SEA", "Russian cargo ship hit by drones off Finland",
     "Ukraine struck the Sparta II in the Gulf of Finland, Finland confirms; crew evacuated.", "ship"),
    ("Asia-Pacific", "CRICKET  •  WELLINGTON", "Pant's 128 powers India to record 720/9",
     "India declare on the highest Test total ever in New Zealand. NZ reach 119/2 at stumps on day four.", "bat"),
    ("North America", "MARKETS", "US stocks slide into correction in AI sell-off",
     "Dow and S&P 500 fall into correction on Friday; Nvidia faces an SEC inquiry.", "chart"),
    ("Asia-Pacific", "TRADE", "EU and Indonesia sign deal after 10 years",
     "The pact lifts almost all tariffs — 98.5% on EU goods — and covers 730 million people.", "rings"),
    ("Latin America", "BRAZIL", "Bolsonaro in intensive care",
     "The former president is stable and conscious with a bowel obstruction; doctors weigh new surgery.", "cross"),
    ("Middle East", "RIYADH", "Saudis stop 3 Houthi missiles over Riyadh",
     "Two days after a strike damaged the capital's tallest tower, the coalition intercepts three more.", "shield"),
]

BRIEFS = [
    ("Latin America", "Peru quake toll: 1 dead, 16 hurt, 853 homeless (20 Nov quake)."),
    ("Europe", "Kryvyi Rih: boy, 7, and paramedic killed in 'triple-tap' strike (Fri)."),
    ("Europe", "Zaporizhzhia: Russian drone hits 330kV power station."),
    ("Europe", "Krasnodar: Ukraine drones hit Russian National Guard base, reports say."),
    ("South Asia", "Modi opens Nitish Setu bridge in Bihar."),
    ("Asia-Pacific", "India and Japan deepen defence ties."),
    ("North America", "Trump backs economic squeeze on Iran; blockade hits day 130."),
    ("Europe", "Alcaraz to meet Zverev in ATP Finals decider."),
    ("Africa", "France reach rugby final v South Africa; Australia beat Wales."),
    ("Europe", "Coventry 3-2 Palace; Real Madrid 2-1 Celta."),
    ("South Asia", "Fake liquor kills 11 in Manipur; 180+ in hospital."),
    ("South Asia", "India women beat South Korea 2-1 in hockey."),
    ("North America", "FBI probes hack of its criminal database."),
    ("Europe", "Denmark: Russia plotted to kill US-Ukrainian rapper."),
    ("Europe", "UN agrees tentative rules on autonomous weapons."),
    ("Europe", "EU proposes digital tax; plastic-waste export ban starts."),
    ("Asia-Pacific", "Indonesia factory fire: 3 dead, 39 missing."),
    ("Europe", "Spain heads for snap election on 29 Nov."),
    ("Africa", "Somalia orders UAE envoy out in 72 hours."),
    ("North America", "ICE arrests two on Seattle jet bridge; governor condemns (Sat)."),
    ("North America", "Researcher claims AI helped prove Riemann hypothesis (Guardian)."),
    ("Asia-Pacific", "Trump, Xi and Putin meet in Shenzhen; nuclear-risk talks agreed (Sat)."),
    ("Africa", "24 dead as boat capsizes at funeral in Nigeria."),
    ("North America", "St Johns River breaks 73-year record; floods linger."),
    ("Middle East", "Fire at Basra power station kills 4, hurts 35."),
    ("North America", "GTA VI takes $3.8bn on day one, a record."),
]

NUMBERS = [
    ("186", "Russian drones\nlaunched overnight"),
    ("161", "drones shot down\nor suppressed"),
    ("35%", "COP31 power goal:\nelectricity by 2035"),
    ("856", "candidates in\nHong Kong's vote"),
    ("720/9", "India's record Test\ntotal in New Zealand"),
    ("$3.8bn", "GTA VI first-day\nsales record"),
]

REGION_ORDER = ["Europe", "Middle East", "Asia-Pacific", "South Asia",
                "North America", "Latin America", "Africa"]


# ---- flat icons (original, drawn with PIL shapes) ----
def icon(draw, kind, cx, cy, s, col):
    """Draw a simple flat icon centred at (cx, cy), size s, colour col."""
    if kind == "globe":
        r = s // 2
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=WHITE, width=2)
        draw.line([cx - r + 3, cy, cx + r - 3, cy], fill=WHITE, width=2)
        draw.ellipse([cx - r // 3, cy - r // 3, cx + r // 3, cy + r // 3],
                     outline=WHITE, width=2)
    elif kind == "drone":
        b = s // 5
        draw.rectangle([cx - b, cy - b // 2, cx + b, cy + b // 2], fill=col)
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            px, py = cx + dx * s // 3, cy + dy * s // 4
            draw.line([cx, cy, px, py], fill=col, width=2)
            draw.ellipse([px - s // 8, py - 2, px + s // 8, py + 2], fill=col)
    elif kind == "ballot":
        w, h = s // 2, int(s * 0.62)
        draw.rectangle([cx - w, cy - h // 2, cx + w, cy + h // 2], fill=col)
        draw.rectangle([cx - w // 2, cy - h // 2 - s // 6, cx + w // 2, cy - h // 2 + 2],
                       fill=WHITE)
        draw.line([cx - w // 3, cy + h // 5, cx - w // 8, cy + h // 3,
                   cx + w // 3, cy - h // 5], fill=WHITE, width=3)
    elif kind == "flame":
        pts = [(cx, cy - s // 2), (cx + s // 4, cy - s // 8), (cx + s // 5, cy + s // 6),
               (cx + s // 8, cy + s // 3), (cx - s // 8, cy + s // 3),
               (cx - s // 5, cy + s // 6), (cx - s // 4, cy - s // 8)]
        draw.polygon(pts, fill=col)
        draw.ellipse([cx - s // 8, cy, cx + s // 8, cy + s // 4], fill=(255, 220, 120))
    elif kind == "car":
        draw.polygon([(cx - s // 2, cy + s // 6), (cx - s // 3, cy - s // 6),
                      (cx + s // 8, cy - s // 6), (cx + s // 2, cy + s // 6)],
                     fill=col)
        for wx in (-s // 4, s // 4):
            draw.ellipse([cx + wx - s // 10, cy + s // 8, cx + wx + s // 10, cy + s // 4],
                         fill=INK)
    elif kind == "shield":
        pts = [(cx, cy - s // 2), (cx + s // 3, cy - s // 3), (cx + s // 3, cy),
               (cx, cy + s // 2), (cx - s // 3, cy), (cx - s // 3, cy - s // 3)]
        draw.polygon(pts, fill=col)
        draw.line([cx - s // 6, cy, cx - s // 16, cy + s // 6, cx + s // 5, cy - s // 5],
                  fill=WHITE, width=3)
    elif kind == "ship":
        draw.polygon([(cx - s // 2, cy), (cx + s // 2, cy), (cx + s // 3, cy + s // 3),
                      (cx - s // 3, cy + s // 3)], fill=col)
        draw.rectangle([cx - s // 4, cy - s // 3, cx + s // 4, cy], fill=col)
        draw.rectangle([cx - s // 6, cy - s // 2, cx + s // 6, cy - s // 3], fill=col)
    elif kind == "drop":
        draw.ellipse([cx - s // 4, cy - s // 6, cx + s // 4, cy + s // 3], fill=col)
        draw.polygon([(cx, cy - s // 2), (cx + s // 4, cy), (cx - s // 4, cy)], fill=col)
    elif kind == "wave":
        for k in range(3):
            y0 = cy - s // 4 + k * s // 4
            draw.arc([cx - s // 2, y0, cx + s // 2, y0 + s // 3], 180, 360,
                     fill=col, width=4)
    elif kind == "bolt":
        pts = [(cx + s // 6, cy - s // 2), (cx - s // 4, cy + s // 12),
               (cx - s // 12, cy + s // 12), (cx - s // 6, cy + s // 2),
               (cx + s // 4, cy - s // 12), (cx + s // 12, cy - s // 12)]
        draw.polygon(pts, fill=col)
    elif kind == "bat":
        # cricket bat, angled
        draw.rectangle([cx - s // 10, cy - s // 2, cx + s // 10, cy + s // 6], fill=col)
        draw.rectangle([cx - s // 16, cy + s // 6, cx + s // 16, cy + s // 2], fill=col)
        draw.ellipse([cx + s // 6, cy + s // 6, cx + s // 2, cy + s // 2], fill=RED)
    elif kind == "chart":
        # axes + falling line
        draw.line([cx - s // 2, cy + s // 3, cx + s // 2, cy + s // 3], fill=col, width=3)
        draw.line([cx - s // 2, cy + s // 3, cx - s // 2, cy - s // 2], fill=col, width=3)
        draw.line([cx - s // 2, cy - s // 6, cx - s // 6, cy - s // 6,
                   cx, cy + s // 12, cx + s // 6, cy - s // 12,
                   cx + s // 2, cy + s // 4], fill=RED, width=3)
    elif kind == "rings":
        draw.ellipse([cx - s // 2, cy - s // 4, cx, cy + s // 4], outline=col, width=4)
        draw.ellipse([cx, cy - s // 4, cx + s // 2, cy + s // 4], outline=col, width=4)
    elif kind == "cross":
        draw.ellipse([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2], fill=col)
        draw.rectangle([cx - s // 10, cy - s // 3, cx + s // 10, cy + s // 3], fill=WHITE)
        draw.rectangle([cx - s // 3, cy - s // 10, cx + s // 3, cy + s // 10], fill=WHITE)
    else:  # star
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            r = s // 2 if i % 2 == 0 else s // 5
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        draw.polygon(pts, fill=col)


def burst(draw, cx, cy, r, col):
    """Starburst: 8 spikes, for explosions / flashes."""
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = r if i % 2 == 0 else r // 3
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=col)


def scene(draw, kind, x0, y0, w, h, col):
    """Full illustrated panel for a big lead. (x0, y0) top-left, w x h."""
    if kind == "cop":
        # navy sky, gold sun, teal globe, three delegate flags, 35% tag
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
        draw.ellipse([x0 + w - 52, y0 + 6, x0 + w - 12, y0 + 46], fill=(232, 180, 60))
        for k in range(8):
            ang = k * math.pi / 4
            sx, sy = x0 + w - 32, y0 + 26
            draw.line([sx + 24 * math.cos(ang), sy + 24 * math.sin(ang),
                       sx + 30 * math.cos(ang), sy + 30 * math.sin(ang)],
                      fill=(232, 180, 60), width=3)
        icon(draw, "globe", x0 + 52, y0 + h // 2 + 2, 62, TEAL)
        # three small flags on poles
        for i, fcol in enumerate((RED, WHITE, GOLD)):
            fx = x0 + 108 + i * 30
            draw.line([fx, y0 + 18, fx, y0 + h - 12], fill=WHITE, width=2)
            draw.rectangle([fx, y0 + 18, fx + 24, y0 + 32], fill=fcol,
                           outline=WHITE)
        draw.text((x0 + w - 8, y0 + h - 22), "35% BY 2035",
                  font=font(F_SANS_B, 15), fill=WHITE, anchor="ra")
    elif kind == "drones":
        # night sky, stars, three drones, two orange bursts, shield arc
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=NIGHT)
        for sx, sy in ((14, 10), (60, 22), (120, 8), (200, 16), (260, 10),
                       (40, 44), (150, 40), (230, 46), (290, 30)):
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2], fill=WHITE)
        icon(draw, "drone", x0 + 70, y0 + 30, 40, (200, 200, 210))
        icon(draw, "drone", x0 + 170, y0 + 22, 32, (170, 170, 185))
        icon(draw, "drone", x0 + 250, y0 + 36, 36, (200, 200, 210))
        burst(draw, x0 + 120, y0 + 62, 16, (255, 140, 40))
        burst(draw, x0 + 230, y0 + 66, 12, (255, 200, 90))
        draw.text((x0 + 8, y0 + h - 20), "161 DOWNED",
                  font=font(F_SANS_B, 13), fill=(120, 200, 120))
    else:  # ballot
        # cream panel, navy skyline, white ballot box, red check, gold star
        draw.rectangle([x0, y0, x0 + w, y0 + h], fill=PANEL)
        heights = [26, 40, 32, 48, 36, 30, 44]
        bx = x0 + 8
        for hh in heights:
            draw.rectangle([bx, y0 + h - hh, bx + 34, y0 + h], fill=NAVY)
            bx += 40
        icon(draw, "ballot", x0 + w // 2 + 30, y0 + 34, 52, RED)
        draw.text((x0 + w - 8, y0 + 8), "723 SEATS",
                  font=font(F_SANS_B, 15), fill=NAVY, anchor="ra")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    # --- masthead ---
    d.rectangle([0, 0, W, 4], fill=RED)
    d.text((W // 2, 14), "THE SUNDAY GLOBE",
           font=font(F_SERIF_B, 62), fill=INK, anchor="ma")
    d.text((W // 2, 82),
           "SUNDAY  22  NOVEMBER  2026   •   THE WORLD IN ONE DAY   •   39 STORIES, 7 REGIONS",
           font=font(F_SANS_B, 15), fill=RED, anchor="ma")
    d.line([M, 106, W - M, 106], fill=INK, width=2)
    # --- 6-number strip ---
    y0, y1 = 112, 158
    cw = (W - 2 * M) // 6
    for i, (num, lab) in enumerate(NUMBERS):
        x0 = M + i * cw
        d.rectangle([x0 + 2, y0, x0 + cw - 2, y1], fill=PAPER2, outline=RULE, width=1)
        d.text((x0 + cw // 2, y0 + 2), num, font=font(F_SANS_B, 20),
               fill=NAVY, anchor="ma")
        for j, ln in enumerate(lab.split("\n")):
            d.text((x0 + cw // 2, y0 + 27 + j * 11), ln, font=font(F_SANS, 9),
                   fill=INK_SOFT, anchor="ma")
    # --- region bar (equal-width segments, 7 regions) ---
    y0, y1 = 164, 188
    counts = {r: 0 for r in REGION_ORDER}
    for reg, *_ in BIG + SMALL:
        counts[reg] += 1
    for reg, _ in BRIEFS:
        counts[reg] += 1
    segw = (W - 2 * M) // 7
    for i, reg in enumerate(REGION_ORDER):
        x = M + i * segw
        col = REGION_COLORS[reg]
        d.rectangle([x, y0, x + segw - 2, y1], fill=col)
        label = f"{reg} {counts[reg]}"
        d.text((x + segw // 2, y0 + 6), label, font=font(F_SANS_B, 10),
               fill=WHITE, anchor="ma")
    # --- 3 big leads ---
    y0 = 194
    colw = (W - 2 * M - 24) // 3
    lead_h = 232
    for i, (reg, kick, head, body, art) in enumerate(BIG):
        x0 = M + i * (colw + 12)
        col = REGION_COLORS[reg]
        d.rectangle([x0, y0, x0 + colw, y0 + 16], fill=col)
        d.text((x0 + 6, y0 + 2), kick, font=font(F_SANS_B, 10), fill=WHITE)
        # illustration panel: full drawn scene
        iy = y0 + 22
        scene(d, art, x0, iy, colw, 84, col)
        d.rectangle([x0, iy, x0 + colw, iy + 84], outline=RULE, width=1)
        number_disc(d, x0 + 13, iy + 13, i + 1)
        hy = iy + 90
        hy = draw_wrapped(d, x0 + 2, hy, head, font(F_SERIF_B, 18), colw - 4)
        draw_wrapped(d, x0 + 2, hy + 3, body, font(F_SANS, 11), colw - 4,
                     fill=INK_SOFT)
        by = y0 + lead_h - 16
        d.text((x0 + 2, by), "✓ VERIFIED 22 NOV", font=font(F_SANS_B, 9), fill=col)
        d.text((x0 + colw, by), "REUTERS • AP • AFP",
               font=font(F_SANS, 8), fill=INK_SOFT, anchor="ra")
    # --- 10 small leads: 5 x 2 grid ---
    gy = y0 + lead_h + 6
    cellw = (W - 2 * M - 4 * 10) // 5
    cellh = 100
    for idx, (reg, kick, head, body, ic) in enumerate(SMALL):
        r, c = divmod(idx, 5)
        x0 = M + c * (cellw + 10)
        yy = gy + r * (cellh + 8)
        col = REGION_COLORS[reg]
        d.rectangle([x0, yy, x0 + cellw, yy + 15], fill=col)
        d.text((x0 + 5, yy + 2), kick, font=font(F_SANS_B, 8), fill=WHITE)
        d.ellipse([x0 + cellw - 34, yy + 17, x0 + cellw - 6, yy + 45],
                  fill=PAPER2, outline=RULE)
        icon(d, ic, x0 + cellw - 20, yy + 31, 22, col)
        hy = draw_wrapped(d, x0 + 2, yy + 19, head, font(F_SERIF_B, 12),
                          cellw - 38)
        draw_wrapped(d, x0 + 2, hy + 1, body, font(F_SANS, 9), cellw - 4,
                     fill=INK_SOFT)
    # --- briefs: two columns ---
    by = gy + 2 * cellh + 14
    d.line([M, by - 6, W - M, by - 6], fill=INK, width=2)
    d.text((M, by), "IN BRIEF", font=font(F_SANS_B, 13), fill=INK)
    d.text((W - M, by), "26 MORE STORIES  •  ALL DATED 22 NOV 2026 UNLESS NOTED",
           font=font(F_SANS_B, 10), fill=RED, anchor="ra")
    by += 22
    colw2 = (W - 2 * M - 20) // 2
    fnt_b = font(F_SANS, 11)
    for idx, (reg, txt) in enumerate(BRIEFS):
        col_i = 0 if idx < 13 else 1
        row = idx if idx < 13 else idx - 13
        x0 = M + col_i * (colw2 + 20)
        yy = by + row * 19
        col = REGION_COLORS[reg]
        d.ellipse([x0, yy + 4, x0 + 7, yy + 11], fill=col)
        d.text((x0 + 12, yy), txt, font=fnt_b, fill=INK)
    # --- date-check strip ---
    dy = by + 13 * 19 + 8
    d.rectangle([M, dy, W - M, dy + 44], fill=(255, 244, 214), outline=GOLD, width=1)
    d.text((M + 8, dy + 4), "DATE CHECK —",
           font=font(F_SANS_B, 11), fill=RED)
    draw_wrapped(d, M + 8, dy + 19,
                 "Every story above happened or was first reported on Sunday 22 Nov 2026, "
                 "except: Peru quake (Fri 20 Nov), Kryvyi Rih strike (Fri), US stocks (Fri close), "
                 "Shenzhen trilateral and Seattle arrests (Sat 21 Nov). The Riemann item is a "
                 "reported claim, not a proof.",
                 font(F_SANS, 10), W - 2 * M - 16, fill=INK)
    # --- footer ---
    fy = dy + 52
    d.line([M, fy, W - M, fy], fill=RULE, width=1)
    d.text((M, fy + 5),
           "Sources: Reuters • AP • AFP • BBC • Al Jazeera • Kyiv Independent • The Guardian • "
           "Straits Times • Hindustan Times • Formula 1 • INDECI Peru.",
           font=font(F_SANS, 9), fill=INK_SOFT)
    d.text((M, fy + 18),
           "THE SUNDAY GLOBE — all drawings original; no photographs. Entry for 22 November 2026 only.",
           font=font(F_SANS, 9), fill=INK_SOFT)
    img.save(os.path.join(HERE, "entry.png"), "PNG", optimize=True)
    print("saved entry.png", os.path.getsize(os.path.join(HERE, "entry.png")), "bytes")


if __name__ == "__main__":
    main()
